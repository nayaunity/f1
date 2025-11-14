import streamlit as st
import fastf1
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import os

warnings.filterwarnings('ignore')

# Enable Fast-F1 caching
cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
fastf1.Cache.enable_cache(cache_dir)

# Page configuration
st.set_page_config(
    page_title="F1 Driver Battle",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="auto"
)

# F1 × Adobe × Notion inspired styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main {
        background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
        color: #ffffff;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Keep header visible but style it */
    header {
        background: transparent !important;
    }

    /* Style the hamburger menu button */
    button[kind="header"] {
        background-color: rgba(225, 6, 0, 0.1) !important;
        border: 1.5px solid rgba(225, 6, 0, 0.3) !important;
        border-radius: 8px !important;
        color: #E10600 !important;
    }

    button[kind="header"]:hover {
        background-color: rgba(225, 6, 0, 0.2) !important;
        border-color: #E10600 !important;
    }

    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #E10600 0%, #FF1E00 100%);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #FF1E00 0%, #E10600 100%);
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.03em !important;
    }

    h1, h2, h3 {
        border: none !important;
        padding-bottom: 0 !important;
    }

    /* Sidebar styling - F1 garage inspired */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #15151e 0%, #0a0a0f 100%);
        border-right: none;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.12);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e0e0e0;
        font-size: 0.875rem;
        font-weight: 500;
    }

    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-size: 0.875rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.75rem !important;
        border-bottom: 2px solid #E10600 !important;
    }

    .stSelectbox label {
        color: #b0b0b0 !important;
        font-size: 0.6875rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin-bottom: 0.5rem !important;
    }

    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px);
    }

    .stSelectbox > div > div:hover {
        border-color: #E10600 !important;
        background: rgba(225, 6, 0, 0.08) !important;
        box-shadow: 0 0 0 3px rgba(225, 6, 0, 0.1);
    }

    .stSelectbox > div > div:focus-within {
        border-color: #E10600 !important;
        box-shadow: 0 0 0 3px rgba(225, 6, 0, 0.15) !important;
        background: rgba(225, 6, 0, 0.08) !important;
    }

    /* Disable typing in selectbox - dropdown only */
    .stSelectbox input,
    [data-baseweb="select"] input,
    [data-baseweb="popover"] input,
    input[role="combobox"] {
        caret-color: transparent !important;
        cursor: pointer !important;
        pointer-events: none !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
    }

    .stSelectbox input:focus,
    [data-baseweb="select"] input:focus,
    input[role="combobox"]:focus {
        caret-color: transparent !important;
        outline: none !important;
    }

    /* Re-enable pointer events on selectbox container so dropdown still works */
    .stSelectbox > div,
    [data-baseweb="select"],
    .stSelectbox [role="button"],
    [data-baseweb="select"] [role="button"] {
        pointer-events: auto !important;
    }

    /* F1 Racing button */
    .stButton > button {
        background: linear-gradient(135deg, #E10600 0%, #FF1E00 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        font-size: 0.8125rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        box-shadow: 0 4px 14px rgba(225, 6, 0, 0.25);
        position: relative;
        overflow: hidden;
    }

    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }

    .stButton > button:hover:before {
        left: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #FF1E00 0%, #E10600 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(225, 6, 0, 0.35);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(225, 6, 0, 0.3);
    }

    .stButton > button:disabled {
        background: linear-gradient(135deg, #6b6b6b 0%, #4a4a4a 100%);
        box-shadow: none;
        cursor: not-allowed;
        opacity: 0.5;
    }

    /* Metrics - Adobe inspired Dark */
    [data-testid="stMetricLabel"] {
        color: #9b9b9b !important;
        font-size: 0.6875rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.875rem !important;
        font-weight: 800 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Notion-style cards - Dark */
    .session-header {
        background: linear-gradient(135deg, #15151e 0%, #0f0f15 100%);
        border: 1.5px solid #2a2a35;
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4), 0 2px 8px rgba(225, 6, 0, 0.1);
        transition: all 0.3s ease;
    }

    .session-header:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5), 0 4px 12px rgba(225, 6, 0, 0.15);
        border-color: #3a3a45;
    }

    .driver-card {
        background: linear-gradient(135deg, #15151e 0%, #12121a 100%);
        border: 1.5px solid #2a2a35;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        height: 100%;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4), 0 2px 8px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .driver-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6), 0 4px 16px rgba(225, 6, 0, 0.2);
        border-color: #E10600;
    }

    .driver-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--team-color, #E10600) 0%, transparent 100%);
    }

    /* F1 Winner badge */
    .winner-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #1a1a1a;
        padding: 0.875rem 2rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.9375rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        box-shadow: 0 4px 16px rgba(255, 215, 0, 0.3);
        font-family: 'Space Grotesk', sans-serif;
    }

    .vs-divider {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #E10600 0%, #FF1E00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0.05em;
        filter: drop-shadow(0 2px 4px rgba(225, 6, 0, 0.2));
    }

    .section-header {
        font-size: 0.8125rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #9b9b9b;
        margin: 3.5rem 0 1.5rem 0;
        padding-bottom: 0.875rem;
        border-bottom: 2px solid #2a2a35;
        font-family: 'Space Grotesk', sans-serif;
    }

    .team-badge {
        display: inline-block;
        padding: 0.375rem 1rem;
        background: linear-gradient(135deg, #2a2a35 0%, #1f1f28 100%);
        border: 1px solid #3a3a45;
        border-radius: 6px;
        font-size: 0.6875rem;
        font-weight: 700;
        color: #b0b0b0;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #2a2a35 50%, transparent 100%);
        margin: 3rem 0;
    }

    .info-box {
        background: linear-gradient(135deg, #15151e 0%, #0f0f15 100%);
        border: 1.5px solid #2a2a35;
        border-left: 4px solid #E10600;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }

    .info-box h3 {
        margin: 0 0 1rem 0;
        font-size: 1.125rem;
        font-weight: 700;
        color: #ffffff !important;
    }

    .info-box p, .info-box ol {
        color: #9b9b9b;
        line-height: 1.7;
    }

    .feature-card {
        background: linear-gradient(135deg, #15151e 0%, #12121a 100%);
        border: 1.5px solid #2a2a35;
        border-radius: 12px;
        padding: 2.5rem;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }

    .feature-card:hover {
        border-color: #E10600;
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6), 0 4px 16px rgba(225, 6, 0, 0.2);
    }

    .feature-card h3 {
        font-size: 1.125rem;
        margin: 0 0 0.875rem 0;
        color: #ffffff !important;
        font-weight: 700;
    }

    .feature-card p {
        color: #9b9b9b;
        font-size: 0.9375rem;
        line-height: 1.7;
        margin: 0;
    }

    .stSpinner > div {
        border-color: #E10600 !important;
    }

    /* Alert styling - Dark Adobe inspired */
    .stSuccess {
        background: linear-gradient(135deg, rgba(102, 187, 106, 0.15) 0%, rgba(76, 175, 80, 0.1) 100%) !important;
        border: 1.5px solid #66bb6a !important;
        border-radius: 10px !important;
        color: #81c784 !important;
        padding: 1rem 1.25rem !important;
        font-weight: 500 !important;
    }

    .stError {
        background: linear-gradient(135deg, rgba(239, 83, 80, 0.15) 0%, rgba(244, 67, 54, 0.1) 100%) !important;
        border: 1.5px solid #ef5350 !important;
        border-radius: 10px !important;
        color: #ef5350 !important;
        padding: 1rem 1.25rem !important;
        font-weight: 500 !important;
    }

    .stWarning {
        background: linear-gradient(135deg, rgba(255, 167, 38, 0.15) 0%, rgba(255, 152, 0, 0.1) 100%) !important;
        border: 1.5px solid #ffa726 !important;
        border-radius: 10px !important;
        color: #ffb74d !important;
        padding: 1rem 1.25rem !important;
        font-weight: 500 !important;
    }

    .stInfo {
        background: linear-gradient(135deg, rgba(66, 165, 245, 0.15) 0%, rgba(33, 150, 243, 0.1) 100%) !important;
        border: 1.5px solid #42a5f5 !important;
        border-radius: 10px !important;
        color: #64b5f6 !important;
        padding: 1rem 1.25rem !important;
        font-weight: 500 !important;
    }

    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        margin-bottom: 0.75rem;
        background: linear-gradient(135deg, #ffffff 0%, #E10600 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        line-height: 1.1;
    }

    .main-subtitle {
        font-size: 1.125rem;
        font-weight: 500;
        color: #9b9b9b;
        letter-spacing: 0.01em;
        margin-bottom: 3rem;
    }

    .driver-name {
        font-size: 1.75rem;
        font-weight: 900;
        margin-bottom: 0.75rem;
        letter-spacing: -0.03em;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
    }

    .lap-time {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #b0b0b0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1.25rem 0;
        line-height: 1;
    }

    .data-quality-badge {
        display: inline-block;
        padding: 0.375rem 1rem;
        border-radius: 6px;
        font-size: 0.6875rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .quality-good {
        background: linear-gradient(135deg, rgba(102, 187, 106, 0.2) 0%, rgba(76, 175, 80, 0.15) 100%);
        color: #81c784;
        border: 1px solid #66bb6a;
    }

    .quality-warning {
        background: linear-gradient(135deg, rgba(255, 167, 38, 0.2) 0%, rgba(255, 152, 0, 0.15) 100%);
        color: #ffb74d;
        border: 1px solid #ffa726;
    }

    /* Speed lines effect on hover */
    @keyframes speedLines {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
</style>

<script>
    // Disable typing in selectboxes - make them dropdown-only
    function disableSelectboxInput() {
        // Target ALL input fields in selectboxes with multiple selectors
        const selectors = [
            '.stSelectbox input',
            '[data-baseweb="select"] input',
            '[data-baseweb="popover"] input',
            'input[role="combobox"]',
            'div[data-baseweb="select"] input'
        ];

        selectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(input => {
                if (input.hasAttribute('data-processed')) return;
                input.setAttribute('data-processed', 'true');

                // Multiple approaches to prevent mobile keyboard
                input.setAttribute('readonly', 'readonly');
                input.setAttribute('inputmode', 'none');
                input.setAttribute('disabled', 'disabled');
                input.style.pointerEvents = 'none';
                input.style.userSelect = 'none';

                // Prevent focus and blur immediately
                const preventFocus = (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    e.target.blur();
                    return false;
                };

                input.addEventListener('focus', preventFocus, true);
                input.addEventListener('focusin', preventFocus, true);
                input.addEventListener('touchstart', preventFocus, true);
                input.addEventListener('touchend', preventFocus, true);
                input.addEventListener('mousedown', preventFocus, true);
                input.addEventListener('click', preventFocus, true);

                // Prevent all keyboard input
                input.addEventListener('keydown', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }, true);

                input.addEventListener('keypress', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }, true);

                input.addEventListener('input', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }, true);

                input.addEventListener('beforeinput', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }, true);
            });
        });
    }

    // Run on initial load
    setTimeout(disableSelectboxInput, 100);
    setTimeout(disableSelectboxInput, 500);
    setTimeout(disableSelectboxInput, 1000);

    // Watch for new selectboxes
    const observer = new MutationObserver(() => {
        disableSelectboxInput();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['class', 'data-baseweb']
    });

    // Also run periodically for safety
    setInterval(disableSelectboxInput, 300);
