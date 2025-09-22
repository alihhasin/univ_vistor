# app_enhanced.py - Enhanced Virtual Campus Tour with Modern Features
from pathlib import Path
import base64, mimetypes
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import IFrame
from geopy.distance import geodesic
import plotly.express as px
import uuid
from datetime import datetime

# Import custom modules
from ui_components import (
    create_location_card, create_metric_card, 
    add_floating_action_button, create_info_banner
)
from search_filters import create_advanced_sidebar, create_quick_filters
from guided_tour import GuidedTour, create_tour_selection_ui, TOUR_PRESETS
from feedback_system import FeedbackSystem, create_feedback_dashboard
from modern_theme import (
    apply_modern_theme, create_modern_header,
    create_modern_quick_filters, create_modern_language_switcher
)
from enhanced_ui import (
    create_welcome_section, create_location_card_enhanced,
    create_interactive_category_filter, create_enhanced_map,
    create_search_bar_enhanced
)

# Page configuration
st.set_page_config(
    page_title="IUST Virtual Campus Tour",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())
if 'tour_active' not in st.session_state:
    st.session_state['tour_active'] = False
if 'filtered_data' not in st.session_state:
    st.session_state['filtered_data'] = None

# Apply modern theme
apply_modern_theme()

# File paths
EXCEL_PATH = Path("data/campus_locations.xlsx")
IMAGES_DIR = Path("images")

# Initialize feedback system
feedback_system = FeedbackSystem()

# ---------- Helper Functions ----------
def norm(s: str) -> str:
    """Clean image name: remove extra spaces and unify separators"""
    return s.replace("\\", "/").strip()

def to_base64_uri(p: Path) -> str | None:
    if not (p and p.exists()):
        return None
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    try:
        b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None

def case_insensitive_search(root: Path, name: str) -> Path | None:
    """Case-insensitive search in folder and all subfolders"""
    lname = name.lower()
    for p in root.rglob("*"):
        if p.is_file() and p.name.lower() == lname:
            return p
    return None

def try_common_ext(root: Path, stem: str) -> Path | None:
    """Try common extensions when not mentioned"""
    exts = [".jpg", ".jpeg", ".png", ".webp"]
    for ext in exts:
        cand = case_insensitive_search(root, stem + ext)
        if cand:
            return cand
    return None

def resolve_image(pic_cell: str) -> Path | None:
    """Resolve image name with multiple strategies"""
    if not pic_cell:
        return None
    s = norm(str(pic_cell))
    rel = Path(s)
    
    # Try direct path
    cand = (IMAGES_DIR / rel).resolve()
    if cand.exists():
        return cand
    
    # Case-insensitive search
    if rel.suffix:
        cand = case_insensitive_search(IMAGES_DIR, rel.name)
        if cand:
            return cand
    
    # Try common extensions
    if not rel.suffix:
        cand = try_common_ext(IMAGES_DIR, rel.name)
        if cand:
            return cand
    
    # Search by stem
    stem = rel.stem.lower()
    for p in IMAGES_DIR.rglob("*"):
        if p.is_file() and p.stem.lower() == stem:
            return p
    return None

@st.cache_data
def load_df(p: Path) -> pd.DataFrame:
    df = pd.read_excel(p, engine="openpyxl")
    need = {
        "ID","Name_AR","Name_EN","Name_FA",
        "Latitude","Longitude",
        "Description_AR","Description_EN","Description_FA",
        "name_pic"
    }
    for c in need:
        if c not in df.columns:
            df[c] = ""
    df["Latitude"]  = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    if "Category" not in df.columns:
        df["Category"] = "General"
    return df

def language_cols(code: str):
    return ("Name_AR","Description_AR") if code=="ar" else \
           ("Name_EN","Description_EN") if code=="en" else \
           ("Name_FA","Description_FA")

def safe_title(row, name_col):
    return (str(row.get(name_col,"")).strip()
            or str(row.get("Name_EN","")).strip()
            or f"ID {row.get('ID','')}")

