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
    layout="wide"
)

# Title and description
st.title("🏎️ F1 Telemetry Battle")
st.markdown("""
Compare telemetry data between two F1 drivers from any race.
Select a year, Grand Prix, session, and two drivers to analyze their performance lap by lap.
""")

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
    """Create speed comparison chart."""
    fig = go.Figure()

    # Get team colors
    color1 = TEAM_COLORS.get(driver1_data['team'], '#FF0000')
    color2 = TEAM_COLORS.get(driver2_data['team'], '#0000FF')

    # Add traces for each driver
    fig.add_trace(go.Scatter(
        x=driver1_data['telemetry']['Distance'],
        y=driver1_data['telemetry']['Speed'],
        mode='lines',
        name=f"{driver1_name} ({driver1_data['team']})",
        line=dict(color=color1, width=2),
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Distance: %{x:.0f}m<br>' +
                      'Speed: %{y:.0f} km/h<br>' +
                      '<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=driver2_data['telemetry']['Distance'],
        y=driver2_data['telemetry']['Speed'],
        mode='lines',
        name=f"{driver2_name} ({driver2_data['team']})",
        line=dict(color=color2, width=2),
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Distance: %{x:.0f}m<br>' +
                      'Speed: %{y:.0f} km/h<br>' +
                      '<extra></extra>'
    ))

    fig.update_layout(
        title="Speed Comparison - Fastest Lap",
        xaxis_title="Distance (meters)",
        yaxis_title="Speed (km/h)",
        hovermode='x unified',
        height=500,
        template='plotly_dark'
    )

    return fig


def create_track_map(driver1_data, driver2_data, driver1_name, driver2_name):
    """Create track map visualization with racing lines colored by speed."""
    fig = go.Figure()

    # Driver 1 racing line
    tel1 = driver1_data['telemetry']
    color1 = TEAM_COLORS.get(driver1_data['team'], '#FF0000')

    fig.add_trace(go.Scatter(
        x=tel1['X'],
        y=tel1['Y'],
        mode='lines',
        name=f"{driver1_name}",
        line=dict(color=color1, width=4),
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Speed: ' + tel1['Speed'].astype(str) + ' km/h<br>' +
                      '<extra></extra>'
    ))

    # Driver 2 racing line
    tel2 = driver2_data['telemetry']
    color2 = TEAM_COLORS.get(driver2_data['team'], '#0000FF')

    fig.add_trace(go.Scatter(
        x=tel2['X'],
        y=tel2['Y'],
        mode='lines',
        name=f"{driver2_name}",
        line=dict(color=color2, width=4),
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Speed: ' + tel2['Speed'].astype(str) + ' km/h<br>' +
                      '<extra></extra>'
    ))

    fig.update_layout(
        title="Track Map - Racing Lines",
        xaxis_title="X Position (meters)",
        yaxis_title="Y Position (meters)",
        height=600,
        template='plotly_dark',
        showlegend=True,
        yaxis=dict(scaleanchor="x", scaleratio=1)
    )

    return fig


def create_delta_time_plot(driver1_data, driver2_data, driver1_name, driver2_name):
    """Create delta time plot showing time difference across the lap."""
    tel1 = driver1_data['telemetry']
    tel2 = driver2_data['telemetry']

    # Interpolate telemetry to same distance points
    min_distance = max(tel1['Distance'].min(), tel2['Distance'].min())
    max_distance = min(tel1['Distance'].max(), tel2['Distance'].max())

    # Create common distance array
    common_distance = np.linspace(min_distance, max_distance, 1000)

    # Convert Time to seconds (from timedelta)
    time1_seconds = tel1['Time'].dt.total_seconds()
    time2_seconds = tel2['Time'].dt.total_seconds()

    # Interpolate time for both drivers
    time1 = np.interp(common_distance, tel1['Distance'], time1_seconds)
    time2 = np.interp(common_distance, tel2['Distance'], time2_seconds)

    # Calculate delta (positive means driver1 is ahead in time/slower)
    delta = time1 - time2

    # Create figure
    fig = go.Figure()

    # Add delta line
    color1 = TEAM_COLORS.get(driver1_data['team'], '#FF0000')
    color2 = TEAM_COLORS.get(driver2_data['team'], '#0000FF')

    fig.add_trace(go.Scatter(
        x=common_distance,
        y=delta,
        mode='lines',
        name='Time Delta',
        line=dict(color='white', width=2),
        fill='tozeroy',
        fillcolor='rgba(255, 255, 255, 0.2)',
        hovertemplate='Distance: %{x:.0f}m<br>' +
                      'Delta: %{y:.3f}s<br>' +
                      '<extra></extra>'
    ))

    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_layout(
        title=f"Delta Time: {driver1_name} vs {driver2_name}",
        xaxis_title="Distance (meters)",
        yaxis_title=f"Time Delta (seconds)<br>Positive = {driver1_name} slower | Negative = {driver2_name} slower",
        height=400,
        template='plotly_dark',
        hovermode='x'
    )

    return fig


