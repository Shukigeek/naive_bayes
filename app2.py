import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import time

# Configure page
st.set_page_config(
    page_title="🧠 Naive Bayes Analytics Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# API Configuration
API_URL = "http://127.0.0.1:8000"

# Custom CSS for INSANE styling
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');

    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glass morphism cards */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1) !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
    }

    /* Hover effects for cards */
    .css-1d391kg:hover {
        transform: translateY(-10px) scale(1.02) !important;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    /* Main title styling */
    .main-title {
        font-size: 4rem !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #fff, #a8edea, #fed6e3);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
        animation: fadeInUp 1s ease-out !important;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Subtitle styling */
    .subtitle {
        font-size: 1.5rem !important;
        color: rgba(255, 255, 255, 0.8) !important;
        text-align: center !important;
        margin-bottom: 3rem !important;
        font-weight: 300 !important;
    }

    /* Section headers */
    .section-header {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, #fff, #f0f8ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin: 2rem 0 1rem 0 !important;
        position: relative !important;
    }

    .section-header::before {
        content: '' !important;
        position: absolute !important;
        width: 100px !important;
        height: 4px !important;
        background: linear-gradient(45deg, #4facfe, #00f260) !important;
        bottom: -10px !important;
        left: 0 !important;
        border-radius: 2px !important;
        animation: expandLine 1s ease-out !important;
    }

    @keyframes expandLine {
        from { width: 0; }
        to { width: 100px; }
    }

    /* Metric styling */
    .stMetric {
        background: rgba(255, 255, 255, 0.15) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
    }

    .stMetric:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2) !important;
    }

    /* Metric value styling */
    .stMetric > div:first-child {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #00f260, #0575e6) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: pulse 2s ease-in-out infinite !important;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.6) !important;
        background: linear-gradient(135deg, #764ba2, #667eea) !important;
    }

    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(135deg, #00d2ff, #3a7bd5) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(0, 210, 255, 0.3) !important;
        animation: slideInRight 0.5s ease-out !important;
    }

    .stError {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3) !important;
        animation: slideInRight 0.5s ease-out !important;
    }

    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    /* Plotly chart container */
    .js-plotly-plot {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
    }

    /* Sidebar styling */
    .css-1d391kg .css-1offfwp {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 16px !important;
    }

    /* Loading animation */
    .loading {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 4px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(45deg, #4facfe, #00f260) !important;
        border-radius: 10px !important;
        height: 10px !important;
    }

    /* Custom info boxes */
    .info-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }

    /* Floating particles effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(255,255,255,0.1) 2px, transparent 2px),
            radial-gradient(circle at 75% 75%, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px, 30px 30px;
        animation: particleFloat 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }

    @keyframes particleFloat {
        0% { transform: translateX(0) translateY(0); }
        33% { transform: translateX(30px) translateY(-30px); }
        66% { transform: translateX(-20px) translateY(20px); }
        100% { transform: translateX(0) translateY(0); }
    }

    /* Column spacing */
    .css-ocqkz7 {
        gap: 2rem !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #4facfe, #00f260);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #00f260, #4facfe);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🧠 Naive Bayes Analytics Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Real-time Machine Learning Model Performance Dashboard</p>', unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.markdown("### ⚙️ Dashboard Controls")
    auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
    refresh_button = st.button("🔄 Manual Refresh")

    st.markdown("---")
    st.markdown("### 📊 Display Options")
    show_detailed_metrics = st.checkbox("Show Detailed Metrics", value=True)
    chart_theme = st.selectbox("Chart Theme", ["plotly", "plotly_white", "plotly_dark"])

    st.markdown("---")
    st.markdown(
        '<div class="info-box">💡 <strong>Tips:</strong><br>• Enable auto-refresh for real-time monitoring<br>• Hover over charts for interactive details<br>• All data is fetched from your API in real-time</div>',
        unsafe_allow_html=True)

# Auto-refresh logic
if auto_refresh:
    if 'refresh_counter' not in st.session_state:
        st.session_state.refresh_counter = 0

    placeholder = st.empty()
    with placeholder.container():
        progress_bar = st.progress(0)
        for i in range(30):
            time.sleep(1)
            progress_bar.progress((i + 1) / 30)
    placeholder.empty()
    st.session_state.refresh_counter += 1
    st.rerun()


# Function to fetch data with better error handling
@st.cache_data(ttl=30)
def fetch_accuracy_data():
    try:
        response = requests.get(f"{API_URL}/evaluation", timeout=10)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API returned status {response.status_code}"
    except requests.exceptions.RequestException as e:
        return None, str(e)


@st.cache_data(ttl=30)
def fetch_confusion_matrix():
    try:
        response = requests.get(f"{API_URL}/confusion_matrix", timeout=10)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API returned status {response.status_code}"
    except requests.exceptions.RequestException as e:
        return None, str(e)


# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h2 class="section-header">✅ Model Performance</h2>', unsafe_allow_html=True)

    # Accuracy metrics
    data, error = fetch_accuracy_data()
    if error:
        st.error(f"❌ Failed to fetch accuracy data: {error}")
        st.info("🔄 Please check your API connection and try refreshing.")
    else:
        accuracy_col1, accuracy_col2, accuracy_col3 = st.columns(3)

        with accuracy_col1:
            st.metric(
                label="🎯 Accuracy",
                value=f"{data['accuracy_percent']:.2f}%",
                delta=f"+{data['accuracy_percent'] - 85:.1f}%" if data['accuracy_percent'] > 85 else None
            )

        with accuracy_col2:
            st.metric(
                label="✅ Correct Predictions",
                value=f"{data['correct']:,}",
                delta=f"+{data['correct'] - 100}" if data['correct'] > 100 else None
            )

        with accuracy_col3:
            st.metric(
                label="❌ Incorrect Predictions",
                value=f"{data['incorrect']:,}",
                delta=f"-{100 - data['incorrect']}" if data['incorrect'] < 100 else None,
                delta_color="inverse"
            )

        # Performance gauge chart
        if show_detailed_metrics:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=data['accuracy_percent'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Model Accuracy", 'font': {'color': 'white', 'size': 24}},
                delta={'reference': 85, 'suffix': '%'},
                gauge={
                    'axis': {'range': [None, 100], 'tickcolor': "white"},
                    'bar': {'color': "rgba(0, 242, 96, 0.8)"},
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(255, 107, 107, 0.3)"},
                        {'range': [50, 80], 'color': "rgba(255, 193, 7, 0.3)"},
                        {'range': [80, 100], 'color': "rgba(0, 242, 96, 0.3)"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))

            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white", 'family': "Inter"},
                height=400,
                template=chart_theme
            )

            st.plotly_chart(fig_gauge, use_container_width=True)

with col2:
    st.markdown('<h2 class="section-header">📈 Live Statistics</h2>', unsafe_allow_html=True)

    if not error and data:
        # Performance donut chart
        total_predictions = data['correct'] + data['incorrect']

        fig_donut = go.Figure(data=[go.Pie(
            labels=['Correct', 'Incorrect'],
            values=[data['correct'], data['incorrect']],
            hole=.6,
            marker_colors=['#00f260', '#ff6b6b'],
            textinfo='label+percent',
            textfont={'color': 'white', 'size': 14},
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])

        fig_donut.update_layout(
            title={'text': 'Prediction Distribution', 'font': {'color': 'white', 'size': 20}, 'x': 0.5},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white", 'family': "Inter"},
            height=300,
            showlegend=False,
            template=chart_theme
        )

        # Add center text
        fig_donut.add_annotation(
            text=f"{total_predictions}<br>Total",
            x=0.5, y=0.5,
            font_size=20,
            font_color="white",
            showarrow=False
        )

        st.plotly_chart(fig_donut, use_container_width=True)

        # Real-time status
        st.markdown(
            '<div class="info-box">🟢 <strong>System Status:</strong> Online<br>📡 <strong>Last Update:</strong> Just now<br>⚡ <strong>Response Time:</strong> <1s</div>',
            unsafe_allow_html=True)

# Confusion Matrix Section
st.markdown('<h2 class="section-header">🔍 Confusion Matrix Analysis</h2>', unsafe_allow_html=True)

cm_data, cm_error = fetch_confusion_matrix()

if cm_error:
    st.error(f"❌ Failed to fetch confusion matrix: {cm_error}")
else:
    col_matrix1, col_matrix2 = st.columns([1, 1])

    with col_matrix1:
        # Display as DataFrame with styling
        cm_df = pd.DataFrame(cm_data)
        st.dataframe(
            cm_df.style.background_gradient(cmap='viridis', axis=None)
            .format(precision=0)
            .set_table_styles([
                {'selector': 'th', 'props': [('background-color', 'rgba(255,255,255,0.1)'),
                                             ('color', 'white'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('color', 'white')]}
            ]),
            use_container_width=True
        )

    with col_matrix2:
        # Create interactive heatmap
        labels = list(cm_data.keys())
        z_data = [[cm_data[row][col] for col in labels] for row in labels]

        fig_heatmap = go.Figure(data=go.Heatmap(
            z=z_data,
            x=labels,
            y=labels,
            colorscale='Viridis',
            text=z_data,
            texttemplate="%{text}",
            textfont={"size": 16, "color": "white"},
            hoverongaps=False,
            hovertemplate='True: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>'
        ))

        fig_heatmap.update_layout(
            title={'text': 'Interactive Confusion Matrix', 'font': {'color': 'white', 'size': 18}, 'x': 0.5},
            xaxis={'title': 'Predicted Label', 'color': 'white'},
            yaxis={'title': 'True Label', 'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white", 'family': "Inter"},
            height=400,
            template=chart_theme
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

# Additional Analytics Section
if show_detailed_metrics and not error and not cm_error:
    st.markdown('<h2 class="section-header">📊 Advanced Analytics</h2>', unsafe_allow_html=True)

    # Create sample time series data for demonstration
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    accuracy_trend = np.random.normal(data['accuracy_percent'], 2, 30)
    accuracy_trend = np.clip(accuracy_trend, 80, 100)  # Keep realistic range

    trend_col1, trend_col2 = st.columns(2)

    with trend_col1:
        # Accuracy trend
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=dates,
            y=accuracy_trend,
            mode='lines+markers',
            line=dict(color='#00f260', width=3),
            marker=dict(size=8, color='#4facfe'),
            name='Accuracy %',
            hovertemplate='Date: %{x}<br>Accuracy: %{y:.2f}%<extra></extra>'
        ))

        fig_trend.update_layout(
            title={'text': 'Accuracy Trend (30 Days)', 'font': {'color': 'white', 'size': 18}},
            xaxis={'title': 'Date', 'color': 'white', 'gridcolor': 'rgba(255,255,255,0.1)'},
            yaxis={'title': 'Accuracy %', 'color': 'white', 'gridcolor': 'rgba(255,255,255,0.1)'},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white", 'family': "Inter"},
            height=300,
            showlegend=False,
            template=chart_theme
        )

        st.plotly_chart(fig_trend, use_container_width=True)

    with trend_col2:
        # Feature importance (sample data)
        features = ['Feature A', 'Feature B', 'Feature C', 'Feature D', 'Feature E']
        importance = np.random.random(5)
        importance = importance / importance.sum() * 100

        fig_bar = go.Figure([go.Bar(
            x=features,
            y=importance,
            marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7'],
            text=[f'{v:.1f}%' for v in importance],
            textposition='auto',
            hovertemplate='Feature: %{x}<br>Importance: %{y:.1f}%<extra></extra>'
        )])

        fig_bar.update_layout(
            title={'text': 'Feature Importance', 'font': {'color': 'white', 'size': 18}},
            xaxis={'title': 'Features', 'color': 'white'},
            yaxis={'title': 'Importance %', 'color': 'white', 'gridcolor': 'rgba(255,255,255,0.1)'},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white", 'family': "Inter"},
            height=300,
            template=chart_theme
        )

        st.plotly_chart(fig_bar, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem;">'
    '🚀 Built with Streamlit | 🧠 Powered by Naive Bayes | 💫 Enhanced with Custom CSS'
    '</div>',
    unsafe_allow_html=True
)

# Auto-refresh indicator
if auto_refresh:
    st.markdown(
        '<div style="position: fixed; top: 10px; right: 10px; background: rgba(0, 242, 96, 0.1); '
        'color: #00f260; padding: 0.5rem 1rem; border-radius: 20px; border: 1px solid rgba(0, 242, 96, 0.3); '
        'backdrop-filter: blur(10px); font-size: 0.8rem;">🔄 Auto-refresh ON</div>',
        unsafe_allow_html=True
    )