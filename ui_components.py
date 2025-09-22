"""
UI Components Module - Modern Theme and Visual Enhancements
"""
import streamlit as st

def apply_modern_theme():
    """Apply modern CSS theme with gradients and animations"""
    st.markdown("""
    <style>
    /* Modern gradient background - IUST Red Theme */
    .stApp {
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
        background-attachment: fixed;
    }
    
    /* Card design with glassmorphism */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .main-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0,0,0,0.15);
    }
    
    /* Glass header */
    .glass-header {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
    
    /* Modern buttons - IUST Theme */
    .stButton > button {
        background: linear-gradient(45deg, #DC143C 30%, #B22222 90%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.4);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(220, 20, 60, 0.6);
        background: linear-gradient(45deg, #B22222 30%, #8B0000 90%);
    }
    
    /* Animated gradient text - IUST Theme */
    .gradient-text {
        background: linear-gradient(45deg, #DC143C, #B22222, #FF6B6B);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient 3s ease infinite;
        font-weight: bold;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating action button */
    .fab-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 999;
    }
    
    .fab {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(45deg, #DC143C, #B22222);
        color: white;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        font-size: 24px;
        transition: transform 0.3s ease;
    }
    
    .fab:hover {
        transform: scale(1.1);
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Custom metrics styling */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #DC143C;
    }
    
    /* Animated entrance */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-entrance {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Loading spinner */
    .loading-spinner {
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top: 3px solid #DC143C;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #DC143C, #B22222);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #B22222, #8B0000);
    }
    </style>
    """, unsafe_allow_html=True)

def create_header(title: str, subtitle: str = ""):
    """Create a beautiful header with gradient text"""
    st.markdown(f"""
    <div class="glass-header animate-entrance">
        <h1 class="gradient-text" style="text-align: center; font-size: 2.5rem; margin-bottom: 0.5rem;">
            {title}
        </h1>
        {f'<p style="text-align: center; color: rgba(255, 255, 255, 0.9); font-size: 1.1rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def create_location_card(location_data: dict, image_uri: str = None) -> str:
    """Create a modern location card with image and details"""
    image_html = ""
    if image_uri:
        image_html = f"""
        <img src="{image_uri}" 
             style="width: 100%; height: 200px; object-fit: cover; border-radius: 15px; margin-bottom: 1rem;">
        """
    
    return f"""
    <div class="main-card animate-entrance">
        {image_html}
        <h3 style="color: #DC143C; margin-bottom: 0.5rem;">{location_data.get('name', 'Unknown Location')}</h3>
        <p style="color: #666; line-height: 1.6;">
            {location_data.get('description', 'No description available.')}
        </p>
        <div style="margin-top: 1rem;">
            <span style="background: linear-gradient(45deg, #DC143C, #B22222); 
                         color: white; padding: 5px 15px; border-radius: 20px; 
                         font-size: 0.9rem; font-weight: 500;">
                {location_data.get('category', 'General')}
            </span>
        </div>
    </div>
    """

def create_metric_card(label: str, value: str, delta: str = None):
    """Create a beautiful metric card"""
    delta_html = ""
    if delta:
        color = "green" if delta.startswith("+") else "red"
        delta_html = f'<p style="color: {color}; font-size: 0.9rem; margin-top: 0.5rem;">{delta}</p>'
    
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #999; font-size: 0.9rem; margin-bottom: 0.5rem;">{label}</p>
        <h2 style="color: #DC143C; margin: 0;">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def add_floating_action_button(icon: str = "↑", action: str = "scrollToTop()"):
    """Add a floating action button"""
    st.markdown(f"""
    <div class="fab-container">
        <button class="fab" onclick="{action}">{icon}</button>
    </div>
    <script>
    function scrollToTop() {{
        window.scrollTo({{
            top: 0,
            behavior: 'smooth'
        }});
    }}
    </script>
    """, unsafe_allow_html=True)

def show_loading_spinner():
    """Display a loading spinner"""
    st.markdown("""
    <div class="loading-spinner"></div>
    """, unsafe_allow_html=True)

def create_info_banner(message: str, type: str = "info"):
    """Create an informational banner"""
    colors = {
        "info": "#DC143C",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#8B0000"
    }
    
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    st.markdown(f"""
    <div style="background: {colors[type]}20; border-left: 4px solid {colors[type]}; 
                padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icons[type]}</span>
        <span style="color: {colors[type]}; font-weight: 500;">{message}</span>
    </div>
    """, unsafe_allow_html=True)

def create_progress_bar(progress: float, label: str = ""):
    """Create a custom progress bar"""
    percentage = int(progress * 100)
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        {f'<p style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">{label}</p>' if label else ''}
        <div style="background: rgba(255, 255, 255, 0.2); border-radius: 10px; overflow: hidden; height: 10px;">
            <div style="background: linear-gradient(45deg, #DC143C, #B22222); 
                        width: {percentage}%; height: 100%; transition: width 0.5s ease;">
            </div>
        </div>
        <p style="text-align: right; color: #DC143C; font-size: 0.9rem; margin-top: 0.5rem;">
            {percentage}%
        </p>
    </div>
    """, unsafe_allow_html=True)