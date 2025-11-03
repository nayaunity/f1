import streamlit as st
import fastf1
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Enable Fast-F1 caching
fastf1.Cache.enable_cache('cache')

# Page configuration
st.set_page_config(
    page_title="F1 Telemetry Battle",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main {
        background: #000000;
        color: #ffffff;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }

    ::-webkit-scrollbar-thumb {
        background: #e10600;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #ff0800;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
    }

    /* Remove default borders */
    h1, h2, h3 {
        border: none !important;
        padding-bottom: 0 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
        border-right: 1px solid #1a1a1a;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #999999;
        font-size: 0.875rem;
        font-weight: 500;
    }

    /* Selectbox styling */
    .stSelectbox label {
        color: #666666 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.5rem !important;
    }

    .stSelectbox > div > div {
        background-color: #0a0a0a !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 6px !important;
        color: #ffffff !important;
    }

    .stSelectbox > div > div:hover {
        border-color: #e10600 !important;
    }

    .stSelectbox > div > div:focus-within {
        border-color: #e10600 !important;
        box-shadow: 0 0 0 1px #e10600 !important;
    }

    /* Button styling */
    .stButton > button {
        background: #e10600;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.01em;
        transition: all 0.2s ease;
        width: 100%;
    }

    .stButton > button:hover {
        background: #ff0800;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(225, 6, 0, 0.3);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Metrics */
    [data-testid="stMetricLabel"] {
        color: #666666 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.875rem !important;
        font-weight: 700 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
    }

    /* Cards */
    .metric-card {
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        border-radius: 8px;
        padding: 1.5rem;
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        border-color: #2a2a2a;
        background: #0f0f0f;
    }

    .session-header {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 1.5rem 2rem;
        margin: 2rem 0;
    }

    .driver-card {
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        border-radius: 8px;
        padding: 2rem 1.5rem;
        height: 100%;
    }

    .winner-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #000000;
        padding: 0.5rem 1.5rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.875rem;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }

    .vs-divider {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        font-size: 3rem;
        font-weight: 900;
        color: #e10600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.1em;
    }

    /* Section headers */
    .section-header {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #666666;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #1a1a1a;
    }

    /* Team badge */
    .team-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: #1a1a1a;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #999999;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #1a1a1a 50%, transparent 100%);
        margin: 2rem 0;
    }

    /* Info box */
    .info-box {
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        border-left: 3px solid #e10600;
        border-radius: 6px;
        padding: 1.5rem;
        margin: 2rem 0;
    }

    .info-box h3 {
        margin: 0 0 1rem 0;
        font-size: 1.125rem;
        font-weight: 600;
    }

    .info-box p, .info-box ol {
        color: #999999;
        line-height: 1.6;
    }

    /* Feature card */
    .feature-card {
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        border-radius: 8px;
        padding: 2rem;
        height: 100%;
        transition: all 0.2s ease;
    }

    .feature-card:hover {
        border-color: #2a2a2a;
        transform: translateY(-2px);
    }

    .feature-card h3 {
        font-size: 1rem;
        margin: 0 0 0.75rem 0;
        color: #ffffff;
    }

    .feature-card p {
        color: #999999;
        font-size: 0.875rem;
        line-height: 1.6;
        margin: 0;
    }

    /* Spinner */
    .stSpinner > div {
        border-color: #e10600 !important;
    }

    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(0, 255, 0, 0.1) !important;
        border: 1px solid rgba(0, 255, 0, 0.3) !important;
        border-radius: 6px !important;
        color: #00ff00 !important;
    }

    .stError {
        background-color: rgba(255, 0, 0, 0.1) !important;
        border: 1px solid rgba(255, 0, 0, 0.3) !important;
        border-radius: 6px !important;
        color: #ff0000 !important;
    }

    /* Title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #ffffff 0%, #999999 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .main-subtitle {
        font-size: 1rem;
        font-weight: 500;
        color: #666666;
        letter-spacing: 0.02em;
        margin-bottom: 2rem;
    }

    /* Driver name styling */
    .driver-name {
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    /* Lap time display */
    .lap-time {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 1rem 0;
    }

    .time-advantage {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.25rem;
        font-weight: 600;
        color: #e10600;
    }
</style>
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
def get_driver_telemetry(_session, driver_code):
    """Get fastest lap telemetry for a specific driver."""
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

        return {
            'telemetry': telemetry,
            'lap_time': fastest_lap['LapTime'],
            'driver': fastest_lap['Driver'],
            'team': fastest_lap['Team'],
            'compound': fastest_lap.get('Compound', 'Unknown')
        }, None
    except Exception as e:
        return None, f"Error loading telemetry for {driver_code}: {str(e)}"


def create_speed_comparison(driver1_data, driver2_data, driver1_name, driver2_name):
    """Create professional speed comparison chart."""
    fig = go.Figure()

    color1 = TEAM_COLORS.get(driver1_data['team'], '#FF0000')
    color2 = TEAM_COLORS.get(driver2_data['team'], '#0000FF')

    # Driver 1 line
    fig.add_trace(go.Scatter(
        x=driver1_data['telemetry']['Distance'],
        y=driver1_data['telemetry']['Speed'],
        mode='lines',
        name=driver1_name,
        line=dict(color=color1, width=3),
        hovertemplate='<b>%{fullData.name}</b><br>Distance: %{x:.0f}m<br>Speed: %{y:.0f} km/h<extra></extra>'
    ))

    # Driver 2 line
    fig.add_trace(go.Scatter(
        x=driver2_data['telemetry']['Distance'],
        y=driver2_data['telemetry']['Speed'],
        mode='lines',
        name=driver2_name,
        line=dict(color=color2, width=3),
        hovertemplate='<b>%{fullData.name}</b><br>Distance: %{x:.0f}m<br>Speed: %{y:.0f} km/h<extra></extra>'
    ))

    fig.update_layout(
        title=None,
        xaxis_title="Distance (m)",
        yaxis_title="Speed (km/h)",
        hovermode='x unified',
        height=500,
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#999999', size=11, family='Inter'),
        margin=dict(l=60, r=40, t=40, b=60),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.08,
            xanchor="left",
            x=0,
            font=dict(size=12, color='#ffffff'),
            bgcolor='rgba(0,0,0,0)'
        ),
        xaxis=dict(
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor='#1a1a1a'
        ),
        yaxis=dict(
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor='#1a1a1a'
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

    # Driver 1 racing line
    fig.add_trace(go.Scatter(
        x=tel1['X'],
        y=tel1['Y'],
        mode='lines',
        name=driver1_name,
        line=dict(color=color1, width=4),
        hovertemplate='<b>%{fullData.name}</b><br>Speed: ' + tel1['Speed'].astype(str) + ' km/h<extra></extra>'
    ))

    # Driver 2 racing line
    fig.add_trace(go.Scatter(
        x=tel2['X'],
        y=tel2['Y'],
        mode='lines',
        name=driver2_name,
        line=dict(color=color2, width=4),
        hovertemplate='<b>%{fullData.name}</b><br>Speed: ' + tel2['Speed'].astype(str) + ' km/h<extra></extra>'
    ))

    fig.update_layout(
        title=None,
        xaxis_title="X Position (m)",
        yaxis_title="Y Position (m)",
        height=600,
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        showlegend=True,
        font=dict(color='#999999', size=11, family='Inter'),
        margin=dict(l=60, r=40, t=40, b=60),
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor='#1a1a1a'
        ),
        xaxis=dict(
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor='#1a1a1a'
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.08,
            xanchor="left",
            x=0,
            font=dict(size=12, color='#ffffff'),
            bgcolor='rgba(0,0,0,0)'
        )
    )

    return fig


def create_delta_time_plot(driver1_data, driver2_data, driver1_name, driver2_name):
    """Create professional delta time plot."""
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

    # Create color array based on delta
    colors = [color1 if d > 0 else color2 for d in delta]

    # Add delta line
    fig.add_trace(go.Scatter(
        x=common_distance,
        y=delta,
        mode='lines',
        name='Time Delta',
        line=dict(color='#ffffff', width=2),
        fill='tozeroy',
        fillcolor='rgba(255, 255, 255, 0.05)',
        hovertemplate='Distance: %{x:.0f}m<br>Delta: %{y:.3f}s<extra></extra>'
    ))

    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="#666666",
        line_width=1
    )

    fig.update_layout(
        title=None,
        xaxis_title="Distance (m)",
        yaxis_title="Time Delta (s)",
        height=600,
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        hovermode='x',
        font=dict(color='#999999', size=11, family='Inter'),
        margin=dict(l=60, r=40, t=40, b=60),
        xaxis=dict(
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor='#1a1a1a'
        ),
        yaxis=dict(
            gridcolor='#1a1a1a',
            showgrid=True,
            zeroline=True,
            zerolinecolor='#666666',
            zerolinewidth=1,
            showline=True,
            linewidth=1,
            linecolor='#1a1a1a'
        ),
        annotations=[
            dict(
                text=f"{driver1_name} slower",
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                showarrow=False,
                font=dict(size=10, color='#666666'),
                bgcolor='rgba(0, 0, 0, 0.8)',
                borderpad=8
            ),
            dict(
                text=f"{driver2_name} slower",
                xref="paper", yref="paper",
                x=0.02, y=0.02,
                showarrow=False,
                font=dict(size=10, color='#666666'),
                bgcolor='rgba(0, 0, 0, 0.8)',
                borderpad=8
            )
        ]
    )

    return fig


