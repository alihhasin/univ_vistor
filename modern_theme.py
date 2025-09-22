"""
Modern UI Theme for IUST Virtual Campus Tour
Clean, professional design with subtle IUST branding
"""

import streamlit as st

def apply_modern_theme():
    """Apply modern, clean theme with subtle IUST branding"""
    st.markdown("""
    <style>
    /* Reset and base styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Main container styling */
    .main {
        padding: 0;
        max-width: 100%;
    }
    
    /* Sidebar modern styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    section[data-testid="stSidebar"] label {
        color: #ecf0f1 !important;
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 8px;
    }
    
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #DC143C 0%, #B91C3C 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.3);
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(220, 20, 60, 0.4);
    }
    
    /* Header redesign */
    .main-header {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #DC143C 0%, #FF6B6B 50%, #DC143C 100%);
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .main-header p {
        color: #5a6c7d;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 15px;
        padding: 0.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        color: #64748b;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f8fafc;
        color: #334155;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #DC143C 0%, #B91C3C 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.2);
    }
    
    /* Quick filter pills */
    .quick-filter {
        display: inline-block;
        background: white;
        border-radius: 25px;
        padding: 0.6rem 1.2rem;
        margin: 0.1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        font-weight: 600;
        color: #475569;
    }
    
    .quick-filter:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        color: #DC143C;
    }
    
    .quick-filter.active {
        background: linear-gradient(135deg, #DC143C 0%, #B91C3C 100%);
        color: white;
    }
    
    /* Cards and content boxes */
    .content-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .content-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    /* Buttons redesign */
    .stButton button {
        background: white;
        color: #334155;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: #f8fafc;
        border-color: #DC143C;
        color: #DC143C;
        transform: translateY(-2px);
    }
    
    /* Primary action buttons */
    .primary-button button {
        background: linear-gradient(135deg, #DC143C 0%, #B91C3C 100%);
        color: white !important;
        border: none;
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.3);
    }
    
    .primary-button button:hover {
        box-shadow: 0 6px 25px rgba(220, 20, 60, 0.4);
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #DC143C;
    }
    
    [data-testid="metric-container"] label {
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #1e293b;
        font-weight: 700;
    }
    
    /* Select boxes and inputs */
    .stSelectbox > div > div,
    .stTextInput input,
    .stTextArea textarea {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        color: #334155;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus,
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #DC143C;
        box-shadow: 0 0 0 3px rgba(220, 20, 60, 0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 10px;
        font-weight: 600;
        color: #334155;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f8fafc;
        color: #DC143C;
    }
    
    /* Info messages */
    .stAlert {
        background: white;
        border-radius: 12px;
        border-left: 4px solid #DC143C;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #DC143C 0%, #FF6B6B 100%);
        border-radius: 10px;
    }
    
    /* Floating elements */
    .floating-card {
        position: fixed;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        z-index: 999;
        padding: 1rem;
    }
    
    /* Animation for elements */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Map container */
    .map-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 25px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #DC143C 0%, #B91C3C 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #8B0000;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Language switcher redesign */
    .lang-switcher {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: white;
        border-radius: 50px;
        box-shadow: 0 5px 25px rgba(0,0,0,0.1);
        padding: 6px;
        display: flex;
        gap: 4px;
    }
    
    .lang-btn {
        width: 36px;
        height: 36px;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        font-size: 18px;
        transition: all 0.3s ease;
        background: transparent;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .lang-btn:hover {
        background: #f8fafc;
        transform: scale(1.1);
    }
    
    .lang-btn.active {
        background: linear-gradient(135deg, #DC143C 0%, #B91C3C 100%);
        box-shadow: 0 2px 10px rgba(220, 20, 60, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def create_modern_header(title: str, subtitle: str):
    """Create a modern, clean header"""
    st.markdown(f"""
    <div class="main-header fade-in">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def create_modern_quick_filters():
    """Create modern quick filter pills"""
    st.markdown("""
    <div style="padding: 1rem 0; text-align: center;">
        <span class="quick-filter">📍 Nearby</span>
        <span class="quick-filter">🟢 Open Now</span>
        <span class="quick-filter">⭐ Popular</span>
        <span class="quick-filter">🆕 Recently Added</span>
        <span class="quick-filter">📚 Academic</span>
        <span class="quick-filter">🍽️ Food & Dining</span>
    </div>
    """, unsafe_allow_html=True)

def create_modern_language_switcher():
    """Create modern language switcher"""
    st.markdown("""
    <div class="lang-switcher">
        <button class="lang-btn" onclick="setLanguage('ar')" title="العربية">
            <span>🇸🇦</span>
        </button>
        <button class="lang-btn active" onclick="setLanguage('en')" title="English">
            <span>🇬🇧</span>
        </button>
        <button class="lang-btn" onclick="setLanguage('fa')" title="فارسی">
            <span>🇮🇷</span>
        </button>
    </div>
    """, unsafe_allow_html=True)