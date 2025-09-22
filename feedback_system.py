"""
Feedback System Module - User ratings and comments functionality
"""
import streamlit as st
import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go

class FeedbackSystem:
    def __init__(self, storage_file: str = "feedback.csv"):
        self.storage_file = storage_file
        self.init_storage()
    
    def init_storage(self):
        """Initialize CSV storage if not exists"""
        if not Path(self.storage_file).exists():
            with open(self.storage_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'location_id', 'location_name', 
                    'rating', 'comment', 'user_session', 
                    'language', 'helpful', 'photo_spot', 'must_visit'
                ])
    
    def create_rating_widget(self, location_id: str, location_name: str, lang_code: str = "en"):
        """Create interactive rating widget for a location"""
        labels = self.get_feedback_labels(lang_code)
        
        # Create a nice container for the feedback section
        with st.container():
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.85));
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                margin: 1rem 0;
            ">
                <h3 style="color: #DC143C; margin-bottom: 1rem;">
                    {labels['rate_location']} {location_name}
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Star rating
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"### {labels['your_rating']}")
                rating = st.feedback("stars", key=f"rating_{location_id}")
                
                if rating is not None:
                    st.markdown(f"You rated: {'⭐' * (rating + 1)}")
            
            with col2:
                # Display current ratings
                stats = self.get_location_stats(location_id)
                if stats['total_ratings'] > 0:
                    self.display_rating_summary(stats, lang_code)
            
            # Comment section
            st.markdown(f"### {labels['share_experience']}")
            comment = st.text_area(
                labels['comment_placeholder'],
                key=f"comment_{location_id}",
                max_chars=500,
                height=100
            )
            
            # Quick feedback buttons
            st.markdown(f"### {labels['quick_feedback']}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                helpful = st.checkbox(labels['helpful'], key=f"helpful_{location_id}")
            with col2:
                photo_spot = st.checkbox(labels['photo_spot'], key=f"photo_{location_id}")
            with col3:
                must_visit = st.checkbox(labels['must_visit'], key=f"must_{location_id}")
            
            # Submit button
            if st.button(labels['submit_feedback'], key=f"submit_{location_id}", type="primary"):
                if rating is not None:
                    success = self.save_feedback(
                        location_id=location_id,
                        location_name=location_name,
                        rating=rating + 1,  # Convert 0-4 to 1-5
                        comment=comment,
                        language=lang_code,
                        helpful=helpful,
                        photo_spot=photo_spot,
                        must_visit=must_visit
                    )
                    
                    if success:
                        st.success(labels['thank_you'])
                        st.balloons()
                        # Clear the form
                        st.session_state[f"comment_{location_id}"] = ""
                        st.rerun()
                else:
                    st.warning(labels['please_rate'])
    
    def get_feedback_labels(self, lang_code: str) -> Dict[str, str]:
        """Get language-specific labels"""
        labels = {
            "en": {
                "rate_location": "Rate",
                "your_rating": "Your Rating",
                "share_experience": "Share Your Experience",
                "comment_placeholder": "What did you think about this location?",
                "quick_feedback": "Quick Feedback",
                "helpful": "👍 Helpful Information",
                "photo_spot": "📸 Great Photo Spot",
                "must_visit": "⭐ Must Visit",
                "submit_feedback": "Submit Feedback",
                "thank_you": "Thank you for your feedback!",
                "please_rate": "Please select a rating before submitting",
                "avg_rating": "Average Rating",
                "total_reviews": "Total Reviews",
                "rating_distribution": "Rating Distribution",
                "recent_comments": "Recent Comments",
                "visitor_feedback": "Visitor Feedback"
            },
            "ar": {
                "rate_location": "قيم",
                "your_rating": "تقييمك",
                "share_experience": "شارك تجربتك",
                "comment_placeholder": "ما رأيك في هذا الموقع؟",
                "quick_feedback": "ملاحظات سريعة",
                "helpful": "👍 معلومات مفيدة",
                "photo_spot": "📸 مكان رائع للتصوير",
                "must_visit": "⭐ يجب زيارته",
                "submit_feedback": "إرسال التقييم",
                "thank_you": "شكراً لك على ملاحظاتك!",
                "please_rate": "يرجى اختيار تقييم قبل الإرسال",
                "avg_rating": "متوسط التقييم",
                "total_reviews": "إجمالي التقييمات",
                "rating_distribution": "توزيع التقييمات",
                "recent_comments": "التعليقات الأخيرة",
                "visitor_feedback": "ملاحظات الزوار"
            },
            "fa": {
                "rate_location": "امتیاز به",
                "your_rating": "امتیاز شما",
                "share_experience": "تجربه خود را به اشتراک بگذارید",
                "comment_placeholder": "نظر شما درباره این مکان چیست؟",
                "quick_feedback": "بازخورد سریع",
                "helpful": "👍 اطلاعات مفید",
                "photo_spot": "📸 مکان عالی برای عکس",
                "must_visit": "⭐ حتماً ببینید",
                "submit_feedback": "ارسال بازخورد",
                "thank_you": "از بازخورد شما متشکریم!",
                "please_rate": "لطفاً قبل از ارسال امتیاز دهید",
                "avg_rating": "میانگین امتیاز",
                "total_reviews": "مجموع نظرات",
                "rating_distribution": "توزیع امتیازات",
                "recent_comments": "نظرات اخیر",
                "visitor_feedback": "بازخورد بازدیدکنندگان"
            }
        }
        return labels.get(lang_code, labels["en"])
    
    def save_feedback(self, location_id: str, location_name: str, rating: int, 
                     comment: str, language: str, helpful: bool = False,
                     photo_spot: bool = False, must_visit: bool = False) -> bool:
        """Save feedback to CSV storage"""
        try:
            with open(self.storage_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    location_id,
                    location_name,
                    rating,
                    comment,
                    st.session_state.get('session_id', 'anonymous'),
                    language,
                    helpful,
                    photo_spot,
                    must_visit
                ])
            return True
        except Exception as e:
            st.error(f"Error saving feedback: {str(e)}")
            return False
    
    def get_location_stats(self, location_id: str) -> Dict:
        """Get aggregated statistics for a location"""
        ratings = []
        comments = []
        tags = {'helpful': 0, 'photo_spot': 0, 'must_visit': 0}
        
        try:
            if Path(self.storage_file).exists():
                df = pd.read_csv(self.storage_file)
                location_data = df[df['location_id'] == location_id]
                
                if not location_data.empty:
                    ratings = location_data['rating'].dropna().tolist()
                    comments = location_data['comment'].dropna().tolist()
                    
                    # Count tags
                    tags['helpful'] = location_data['helpful'].sum() if 'helpful' in location_data else 0
                    tags['photo_spot'] = location_data['photo_spot'].sum() if 'photo_spot' in location_data else 0
                    tags['must_visit'] = location_data['must_visit'].sum() if 'must_visit' in location_data else 0
        except Exception as e:
            st.error(f"Error reading feedback: {str(e)}")
        
        return {
            'avg_rating': sum(ratings) / len(ratings) if ratings else 0,
            'total_ratings': len(ratings),
            'ratings': ratings,
            'recent_comments': comments[-5:] if comments else [],
            'tags': tags
        }
    
    def display_rating_summary(self, stats: Dict, lang_code: str):
        """Display rating summary with visualizations"""
        labels = self.get_feedback_labels(lang_code)
        
        # Average rating and total reviews
        col1, col2 = st.columns(2)
        
        with col1:
            avg_rating = stats['avg_rating']
            st.metric(
                labels['avg_rating'],
                f"{avg_rating:.1f} ⭐",
                delta=None
            )
        
        with col2:
            st.metric(
                labels['total_reviews'],
                stats['total_ratings'],
                delta=None
            )
        
        # Rating distribution chart
        if stats['ratings']:
            rating_counts = pd.Series(stats['ratings']).value_counts().sort_index()
            
            fig = go.Figure(data=[
                go.Bar(
                    x=['⭐' * i for i in rating_counts.index],
                    y=rating_counts.values,
                    marker_color='rgba(102, 126, 234, 0.8)'
                )
            ])
            
            fig.update_layout(
                title=labels['rating_distribution'],
                xaxis_title="Rating",
                yaxis_title="Count",
                height=200,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def display_recent_feedback(self, location_id: str, lang_code: str):
        """Display recent feedback for a location"""
        stats = self.get_location_stats(location_id)
        labels = self.get_feedback_labels(lang_code)
        
        if stats['recent_comments']:
            st.markdown(f"### {labels['recent_comments']}")
            
            for comment in stats['recent_comments']:
                if comment and comment.strip():
                    st.markdown(f"""
                    <div style="
                        background: #f0f4f8;
                        border-left: 3px solid #DC143C;
                        padding: 1rem;
                        margin: 0.5rem 0;
                        border-radius: 5px;
                    ">
                        💬 {comment}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Display tags summary
        if stats['tags'] and any(stats['tags'].values()):
            st.markdown("### 🏷️ Visitor Tags")
            cols = st.columns(3)
            
            if stats['tags']['helpful'] > 0:
                cols[0].info(f"👍 Helpful ({stats['tags']['helpful']})")
            
            if stats['tags']['photo_spot'] > 0:
                cols[1].info(f"📸 Photo Spot ({stats['tags']['photo_spot']})")
            
            if stats['tags']['must_visit'] > 0:
                cols[2].info(f"⭐ Must Visit ({stats['tags']['must_visit']})")
    
    def get_overall_statistics(self) -> pd.DataFrame:
        """Get overall feedback statistics for all locations"""
        try:
            if Path(self.storage_file).exists():
                df = pd.read_csv(self.storage_file)
                
                # Group by location and calculate stats
                stats = df.groupby('location_name').agg({
                    'rating': ['mean', 'count'],
                    'helpful': 'sum',
                    'photo_spot': 'sum',
                    'must_visit': 'sum'
                }).round(2)
                
                stats.columns = ['Avg Rating', 'Total Reviews', 'Helpful', 'Photo Spot', 'Must Visit']
                stats = stats.sort_values('Avg Rating', ascending=False)
                
                return stats
        except Exception as e:
            st.error(f"Error getting statistics: {str(e)}")
            return pd.DataFrame()
    
    def export_feedback_report(self) -> bytes:
        """Export feedback data as JSON report"""
        try:
            if Path(self.storage_file).exists():
                df = pd.read_csv(self.storage_file)
                
                report = {
                    'export_date': datetime.now().isoformat(),
                    'total_feedback': len(df),
                    'locations': {}
                }
                
                for location in df['location_name'].unique():
                    location_data = df[df['location_name'] == location]
                    report['locations'][location] = {
                        'avg_rating': location_data['rating'].mean(),
                        'total_ratings': len(location_data),
                        'comments': location_data['comment'].dropna().tolist(),
                        'tags': {
                            'helpful': int(location_data['helpful'].sum()),
                            'photo_spot': int(location_data['photo_spot'].sum()),
                            'must_visit': int(location_data['must_visit'].sum())
                        }
                    }
                
                return json.dumps(report, indent=2, ensure_ascii=False).encode('utf-8')
        except Exception as e:
            st.error(f"Error exporting report: {str(e)}")
            return b"{}"


def create_feedback_dashboard(feedback_system: FeedbackSystem, lang_code: str = "en"):
    """Create a dashboard for viewing all feedback"""
    labels = feedback_system.get_feedback_labels(lang_code)
    
    st.markdown(f"## 📊 {labels['visitor_feedback']} Dashboard")
    
    # Get overall statistics
    stats_df = feedback_system.get_overall_statistics()
    
    if not stats_df.empty:
        # Top rated locations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 Top Rated Locations")
            top_rated = stats_df.nlargest(5, 'Avg Rating')[['Avg Rating', 'Total Reviews']]
            st.dataframe(top_rated, use_container_width=True)
        
        with col2:
            st.markdown("### 📸 Most Photographed")
            most_photographed = stats_df.nlargest(5, 'Photo Spot')[['Photo Spot', 'Avg Rating']]
            st.dataframe(most_photographed, use_container_width=True)
        
        # Visualizations
        st.markdown("### 📈 Rating Distribution")
        
        fig = px.bar(
            stats_df.reset_index(),
            x='location_name',
            y='Avg Rating',
            color='Total Reviews',
            title="Average Ratings by Location",
            labels={'location_name': 'Location', 'Avg Rating': 'Average Rating'},
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Export option
        st.markdown("### 📥 Export Data")
        if st.button("Generate Feedback Report"):
            report_data = feedback_system.export_feedback_report()
            st.download_button(
                label="Download Report (JSON)",
                data=report_data,
                file_name=f"feedback_report_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    else:
        st.info("No feedback data available yet. Start collecting feedback from visitors!")