# Main App Layout
st.markdown("<div class='main-title'>F1 Telemetry Battle</div>", unsafe_allow_html=True)
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
        options=["Race", "Qualifying", "Sprint", "Practice 1", "Practice 2", "Practice 3"],
        index=0
    )

    st.markdown("")

    if st.button("Load Session"):
        if gp:
            with st.spinner("Loading session data..."):
                session, error = load_session(year, gp, session_type)
                if error:
                    st.error(f"Error: {error}")
                    st.session_state.session = None
                else:
                    st.session_state.session = session
                    st.session_state.year = year
                    st.session_state.gp = gp
                    st.session_state.session_type = session_type
                    st.success("Session loaded")
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

        if st.button("Compare"):
            if driver1 == driver2:
                st.error("Select two different drivers")
            else:
                with st.spinner("Loading telemetry..."):
                    driver1_data, error1 = get_driver_telemetry(session, driver1)
                    driver2_data, error2 = get_driver_telemetry(session, driver2)

                    if error1:
                        st.error(f"Error: {error1}")
                    elif error2:
                        st.error(f"Error: {error2}")
                    else:
                        st.session_state.driver1_data = driver1_data
                        st.session_state.driver2_data = driver2_data
                        st.session_state.driver1_name = driver1
                        st.session_state.driver2_name = driver2
                        st.success("Ready")
                        st.rerun()

