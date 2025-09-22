"""
Insights Module - Advanced analytics and alumni showcase
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from typing import Dict, List

def create_campus_highlights_tab(df: pd.DataFrame, lang_code: str = "en"):
    """Tab showing featured locations and campus achievements"""
    
    labels = get_insights_labels(lang_code)
    st.subheader(f"🌟 {labels['campus_highlights']}")
    
    # Featured locations carousel
    featured_locations = get_featured_locations(lang_code)
    
    # Create selection slider
    if featured_locations:
        selected = st.select_slider(
            labels['featured_locations'],
            options=range(len(featured_locations)),
            format_func=lambda x: featured_locations[x]['name'],
            label_visibility="collapsed"
        )
        
        location = featured_locations[selected]
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display featured location card
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.85));
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            ">
                <h3 style="color: #667eea;">{location['name']}</h3>
                <p style="color: #666; font-size: 1.1rem; margin: 1rem 0;">
                    {location['highlight']}
                </p>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    {' '.join([f'<span style="background: #667eea; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;">{tag}</span>' for tag in location.get('tags', [])])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Display statistics
            for stat_name, stat_value in location['stats'].items():
                st.metric(stat_name, stat_value)
    
    # Timeline of achievements
    st.markdown(f"### 📅 {labels['recent_achievements']}")
    
    timeline_data = get_timeline_data(lang_code)
    if timeline_data:
        fig = create_timeline_chart(timeline_data, lang_code)
        st.plotly_chart(fig, use_container_width=True)

def create_visitor_insights_tab(df: pd.DataFrame, lang_code: str = "en"):
    """Tab showing visitor patterns and popular routes"""
    
    labels = get_insights_labels(lang_code)
    st.subheader(f"👥 {labels['visitor_insights']}")
    
    # Simulated visitor data
    visitor_data = generate_visitor_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Peak visit times
        st.markdown(f"### 🕐 {labels['peak_times']}")
        fig = px.line(
            x=visitor_data['hour'],
            y=visitor_data['visitors'],
            title=labels['hourly_pattern'],
            labels={'x': labels['hour'], 'y': labels['visitors']}
        )
        fig.update_traces(fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.2)', line_color='#667eea')
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Popular routes
        st.markdown(f"### 🛤️ {labels['popular_routes']}")
        routes = get_popular_routes(lang_code)
        
        fig = px.pie(
            values=list(routes.values()),
            names=list(routes.keys()),
            title=labels['most_popular_tours'],
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#ffa0a0', '#88d3ce']
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Visitor flow visualization
    st.markdown(f"### 🗺️ {labels['visitor_flow']}")
    
    # Create Sankey diagram for visitor flow
    fig = create_visitor_flow_diagram(lang_code)
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly patterns
    st.markdown(f"### 📊 {labels['weekly_patterns']}")
    weekly_data = generate_weekly_data(lang_code)
    
    fig = px.bar(
        weekly_data,
        x='day',
        y='visitors',
        color='type',
        title=labels['visitors_by_day'],
        barmode='group',
        color_discrete_map={'Student': '#667eea', 'Visitor': '#764ba2', 'Staff': '#f093fb'}
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def create_alumni_showcase_tab(df: pd.DataFrame, lang_code: str = "en"):
    """Tab showcasing notable alumni and their connection to locations"""
    
    labels = get_insights_labels(lang_code)
    st.subheader(f"🎓 {labels['notable_alumni']}")
    
    alumni_data = get_alumni_data(lang_code)
    
    # Alumni search/filter
    search_term = st.text_input(
        labels['search_alumni'],
        placeholder=labels['search_placeholder']
    )
    
    # Filter alumni if search term provided
    if search_term:
        alumni_data = [
            alum for alum in alumni_data 
            if search_term.lower() in alum['name'].lower() or 
               search_term.lower() in alum['achievement'].lower()
        ]
    
    # Display alumni cards
    for idx, alum in enumerate(alumni_data):
        with st.expander(f"🌟 {alum['name']} - {labels['class_of']} {alum['year']}"):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                # Alumni photo placeholder
                st.markdown(f"""
                <div style="
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 2rem;
                    font-weight: bold;
                ">
                    {alum['name'][0]}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                **{labels['achievement']}:**  
                {alum['achievement']}
                
                **{labels['department']}:**  
                {alum['department']}
                
                **{labels['favorite_spot']}:**  
                {alum['location']}
                """)
            
            with col3:
                st.info(f'"{alum["quote"]}"')
                
                if st.button(
                    f"{labels['visit']} {alum['location']}", 
                    key=f"alum_{idx}_{alum['name']}"
                ):
                    st.session_state['focus_location'] = alum['location']
                    st.success(labels['location_selected'])
    
    # Alumni statistics
    st.markdown(f"### 📊 {labels['alumni_impact']}")
    
    impact_metrics = get_alumni_metrics(lang_code)
    
    cols = st.columns(len(impact_metrics))
    for col, (metric, value) in zip(cols, impact_metrics.items()):
        col.metric(metric, value)
    
    # Alumni distribution by field
    st.markdown(f"### 🌍 {labels['alumni_fields']}")
    
    fields_data = get_alumni_fields_distribution(lang_code)
    fig = px.treemap(
        fields_data,
        path=['field', 'subfield'],
        values='count',
        title=labels['alumni_by_field'],
        color='count',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def get_insights_labels(lang_code: str) -> Dict[str, str]:
    """Get language-specific labels for insights"""
    labels = {
        "en": {
            "campus_highlights": "Campus Highlights",
            "featured_locations": "Featured Locations",
            "recent_achievements": "Recent Achievements",
            "visitor_insights": "Visitor Insights",
            "peak_times": "Peak Visit Times",
            "hourly_pattern": "Hourly Visitor Pattern",
            "hour": "Hour",
            "visitors": "Visitors",
            "popular_routes": "Popular Routes",
            "most_popular_tours": "Most Popular Tours",
            "visitor_flow": "Visitor Flow Map",
            "weekly_patterns": "Weekly Patterns",
            "visitors_by_day": "Visitors by Day",
            "notable_alumni": "Notable Alumni",
            "search_alumni": "Search Alumni",
            "search_placeholder": "Name or achievement...",
            "class_of": "Class of",
            "achievement": "Achievement",
            "department": "Department",
            "favorite_spot": "Favorite Campus Spot",
            "visit": "Visit",
            "location_selected": "Location marked on map",
            "alumni_impact": "Alumni Impact",
            "alumni_fields": "Alumni Distribution by Field",
            "alumni_by_field": "Alumni Professional Fields"
        },
        "ar": {
            "campus_highlights": "أبرز معالم الحرم الجامعي",
            "featured_locations": "المواقع المميزة",
            "recent_achievements": "الإنجازات الأخيرة",
            "visitor_insights": "إحصائيات الزوار",
            "peak_times": "أوقات الذروة",
            "hourly_pattern": "نمط الزيارات بالساعة",
            "hour": "الساعة",
            "visitors": "الزوار",
            "popular_routes": "المسارات الشائعة",
            "most_popular_tours": "الجولات الأكثر شعبية",
            "visitor_flow": "خريطة تدفق الزوار",
            "weekly_patterns": "الأنماط الأسبوعية",
            "visitors_by_day": "الزوار حسب اليوم",
            "notable_alumni": "الخريجون المتميزون",
            "search_alumni": "البحث عن الخريجين",
            "search_placeholder": "الاسم أو الإنجاز...",
            "class_of": "دفعة",
            "achievement": "الإنجاز",
            "department": "القسم",
            "favorite_spot": "المكان المفضل في الحرم",
            "visit": "زيارة",
            "location_selected": "تم تحديد الموقع على الخريطة",
            "alumni_impact": "تأثير الخريجين",
            "alumni_fields": "توزيع الخريجين حسب المجال",
            "alumni_by_field": "مجالات عمل الخريجين"
        },
        "fa": {
            "campus_highlights": "نقاط برجسته پردیس",
            "featured_locations": "مکان‌های ویژه",
            "recent_achievements": "دستاوردهای اخیر",
            "visitor_insights": "آمار بازدیدکنندگان",
            "peak_times": "ساعات شلوغی",
            "hourly_pattern": "الگوی بازدید ساعتی",
            "hour": "ساعت",
            "visitors": "بازدیدکنندگان",
            "popular_routes": "مسیرهای محبوب",
            "most_popular_tours": "محبوب‌ترین تورها",
            "visitor_flow": "نقشه جریان بازدیدکنندگان",
            "weekly_patterns": "الگوهای هفتگی",
            "visitors_by_day": "بازدیدکنندگان بر اساس روز",
            "notable_alumni": "فارغ‌التحصیلان برجسته",
            "search_alumni": "جستجوی فارغ‌التحصیلان",
            "search_placeholder": "نام یا دستاورد...",
            "class_of": "فارغ‌التحصیل سال",
            "achievement": "دستاورد",
            "department": "بخش",
            "favorite_spot": "مکان مورد علاقه در پردیس",
            "visit": "بازدید",
            "location_selected": "مکان روی نقشه مشخص شد",
            "alumni_impact": "تأثیر فارغ‌التحصیلان",
            "alumni_fields": "توزیع فارغ‌التحصیلان بر اساس رشته",
            "alumni_by_field": "زمینه‌های کاری فارغ‌التحصیلان"
        }
    }
    return labels.get(lang_code, labels["en"])

def get_featured_locations(lang_code: str) -> List[Dict]:
    """Get featured campus locations with statistics"""
    if lang_code == "en":
        return [
            {
                'name': 'Innovation Hub',
                'highlight': 'Home to 50+ startups and tech companies',
                'stats': {
                    'Startups': '52',
                    'Patents': '128',
                    'Awards': '15'
                },
                'tags': ['Technology', 'Innovation', 'Entrepreneurship']
            },
            {
                'name': 'Research Center',
                'highlight': 'Leading AI and robotics research in Middle East',
                'stats': {
                    'Publications': '342',
                    'Citations': '5,420',
                    'Projects': '28'
                },
                'tags': ['Research', 'AI', 'Robotics']
            },
            {
                'name': 'Central Library',
                'highlight': '24/7 access with 100,000+ volumes',
                'stats': {
                    'Books': '100K+',
                    'Digital Resources': '50K+',
                    'Study Spaces': '500'
                },
                'tags': ['Study', '24/7', 'Resources']
            }
        ]
    # Add Arabic and Farsi translations as needed
    return []

def get_timeline_data(lang_code: str) -> List[Dict]:
    """Get timeline data for achievements"""
    base_date = datetime.now()
    
    if lang_code == "en":
        return [
            {
                'date': (base_date - timedelta(days=30)).strftime('%Y-%m-%d'),
                'event': 'AI Lab Grand Opening',
                'category': 'Infrastructure',
                'description': 'State-of-the-art AI research facility opened'
            },
            {
                'date': (base_date - timedelta(days=60)).strftime('%Y-%m-%d'),
                'event': 'MIT Partnership Announced',
                'category': 'Partnership',
                'description': 'Collaboration agreement with MIT signed'
            },
            {
                'date': (base_date - timedelta(days=90)).strftime('%Y-%m-%d'),
                'event': 'National Innovation Award',
                'category': 'Achievement',
                'description': 'Student startup wins national competition'
            }
        ]
    return []

def create_timeline_chart(timeline_data: List[Dict], lang_code: str):
    """Create timeline visualization"""
    df = pd.DataFrame(timeline_data)
    
    fig = px.scatter(
        df,
        x='date',
        y='category',
        text='event',
        color='category',
        size_max=20,
        height=300,
        color_discrete_map={
            'Infrastructure': '#667eea',
            'Partnership': '#764ba2',
            'Achievement': '#f093fb'
        }
    )
    
    fig.update_traces(
        textposition='top center',
        marker=dict(size=15, line=dict(width=2, color='white'))
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_title="Date",
        yaxis_title="Category"
    )
    
    return fig

def generate_visitor_data() -> Dict:
    """Generate simulated visitor data"""
    return {
        'hour': list(range(8, 18)),
        'visitors': [20, 45, 60, 80, 95, 110, 100, 120, 90, 70],
        'day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'daily_visitors': [450, 480, 520, 510, 490, 350, 280]
    }

def get_popular_routes(lang_code: str) -> Dict:
    """Get popular tour routes"""
    if lang_code == "en":
        return {
            "Engineering Tour": 145,
            "Full Campus": 132,
            "Research Facilities": 98,
            "Student Life": 87,
            "Quick Overview": 76
        }
    elif lang_code == "ar":
        return {
            "جولة الهندسة": 145,
            "الحرم الكامل": 132,
            "مرافق البحث": 98,
            "الحياة الطلابية": 87,
            "نظرة سريعة": 76
        }
    else:  # Farsi
        return {
            "تور مهندسی": 145,
            "کل پردیس": 132,
            "امکانات تحقیقاتی": 98,
            "زندگی دانشجویی": 87,
            "بررسی سریع": 76
        }

def create_visitor_flow_diagram(lang_code: str):
    """Create Sankey diagram for visitor flow"""
    
    labels_dict = {
        "en": ["Main Gate", "Library", "Engineering", "Sports Complex", "Cafeteria", "Exit"],
        "ar": ["البوابة الرئيسية", "المكتبة", "الهندسة", "المجمع الرياضي", "الكافيتيريا", "الخروج"],
        "fa": ["دروازه اصلی", "کتابخانه", "مهندسی", "مجموعه ورزشی", "کافه‌تریا", "خروج"]
    }
    
    labels = labels_dict.get(lang_code, labels_dict["en"])
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=["#667eea", "#764ba2", "#f093fb", "#ffa0a0", "#88d3ce", "#808080"]
        ),
        link=dict(
            source=[0, 0, 0, 1, 2, 2, 3, 4],
            target=[1, 2, 3, 4, 3, 5, 5, 5],
            value=[40, 60, 30, 25, 35, 40, 20, 15],
            color=["rgba(102, 126, 234, 0.4)"] * 8
        )
    )])
    
    fig.update_layout(
        title_text="Common Visitor Paths Through Campus",
        font_size=10,
        height=400
    )
    
    return fig

def generate_weekly_data(lang_code: str) -> pd.DataFrame:
    """Generate weekly visitor pattern data"""
    days = {
        "en": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        "ar": ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد'],
        "fa": ['دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه', 'شنبه', 'یکشنبه']
    }
    
    data = []
    for i, day in enumerate(days.get(lang_code, days["en"])):
        data.append({'day': day, 'type': 'Student', 'visitors': random.randint(200, 400)})
        data.append({'day': day, 'type': 'Visitor', 'visitors': random.randint(50, 150)})
        data.append({'day': day, 'type': 'Staff', 'visitors': random.randint(100, 200)})
    
    return pd.DataFrame(data)

def get_alumni_data(lang_code: str) -> List[Dict]:
    """Get notable alumni data"""
    if lang_code == "en":
        return [
            {
                'name': 'Dr. Sarah Johnson',
                'year': '2010',
                'achievement': 'NASA Mars Mission Lead Engineer',
                'department': 'Aerospace Engineering',
                'location': 'Engineering Building',
                'quote': 'The labs here shaped my passion for space exploration.'
            },
            {
                'name': 'Ahmed Al-Rashid',
                'year': '2015',
                'achievement': 'Forbes 30 Under 30 - Tech Entrepreneur',
                'department': 'Computer Science',
                'location': 'Innovation Hub',
                'quote': 'This is where my startup journey began.'
            },
            {
                'name': 'Dr. Fatima Mohammadi',
                'year': '2008',
                'achievement': 'WHO Regional Health Director',
                'department': 'Biomedical Engineering',
                'location': 'Research Center',
                'quote': 'IUST taught me to think beyond boundaries.'
            },
            {
                'name': 'Prof. Li Wei',
                'year': '2005',
                'achievement': 'Nobel Prize Nominee - Physics',
                'department': 'Physics',
                'location': 'Physics Laboratory',
                'quote': 'The foundation of my research was built here.'
            }
        ]
    # Add translations for other languages
    return []

def get_alumni_metrics(lang_code: str) -> Dict:
    """Get alumni impact metrics"""
    if lang_code == "en":
        return {
            "Total Alumni": "25,000+",
            "Countries": "87",
            "CEOs/Founders": "342",
            "Patent Holders": "1,250",
            "Award Winners": "856"
        }
    elif lang_code == "ar":
        return {
            "إجمالي الخريجين": "25,000+",
            "البلدان": "87",
            "الرؤساء التنفيذيون": "342",
            "أصحاب البراءات": "1,250",
            "الفائزون بالجوائز": "856"
        }
    else:  # Farsi
        return {
            "کل فارغ‌التحصیلان": "25,000+",
            "کشورها": "87",
            "مدیران عامل": "342",
            "دارندگان پتنت": "1,250",
            "برندگان جایزه": "856"
        }

def get_alumni_fields_distribution(lang_code: str) -> pd.DataFrame:
    """Get alumni distribution by professional field"""
    if lang_code == "en":
        data = [
            {'field': 'Technology', 'subfield': 'Software', 'count': 3500},
            {'field': 'Technology', 'subfield': 'Hardware', 'count': 2100},
            {'field': 'Technology', 'subfield': 'AI/ML', 'count': 1800},
            {'field': 'Engineering', 'subfield': 'Civil', 'count': 2800},
            {'field': 'Engineering', 'subfield': 'Mechanical', 'count': 2400},
            {'field': 'Engineering', 'subfield': 'Electrical', 'count': 2200},
            {'field': 'Business', 'subfield': 'Entrepreneurship', 'count': 1500},
            {'field': 'Business', 'subfield': 'Management', 'count': 1200},
            {'field': 'Research', 'subfield': 'Academic', 'count': 2000},
            {'field': 'Research', 'subfield': 'Industry R&D', 'count': 1800}
        ]
    else:
        # Add translated field names for other languages
        data = []
    
    return pd.DataFrame(data)