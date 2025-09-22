"""
Guided Tour Module - Virtual tour experience with storytelling
"""
import streamlit as st
import pandas as pd
import time
from typing import List, Dict, Optional
import folium
from streamlit_folium import st_folium

class GuidedTour:
    def __init__(self, locations: List[Dict], lang_code: str = "en"):
        self.locations = locations
        self.lang_code = lang_code
        self.current_step = 0
        self.is_playing = False
        
        # Tour narratives in multiple languages
        self.narratives = self.get_tour_narratives()
    
    def get_tour_narratives(self) -> Dict:
        """Get tour narratives in different languages"""
        return {
            "en": {
                "welcome": "Welcome to the IUST Virtual Campus Tour! Let's explore the remarkable facilities and landmarks of Iran University of Science and Technology.",
                "engineering": "Here we have the {name}, a hub of innovation where students work on cutting-edge projects in {field}.",
                "library": "The {name} is the heart of academic life, housing over 100,000 volumes and providing 24/7 study spaces.",
                "sports": "Our {name} offers world-class facilities for athletics, swimming, and various sports activities.",
                "research": "The {name} is where groundbreaking research happens, contributing to scientific advancement.",
                "end": "Thank you for joining our virtual tour! We hope you enjoyed exploring IUST campus."
            },
            "ar": {
                "welcome": "مرحباً بكم في جولة الحرم الجامعي الافتراضية لجامعة إيران للعلوم والتكنولوجيا!",
                "engineering": "هنا لدينا {name}، مركز الابتكار حيث يعمل الطلاب على مشاريع متطورة في {field}.",
                "library": "{name} هي قلب الحياة الأكاديمية، تضم أكثر من 100,000 مجلد.",
                "sports": "{name} يوفر مرافق عالمية للرياضة والسباحة.",
                "research": "{name} حيث يحدث البحث الرائد.",
                "end": "شكراً لانضمامكم لجولتنا الافتراضية!"
            },
            "fa": {
                "welcome": "به تور مجازی پردیس دانشگاه علم و صنعت ایران خوش آمدید!",
                "engineering": "اینجا {name} را داریم، مرکز نوآوری که دانشجویان روی پروژه‌های پیشرفته در {field} کار می‌کنند.",
                "library": "{name} قلب زندگی دانشگاهی است، با بیش از 100,000 جلد کتاب.",
                "sports": "{name} امکانات جهانی برای ورزش و شنا فراهم می‌کند.",
                "research": "{name} جایی که تحقیقات پیشگامانه انجام می‌شود.",
                "end": "از شما برای پیوستن به تور مجازی ما سپاسگزاریم!"
            }
        }
    
    def create_tour_controls(self):
        """Create tour navigation controls"""
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        with col1:
            if st.button("⬅️", help="Previous stop", disabled=(self.current_step == 0)):
                if self.current_step > 0:
                    self.current_step -= 1
                    st.session_state['tour_step'] = self.current_step
                    st.rerun()
        
        with col2:
            if st.button("▶️" if not self.is_playing else "⏸️", help="Play/Pause"):
                self.is_playing = not self.is_playing
                st.session_state['tour_playing'] = self.is_playing
                st.rerun()
        
        with col3:
            progress = (self.current_step + 1) / len(self.locations)
            st.progress(progress, f"Stop {self.current_step + 1} of {len(self.locations)}")
        
        with col4:
            if st.button("➡️", help="Next stop", disabled=(self.current_step >= len(self.locations) - 1)):
                if self.current_step < len(self.locations) - 1:
                    self.current_step += 1
                    st.session_state['tour_step'] = self.current_step
                    st.rerun()
        
        with col5:
            if st.button("🔄", help="Restart tour"):
                self.current_step = 0
                st.session_state['tour_step'] = 0
                st.rerun()
    
    def display_tour_stop(self, location: Dict, step: int):
        """Display a single tour stop with rich information"""
        # Get the appropriate narrative
        narrative = self.get_narrative_for_location(location, step)
        
        # Create an attractive tour stop display
        st.markdown(f"""
        <div class="tour-stop animate-entrance" style="
            background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.85));
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin: 1rem 0;
        ">
            <h2 style="color: #DC143C; margin-bottom: 1rem;">
                📍 Stop {step + 1}: {location.get('name', 'Unknown Location')}
            </h2>
            <p style="color: #666; font-size: 1.1rem; line-height: 1.8; margin-bottom: 1rem;">
                {narrative}
            </p>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
                <span style="background: #DC143C; color: white; padding: 5px 15px; border-radius: 20px;">
                    {location.get('category', 'General')}
                </span>
                <span style="background: #764ba2; color: white; padding: 5px 15px; border-radius: 20px;">
                    ⏱️ {location.get('visit_duration', '10-15 min')}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display additional information in columns
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Description
            desc_col = f"Description_{self.lang_code.upper()}" if self.lang_code != "fa" else "Description_FA"
            description = location.get(desc_col, location.get('Description_EN', ''))
            if description:
                st.info(description)
        
        with col2:
            # Quick facts
            st.markdown("### 📊 Quick Facts")
            facts = self.get_location_facts(location)
            for fact in facts:
                st.markdown(f"• {fact}")
    
    def get_narrative_for_location(self, location: Dict, step: int) -> str:
        """Generate contextual narrative for each location"""
        narratives = self.narratives.get(self.lang_code, self.narratives['en'])
        
        if step == 0:
            return narratives['welcome']
        elif step == len(self.locations) - 1:
            return narratives['end']
        else:
            category = location.get('category', '').lower()
            name = location.get(f'Name_{self.lang_code.upper()}' if self.lang_code != 'fa' else 'Name_FA', 
                               location.get('Name_EN', 'this location'))
            
            if 'engineering' in category:
                return narratives['engineering'].format(name=name, field=category)
            elif 'library' in category:
                return narratives['library'].format(name=name)
            elif 'sport' in category:
                return narratives['sports'].format(name=name)
            elif 'research' in category:
                return narratives['research'].format(name=name)
            else:
                return f"Now we visit {name}, an important part of our campus."
    
    def get_location_facts(self, location: Dict) -> List[str]:
        """Get interesting facts about a location"""
        facts = []
        
        if location.get('year_built'):
            facts.append(f"Established in {location.get('year_built')}")
        
        if location.get('capacity'):
            facts.append(f"Capacity: {location.get('capacity')} people")
        
        if location.get('special_features'):
            facts.append(f"Features: {location.get('special_features')}")
        
        # Add default facts based on category
        category = location.get('category', '').lower()
        if 'engineering' in category:
            facts.append("State-of-the-art laboratories")
            facts.append("Industry partnerships")
        elif 'library' in category:
            facts.append("Digital resources available")
            facts.append("Group study rooms")
        elif 'sport' in category:
            facts.append("Professional equipment")
            facts.append("Trained instructors")
        
        return facts[:3]  # Return maximum 3 facts
    
    def auto_play_tour(self, interval: int = 5):
        """Automatically advance through tour stops"""
        if self.is_playing and self.current_step < len(self.locations) - 1:
            time.sleep(interval)
            self.current_step += 1
            st.session_state['tour_step'] = self.current_step
            st.rerun()
    
    def create_tour_map(self, df, current_location: Dict):
        """Create a map focused on the current tour stop"""
        # Center map on current location
        lat = current_location.get('Latitude', 35.7219)
        lon = current_location.get('Longitude', 51.3347)
        
        m = folium.Map(location=[lat, lon], zoom_start=17)
        
        # Add markers for all tour stops
        for idx, loc in enumerate(self.locations):
            loc_lat = loc.get('Latitude', 35.7219)
            loc_lon = loc.get('Longitude', 51.3347)
            
            # Different styling for current location
            if idx == self.current_step:
                icon = folium.Icon(color='red', icon='star')
                folium.Marker(
                    [loc_lat, loc_lon],
                    popup=f"Current Stop: {loc.get('Name_EN', '')}",
                    tooltip="You are here",
                    icon=icon
                ).add_to(m)
                
                # Add a circle to highlight current location
                folium.Circle(
                    [loc_lat, loc_lon],
                    radius=50,
                    color='red',
                    fill=True,
                    fillColor='red',
                    fillOpacity=0.2
                ).add_to(m)
            else:
                # Regular markers for other stops
                icon_color = 'green' if idx < self.current_step else 'blue'
                icon = folium.Icon(color=icon_color, icon='info-sign')
                folium.Marker(
                    [loc_lat, loc_lon],
                    popup=f"Stop {idx + 1}: {loc.get('Name_EN', '')}",
                    tooltip=f"Stop {idx + 1}",
                    icon=icon
                ).add_to(m)
        
        # Draw path between stops
        if len(self.locations) > 1:
            path_coords = [[loc.get('Latitude', 35.7219), 
                           loc.get('Longitude', 51.3347)] 
                          for loc in self.locations]
            
            folium.PolyLine(
                path_coords,
                color='blue',
                weight=2,
                opacity=0.6,
                dash_array='10'
            ).add_to(m)
        
        return m


# Tour presets configuration - using actual location names from Excel
TOUR_PRESETS = {
    "en": {
        "Engineering Excellence": {
            "locations": ["Mechanical Engineering", "Electrical Engineering", "Civil Engineering", 
                          "Computer Engineering", "Industrial Engineering"],
            "duration": "45 minutes",
            "highlights": "Explore our cutting-edge engineering facilities"
        },
        "Campus Highlights": {
            "locations": ["main gate", "Central Library", "University Presidency", 
                          "Stadium", "Railway Engineering"],
            "duration": "30 minutes",
            "highlights": "Discover the main landmarks of IUST"
        },
        "Student Life": {
            "locations": ["Stadium", "Swimming Pool", "Central Library", 
                          "Cars parking", "University Presidency"],
            "duration": "35 minutes",
            "highlights": "Experience campus life at IUST"
        },
        "Academic Tour": {
            "locations": ["Mathematics and computer science", "Physics", "Chemistry", 
                          "Architecture & Environmental Design", "Modern Technologies"],
            "duration": "40 minutes",
            "highlights": "Explore academic departments"
        }
    },
    "ar": {
        "التميز الهندسي": {
            "locations": ["Mechanical Engineering", "Electrical Engineering", "Civil Engineering", 
                          "Computer Engineering", "Industrial Engineering"],
            "duration": "45 دقيقة",
            "highlights": "استكشف منشآتنا الهندسية المتطورة"
        },
        "معالم الحرم الجامعي": {
            "locations": ["main gate", "Central Library", "University Presidency", 
                          "Stadium", "Railway Engineering"],
            "duration": "30 دقيقة",
            "highlights": "اكتشف المعالم الرئيسية للجامعة"
        },
        "الحياة الطلابية": {
            "locations": ["Stadium", "Swimming Pool", "Central Library", 
                          "Cars parking", "University Presidency"],
            "duration": "35 دقيقة",
            "highlights": "تجربة الحياة الجامعية"
        }
    },
    "fa": {
        "تعالی مهندسی": {
            "locations": ["Mechanical Engineering", "Electrical Engineering", "Civil Engineering", 
                          "Computer Engineering", "Industrial Engineering"],
            "duration": "45 دقیقه",
            "highlights": "کاوش در امکانات مهندسی پیشرفته ما"
        },
        "نقاط برجسته پردیس": {
            "locations": ["main gate", "Central Library", "University Presidency", 
                          "Stadium", "Railway Engineering"],
            "duration": "30 دقیقه",
            "highlights": "کشف نشانه‌های اصلی دانشگاه"
        },
        "زندگی دانشجویی": {
            "locations": ["Stadium", "Swimming Pool", "Central Library", 
                          "Cars parking", "University Presidency"],
            "duration": "35 دقیقه",
            "highlights": "تجربه زندگی دانشگاهی"
        }
    }
}

def create_tour_selection_ui(df, lang_code: str):
    """Create UI for tour selection"""
    presets = TOUR_PRESETS.get(lang_code, TOUR_PRESETS['en'])
    
    st.markdown("### 🎭 Choose a Guided Tour")
    
    # Display tour options as cards
    cols = st.columns(len(presets))
    
    for idx, (col, (tour_name, tour_info)) in enumerate(zip(cols, presets.items())):
        with col:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 15px;
                padding: 1.5rem;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            ">
                <div>
                    <h4 style="color: #DC143C; margin-bottom: 0.5rem;">{tour_name}</h4>
                    <p style="color: #999; font-size: 0.9rem;">⏱️ {tour_info['duration']}</p>
                    <p style="color: #666; font-size: 0.9rem;">{tour_info['highlights']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Start Tour", key=f"tour_{idx}", use_container_width=True):
                # Get locations for this tour
                location_names = tour_info['locations']
                tour_locations = []
                
                for loc_name in location_names:
                    # Find location in dataframe by matching Name_EN
                    matching_rows = df[df['Name_EN'].str.lower() == loc_name.lower()]
                    if not matching_rows.empty:
                        tour_locations.append(matching_rows.iloc[0].to_dict())
                    else:
                        # Try partial match if exact match fails
                        partial_matches = df[df['Name_EN'].str.contains(loc_name, case=False, na=False)]
                        if not partial_matches.empty:
                            tour_locations.append(partial_matches.iloc[0].to_dict())
                
                if tour_locations:
                    st.session_state['active_tour'] = GuidedTour(tour_locations, lang_code)
                    st.session_state['tour_active'] = True
                    st.rerun()
                else:
                    st.warning(f"Could not find all tour locations. Found {len(tour_locations)} out of {len(location_names)} locations.")
