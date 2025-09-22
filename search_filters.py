"""
Search and Filters Module - Advanced search and filtering capabilities
"""
import streamlit as st
import pandas as pd
from geopy.distance import geodesic
from typing import List, Dict, Optional

def create_advanced_sidebar(df: pd.DataFrame, lang_code: str = "en") -> pd.DataFrame:
    """Create advanced search and filter sidebar"""
    
    # Language-specific labels
    labels = get_filter_labels(lang_code)
    
    with st.sidebar:
        st.markdown(f"## {labels['search_title']}")
        
        # Search box
        search_term = st.text_input(
            labels['search_placeholder'],
            placeholder=labels['search_help'],
            help=labels['search_tooltip']
        )
        
        # Real-time search results counter
        if search_term:
            name_col = f"Name_{lang_code.upper()}" if lang_code != "fa" else "Name_FA"
            desc_col = f"Description_{lang_code.upper()}" if lang_code != "fa" else "Description_FA"
            
            matches = df[
                df[name_col].str.contains(search_term, case=False, na=False) |
                df[desc_col].str.contains(search_term, case=False, na=False) |
                df['Category'].str.contains(search_term, case=False, na=False)
            ]
            st.caption(f"{labels['found']} {len(matches)} {labels['results']}")
        
        st.markdown("---")
        
        # Category filter with icons
        categories = df['Category'].unique().tolist()
        category_icons = get_category_icons()
        
        selected_categories = st.multiselect(
            labels['categories'],
            categories,
            format_func=lambda x: f"{category_icons.get(x, '📍')} {x}"
        )
        
        # Advanced filters in expander
        with st.expander(labels['advanced_filters']):
            # Distance radius filter
            st.markdown(f"### {labels['distance_filter']}")
            col1, col2 = st.columns(2)
            
            with col1:
                name_col = f"Name_{lang_code.upper()}" if lang_code != "fa" else "Name_FA"
                center_point = st.selectbox(
                    labels['from_location'],
                    df[name_col].tolist() if name_col in df.columns else []
                )
            
            with col2:
                radius = st.slider(
                    labels['radius'],
                    0.1, 5.0, 1.0, 0.1
                )
            
            # Facility filters
            st.markdown(f"### {labels['facilities']}")
            facilities = {}
            facilities['parking'] = st.checkbox(labels['parking'])
            facilities['cafeteria'] = st.checkbox(labels['cafeteria'])
            facilities['wifi'] = st.checkbox(labels['wifi'])
            facilities['wheelchair'] = st.checkbox(labels['wheelchair'])
            facilities['prayer_room'] = st.checkbox(labels['prayer_room'])
            
            # Time-based filters
            st.markdown(f"### {labels['operating_hours']}")
            time_filters = {}
            time_filters['open_now'] = st.checkbox(labels['open_now'])
            time_filters['open_weekends'] = st.checkbox(labels['open_weekends'])
            time_filters['24_7'] = st.checkbox(labels['24_7'])
        
        # Sort options
        st.markdown("---")
        st.markdown(f"### {labels['sort_by']}")
        sort_options = [
            labels['alphabetical'],
            labels['distance'],
            labels['popular'],
            labels['recent']
        ]
        sort_by = st.radio(
            labels['sort_results'],
            sort_options,
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Apply filters button
        col1, col2 = st.columns(2)
        with col1:
            apply_button = st.button(
                labels['apply_filters'],
                type="primary",
                use_container_width=True
            )
        
        with col2:
            reset_button = st.button(
                labels['reset_all'],
                use_container_width=True
            )
        
        # Process filters
        if apply_button:
            filtered_df = apply_all_filters(
                df, search_term, selected_categories,
                center_point, radius, facilities,
                time_filters, sort_by, lang_code
            )
            st.success(f"{labels['showing']} {len(filtered_df)} {labels['locations']}")
            return filtered_df
        
        if reset_button:
            st.session_state.clear()
            st.rerun()
    
    return df

def get_filter_labels(lang_code: str) -> Dict[str, str]:
    """Get language-specific labels for filters"""
    labels = {
        "en": {
            "search_title": "🔍 Search & Filters",
            "search_placeholder": "Search locations",
            "search_help": "Type to search...",
            "search_tooltip": "Search by name, description, or category",
            "found": "Found",
            "results": "results",
            "categories": "Categories",
            "advanced_filters": "Advanced Filters",
            "distance_filter": "📍 Distance Filter",
            "from_location": "From location",
            "radius": "Radius (km)",
            "facilities": "🏢 Facilities",
            "parking": "🚗 Parking Available",
            "cafeteria": "☕ Cafeteria",
            "wifi": "📶 WiFi Zone",
            "wheelchair": "♿ Wheelchair Accessible",
            "prayer_room": "🕌 Prayer Room",
            "operating_hours": "🕐 Operating Hours",
            "open_now": "Open Now",
            "open_weekends": "Open on Weekends",
            "24_7": "24/7 Access",
            "sort_by": "🔄 Sort By",
            "sort_results": "Sort results by",
            "alphabetical": "Alphabetical",
            "distance": "Distance",
            "popular": "Most Popular",
            "recent": "Recently Added",
            "apply_filters": "Apply Filters 🎯",
            "reset_all": "Reset All",
            "showing": "Showing",
            "locations": "locations"
        },
        "ar": {
            "search_title": "🔍 البحث والفلاتر",
            "search_placeholder": "البحث عن المواقع",
            "search_help": "اكتب للبحث...",
            "search_tooltip": "البحث بالاسم أو الوصف أو الفئة",
            "found": "تم العثور على",
            "results": "نتيجة",
            "categories": "الفئات",
            "advanced_filters": "فلاتر متقدمة",
            "distance_filter": "📍 تصفية المسافة",
            "from_location": "من الموقع",
            "radius": "نصف القطر (كم)",
            "facilities": "🏢 المرافق",
            "parking": "🚗 موقف سيارات متاح",
            "cafeteria": "☕ كافيتيريا",
            "wifi": "📶 منطقة واي فاي",
            "wheelchair": "♿ متاح للكراسي المتحركة",
            "prayer_room": "🕌 غرفة الصلاة",
            "operating_hours": "🕐 ساعات العمل",
            "open_now": "مفتوح الآن",
            "open_weekends": "مفتوح في عطلات نهاية الأسبوع",
            "24_7": "متاح 24/7",
            "sort_by": "🔄 ترتيب حسب",
            "sort_results": "ترتيب النتائج حسب",
            "alphabetical": "أبجدي",
            "distance": "المسافة",
            "popular": "الأكثر شعبية",
            "recent": "المضاف حديثاً",
            "apply_filters": "تطبيق الفلاتر 🎯",
            "reset_all": "إعادة تعيين الكل",
            "showing": "عرض",
            "locations": "موقع"
        },
        "fa": {
            "search_title": "🔍 جستجو و فیلترها",
            "search_placeholder": "جستجوی مکان‌ها",
            "search_help": "برای جستجو تایپ کنید...",
            "search_tooltip": "جستجو بر اساس نام، توضیحات یا دسته‌بندی",
            "found": "یافت شد",
            "results": "نتیجه",
            "categories": "دسته‌بندی‌ها",
            "advanced_filters": "فیلترهای پیشرفته",
            "distance_filter": "📍 فیلتر فاصله",
            "from_location": "از مکان",
            "radius": "شعاع (کیلومتر)",
            "facilities": "🏢 امکانات",
            "parking": "🚗 پارکینگ موجود",
            "cafeteria": "☕ کافه‌تریا",
            "wifi": "📶 منطقه وای‌فای",
            "wheelchair": "♿ دسترسی ویلچر",
            "prayer_room": "🕌 نمازخانه",
            "operating_hours": "🕐 ساعات کاری",
            "open_now": "اکنون باز",
            "open_weekends": "آخر هفته باز",
            "24_7": "دسترسی 24/7",
            "sort_by": "🔄 مرتب‌سازی بر اساس",
            "sort_results": "مرتب‌سازی نتایج بر اساس",
            "alphabetical": "الفبایی",
            "distance": "فاصله",
            "popular": "محبوب‌ترین",
            "recent": "اخیراً اضافه شده",
            "apply_filters": "اعمال فیلترها 🎯",
            "reset_all": "بازنشانی همه",
            "showing": "نمایش",
            "locations": "مکان"
        }
    }
    
    return labels.get(lang_code, labels["en"])

def get_category_icons() -> Dict[str, str]:
    """Get icons for different categories"""
    return {
        "Engineering": "🏗️",
        "Sports": "⚽",
        "Academic": "📚",
        "Administrative": "🏛️",
        "Student Services": "👥",
        "Library": "📖",
        "Research": "🔬",
        "Medical": "🏥",
        "Cafeteria": "🍽️",
        "Parking": "🚗",
        "Dormitory": "🏠",
        "Laboratory": "🧪",
        "General": "📍"
    }

def apply_all_filters(
    df: pd.DataFrame,
    search_term: str,
    categories: List[str],
    center_point: str,
    radius: float,
    facilities: Dict[str, bool],
    time_filters: Dict[str, bool],
    sort_by: str,
    lang_code: str
) -> pd.DataFrame:
    """Apply all filters to dataframe"""
    filtered = df.copy()
    
    # Text search across all language columns
    if search_term:
        search_cols = []
        for lang in ["EN", "AR", "FA"]:
            if f"Name_{lang}" in filtered.columns:
                search_cols.append(f"Name_{lang}")
            if f"Description_{lang}" in filtered.columns:
                search_cols.append(f"Description_{lang}")
        
        if search_cols:
            mask = filtered[search_cols[0]].str.contains(search_term, case=False, na=False)
            for col in search_cols[1:]:
                mask |= filtered[col].str.contains(search_term, case=False, na=False)
            filtered = filtered[mask]
    
    # Category filter
    if categories:
        filtered = filtered[filtered['Category'].isin(categories)]
    
    # Distance filter
    if center_point and radius:
        name_col = f"Name_{lang_code.upper()}" if lang_code != "fa" else "Name_FA"
        if name_col in df.columns:
            center_row = df[df[name_col] == center_point]
            if not center_row.empty:
                center_lat = center_row.iloc[0]['Latitude']
                center_lon = center_row.iloc[0]['Longitude']
                
                def within_radius(row):
                    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
                        distance = geodesic(
                            (center_lat, center_lon),
                            (row['Latitude'], row['Longitude'])
                        ).km
                        return distance <= radius
                    return False
                
                filtered = filtered[filtered.apply(within_radius, axis=1)]
    
    # Facility filters (assuming these columns exist or using mock data)
    # In production, these would be actual columns in your Excel file
    if facilities.get('parking'):
        # filtered = filtered[filtered.get('has_parking', True)]
        pass  # Placeholder for actual filter
    
    # Sorting
    labels = get_filter_labels(lang_code)
    name_col = f"Name_{lang_code.upper()}" if lang_code != "fa" else "Name_FA"
    
    if sort_by == labels['alphabetical'] and name_col in filtered.columns:
        filtered = filtered.sort_values(name_col)
    elif sort_by == labels['distance'] and center_point:
        # Calculate distances and sort
        if not filtered.empty and center_point:
            center_row = df[df[name_col] == center_point]
            if not center_row.empty:
                center_lat = center_row.iloc[0]['Latitude']
                center_lon = center_row.iloc[0]['Longitude']
                
                filtered['_distance'] = filtered.apply(
                    lambda row: geodesic(
                        (center_lat, center_lon),
                        (row['Latitude'], row['Longitude'])
                    ).km if pd.notna(row['Latitude']) and pd.notna(row['Longitude']) else float('inf'),
                    axis=1
                )
                filtered = filtered.sort_values('_distance')
                filtered = filtered.drop('_distance', axis=1)
    
    return filtered

def create_search_suggestions(df: pd.DataFrame, search_term: str, lang_code: str) -> List[str]:
    """Generate search suggestions based on partial input"""
    if not search_term or len(search_term) < 2:
        return []
    
    suggestions = set()
    name_col = f"Name_{lang_code.upper()}" if lang_code != "fa" else "Name_FA"
    
    # Add matching location names
    if name_col in df.columns:
        matches = df[df[name_col].str.contains(search_term, case=False, na=False)][name_col]
        suggestions.update(matches.tolist()[:5])
    
    # Add matching categories
    category_matches = df[df['Category'].str.contains(search_term, case=False, na=False)]['Category'].unique()
    suggestions.update(category_matches[:3])
    
    return list(suggestions)[:8]  # Return max 8 suggestions

def create_quick_filters(df: pd.DataFrame, lang_code: str):
    """Create quick filter buttons for common searches"""
    labels = {
        "en": {
            "nearby": "📍 Nearby",
            "open_now": "🕐 Open Now",
            "popular": "⭐ Popular",
            "new": "🆕 New"
        },
        "ar": {
            "nearby": "📍 قريب",
            "open_now": "🕐 مفتوح الآن",
            "popular": "⭐ شائع",
            "new": "🆕 جديد"
        },
        "fa": {
            "nearby": "📍 نزدیک",
            "open_now": "🕐 باز",
            "popular": "⭐ محبوب",
            "new": "🆕 جدید"
        }
    }
    
    quick_labels = labels.get(lang_code, labels["en"])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(quick_labels["nearby"], use_container_width=True):
            st.session_state['quick_filter'] = 'nearby'
    
    with col2:
        if st.button(quick_labels["open_now"], use_container_width=True):
            st.session_state['quick_filter'] = 'open_now'
    
    with col3:
        if st.button(quick_labels["popular"], use_container_width=True):
            st.session_state['quick_filter'] = 'popular'
    
    with col4:
        if st.button(quick_labels["new"], use_container_width=True):
            st.session_state['quick_filter'] = 'new'