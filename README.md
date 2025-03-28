# Air Quality Index Dashboard 🌬️<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" alt="Description of the GIF" />
A comprehensive Streamlit-based Air Quality Index (AQI) application that provides real-time environmental health insights using OpenWeatherMap data.

## Features

- 📊 Real-time AQI data visualization
- 🌍 Global location support
- 📈 Interactive pollutant tracking
- 🎨 Responsive design with smooth transitions
- 🎯 Color-coded AQI category representation
- 📱 Mobile-friendly interface

## Technologies Used

- Python 3.11
- Streamlit
- Plotly
- OpenWeatherMap API
- Pandas
- NumPy

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repo-url>
cd aqi-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Create a `.env` file in the root directory
- Add your OpenWeatherMap API key:
```
OPENWEATHERMAP_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter a city name in the search box
2. View real-time AQI data and pollutant levels
3. Check historical trends using the time range selector
4. Read health recommendations based on current AQI

## Project Structure <img src="https://user-images.githubusercontent.com/74038190/212284087-bbe7e430-757e-4901-90bf-4cd2ce3e1852.gif" style="width: 44px; height: auto;" />


```
├── app.py               # Main Streamlit application
├── api_client.py        # OpenWeatherMap API client
├── aqi_calculator.py    # AQI calculation logic
├── utils.py            # Utility functions
├── .streamlit/         # Streamlit configuration
└── README.md           # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