# Main content
if all(key in st.session_state for key in ['driver1_data', 'driver2_data']):
    driver1_data = st.session_state.driver1_data
    driver2_data = st.session_state.driver2_data
    driver1_name = st.session_state.driver1_name
    driver2_name = st.session_state.driver2_name

    # Session info
    st.markdown(f"""
    <div class='session-header'>
        <div style='font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #666666; letter-spacing: 0.05em; margin-bottom: 0.5rem;'>
            {st.session_state.year} {st.session_state.gp}
        </div>
        <div style='font-size: 1.125rem; font-weight: 600; color: #ffffff;'>
            {st.session_state.session_type}
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    # Winner announcement
    col1, col2, col3 = st.columns([1, 0.3, 1])

    with col1:
        st.markdown(f"""
        <div class='driver-card' style='border-left: 3px solid {TEAM_COLORS.get(driver1_data['team'], '#FF0000')}'>
            <div class='driver-name'>{driver1_name}</div>
            <div class='team-badge'>{driver1_data['team']}</div>
            <div class='lap-time'>{lap_time_1:.3f}</div>
            <div style='color: #666666; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 2rem;'>LAP TIME</div>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Max Speed", f"{max_speed_1:.0f} km/h")
        st.metric("Avg Speed", f"{avg_speed_1:.1f} km/h")
        st.metric("Tire", driver1_data['compound'])

    with col2:
        st.markdown("<div class='vs-divider'>VS</div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='driver-card' style='border-left: 3px solid {TEAM_COLORS.get(driver2_data['team'], '#0000FF')}'>
            <div class='driver-name'>{driver2_name}</div>
            <div class='team-badge'>{driver2_data['team']}</div>
            <div class='lap-time'>{lap_time_2:.3f}</div>
            <div style='color: #666666; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 2rem;'>LAP TIME</div>
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
    st.plotly_chart(speed_fig, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Racing Line</div>", unsafe_allow_html=True)
        track_fig = create_track_map(driver1_data, driver2_data, driver1_name, driver2_name)
        st.plotly_chart(track_fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Time Delta</div>", unsafe_allow_html=True)
        delta_fig = create_delta_time_plot(driver1_data, driver2_data, driver1_name, driver2_name)
        st.plotly_chart(delta_fig, use_container_width=True)

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
<div style='text-align: center; color: #333333; font-size: 0.75rem; padding: 2rem 0;'>
    Unofficial application • Data provided by Fast-F1 • Not affiliated with Formula 1 or FIA
</div>
""", unsafe_allow_html=True)