</script>
""", unsafe_allow_html=True)

# Team colors for visualization (2024 season)
TEAM_COLORS = {
    'Red Bull Racing': '#3671C6',
    'Ferrari': '#E8002D',
    'Mercedes': '#27F4D2',
    'McLaren': '#FF8000',
    'Aston Martin': '#229971',
    'Alpine': '#FF87BC',
    'Williams': '#64C4FF',
    'AlphaTauri': '#5E8FAA',
    'Alfa Romeo': '#C92D4B',
    'Haas F1 Team': '#B6BABD',
    'RB': '#6692FF',
    'Kick Sauber': '#52E252'
}


def validate_telemetry_data(telemetry_data, driver_name):
    """Validate telemetry data quality and completeness."""
    issues = []

    tel = telemetry_data['telemetry']

    # Check if we have position data
    if 'X' not in tel.columns or 'Y' not in tel.columns:
        issues.append("Missing track position data")
    else:
        # Check for null values in position
        if tel['X'].isna().any() or tel['Y'].isna().any():
            issues.append("Incomplete track position data")

        # Check if position data looks reasonable (not all zeros)
        if tel['X'].std() < 1 or tel['Y'].std() < 1:
            issues.append("Invalid track position data")

    # Check speed data
    if 'Speed' not in tel.columns:
        issues.append("Missing speed data")
    else:
        if tel['Speed'].isna().any():
            issues.append("Incomplete speed data")
        if tel['Speed'].max() < 50:  # Should have speeds over 50 km/h
            issues.append("Suspiciously low speed data")

    # Check distance data
    if 'Distance' not in tel.columns:
        issues.append("Missing distance data")
    else:
        if tel['Distance'].isna().any():
            issues.append("Incomplete distance data")
        # A full lap should be at least 3km
        if tel['Distance'].max() < 3000:
            issues.append(f"Incomplete lap (only {tel['Distance'].max():.0f}m)")

    # Check time data
    if 'Time' not in tel.columns:
        issues.append("Missing time data")

    return issues


@st.cache_data(show_spinner=False)
def load_session(year, gp, session_type):
    """Load F1 session data with caching."""
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()
        return session, None
    except Exception as e:
        return None, str(e)


@st.cache_data(show_spinner=False)
def get_driver_telemetry(_session, driver_code, year, gp, session_type):
    """Get fastest lap telemetry for a specific driver with validation."""
    try:
        driver_laps = _session.laps.pick_drivers(driver_code)
        if driver_laps.empty:
            return None, f"No laps found for driver {driver_code}"

        fastest_lap = driver_laps.pick_fastest()
        if fastest_lap is None or pd.isna(fastest_lap['LapTime']):
            return None, f"No valid fastest lap for driver {driver_code}"

        telemetry = fastest_lap.get_telemetry()
        if telemetry.empty:
            return None, f"No telemetry data available for driver {driver_code}"

        result = {
            'telemetry': telemetry,
            'lap_time': fastest_lap['LapTime'],
            'driver': fastest_lap['Driver'],
            'team': fastest_lap['Team'],
            'compound': fastest_lap.get('Compound', 'Unknown'),
            'lap_number': fastest_lap.get('LapNumber', 'Unknown'),
            'year': year,
            'gp': gp,
            'session_type': session_type
        }

        # Validate data quality
        issues = validate_telemetry_data(result, driver_code)
        result['data_issues'] = issues

        return result, None
    except Exception as e:
        return None, f"Error loading telemetry for {driver_code}: {str(e)}"


def create_speed_comparison(driver1_data, driver2_data, driver1_name, driver2_name):
    """Create professional speed comparison chart."""
    fig = go.Figure()

    color1 = TEAM_COLORS.get(driver1_data['team'], '#FF0000')
    color2 = TEAM_COLORS.get(driver2_data['team'], '#0000FF')

    fig.add_trace(go.Scatter(
        x=driver1_data['telemetry']['Distance'],
        y=driver1_data['telemetry']['Speed'],
        mode='lines',
        name=f"{driver1_name} (Lap {driver1_data['lap_number']})",
        line=dict(color=color1, width=3),
        hovertemplate='<b>%{fullData.name}</b><br>Distance: %{x:.0f}m<br>Speed: %{y:.0f} km/h<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=driver2_data['telemetry']['Distance'],
        y=driver2_data['telemetry']['Speed'],
        mode='lines',
        name=f"{driver2_name} (Lap {driver2_data['lap_number']})",
        line=dict(color=color2, width=3),
        hovertemplate='<b>%{fullData.name}</b><br>Distance: %{x:.0f}m<br>Speed: %{y:.0f} km/h<extra></extra>'
    ))

    fig.update_layout(
        showlegend=True,
        xaxis_title="Distance (m)",
        yaxis_title="Speed (km/h)",
        hovermode='x unified',
        height=500,
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#000000',
        font=dict(color='#9b9b9b', size=11, family='Inter'),
        margin=dict(l=60, r=40, t=20, b=60),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=12, color='#ffffff'),
            bgcolor='rgba(21, 21, 30, 0.95)',
            bordercolor='#2a2a35',
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=False,
            showline=True,
            linewidth=1.5,
            linecolor='#2a2a35',
            title_font=dict(size=12, color='#9b9b9b')
        ),
        yaxis=dict(
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=False,
            showline=True,
            linewidth=1.5,
            linecolor='#2a2a35',
            title_font=dict(size=12, color='#9b9b9b')
        )
    )

    return fig


def create_track_map(driver1_data, driver2_data, driver1_name, driver2_name):
    """Create professional track map visualization."""
    fig = go.Figure()

    tel1 = driver1_data['telemetry']
    tel2 = driver2_data['telemetry']

    color1 = TEAM_COLORS.get(driver1_data['team'], '#FF0000')
    color2 = TEAM_COLORS.get(driver2_data['team'], '#0000FF')

    # Driver 2 racing line - thick, dashed, semi-transparent background
    fig.add_trace(go.Scatter(
        x=tel2['X'],
        y=tel2['Y'],
        mode='lines',
        name=f"{driver2_name} (Lap {driver2_data['lap_number']})",
        line=dict(color=color2, width=8, dash='dash'),
        opacity=0.5,
        hovertemplate='<b>%{fullData.name}</b><br>Speed: ' + tel2['Speed'].astype(str) + ' km/h<extra></extra>'
    ))

    # Driver 1 racing line - solid, bright, on top
    fig.add_trace(go.Scatter(
        x=tel1['X'],
        y=tel1['Y'],
        mode='lines',
        name=f"{driver1_name} (Lap {driver1_data['lap_number']})",
        line=dict(color=color1, width=3),
        hovertemplate='<b>%{fullData.name}</b><br>Speed: ' + tel1['Speed'].astype(str) + ' km/h<extra></extra>'
    ))

    fig.update_layout(
        showlegend=True,
        xaxis_title="X Position (m)",
        yaxis_title="Y Position (m)",
        height=600,
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#000000',
        font=dict(color='#9b9b9b', size=11, family='Inter'),
        margin=dict(l=60, r=40, t=20, b=60),
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=False,
            showline=True,
            linewidth=1.5,
            linecolor='#2a2a35',
            title_font=dict(size=12, color='#9b9b9b')
        ),
        xaxis=dict(
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=False,
            showline=True,
            linewidth=1.5,
            linecolor='#2a2a35',
            title_font=dict(size=12, color='#9b9b9b')
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=12, color='#ffffff'),
            bgcolor='rgba(21, 21, 30, 0.95)',
            bordercolor='#2a2a35',
            borderwidth=1
        )
    )

    return fig


def create_delta_time_plot(driver1_data, driver2_data, driver1_name, driver2_name):
    """Create intuitive delta time plot with color coding."""
    tel1 = driver1_data['telemetry']
    tel2 = driver2_data['telemetry']

    min_distance = max(tel1['Distance'].min(), tel2['Distance'].min())
    max_distance = min(tel1['Distance'].max(), tel2['Distance'].max())
    common_distance = np.linspace(min_distance, max_distance, 1000)

    time1_seconds = tel1['Time'].dt.total_seconds()
    time2_seconds = tel2['Time'].dt.total_seconds()

    time1 = np.interp(common_distance, tel1['Distance'], time1_seconds)
    time2 = np.interp(common_distance, tel2['Distance'], time2_seconds)
    delta = time1 - time2

    fig = go.Figure()

    color1 = TEAM_COLORS.get(driver1_data['team'], '#FF0000')
    color2 = TEAM_COLORS.get(driver2_data['team'], '#0000FF')

    delta_driver2_winning = [d if d > 0 else 0 for d in delta]
    delta_driver1_winning = [d if d < 0 else 0 for d in delta]

    fig.add_trace(go.Scatter(
        x=common_distance,
        y=delta_driver2_winning,
        mode='lines',
        name=f'{driver2_name} faster here',
        line=dict(color=color2, width=0),
        fill='tozeroy',
        fillcolor=f'rgba({int(color2[1:3], 16)}, {int(color2[3:5], 16)}, {int(color2[5:7], 16)}, 0.3)',
        hovertemplate=f'<b>{driver2_name} gaining</b><br>Distance: %{{x:.0f}}m<br>Advantage: %{{y:.3f}}s<extra></extra>',
        showlegend=True
    ))

    fig.add_trace(go.Scatter(
        x=common_distance,
        y=delta_driver1_winning,
        mode='lines',
        name=f'{driver1_name} faster here',
        line=dict(color=color1, width=0),
        fill='tozeroy',
        fillcolor=f'rgba({int(color1[1:3], 16)}, {int(color1[3:5], 16)}, {int(color1[5:7], 16)}, 0.3)',
        hovertemplate=f'<b>{driver1_name} gaining</b><br>Distance: %{{x:.0f}}m<br>Advantage: %{{y:.3f}}s<extra></extra>',
        showlegend=True
    ))

    fig.add_trace(go.Scatter(
        x=common_distance,
        y=delta,
        mode='lines',
        name='Gap between drivers',
        line=dict(color='#ffffff', width=2),
        hovertemplate='Distance: %{x:.0f}m<br>Time gap: %{y:.3f}s<extra></extra>',
        showlegend=False
    ))

    fig.add_hline(
        y=0,
        line_dash="solid",
        line_color="#9b9b9b",
        line_width=2,
        annotation_text="Even",
        annotation_position="right",
        annotation_font_size=10,
        annotation_font_color="#9b9b9b"
    )

    fig.update_layout(
        showlegend=True,
        xaxis_title="Distance around the lap (meters)",
        yaxis_title="Time Gap (seconds)",
        height=600,
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#000000',
        hovermode='x unified',
        font=dict(color='#9b9b9b', size=11, family='Inter'),
        margin=dict(l=60, r=40, t=20, b=60),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11, color='#ffffff'),
            bgcolor='rgba(21, 21, 30, 0.95)',
            bordercolor='#2a2a35',
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=False,
            showline=True,
            linewidth=1.5,
            linecolor='#2a2a35',
            title_font=dict(size=12, color='#9b9b9b')
        ),
        yaxis=dict(
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=True,
            zerolinecolor='#9b9b9b',
            zerolinewidth=2,
            showline=True,
            linewidth=1.5,
            linecolor='#2a2a35',
            title_font=dict(size=12, color='#9b9b9b')
        ),
        annotations=[
            dict(
                text=f"↑ {driver2_name} ahead",
                xref="paper", yref="paper",
                x=0.98, y=0.98,
                showarrow=False,
                font=dict(size=11, color=color2),
                bgcolor='rgba(21, 21, 30, 0.95)',
                bordercolor='#2a2a35',
                borderwidth=1,
                borderpad=8,
                xanchor='right'
            ),
            dict(
                text=f"↓ {driver1_name} ahead",
                xref="paper", yref="paper",
                x=0.98, y=0.02,
                showarrow=False,
                font=dict(size=11, color=color1),
                bgcolor='rgba(21, 21, 30, 0.95)',
                bordercolor='#2a2a35',
                borderwidth=1,
                borderpad=8,
                xanchor='right'
            )
        ]
    )

    return fig


# Main App Layout
st.markdown("<div class='main-title'>F1 Driver Battle</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Professional telemetry analysis and driver comparison</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Session Selection")
    st.markdown("")

    current_year = datetime.now().year
    year = st.selectbox("Season", options=list(range(2024, 2017, -1)), index=0)

    try:
        schedule = fastf1.get_event_schedule(year)
        available_events = schedule[schedule['EventName'].notna()]['EventName'].tolist()
        event_names = [event for event in available_events if event]
    except Exception as e:
        st.error(f"Error loading schedule: {e}")
        available_events = []
        event_names = []

    if event_names:
        gp = st.selectbox("Grand Prix", options=event_names, index=0)
    else:
        st.warning("No events available")
        gp = None

    session_type = st.selectbox(
        "Session Type",
        options=["Qualifying", "Race", "Sprint", "Practice 1", "Practice 2", "Practice 3"],
        index=0,
        help="Qualifying and Race provide the most reliable comparison data"
    )

    st.markdown("")

    if st.button("Load Session"):
        if gp:
            # Clear previous comparison data
            for key in ['driver1_data', 'driver2_data', 'driver1_name', 'driver2_name']:
                if key in st.session_state:
                    del st.session_state[key]

            with st.spinner("Loading session data..."):
                session, error = load_session(year, gp, session_type)
                if error:
                    st.error(f"Error: {error}")
                    st.session_state.session = None
                    if 'loaded_session_params' in st.session_state:
                        del st.session_state['loaded_session_params']
                else:
                    st.session_state.session = session
                    st.session_state.year = year
                    st.session_state.gp = gp
                    st.session_state.session_type = session_type
                    # Store the loaded session parameters for validation
                    st.session_state.loaded_session_params = {
                        'year': year,
                        'gp': gp,
                        'session_type': session_type
                    }
                    st.success(f"✓ Loaded {year} {gp} {session_type}")
        else:
            st.warning("Select a Grand Prix")

    if 'session' in st.session_state and st.session_state.session is not None:
        session = st.session_state.session
        drivers = session.laps['Driver'].unique().tolist()
        drivers.sort()

        st.markdown("")
        st.markdown("### Driver Selection")
        st.markdown("")

        driver1 = st.selectbox("Driver 1", options=drivers, index=0 if len(drivers) > 0 else None)
        driver2 = st.selectbox("Driver 2", options=drivers, index=1 if len(drivers) > 1 else 0)

        st.markdown("")

        # Warning for practice sessions
        if "Practice" in st.session_state.session_type:
            st.warning("⚠️ Practice data may be incomplete. Qualifying or Race recommended.")

        # Check if current selection matches loaded session
        session_changed = False
        if 'loaded_session_params' in st.session_state:
            loaded_params = st.session_state.loaded_session_params
            if (loaded_params['year'] != year or
                loaded_params['gp'] != gp or
                loaded_params['session_type'] != session_type):
                session_changed = True

        # Show warning if session details changed
        if session_changed:
            st.warning("⚠️ Session details changed. Click 'Load Session' first.")

        # Disable Compare button if session details don't match loaded session
        compare_disabled = session_changed or 'loaded_session_params' not in st.session_state

        if st.button("Compare", disabled=compare_disabled):
            if driver1 == driver2:
                st.error("Select two different drivers")
            else:
                # Clear old data
                for key in ['driver1_data', 'driver2_data', 'driver1_name', 'driver2_name']:
                    if key in st.session_state:
                        del st.session_state[key]

                with st.spinner(f"Loading telemetry for {driver1} and {driver2}..."):
                    driver1_data, error1 = get_driver_telemetry(
                        session, driver1,
                        st.session_state.year,
                        st.session_state.gp,
                        st.session_state.session_type
                    )
                    driver2_data, error2 = get_driver_telemetry(
                        session, driver2,
                        st.session_state.year,
                        st.session_state.gp,
                        st.session_state.session_type
                    )

                    if error1:
                        st.error(f"Error loading {driver1}: {error1}")
                    elif error2:
                        st.error(f"Error loading {driver2}: {error2}")
                    else:
                        st.session_state.driver1_data = driver1_data
                        st.session_state.driver2_data = driver2_data
                        st.session_state.driver1_name = driver1
                        st.session_state.driver2_name = driver2
                        st.success("✓ Comparison ready")
                        st.rerun()

# Main content
if all(key in st.session_state for key in ['driver1_data', 'driver2_data']):
    driver1_data = st.session_state.driver1_data
    driver2_data = st.session_state.driver2_data
    driver1_name = st.session_state.driver1_name
    driver2_name = st.session_state.driver2_name

    # Session info with data verification
    st.markdown(f"""
    <div class='session-header'>
        <div style='font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; color: #9b9b9b; letter-spacing: 0.08em; margin-bottom: 0.5rem;'>
            {driver1_data['year']} {driver1_data['gp']}
        </div>
        <div style='font-size: 1.25rem; font-weight: 700; color: #ffffff;'>
            {driver1_data['session_type']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Data quality warnings
    has_issues = False
    if driver1_data['data_issues'] or driver2_data['data_issues']:
        has_issues = True
        st.warning("**Data Quality Issues Detected:**")

        col1, col2 = st.columns(2)
        with col1:
            if driver1_data['data_issues']:
                st.markdown(f"**{driver1_name}:**")
                for issue in driver1_data['data_issues']:
                    st.markdown(f"- {issue}")

        with col2:
            if driver2_data['data_issues']:
                st.markdown(f"**{driver2_name}:**")
                for issue in driver2_data['data_issues']:
                    st.markdown(f"- {issue}")

        st.info("**Recommendation:** Try selecting a different session (Qualifying or Race) or different drivers for more complete data.")

    # Practice session warning
    if "Practice" in driver1_data['session_type']:
        st.info("""
        **About Practice Sessions:** Drivers run different programs and may not complete full push laps.
        For the most accurate comparisons, use **Qualifying** or **Race** sessions.
        """)

    # Calculate stats
    tel1 = driver1_data['telemetry']
    tel2 = driver2_data['telemetry']

    lap_time_1 = driver1_data['lap_time'].total_seconds()
    lap_time_2 = driver2_data['lap_time'].total_seconds()
    time_diff = abs(lap_time_1 - lap_time_2)
    faster_driver = driver1_name if lap_time_1 < lap_time_2 else driver2_name

    max_speed_1 = tel1['Speed'].max()
    max_speed_2 = tel2['Speed'].max()
    avg_speed_1 = tel1['Speed'].mean()
    avg_speed_2 = tel2['Speed'].mean()

    # Driver comparison cards
    col1, col2, col3 = st.columns([1, 0.3, 1])

    with col1:
        quality_class = "quality-warning" if driver1_data['data_issues'] else "quality-good"
        quality_text = "Data Issues" if driver1_data['data_issues'] else "Complete Data"

        st.markdown(f"""
        <div class='driver-card' style='--team-color: {TEAM_COLORS.get(driver1_data['team'], '#E10600')}'>
            <div class='driver-name'>{driver1_name}</div>
            <div class='team-badge'>{driver1_data['team']}</div>
            <div style='margin: 0.5rem 0;'>
                <span class='data-quality-badge {quality_class}'>{quality_text}</span>
            </div>
            <div class='lap-time'>{lap_time_1:.3f}</div>
            <div style='color: #9b9b9b; font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 2rem;'>
                LAP {driver1_data['lap_number']} TIME
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Max Speed", f"{max_speed_1:.0f} km/h")
        st.metric("Avg Speed", f"{avg_speed_1:.1f} km/h")
        st.metric("Tire", driver1_data['compound'])

    with col2:
        st.markdown("<div class='vs-divider'>VS</div>", unsafe_allow_html=True)

    with col3:
        quality_class = "quality-warning" if driver2_data['data_issues'] else "quality-good"
        quality_text = "Data Issues" if driver2_data['data_issues'] else "Complete Data"

        st.markdown(f"""
        <div class='driver-card' style='--team-color: {TEAM_COLORS.get(driver2_data['team'], '#E10600')}'>
            <div class='driver-name'>{driver2_name}</div>
            <div class='team-badge'>{driver2_data['team']}</div>
            <div style='margin: 0.5rem 0;'>
                <span class='data-quality-badge {quality_class}'>{quality_text}</span>
            </div>
            <div class='lap-time'>{lap_time_2:.3f}</div>
            <div style='color: #9b9b9b; font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 2rem;'>
                LAP {driver2_data['lap_number']} TIME
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Max Speed", f"{max_speed_2:.0f} km/h")
        st.metric("Avg Speed", f"{avg_speed_2:.1f} km/h")
        st.metric("Tire", driver2_data['compound'])

    # Winner badge
    st.markdown(f"""
    <div style='text-align: center; margin: 3rem 0 2rem 0;'>
        <div class='winner-badge'>
            Fastest Lap: {faster_driver} +{time_diff:.3f}s
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Charts
    st.markdown("<div class='section-header'>Speed Comparison</div>", unsafe_allow_html=True)
    speed_fig = create_speed_comparison(driver1_data, driver2_data, driver1_name, driver2_name)
    st.plotly_chart(speed_fig, width='stretch')

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Racing Line</div>", unsafe_allow_html=True)
        if driver1_data['data_issues'] or driver2_data['data_issues']:
            st.caption("⚠️ Track position data may be incomplete")
        track_fig = create_track_map(driver1_data, driver2_data, driver1_name, driver2_name)
        st.plotly_chart(track_fig, width='stretch')

    with col2:
        st.markdown("<div class='section-header'>Time Delta</div>", unsafe_allow_html=True)
        delta_fig = create_delta_time_plot(driver1_data, driver2_data, driver1_name, driver2_name)
        st.plotly_chart(delta_fig, width='stretch')

else:
    # Welcome screen
    st.markdown("""
    <div class='info-box'>
        <h3>Getting Started</h3>
        <ol style='color: #999999; line-height: 1.8;'>
            <li>Select a season, Grand Prix, and session type from the sidebar</li>
            <li>Click "Load Session" to fetch the data</li>
            <li>Choose two drivers to compare</li>
            <li>Click "Compare" to view the analysis</li>
        </ol>
        <p><strong>Best results:</strong> Use Qualifying or Race sessions for complete, comparable data.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>Speed Analysis</h3>
            <p>Compare speed profiles throughout the lap with precise telemetry data showing acceleration, braking, and top speed zones.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>Racing Lines</h3>
            <p>Visualize the exact trajectory both drivers took around the circuit to identify optimal racing lines and differences.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3>Time Delta</h3>
            <p>Analyze where time is gained and lost throughout the lap with precise sector-by-sector timing comparisons.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin: 4rem 0;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; color: #9b9b9b; font-size: 0.75rem; padding: 2rem 0;'>
    Unofficial application • Data provided by Fast-F1 • Not affiliated with Formula 1 or FIA
</div>
""", unsafe_allow_html=True)
