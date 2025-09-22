"""
Enhanced UI Components - Modern, clean design with improved UX
"""
import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
import folium
from folium import Icon, Marker, CircleMarker
try:
    from folium import plugins
except ImportError:
    plugins = None
import base64
from pathlib import Path

def create_welcome_section(lang_code: str = "en"):
    """Create an engaging welcome section with stats"""
    
    texts = {
        "en": {
            "welcome": "Welcome to IUST Virtual Campus",
            "explore": "Explore Our Campus",
            "discover": "Discover amazing places, facilities, and services",
            "stats_buildings": "Buildings",
            "stats_facilities": "Facilities",
            "stats_services": "Services",
            "stats_areas": "Green Areas"
        },
        "ar": {
            "welcome": "مرحبًا بكم في الحرم الجامعي الافتراضي IUST",
            "explore": "استكشف حرمنا الجامعي",
            "discover": "اكتشف أماكن ومرافق وخدمات مذهلة",
            "stats_buildings": "المباني",
            "stats_facilities": "المرافق",
            "stats_services": "الخدمات",
            "stats_areas": "المساحات الخضراء"
        },
        "fa": {
            "welcome": "به پردیس مجازی IUST خوش آمدید",
            "explore": "پردیس ما را کاوش کنید",
            "discover": "مکان‌ها، امکانات و خدمات شگفت‌انگیز را کشف کنید",
            "stats_buildings": "ساختمان‌ها",
            "stats_facilities": "امکانات",
            "stats_services": "خدمات",
            "stats_areas": "فضاهای سبز"
        }
    }
    
    text = texts.get(lang_code, texts["en"])
    
    # Create welcome banner with gradient background
    welcome_html = f'''
    <div style="
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        color: black;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(220, 20, 60, 0.3);
    ">
        <div style="position: relative; z-index: 1;">
            <h1 style="
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 0.5rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                color: white;
            ">{text["welcome"]}</h1>
            <h2 style="
                font-size: 1.3rem;
                font-weight: 300;
                margin-bottom: 1rem;
                opacity: 0.95;
                color: white;
            ">{text["explore"]}</h2>
            <p style="
                font-size: 1rem;
                opacity: 0.9;
                max-width: 600px;
                margin: 0 auto;
                color: white;
            ">{text["discover"]}</p>
        </div>
    </div>
    '''
    
    st.markdown(welcome_html, unsafe_allow_html=True)
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("🏢", "45+", text['stats_buildings']),
        ("🎓", "30+", text['stats_facilities']),
        ("🔧", "20+", text['stats_services']),
        ("🌳", "15+", text['stats_areas'])
    ]
    
    for col, (icon, number, label) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                transition: transform 0.3s ease;
                cursor: pointer;
            " onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-size: 2rem; font-weight: 700; color: #1e293b;">{number}</div>
                <div style="color: #64748b; font-size: 0.9rem; margin-top: 0.5rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

