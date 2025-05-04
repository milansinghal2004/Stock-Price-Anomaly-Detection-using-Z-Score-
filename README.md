# Stock Price Predictor

A Python-based GUI application for predicting stock prices using historical data, forecasting future prices with the Prophet library, and detecting anomalies in stock price data. The application features an interactive interface built with Tkinter, including date pickers, result tables, and a zoomable/pannable plot for visualizing forecasts and anomalies.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Stock Price Forecasting**: Fetches historical stock data using `yfinance` and predicts future prices with the `Prophet` library.
- **Anomaly Detection**: Identifies unusual price movements in historical data using z-scores.
- **Interactive GUI**:
  - Input fields for stock ticker, start/end dates (with calendar pickers), and forecast period.
  - Displays forecast results (predicted price, confidence intervals) and anomalies in scrollable tables.
  - Interactive Matplotlib plot with zoom (mouse wheel) and pan (click-and-drag) functionality.
  - Tooltips for user guidance on input fields and plot.
- **Responsive Design**: Adapts to different window sizes with a clean, modern interface.
- **Error Handling**: Validates user inputs and provides user-friendly error messages for invalid tickers, dates, or data issues.

## Requirements
### Software
- **Python**: Version 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Internet Connection**: Required to fetch stock data via `yfinance`

### Python Libraries
- `tkinter`: For the GUI (usually included with Python)
- `pandas`: For data manipulation
- `yfinance`: For fetching stock data
- `prophet`: For time-series forecasting
- `matplotlib`: For plotting
- `tkcalendar`: For date picker widgets
- `scipy`: For anomaly detection
- `uuid`: For generating unique identifiers

## Installation
Follow these steps to set up the application on your system.

### Step 1: Install Python
Ensure Python 3.8 or higher is installed. Download it from [python.org](https://www.python.org/downloads/) if needed. Verify the installation by running:
```bash
python --version
```

### Step 2: Set Up a Virtual Environment (Recommended)
Create a virtual environment to manage dependencies:
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### Step 3: Install Dependencies
Install the required Python libraries using pip:
```bash
pip install pandas yfinance prophet matplotlib tkcalendar scipy
```

Alternatively, save the following as `requirements.txt`:
```
pandas
yfinance
prophet
matplotlib
tkcalendar
scipy
```
Then run:
```bash
pip install -r requirements.txt
```

### Step 4: Download the Code
Save the provided Python script as `stock_predictor.py`. Ensure it is in your working directory.

## Usage
Follow these steps to run and use the application.

### Step 1: Run the Application
With the virtual environment activated, run the script:
```bash
python stock_predictor.py
```

A GUI window titled "Stock Price Predictor" will appear.

### Step 2: Enter Input Parameters
1. **Stock Ticker**: Enter a valid stock ticker symbol (e.g., `NVDA` for NVIDIA, `AAPL` for Apple). Use uppercase letters.
2. **Start Date**: Select the start date for historical data using the calendar picker (default: 2020-01-01).
3. **End Date**: Select the end date for historical data (default: 2024-12-31). Must be on or before the current date (May 2, 2025, in the code).
4. **Forecast Period**: Choose the number of days to forecast (options: 30, 60, 90, 180, 365 days).

Hover over input fields for tooltips with guidance.

### Step 3: Generate Predictions
Click the **Predict Stock Price** button. The application will:
- Fetch historical stock data for the specified ticker and date range.
- Detect anomalies in the historical data (price movements with z-scores > 2).
- Forecast future prices using Prophet.
- Display results in two tables:
  - **Forecast Results**: Shows predicted prices, lower/upper confidence intervals, and dates for the forecast period.
  - **Detected Anomalies**: Lists dates, prices, and z-scores for anomalous price points.
- Render an interactive plot showing historical data, forecast, confidence intervals, and anomalies.

### Step 4: Interact with the Plot
- **Zoom**: Use the mouse wheel to zoom in/out, centered at the cursor position.
- **Pan**: Click and drag to move the plot horizontally or vertically.
- **View Details**: Hover over the plot for a tooltip about interaction options.

### Step 5: Review Results
- Scroll through the **Forecast Results** table to view predicted prices.
- Check the **Detected Anomalies** table for significant price outliers.
- Adjust inputs and click **Predict Stock Price** again to generate new predictions.

## Troubleshooting
- **Error: "No data found for the given ticker and date range"**
  - Ensure the ticker is valid (e.g., `NVDA`, not `nvidia`).
  - Check that the date range includes trading days and is not in the future (beyond May 2, 2025).
- **Error: "Please enter valid dates in YYYY-MM-DD format"**
  - Verify that the selected dates are in the correct format. Use the calendar picker to avoid manual entry errors.
- **Application Freezes During Prediction**
  - Large date ranges or long forecast periods may slow down the app. Try reducing the date range or forecast period.
  - Ensure a stable internet connection for data fetching.
- **Missing Library Errors**
  - Run `pip install` for any missing libraries (see [Installation](#installation)).
  - Ensure the virtual environment is activated.
- **Plot Interaction Issues**
  - If zooming/panning becomes unresponsive, try generating a new prediction to reset the plot.
  - Ensure no other applications are interfering with mouse events.

For additional help, check the console for detailed error messages or consult the library documentation:
- [yfinance](https://pypi.org/project/yfinance/)
- [Prophet](https://facebook.github.io/prophet/)
- [tkcalendar](https://pypi.org/project/tkcalendar/)

## Limitations
- **Data Availability**: Relies on `yfinance` for stock data, which may have delays, missing data, or restrictions for certain tickers.
- **Forecast Accuracy**: Prophet's predictions are based on historical trends and may not account for sudden market events or external factors.
- **Date Range**: The code enforces an end date on or before May 2, 2025, due to hardcoded logic. To use a more recent date, modify the `current_date` variable in `predict_stock` to `datetime.now()`.
- **Performance**: Long date ranges or forecast periods can cause delays, as the app processes data synchronously.
- **Plot Reset**: No built-in button to reset the plot to its original view after zooming/panning.
- **Dependency Management**: Users must manually install dependencies; no automated setup script is provided.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository (if hosted) or create a copy of the script.
2. Make improvements (e.g., add features, fix bugs, optimize performance).
3. Test changes thoroughly.
4. Submit a pull request or share the updated script with a description of changes.

Suggested improvements:
- Add a reset button for the plot.
- Implement asynchronous data fetching to improve UI responsiveness.
- Support exporting predictions or plots to files.
- Add more anomaly detection methods (e.g., moving averages).


---
*Milan Singhal*