def display_summary_stats(driver1_data, driver2_data, driver1_name, driver2_name):
    """Display summary statistics for both drivers."""
    col1, col2, col3 = st.columns(3)

    # Calculate statistics
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

    # Display metrics
    with col1:
        st.metric(
            label=f"{driver1_name} Lap Time",
            value=f"{lap_time_1:.3f}s",
            delta=f"{-time_diff:.3f}s" if lap_time_1 < lap_time_2 else f"+{time_diff:.3f}s"
        )
        st.metric(
            label=f"{driver1_name} Max Speed",
            value=f"{max_speed_1:.0f} km/h"
        )
        st.metric(
            label=f"{driver1_name} Avg Speed",
            value=f"{avg_speed_1:.0f} km/h"
        )

    with col2:
        st.metric(
            label=f"{driver2_name} Lap Time",
            value=f"{lap_time_2:.3f}s",
            delta=f"{-time_diff:.3f}s" if lap_time_2 < lap_time_1 else f"+{time_diff:.3f}s"
        )
        st.metric(
            label=f"{driver2_name} Max Speed",
            value=f"{max_speed_2:.0f} km/h"
        )
        st.metric(
            label=f"{driver2_name} Avg Speed",
            value=f"{avg_speed_2:.0f} km/h"
        )

    with col3:
        st.metric(
            label="Faster Driver",
            value=faster_driver,
            delta=f"{time_diff:.3f}s advantage"
        )
        st.metric(
            label="Speed Difference (Max)",
            value=f"{abs(max_speed_1 - max_speed_2):.0f} km/h"
        )
        st.metric(
            label="Tire Compound",
            value=f"{driver1_data['compound']} vs {driver2_data['compound']}"
        )


# Sidebar - Data Selection Interface
st.sidebar.header("Select Data")

# Year selector
current_year = datetime.now().year
year = st.sidebar.selectbox(
    "Year",
    options=list(range(2024, 2017, -1)),
    index=0
)

# Get available events for the selected year
try:
    schedule = fastf1.get_event_schedule(year)
    # Filter to only past events or current year events
    available_events = schedule[schedule['EventName'].notna()]['EventName'].tolist()
    event_names = [event for event in available_events if event]
except Exception as e:
    st.sidebar.error(f"Error loading schedule: {e}")
    available_events = []
    event_names = []

# Grand Prix selector
if event_names:
    gp = st.sidebar.selectbox(
        "Grand Prix",
        options=event_names,
        index=0
    )
else:
    st.sidebar.warning("No events available for selected year")
    gp = None

# Session type selector
session_type = st.sidebar.selectbox(
    "Session Type",
    options=["Race", "Qualifying", "Sprint", "Practice 1", "Practice 2", "Practice 3"],
    index=0
)

# Load session button
if st.sidebar.button("Load Session", type="primary"):
    if gp:
        with st.spinner(f"Loading {year} {gp} {session_type}..."):
            session, error = load_session(year, gp, session_type)

            if error:
                st.error(f"Error loading session: {error}")
                st.session_state.session = None
            else:
                st.session_state.session = session
                st.session_state.year = year
                st.session_state.gp = gp
                st.session_state.session_type = session_type
                st.sidebar.success("Session loaded successfully!")
    else:
        st.sidebar.warning("Please select a Grand Prix")

