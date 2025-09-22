# 🏛️ IUST Virtual Campus Tour - Enhanced Edition

A modern, feature-rich virtual campus tour application for Iran University of Science and Technology (IUST) built with Streamlit.

## ✨ Key Features

### 🎨 Modern UI/UX
- **Gradient backgrounds** and glassmorphism effects
- **Animated components** with smooth transitions  
- **Card-based layouts** with hover effects
- **Floating action buttons** for quick navigation
- **Responsive design** for all screen sizes

### 🗺️ Interactive Map
- **Color-coded markers** by category (Engineering, Library, Sports, etc.)
- **Rich popups** with images and descriptions
- **Base64 embedded images** for fast loading
- **Smart image resolver** handling various naming conventions

### 🎭 Guided Tours
- **Pre-configured tour routes**:
  - Engineering Excellence Tour
  - Campus Highlights Tour
  - Student Life Tour
  - Research & Innovation Tour
- **Auto-play functionality** with adjustable speed
- **Step-by-step navigation** with progress tracking
- **Contextual storytelling** for each location

### 🔍 Advanced Search & Filters
- **Real-time search** across names, descriptions, and categories
- **Category filters** with icon indicators
- **Distance-based filtering** from any location
- **Facility filters** (parking, cafeteria, WiFi, accessibility)
- **Quick filter buttons** for common searches
- **Sort options** (alphabetical, distance, popularity)

### 💬 Feedback System
- **5-star rating system** for each location
- **Comment collection** with text feedback
- **Quick feedback tags** (Helpful, Photo Spot, Must Visit)
- **Feedback dashboard** with analytics
- **Export functionality** for feedback reports

### 🌐 Multilingual Support
- **Three languages**: Arabic, English, and Persian/Farsi
- **RTL/LTR layout** automatic switching
- **Floating language switcher** for easy access
- **Fully translated UI** including all labels and messages

### 📊 Analytics & Insights
- **Category distribution** charts
- **Location statistics** with metrics
- **Distance calculator** between any two points
- **Path visualization** on map

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
```bash
cd /Users/sj/development/frontend/univ_vistor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
univ_vistor/
│
├── app.py                  # Main application with all enhancements
├── ui_components.py        # Modern UI components and themes
├── search_filters.py       # Advanced search and filtering
├── guided_tour.py          # Guided tour functionality
├── feedback_system.py      # Rating and feedback system
├── insights.py             # Visitor analytics and alumni showcase
│
├── data/
│   └── campus_locations.xlsx  # Location database
│
├── images/                 # Campus location images
│   ├── main_gate.jpg
│   ├── central_library.png
│   └── ...
│
├── requirements.txt        # All dependencies
└── README.md              # This file
```

## 🎯 Usage Guide

### Basic Navigation
1. **Choose your language** from the dropdown or floating switcher
2. **Browse the map** to explore campus locations
3. **Click on markers** to see detailed information and images
4. **Use the sidebar** to filter locations

### Taking a Guided Tour
1. Go to the **"🎭 Guided Tour"** tab
2. Select a tour type (Engineering, Campus Highlights, etc.)
3. Click **"Start Tour"**
4. Use controls to navigate or enable auto-play
5. Click **"Exit Tour"** when finished

### Searching and Filtering
1. Open the **sidebar** (left side)
2. Use the **search box** to find specific locations
3. Select **categories** to filter
4. Apply **advanced filters** for specific needs
5. Click **"Apply Filters"** to update the map

### Providing Feedback
1. Go to the **"💬 Feedback"** tab
2. Select a location from the dropdown
3. Rate with **stars** (1-5)
4. Add optional **comments**
5. Select **quick tags** if applicable
6. Click **"Submit Feedback"**

### Calculating Distances
1. Go to the **"🧭 Distances"** tab
2. Select **starting point**
3. Select **destination**
4. View the calculated distance
5. Optionally view the **path on map**

## 🔧 Configuration

### Adding New Locations
Edit `data/campus_locations.xlsx` with columns:
- `ID`: Unique identifier
- `Name_EN`, `Name_AR`, `Name_FA`: Names in different languages
- `Description_EN`, `Description_AR`, `Description_FA`: Descriptions
- `Latitude`, `Longitude`: GPS coordinates
- `Category`: Location category
- `name_pic`: Image filename

### Adding Images
Place images in the `images/` folder. The app automatically finds images using:
- Exact filename match
- Case-insensitive search
- Common extensions (.jpg, .jpeg, .png, .webp)
- Partial name matching

## 🚀 Deployment

### Streamlit Community Cloud (Recommended)
1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy directly from repository

### Local Network
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### Production Server
Consider using:
- **Heroku** with Streamlit buildpack
- **AWS EC2** with nginx reverse proxy
- **Google Cloud Run** for auto-scaling
- **Azure App Service**

## 📱 Mobile Support

The app is fully responsive with:
- Touch-optimized controls
- Swipe gestures support
- Mobile-friendly navigation
- Responsive image sizing
- Optimized map controls

## 🔐 Security Features

- Input sanitization for user feedback
- Session management with unique IDs
- Safe image handling with base64 encoding
- No direct file system access from UI
- CSRF protection ready (optional)

## 🤝 Contributing

To add new features:
1. Create a new module in the project directory
2. Import it in `app.py`
3. Add UI integration in the appropriate tab
4. Update `requirements.txt` if needed

## 📄 License

This project is created for Iran University of Science and Technology.
© 2024 IUST Virtual Campus Tour

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Maps powered by [Folium](https://python-folium.readthedocs.io)
- Charts by [Plotly](https://plotly.com)
- Distance calculations using [GeoPy](https://geopy.readthedocs.io)

## 📞 Support

For issues or questions about the enhanced features:
- Check the diagnostics tab in the app
- Review the console output for errors
- Ensure all dependencies are installed
- Verify image files are in the correct location

---

**Enjoy exploring IUST campus virtually! 🎓**