def create_location_card_enhanced(location_data: Dict, image_path: Optional[Path] = None, lang_code: str = "en"):
    """Create an enhanced location card with better visual design"""
    
    name = location_data.get(f'Name_{lang_code.upper()}', location_data.get('Name_EN', 'Unknown'))
    description = location_data.get(f'Description_{lang_code.upper()}', '')
    category = location_data.get('Category', 'General')
    
    # Category colors and icons
    category_styles = {
        'Engineering': {'color': '#ef4444', 'icon': '🏭'},
        'Library': {'color': '#8b5cf6', 'icon': '📚'},
        'Sports': {'color': '#10b981', 'icon': '⚽'},
        'Administration': {'color': '#3b82f6', 'icon': '🏢'},
        'Food': {'color': '#f59e0b', 'icon': '🍽️'},
        'Medical': {'color': '#ec4899', 'icon': '🏥'},
        'General': {'color': '#6b7280', 'icon': '📍'}
    }
    
    style = category_styles.get(category, category_styles['General'])
    
    # Image handling
    image_html = ""
    if image_path and image_path.exists():
        try:
            with open(image_path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
                image_html = f"""
                <div style="
                    width: 100%;
                    height: 200px;
                    background-image: url('data:image/jpeg;base64,{data}');
                    background-size: cover;
                    background-position: center;
                    border-radius: 15px 15px 0 0;
                "></div>
                """
        except:
            pass
    
    if not image_html:
        # Placeholder if no image
        image_html = f"""
        <div style="
            width: 100%;
            height: 200px;
            background: linear-gradient(135deg, {style['color']}40 0%, {style['color']}20 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 15px 15px 0 0;
            font-size: 4rem;
        ">{style['icon']}</div>
        """
    
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        margin-bottom: 1.5rem;
    " onmouseover="this.style.transform='translateY(-10px); this.style.boxShadow='0 15px 35px rgba(0,0,0,0.12)'" 
       onmouseout="this.style.transform='translateY(0); this.style.boxShadow='0 10px 25px rgba(0,0,0,0.08)'">
        {image_html}
        <div style="padding: 1.5rem;">
            <div style="
                display: flex;
                align-items: center;
                margin-bottom: 0.5rem;
            ">
                <span style="
                    background: {style['color']}15;
                    color: {style['color']};
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.85rem;
                    font-weight: 600;
                ">{style['icon']} {category}</span>
            </div>
            <h3 style="
                color: #1e293b;
                font-size: 1.25rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            ">{name}</h3>
            <p style="
                color: #64748b;
                font-size: 0.95rem;
                line-height: 1.6;
                margin-bottom: 1rem;
            ">{description[:150]}{'...' if len(description) > 150 else ''}</p>
            <div style="
                display: flex;
                gap: 0.5rem;
            ">
                <button style="
                    background: linear-gradient(135deg, #DC143C 0%, #B91C3C 100%);
                    color: white;
                    border: none;
                    padding: 0.5rem 1.25rem;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">View Details</button>
                <button style="
                    background: white;
                    color: #64748b;
                    border: 2px solid #e2e8f0;
                    padding: 0.5rem 1.25rem;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">Get Directions</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_interactive_category_filter(categories: List[str], lang_code: str = "en"):
    """Create interactive category filter with visual cards"""
    
    category_data = {
        'Engineering': {'icon': '🏭', 'color': '#ef4444'},
        'Library': {'icon': '📚', 'color': '#8b5cf6'},
        'Sports': {'icon': '⚽', 'color': '#10b981'},
        'Administration': {'icon': '🏢', 'color': '#3b82f6'},
        'Food': {'icon': '🍽️', 'color': '#f59e0b'},
        'Medical': {'icon': '🏥', 'color': '#ec4899'},
        'Parking': {'icon': '🚗', 'color': '#06b6d4'},
        'Dormitory': {'icon': '🏠', 'color': '#f97316'}
    }
    
    st.markdown("""
    <style>
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .category-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .category-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    .category-card.active {
        border-color: #DC143C;
        background: #DC143C10;
    }
    
    .category-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .category-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #334155;
    }
    
    .category-count {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create category grid
    cols = st.columns(4)
    selected_categories = []
    
    for idx, cat in enumerate(categories[:8]):  # Show first 8 categories
        col_idx = idx % 4
        data = category_data.get(cat, {'icon': '📍', 'color': '#6b7280'})
        
        with cols[col_idx]:
            if st.button(
                f"{data['icon']} {cat}",
                key=f"cat_{cat}",
                use_container_width=True
            ):
                if cat not in st.session_state.get('selected_categories', []):
                    if 'selected_categories' not in st.session_state:
                        st.session_state.selected_categories = []
                    st.session_state.selected_categories.append(cat)
                else:
                    st.session_state.selected_categories.remove(cat)
                st.rerun()

def create_enhanced_map(df: pd.DataFrame, lang_code: str = "en"):
    """Create an enhanced interactive map with better styling"""
    
    # Calculate map center
    if df["Latitude"].notna().any() and df["Longitude"].notna().any():
        lat_center = float(df["Latitude"].mean())
        lon_center = float(df["Longitude"].mean())
    else:
        lat_center, lon_center = 35.7219, 51.3347
    
    # Create map with custom styling
    m = folium.Map(
        location=[lat_center, lon_center],
        zoom_start=15,
        tiles=None,
        prefer_canvas=True,
        zoom_control=False
    )
    
    # Add custom tile layer with attribution
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name='Light',
        control=True
    ).add_to(m)
    
    # Add alternative dark layer
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name='Dark',
        control=True
    ).add_to(m)
    
    # Custom zoom control if plugins available
    if plugins:
        try:
            plugins.Fullscreen(
                position='topright',
                title='Fullscreen',
                title_cancel='Exit fullscreen',
                force_separate_button=True
            ).add_to(m)
            
            # Add marker cluster
            from folium.plugins import MarkerCluster
            marker_cluster = MarkerCluster(
                name='Clustered Markers',
                control=True
            ).add_to(m)
        except:
            # If plugins fail, markers will be added directly to map
            marker_cluster = m
    else:
        marker_cluster = m
    
    # Category styling
    category_styles = {
        'Engineering': {'color': 'darkred', 'icon': 'cog'},
        'Library': {'color': 'purple', 'icon': 'book'},
        'Sports': {'color': 'green', 'icon': 'trophy'},
        'Administration': {'color': 'blue', 'icon': 'briefcase'},
        'Food': {'color': 'orange', 'icon': 'cutlery'},
        'Medical': {'color': 'pink', 'icon': 'medkit'},
        'Parking': {'color': 'gray', 'icon': 'car'},
        'General': {'color': 'red', 'icon': 'info-sign'}
    }
    
    # Add markers
    for _, row in df.iterrows():
        try:
            lat = float(row["Latitude"])
            lon = float(row["Longitude"])
        except (TypeError, ValueError):
            continue
        
        name_col = f"Name_{lang_code.upper()}" if lang_code != "fa" else "Name_FA"
        desc_col = f"Description_{lang_code.upper()}" if lang_code != "fa" else "Description_FA"
        
        title = str(row.get(name_col, "")).strip() or str(row.get("Name_EN", "")).strip()
        description = str(row.get(desc_col, "")).strip()
        category = str(row.get('Category', 'General'))
        
        style = category_styles.get(category, category_styles['General'])
        
        # Create rich HTML popup
        popup_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; width: 250px;">
            <div style="background: linear-gradient(135deg, #DC143C 0%, #B91C3C 100%); 
                        color: white; padding: 10px; margin: -10px -10px 10px -10px;
                        border-radius: 4px 4px 0 0;">
                <b style="font-size: 16px;">{title}</b>
            </div>
            <div style="padding: 0 10px 10px 10px;">
                <p style="color: #666; font-size: 14px; margin: 0 0 10px 0;">{description[:200]}{'...' if len(description) > 200 else ''}</p>
                <div style="display: flex; gap: 5px;">
                    <span style="background: #f0f0f0; padding: 3px 8px; border-radius: 12px; font-size: 12px;">
                        {category}
                    </span>
                </div>
            </div>
        </div>
        """
        
        # Add marker with custom icon
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=folium.Tooltip(title),
            icon=folium.Icon(
                color=style['color'],
                icon=style['icon'],
                prefix='fa'
            )
        ).add_to(marker_cluster)
    
    # Add layer control
    folium.LayerControl(position='topright').add_to(m)
    
    # Add custom CSS for map
    css = """
    <style>
    .leaflet-popup-content-wrapper {
        border-radius: 8px !important;
        box-shadow: 0 3px 14px rgba(0,0,0,0.4) !important;
    }
    .leaflet-popup-tip {
        box-shadow: 0 3px 14px rgba(0,0,0,0.4) !important;
    }
    </style>
    """
    m.get_root().html.add_child(folium.Element(css))
    
    return m

def create_search_bar_enhanced():
    """Create an enhanced search bar with suggestions"""
    st.markdown("""
    <style>
    .search-container {
        background: white;
        border-radius: 50px;
        padding: 0.75rem 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        margin: 2rem 0;
    }
    
    .search-icon {
        color: #64748b;
        margin-right: 1rem;
        font-size: 1.2rem;
    }
    
    .search-input {
        border: none;
        outline: none;
        width: 100%;
        font-size: 1rem;
        color: #334155;
    }
    
    .search-input::placeholder {
        color: #94a3b8;
    }
    
    .search-button {
        background: linear-gradient(135deg, #DC143C 0%, #B91C3C 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .search-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.3);
    }
    </style>
    
    <div class="search-container">
        <span class="search-icon">🔍</span>
        <input type="text" class="search-input" placeholder="Search for buildings, facilities, services..." />
        <button class="search-button">Search</button>
    </div>
    """, unsafe_allow_html=True)

def create_navigation_tabs_enhanced():
    """Create enhanced navigation tabs with better styling"""
    st.markdown("""
    <style>
    .nav-tabs {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        background: white;
        padding: 0.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .nav-tab {
        flex: 1;
        padding: 1rem;
        border: none;
        background: transparent;
        border-radius: 10px;
        font-weight: 600;
        color: #64748b;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .nav-tab:hover {
        background: #f8fafc;
        color: #334155;
    }
    
    .nav-tab.active {
        background: linear-gradient(135deg, #DC143C 0%, #B91C3C 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.2);
    }
    
    .nav-tab-icon {
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)