import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

from api_client import OpenWeatherMapClient
from utils import AQICalculator, create_aqi_trend_plot, format_pollutant_name

# Initialize classes
api_client = OpenWeatherMapClient()
aqi_calculator = AQICalculator()

# Page configuration
st.set_page_config(
    page_title="Air Quality Index Dashboard",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme and state management
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Custom CSS with enhanced styling and animations
st.markdown("""
<style>
    /* Color palette */
    :root {
        --primary: #00B4D8;
        --secondary: #0077B6;
        --success: #28A745;
        --warning: #FFC107;
        --danger: #DC3545;
        --purple: #800080;
        --hazard: #7E0023;
        --light: #F8F9FA;
        --dark: #212529;
        --gray: #6C757D;
        --text-primary: #212529;
        --text-secondary: #495057;
        --text-muted: #6C757D;
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8F9FA;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Dark theme variables */
    [data-theme="dark"] {
        --text-primary: #E9ECEF;
        --text-secondary: #CED4DA;
        --text-muted: #ADB5BD;
        --bg-primary: #1a1c24;
        --bg-secondary: #2a2d3e;
    }

    /* Base theme styles */
    body {
        font-family: 'Inter', -apple-system, sans-serif;
        transition: var(--transition);
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }

    .dark-theme {
        --text-primary: #E9ECEF;
        --text-secondary: #CED4DA;
        --text-muted: #ADB5BD;
        --bg-primary: #1a1c24;
        --bg-secondary: #2a2d3e;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        transition: var(--transition);
    }

    p, span, div {
        color: var(--text-primary);
        transition: var(--transition);
    }

    .text-muted {
        color: var(--text-muted) !important;
    }

    /* Navigation */
    .navbar {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        padding: 1rem;
        margin: -1rem -1rem 1rem -1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    /* Card Styles */
    .metric-card {
        background: var(--bg-secondary);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: var(--transition);
        margin: 1rem 0;
        border: 1px solid rgba(128,128,128,0.1);
    }

    .dark-theme .metric-card {
        background: var(--bg-secondary);
        border-color: rgba(255,255,255,0.1);
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    /* Grid Layout */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }

    /* Value displays */
    .value-display {
        font-size: 2rem;
        font-weight: 600;
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Category badges */
    .category-badge {
        display: inline-block;
        padding: 0.25rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.5rem 0;
        background: rgba(255,255,255,0.1);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }

    /* FAQ specific styling */
    .stExpander {
        background: var(--bg-secondary);
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid rgba(128,128,128,0.1);
    }

    .stExpander > div:first-child {
        border-radius: 8px;
        background: var(--bg-secondary);
    }

    .stExpander div[data-testid="stExpander"] {
        color: var(--text-primary) !important;
    }

    /* Style the FAQ content specifically */
    .faq-content {
        color: var(--text-primary);
        background: var(--bg-secondary);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        line-height: 1.6;
    }

    /* Form elements */
    .stTextInput input {
        color: var(--text-primary) !important;
        background: var(--bg-secondary) !important;
        border: 1px solid rgba(128,128,128,0.2) !important;
    }

    .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(0,180,216,0.2) !important;
    }

    /* Sidebar styling */
    .sidebar .metric-card {
        background: rgba(128,128,128,0.05);
    }

    /* Alert styling */
    .alert {
        background: rgba(220,53,69,0.1);
        color: var(--danger);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Navigation bar
st.markdown("""
<div class="navbar">
    <div class="nav-title">
        <h1>🌬️ AirVision Dashboard</h1>
    </div>
    <div class="nav-controls">
        <button class="nav-button" onclick="toggleTheme()">
            🌓 Toggle Theme
        </button>
        <button class="nav-button">
            ℹ️ Help
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    city = st.text_input("Enter city name", "San Francisco")
    if city:
        try:
            with st.spinner('🔄 Fetching air quality data...'):
                # Get coordinates for the selected city
                lat, lon = api_client.get_coordinates(city)
                # Get the current air quality data
                air_quality_data = api_client.get_air_quality(lat, lon)
                aqi = air_quality_data['list'][0]['main']['aqi']
                category, color = aqi_calculator.get_aqi_category(aqi)
                
                st.markdown(f"<h2 style='color: {color};'>Current AQI: {aqi} ({category})</h2>", unsafe_allow_html=True)
                st.markdown(f"<p>{aqi_calculator.get_health_recommendation(aqi)}</p>", unsafe_allow_html=True)
                
                # Fetch historical data for the past 7 days
                end_time = datetime.now()
                start_time = end_time - timedelta(days=7)
                historical_data = api_client.get_historical_data(lat, lon, start_time, end_time)
                fig = create_aqi_trend_plot(historical_data)
                st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Sidebar with FAQ and information
with st.sidebar:
    st.markdown("""
    <div class="metric-card">
        <h4>ℹ️ About AQI</h4>
        <p>The Air Quality Index (AQI) helps you understand air quality levels and their impact on health.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-card">
        <h4 style="color: var(--text-primary);">❓ Frequently Asked Questions</h4>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("What is AQI?"):
        st.markdown("""
        <div class="faq-content">
            The Air Quality Index (AQI) is a scale used to communicate how polluted the air currently is or how polluted it is forecast to become.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("How is AQI calculated?"):
        st.markdown("""
        <div class="faq-content">
            AQI is calculated using measurements of various air pollutants, including PM2.5, PM10, ozone, and carbon monoxide. Each pollutant is assigned a score based on its concentration.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("What do the colors mean?"):
        st.markdown("""
        <div class="faq-content">
            <div class="category-badge" style="background: #28A74520; color: #28A745; margin: 0.5rem 0;">
                🟢 0-50: Good - Air quality is satisfactory
            </div>
            <div class="category-badge" style="background: #FFC10720; color: #FFC107; margin: 0.5rem 0;">
                🟡 51-100: Moderate - Acceptable air quality
            </div>
            <div class="category-badge" style="background: #FFA50020; color: #FFA500; margin: 0.5rem 0;">
                🟠 101-150: Unhealthy for Sensitive Groups
            </div>
            <div class="category-badge" style="background: #DC354520; color: #DC3545; margin: 0.5rem 0;">
                🔴 151-200: Unhealthy - Everyone may experience effects
            </div>
            <div class="category-badge" style="background: #80008020; color: #800080; margin: 0.5rem 0;">
                🟣 201-300: Very Unhealthy - Health warnings
            </div>
            <div class="category-badge" style="background: #7E002320; color: #7E0023; margin: 0.5rem 0;">
                🟤 301+: Hazardous - Health alert
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("How often is the data updated?"):
        st.markdown("""
        <div class="faq-content">
            <p style="color: var(--text-primary);">
            The air quality data is updated in real-time from OpenWeatherMap API. 
            Each query fetches the latest available data for your location.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card" style="margin-top: 1rem;">
        <h4>🔄 Updates</h4>
        <p class="text-muted">Last refreshed: {datetime.now().strftime("%B %d, %Y %H:%M")}</p>
    </div>
    """, unsafe_allow_html=True)

OPENWEATHERMAP_API_KEY=your_api_key_here