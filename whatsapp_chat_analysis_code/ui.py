import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for advanced styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Montserrat:wght@400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main title styling */
    h1 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        border-right: 2px solid #667eea;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #4a5568;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Cards/Containers */
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border-left: 4px solid #667eea;
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Welcome screen */
    .welcome-container {
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .welcome-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .welcome-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        margin-bottom: 30px;
        opacity: 0.9;
    }
    
    .feature-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Montserrat', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: #2d3748;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        border: 2px dashed rgba(255, 255, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>💬 Chat Analyzer</h1>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "📁 Upload WhatsApp Chat", 
        type=["txt"],
        help="Export your WhatsApp chat and upload the .txt file"
    )
    
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocesdata(data)
        
        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.insert(0, "Overall")
        
        st.markdown("---")
        st.markdown("### 👤 Select User")
        selected_user = st.selectbox("", user_list, label_visibility="collapsed")
        
        st.markdown("---")
        analyze_button = st.button("🚀 Analyze Chat", use_container_width=True)
    else:
        analyze_button = False

# Main content
if uploaded_file is None:
    # Welcome Screen
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-title">💬 WhatsApp Chat Analyzer</div>
            <div class="welcome-subtitle">Unlock insights from your conversations with advanced analytics</div>
            <p style="font-size: 1.1rem; margin-top: 20px;">
                📊 Get detailed statistics • 📈 Visualize trends • 😊 Analyze emotions
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("<h2 style='text-align: center; margin: 40px 0 30px 0;'>✨ Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="feature-box">
                <div class="feature-icon">📊</div>
                <h3>Statistics</h3>
                <p>Messages, words, media & links count</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-box">
                <div class="feature-icon">📈</div>
                <h3>Timelines</h3>
                <p>Track activity over time</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-box">
                <div class="feature-icon">🔥</div>
                <h3>Activity Maps</h3>
                <p>Discover peak hours & days</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="feature-box">
                <div class="feature-icon">😊</div>
                <h3>Emoji Analysis</h3>
                <p>Most used emojis & patterns</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Instructions
    st.markdown("<h2 style='text-align: center; margin: 50px 0 30px 0;'>🚀 Getting Started</h2>", unsafe_allow_html=True)
    
    st.info("""
        **📱 How to export WhatsApp chat:**
        
        1. Open WhatsApp and go to the chat you want to analyze
        2. Tap on the three dots (⋮) in the top right corner
        3. Select "More" → "Export chat"
        4. Choose "Without media"
        5. Upload the exported .txt file using the sidebar
    """)

elif analyze_button:
    # Statistics Section
    st.markdown("<div class='section-header'>📊 Top Statistics</div>", unsafe_allow_html=True)
    
    num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="💬 Total Messages", value=f"{num_messages:,}")
    with col2:
        st.metric(label="📝 Total Words", value=f"{words:,}")
    with col3:
        st.metric(label="📷 Media Shared", value=f"{num_media_messages:,}")
    with col4:
        st.metric(label="🔗 Links Shared", value=f"{links:,}")
    
    # Timeline Section
    st.markdown("<div class='section-header'>📈 Activity Timelines</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(timeline['time'], timeline['message'], color='#667eea', linewidth=2.5, marker='o')
        ax.fill_between(timeline['time'], timeline['message'], alpha=0.3, color='#667eea')
        plt.xticks(rotation=45, ha='right')
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### 📆 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#764ba2', linewidth=2)
        plt.xticks(rotation=45, ha='right')
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)
    
    # Activity Map Section
    st.markdown("<div class='section-header'>🔥 Activity Patterns</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Most Busy Day")
        busy_day = helper.weak_activity_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(busy_day.index, busy_day.values, color='#667eea', alpha=0.8)
        ax.set_xlabel('Day', fontsize=12, fontweight='bold')
        ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### 📊 Most Busy Month")
        busy_month = helper.monthly_activity_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(busy_month.index, busy_month.values, color='#764ba2', alpha=0.8)
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("#### 🗓️ Weekly Activity Heatmap")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(user_heatmap, cmap='YlOrRd', linewidths=0.5, cbar_kws={'label': 'Messages'})
    plt.xlabel('Hour', fontsize=12, fontweight='bold')
    plt.ylabel('Day', fontsize=12, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Busiest Users (Only for Overall)
    if selected_user == 'Overall':
        st.markdown("<div class='section-header'>👥 Most Active Users</div>", unsafe_allow_html=True)
        x, new_df = helper.most_busy_users(df)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(x.index, x.values, color='#667eea', alpha=0.8)
            ax.set_xlabel('User', fontsize=12, fontweight='bold')
            ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            ax.grid(True, alpha=0.3, axis='y', linestyle='--')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.markdown("#### 📋 User Statistics")
            st.dataframe(new_df, use_container_width=True, height=400)
    
    # Word Analysis Section
    st.markdown("<div class='section-header'>💭 Word Analysis</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### ☁️ Word Cloud")
        df_wc = helper.create_worldcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### 📊 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = plt.cm.viridis(range(len(most_common_df)))
        ax.barh(most_common_df['word'], most_common_df['count'], color=colors)
        ax.set_xlabel('Count', fontsize=12, fontweight='bold')
        ax.set_ylabel('Words', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)
    
    # Emoji Analysis Section
    st.markdown("<div class='section-header'>😊 Emoji Analysis</div>", unsafe_allow_html=True)
    
    emoji_df = helper.emoji_helper(selected_user, df)
    
    if not emoji_df.empty:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 Emoji Usage Table")
            st.dataframe(emoji_df, use_container_width=True, height=400)
        
        with col2:
            st.markdown("#### 🥧 Top 5 Emojis")
            fig, ax = plt.subplots(figsize=(8, 8))
            colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%", 
                   colors=colors, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
            ax.axis('equal')
            st.pyplot(fig)
    else:
        st.info("No emojis found in the selected chat!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #718096; padding: 20px;'>
            <p>Made with ❤️ using Streamlit | WhatsApp Chat Analyzer</p>
        </div>
    """, unsafe_allow_html=True)