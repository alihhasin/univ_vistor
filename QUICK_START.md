# 🚀 Quick Start Guide - IUST Virtual Campus Tour

## Installation & Running (3 Simple Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
streamlit run app.py
```

### Step 3: Open in Browser
The app will automatically open at: `http://localhost:8501`

---

## 🎯 What's New in the Enhanced Version?

### ✨ Major Enhancements
1. **Modern UI** - Gradient backgrounds, animations, glassmorphism
2. **Guided Tours** - 4 pre-configured tours with auto-play
3. **Advanced Search** - Real-time filtering with multiple criteria  
4. **Feedback System** - 5-star ratings and comments
5. **Visitor Analytics** - Interactive charts and flow diagrams
6. **Alumni Showcase** - Notable graduates and their achievements
7. **Mobile Responsive** - Touch-friendly design
8. **Multi-language** - Arabic, English, Persian with RTL support

### 📱 Key Features to Try

#### 1. Take a Guided Tour
- Go to **"🎭 Guided Tour"** tab
- Choose "Engineering Excellence" or "Campus Highlights"
- Click "Start Tour" and enjoy the narrated experience

#### 2. Explore with Filters
- Open the **sidebar** (left side)
- Type in the search box or select categories
- Apply distance filters to find nearby locations

#### 3. Leave Feedback
- Visit **"💬 Feedback"** tab
- Select any location
- Rate with stars and leave comments

#### 4. View Analytics
- Check **"📊 Insights"** tab
- See visitor patterns and popular routes
- Explore alumni achievements

---

## 🔧 Troubleshooting

### If the app doesn't start:
1. Make sure Python 3.8+ is installed
2. Check all dependencies: `pip list`
3. Try: `python -m streamlit run app.py`

### If images don't appear:
- Verify the `images/` folder exists
- Check image filenames match the Excel data

### If language switching doesn't work:
- Clear browser cache
- Refresh the page (F5)

---

## 📁 File Structure
```
univ_vistor/
├── app.py                 # Main app (RUN THIS)
├── ui_components.py       # UI themes
├── search_filters.py      # Search system
├── guided_tour.py        # Tour system
├── feedback_system.py    # Ratings
├── insights.py          # Analytics
├── data/
│   └── campus_locations.xlsx
├── images/
│   └── [your images]
└── requirements.txt      # Dependencies
```

---

## 🎨 Customization Tips

### Change Colors
Edit `ui_components.py` line 19-20:
```python
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
```

### Add New Tour Routes
Edit `guided_tour.py` line 250-308

### Modify Language Labels
Edit language dictionaries in each module

---

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. View console for error messages
3. Ensure all files are in correct locations

---

**Enjoy your enhanced virtual campus tour! 🎓✨**