# Driver selection (only show if session is loaded)
if 'session' in st.session_state and st.session_state.session is not None:
    session = st.session_state.session

    # Get list of drivers
    drivers = session.laps['Driver'].unique().tolist()
    drivers.sort()

    st.sidebar.subheader("Select Drivers to Compare")

    driver1 = st.sidebar.selectbox(
        "Driver 1",
        options=drivers,
        index=0 if len(drivers) > 0 else None
    )

    driver2 = st.sidebar.selectbox(
        "Driver 2",
        options=drivers,
        index=1 if len(drivers) > 1 else 0
    )

    # Compare button
    if st.sidebar.button("Compare Drivers", type="primary"):
        if driver1 == driver2:
            st.error("Please select two different drivers")
        else:
            with st.spinner(f"Loading telemetry data for {driver1} and {driver2}..."):
                # Load telemetry for both drivers
                driver1_data, error1 = get_driver_telemetry(session, driver1)
                driver2_data, error2 = get_driver_telemetry(session, driver2)

                if error1:
                    st.error(f"Error loading {driver1}: {error1}")
                elif error2:
                    st.error(f"Error loading {driver2}: {error2}")
                else:
                    st.session_state.driver1_data = driver1_data
                    st.session_state.driver2_data = driver2_data
                    st.session_state.driver1_name = driver1
                    st.session_state.driver2_name = driver2
                    st.sidebar.success("Telemetry loaded successfully!")

# Display visualizations if data is loaded
if all(key in st.session_state for key in ['driver1_data', 'driver2_data']):
    driver1_data = st.session_state.driver1_data
    driver2_data = st.session_state.driver2_data
    driver1_name = st.session_state.driver1_name
    driver2_name = st.session_state.driver2_name

    # Display session info
    st.subheader(f"{st.session_state.year} {st.session_state.gp} - {st.session_state.session_type}")
    st.markdown(f"**Comparing:** {driver1_name} ({driver1_data['team']}) vs {driver2_name} ({driver2_data['team']})")

    # Summary statistics
    st.markdown("---")
    st.subheader("Summary Statistics")
    display_summary_stats(driver1_data, driver2_data, driver1_name, driver2_name)

    # Visualizations
    st.markdown("---")
    st.subheader("Telemetry Analysis")

    # Speed comparison
    with st.spinner("Creating speed comparison chart..."):
        speed_fig = create_speed_comparison(driver1_data, driver2_data, driver1_name, driver2_name)
        st.plotly_chart(speed_fig, use_container_width=True)

    # Track map and delta time side by side
    col1, col2 = st.columns([1, 1])

    with col1:
        with st.spinner("Creating track map..."):
            track_fig = create_track_map(driver1_data, driver2_data, driver1_name, driver2_name)
            st.plotly_chart(track_fig, use_container_width=True)

    with col2:
        with st.spinner("Creating delta time plot..."):
            delta_fig = create_delta_time_plot(driver1_data, driver2_data, driver1_name, driver2_name)
            st.plotly_chart(delta_fig, use_container_width=True)

else:
    # Show instructions if no data loaded
    st.info("👈 Use the sidebar to select a year, Grand Prix, and session, then click 'Load Session' to begin.")

    # Show example
    with st.expander("How to use this app"):
        st.markdown("""
        1. **Select Year:** Choose a season from 2018-2024
        2. **Select Grand Prix:** Pick a race from that season
        3. **Select Session Type:** Choose Race, Qualifying, or Practice
        4. **Load Session:** Click the button to load the session data
        5. **Select Drivers:** Choose two drivers to compare
        6. **Compare:** Click 'Compare Drivers' to see the analysis

        The app will display:
        - Lap time and speed statistics
        - Speed comparison throughout the lap
        - Track map with racing lines
        - Delta time plot showing where time is gained/lost
        """)

# Footer
st.markdown("---")
st.caption("Unofficial app. Data provided by Fast-F1. This app is not affiliated with Formula 1 or the FIA.")
