# 🏎️ F1 Telemetry Battle

A Streamlit web application that allows you to compare telemetry data between two F1 drivers from any race. Analyze speed, racing lines, and lap time deltas using real F1 timing data from the Fast-F1 package.

![F1 Telemetry Battle](https://img.shields.io/badge/F1-Telemetry%20Battle-red?style=for-the-badge&logo=formula-1)

## Features

- **Compare Any Two Drivers** from F1 races (2018-2024)
- **Speed Comparison Chart**: See how drivers' speeds differ throughout the lap
- **Track Map Visualization**: View racing lines overlaid on the circuit layout
- **Delta Time Plot**: Analyze where drivers gain or lose time
- **Summary Statistics**: Lap times, max speeds, average speeds, and tire compounds
- **Interactive Visualizations**: Powered by Plotly for smooth, responsive charts
- **Real F1 Data**: Accurate telemetry from Fast-F1

## Demo

![Demo Screenshot Placeholder](https://via.placeholder.com/800x400.png?text=Demo+Screenshot+Coming+Soon)

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/f1-telemetry-battle.git
   cd f1-telemetry-battle
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   The app should automatically open at `http://localhost:8501`

## Usage

1. **Select Year**: Choose an F1 season (2018-2024)
2. **Select Grand Prix**: Pick a race from the selected season
3. **Select Session Type**: Choose Race, Qualifying, Sprint, or Practice
4. **Load Session**: Click "Load Session" to fetch the data
5. **Select Drivers**: Choose two drivers to compare
6. **Compare**: Click "Compare Drivers" to generate the analysis

The app will display:
- Lap time and speed statistics for both drivers
- Speed comparison chart throughout the lap
- Track map showing both drivers' racing lines
- Delta time plot showing time gained/lost at each point

## Deploy to Streamlit Cloud

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://share.streamlit.io)
3. Create a new app and connect it to your forked repository
4. Deploy! (Streamlit will automatically detect `app.py`)

## Technologies Used

- **[Streamlit](https://streamlit.io/)**: Web application framework
- **[Fast-F1](https://github.com/theOehrly/Fast-F1)**: F1 timing and telemetry data
- **[Plotly](https://plotly.com/)**: Interactive visualizations
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation
- **[NumPy](https://numpy.org/)**: Numerical computing

## Data Source

All F1 data is provided by the [Fast-F1](https://github.com/theOehrly/Fast-F1) Python package, which retrieves official F1 timing data from the Formula 1 live timing service.

## Project Structure

```
f1-telemetry-battle/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
└── cache/                # Fast-F1 cache directory (auto-created)
```

## Known Limitations

- Telemetry data is not available for all sessions before 2018
- Some practice sessions may have limited or no telemetry data
- Data loading can take 10-30 seconds for the first request (cached afterwards)
- Track position data (X/Y coordinates) may not be available for older races

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Disclaimer

This is an unofficial application and is not affiliated with, endorsed by, or connected to Formula 1, the FIA, or any F1 teams. All F1-related trademarks are property of Formula One Licensing BV.

## Credits

- **Fast-F1 Package**: [theOehrly/Fast-F1](https://github.com/theOehrly/Fast-F1)
- **Data Source**: Formula 1 via Fast-F1
- **Built with**: Streamlit, Plotly, Python

## Acknowledgments

Special thanks to the Fast-F1 development team for providing easy access to F1 timing and telemetry data.

---

**Made with ❤️ for F1 fans and data enthusiasts**