def inject_rtl(is_rtl: bool):
    if is_rtl:
        st.markdown("""
        <style>
          html, body, .stApp { direction: rtl; }
          .stMarkdown, .stPlotlyChart, .stSelectbox { text-align: right; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<style>html, body, .stApp { direction: ltr; }</style>", unsafe_allow_html=True)

# Language switcher function removed - using modern_theme version

# ---------- UI Text Labels ----------
labels = {
    "ar": {
        "choose_label": "اختر لغتك",
        "map_tab": "🗺️ الخريطة التفاعلية",
        "insights_tab": "📊 الإحصاءات",
        "distance_tab": "🧭 المسافات",
        "tour_tab": "🎭 الجولة الإرشادية",
        "feedback_tab": "💬 التقييمات",
        "distance_header": "🧭 حساب المسافة بين موقعين",
        "distance_from": "نقطة الانطلاق",
        "distance_to": "نقطة الوصول",
        "distance_result": "المسافة التقريبية",
        "distance_note": "المسافة محسوبة جغرافيًا (geodesic) على سطح الأرض.",
        "diag": "🔎 التشخيص (اختياري)",
        "welcome": "مرحباً بكم في جولة الحرم الجامعي الافتراضية",
        "subtitle": "جامعة إيران للعلوم والتكنولوجيا"
    },
    "en": {
        "choose_label": "Choose your language",
        "map_tab": "🗺️ Interactive Map",
        "insights_tab": "📊 Insights",
        "distance_tab": "🧭 Distances",
        "tour_tab": "🎭 Guided Tour",
        "feedback_tab": "💬 Feedback",
        "distance_header": "🧭 Distance between two locations",
        "distance_from": "Starting point",
        "distance_to": "Destination point",
        "distance_result": "Approx. Distance",
        "distance_note": "Geodesic distance on Earth surface.",
        "diag": "🔎 Diagnostics (optional)",
        "welcome": "Welcome to Virtual Campus Tour",
        "subtitle": "Iran University of Science and Technology"
    },
    "fa": {
        "choose_label": "زبان خود را انتخاب کنید",
        "map_tab": "🗺️ نقشه تعاملی",
        "insights_tab": "📊 آمار",
        "distance_tab": "🧭 فاصله‌ها",
        "tour_tab": "🎭 تور راهنما",
        "feedback_tab": "💬 بازخورد",
        "distance_header": "🧭 محاسبه فاصله بین دو مکان",
        "distance_from": "نقطه شروع",
        "distance_to": "نقطه مقصد",
        "distance_result": "فاصله تقریبی",
        "distance_note": "فاصله ژئودزیک روی سطح زمین.",
        "diag": "🔎 عیب‌یابی (اختیاری)",
        "welcome": "به تور مجازی پردیس خوش آمدید",
        "subtitle": "دانشگاه علم و صنعت ایران"
    }
}

# ---------- Load Data ----------
try:
    df = load_df(EXCEL_PATH)
except Exception as e:
    st.error(f"Unable to read Excel file: {e}")
    st.stop()

# ---------- Language Selector ----------
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    lang_display = st.selectbox(
        "🌐 Language / لغة / زبان",
        ["العربية","English","فارسی"],
        index=1,
        label_visibility="collapsed"
    )

lang_code = "ar" if lang_display=="العربية" else "en" if lang_display=="English" else "fa"
texts = labels[lang_code]
name_col, desc_col = language_cols(lang_code)
inject_rtl(lang_code in ("ar","fa"))

# Create welcome section with stats
create_welcome_section(lang_code)

# Add modern floating language switcher
create_modern_language_switcher()

# Functional search bar
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    search_term = st.text_input(
        "Search",
        placeholder="Search for buildings, facilities, services...",
        label_visibility="collapsed"
    )
    if search_term:
        # Filter dataframe based on search
        search_mask = (
            filtered_df[name_col].str.contains(search_term, case=False, na=False) |
            filtered_df[desc_col].str.contains(search_term, case=False, na=False) |
            filtered_df['Category'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[search_mask]
        st.success(f"Found {len(filtered_df)} results for '{search_term}'")

# Apply filters from sidebar
filtered_df = create_advanced_sidebar(df, lang_code)
if st.session_state.get('filtered_data') is not None:
    filtered_df = st.session_state['filtered_data']

# Interactive category filter
unique_categories = df['Category'].dropna().unique().tolist()
create_interactive_category_filter(unique_categories, lang_code)

# ---------- Main Tabs ----------
tab_map, tab_tour, tab_insights, tab_distance, tab_feedback = st.tabs([
    texts["map_tab"],
    texts["tour_tab"],
    texts["insights_tab"],
    texts["distance_tab"],
    texts["feedback_tab"]
])

with tab_map:
    # Section header
    st.markdown(f"### {texts['map_tab']}")
    st.markdown("Interactive campus locations with detailed information")
    
    # Display the enhanced map
    try:
        enhanced_map = create_enhanced_map(filtered_df, lang_code)
        st_folium(enhanced_map, width=None, height=600, returned_objects=["last_object_clicked"])
    except Exception as e:
        st.error(f"Error loading map: {str(e)}")
        # Fallback to simple map
        if filtered_df["Latitude"].notna().any() and filtered_df["Longitude"].notna().any():
            lat_center = float(filtered_df["Latitude"].mean())
            lon_center = float(filtered_df["Longitude"].mean())
        else:
            lat_center, lon_center = 35.7219, 51.3347
        
        simple_map = folium.Map(
            location=[lat_center, lon_center],
            zoom_start=15,
            tiles="OpenStreetMap"
        )
        
        # Add simple markers
        for _, row in filtered_df.iterrows():
            try:
                lat = float(row["Latitude"])
                lon = float(row["Longitude"])
                title = str(row.get(name_col, "")).strip() or "Location"
                
                folium.Marker(
                    [lat, lon],
                    tooltip=title,
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(simple_map)
            except (TypeError, ValueError):
                continue
        
        st_folium(simple_map, width=None, height=600)
    
    # Location cards section
    st.markdown("### Featured Locations")
    
    # Display location cards in grid
    if not filtered_df.empty:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(filtered_df.head(6).iterrows()):
            with cols[idx % 3]:
                pic_name = norm(str(row.get("name_pic", "")))
                img_path = resolve_image(pic_name) if pic_name else None
                create_location_card_enhanced(row.to_dict(), img_path, lang_code)
    else:
        st.info("No locations to display")

with tab_tour:
    st.subheader(texts["tour_tab"])
    
    if not st.session_state.get('tour_active', False):
        # Show tour selection
        create_tour_selection_ui(filtered_df, lang_code)
    else:
        # Active tour interface
        tour = st.session_state.get('active_tour')
        if tour:
            # Tour controls
            tour.create_tour_controls()
            
            # Display current stop
            if tour.current_step < len(tour.locations):
                current_location = tour.locations[tour.current_step]
                tour.display_tour_stop(current_location, tour.current_step)
                
                # Tour map
                tour_map = tour.create_tour_map(filtered_df, current_location)
                st_folium(tour_map, width=None, height=400)
            
            # Exit tour button
            if st.button("🚪 Exit Tour", type="secondary"):
                st.session_state['tour_active'] = False
                st.session_state['active_tour'] = None
                st.rerun()

with tab_insights:
    st.subheader(texts["insights_tab"])
    
    # Category distribution
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            counts = filtered_df["Category"].fillna("General").value_counts().reset_index()
            counts.columns = ["Category","Count"]
            
            fig = px.bar(
                counts, x="Category", y="Count",
                title="Locations by Category",
                color="Count",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.info("No data available for visualization.")
    
    with col2:
        # Statistics cards
        st.markdown("### 📊 Quick Stats")
        total_locations = len(filtered_df)
        categories = filtered_df["Category"].nunique()
        
        col_a, col_b = st.columns(2)
        with col_a:
            create_metric_card("Total Locations", str(total_locations))
        with col_b:
            create_metric_card("Categories", str(categories))
        
        # Most common category
        if not filtered_df.empty:
            top_category = filtered_df["Category"].mode().iloc[0] if not filtered_df["Category"].mode().empty else "N/A"
            st.info(f"Most common category: **{top_category}**")

with tab_distance:
    st.subheader(texts["distance_header"])
    valid = filtered_df.dropna(subset=["Latitude","Longitude"]).copy()
    valid["Label"] = valid[name_col].fillna(valid["Name_EN"]).fillna(valid["ID"].astype(str))
    
    if len(valid) < 2:
        create_info_banner(
            "Need at least two locations with valid coordinates.",
            "warning"
        )
    else:
        names = valid["Label"].tolist()
        c1, c2 = st.columns(2)
        
        with c1:
            a = st.selectbox(
                texts["distance_from"],
                names, index=0
            )
        with c2:
            b = st.selectbox(
                texts["distance_to"],
                names, index=1 if len(names)>1 else 0
            )
        
        if a and b:
            ra = valid.loc[valid["Label"]==a].iloc[0]
            rb = valid.loc[valid["Label"]==b].iloc[0]
            p1 = (float(ra["Latitude"]), float(ra["Longitude"]))
            p2 = (float(rb["Latitude"]), float(rb["Longitude"]))
            dist_km = geodesic(p1, p2).km
            
            # Display result
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                create_metric_card(
                    texts["distance_result"],
                    f"{dist_km:.2f} km",
                    f"+{dist_km*1000:.0f} meters" if dist_km < 1 else None
                )
            
            st.caption(texts["distance_note"])
            
            # Show path on map
            with st.expander("View Path on Map"):
                path_map = folium.Map(
                    location=[(p1[0]+p2[0])/2, (p1[1]+p2[1])/2],
                    zoom_start=15
                )
                
                # Add markers
                folium.Marker(p1, tooltip=a, icon=folium.Icon(color='green')).add_to(path_map)
                folium.Marker(p2, tooltip=b, icon=folium.Icon(color='red')).add_to(path_map)
                
                # Draw line
                folium.PolyLine([p1, p2], color='blue', weight=3, opacity=0.8).add_to(path_map)
                
                st_folium(path_map, width=None, height=400)

with tab_feedback:
    st.subheader(texts["feedback_tab"])
    
    # Select location for feedback
    valid_locations = filtered_df.dropna(subset=["Latitude","Longitude"]).copy()
    if not valid_locations.empty:
        location_names = valid_locations[name_col].fillna(valid_locations["Name_EN"]).tolist()
        
        selected_location = st.selectbox(
            "Select a location to review:",
            location_names
        )
        
        if selected_location:
            # Get location ID
            loc_row = valid_locations[
                (valid_locations[name_col] == selected_location) |
                (valid_locations["Name_EN"] == selected_location)
            ].iloc[0]
            
            location_id = str(loc_row.get('ID', 'unknown'))
            
            # Display location info
            col1, col2 = st.columns([2, 3])
            
            with col1:
                # Show image if available
                pic_name = norm(str(loc_row.get("name_pic","")))
                img_path = resolve_image(pic_name)
                if img_path:
                    data_uri = to_base64_uri(img_path)
                    if data_uri:
                        st.markdown(f'<img src="{data_uri}" style="width:100%;border-radius:10px;">', 
                                  unsafe_allow_html=True)
            
            with col2:
                # Create feedback widget
                feedback_system.create_rating_widget(location_id, selected_location, lang_code)
            
            # Show existing feedback
            feedback_system.display_recent_feedback(location_id, lang_code)
    
    # Feedback dashboard
    with st.expander("View Feedback Dashboard"):
        create_feedback_dashboard(feedback_system, lang_code)

# Add floating action button
add_floating_action_button("↑", "scrollToTop()")

# Footer
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #999;'>" 
    f"© 2024 Iran University of Science and Technology | Virtual Campus Tour" 
    f"</div>",
    unsafe_allow_html=True
)