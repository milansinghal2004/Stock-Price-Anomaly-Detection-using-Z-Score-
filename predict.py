import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import yfinance as yf
from prophet import Prophet
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
from scipy.stats import zscore
import uuid

class StockPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Price Predictor")
        self.root.geometry("1200x900")
        self.root.minsize(800, 600)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', padding=10, font=('Helvetica', 12))
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TCombobox', font=('Helvetica', 12))
        self.style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))
        self.style.configure('Treeview', font=('Helvetica', 11), rowheight=25)

        # Define color scheme
        self.bg_color = "#f0f4f8"
        self.accent_color = "#007bff"
        self.text_color = "#333333"
        self.root.configure(bg=self.bg_color)

        # Main container
        self.container = ttk.Frame(self.root, padding="15", style='Custom.TFrame')
        self.container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Custom style for frame
        self.style.configure('Custom.TFrame', background=self.bg_color)

        # Input frame
        self.input_frame = ttk.LabelFrame(self.container, text="Input Parameters", padding=10)
        self.input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10, padx=10)
        self.input_frame.columnconfigure(1, weight=1)

        # Ticker input
        ttk.Label(self.input_frame, text="Stock Ticker (e.g., NVDA):", foreground=self.text_color).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.ticker_entry = ttk.Entry(self.input_frame)
        self.ticker_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.add_tooltip(self.ticker_entry, "Enter the stock ticker symbol (e.g., NVDA for NVIDIA)")

        # Date range inputs with calendar
        ttk.Label(self.input_frame, text="Start Date:", foreground=self.text_color).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.start_date_entry = DateEntry(self.input_frame, date_pattern='yyyy-mm-dd', 
                                        selectmode='day', year=2020, month=1, day=1,
                                        font=('Helvetica', 12))
        self.start_date_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.add_tooltip(self.start_date_entry, "Select the start date for historical data")

        ttk.Label(self.input_frame, text="End Date:", foreground=self.text_color).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.end_date_entry = DateEntry(self.input_frame, date_pattern='yyyy-mm-dd', 
                                       selectmode='day', year=2024, month=12, day=31,
                                       font=('Helvetica', 12))
        self.end_date_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.add_tooltip(self.end_date_entry, "Select the end date for historical data")

        # Forecast period dropdown
        ttk.Label(self.input_frame, text="Forecast Period (days):", foreground=self.text_color).grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.forecast_days = tk.StringVar(value="30")
        self.forecast_dropdown = ttk.Combobox(self.input_frame, textvariable=self.forecast_days, 
                                            values=["30", "60", "90", "180", "365"],
                                            font=('Helvetica', 12))
        self.forecast_dropdown.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.add_tooltip(self.forecast_dropdown, "Select the number of days to forecast")

        # Predict button
        self.predict_button = ttk.Button(self.input_frame, text="Predict Stock Price", command=self.predict_stock,
                                       style='Accent.TButton')
        self.predict_button.grid(row=4, column=0, columnspan=2, pady=15)
        self.style.configure('Accent.TButton', background=self.accent_color, foreground='white')
        self.add_tooltip(self.predict_button, "Click to generate stock price predictions")

        # Results frame (side by side layout for Forecast Results and Detected Anomalies)
        self.results_frame = ttk.Frame(self.container)
        self.results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=10)
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.columnconfigure(1, weight=1)
        self.results_frame.rowconfigure(1, weight=1)

        # Forecast Results area (left side)
        ttk.Label(self.results_frame, text="Forecast Results", font=('Helvetica', 14, 'bold'),
                 foreground=self.text_color).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.result_tree = ttk.Treeview(self.results_frame, columns=("Date", "Predicted", "Lower", "Upper"), 
                                      show="headings", height=8)
        self.result_tree.heading("Date", text="Date")
        self.result_tree.heading("Predicted", text="Predicted Price")
        self.result_tree.heading("Lower", text="Lower Bound")
        self.result_tree.heading("Upper", text="Upper Bound")
        self.result_tree.column("Date", width=150)
        self.result_tree.column("Predicted", width=150)
        self.result_tree.column("Lower", width=150)
        self.result_tree.column("Upper", width=150)
        self.result_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)

        # Scrollbar for Forecast Treeview
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        scrollbar.grid(row=1, column=0, sticky=(tk.E, tk.N, tk.S), pady=5, padx=(0, 5))
        self.result_tree.configure(yscrollcommand=scrollbar.set)

        # Anomalies area (right side)
        ttk.Label(self.results_frame, text="Detected Anomalies", font=('Helvetica', 14, 'bold'),
                 foreground=self.text_color).grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        self.anomaly_tree = ttk.Treeview(self.results_frame, columns=("Date", "Price", "Z-Score"), 
                                       show="headings", height=8)
        self.anomaly_tree.heading("Date", text="Date")
        self.anomaly_tree.heading("Price", text="Price")
        self.anomaly_tree.heading("Z-Score", text="Z-Score")
        self.anomaly_tree.column("Date", width=150)
        self.anomaly_tree.column("Price", width=150)
        self.anomaly_tree.column("Z-Score", width=150)
        self.anomaly_tree.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)

        # Scrollbar for Anomaly Treeview
        anomaly_scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.anomaly_tree.yview)
        anomaly_scrollbar.grid(row=1, column=1, sticky=(tk.E, tk.N, tk.S), pady=5, padx=(0, 5))
        self.anomaly_tree.configure(yscrollcommand=anomaly_scrollbar.set)

        # Plot frame
        self.plot_frame = ttk.Frame(self.container)
        self.plot_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=10)
        self.plot_frame.columnconfigure(0, weight=1)
        self.plot_frame.rowconfigure(0, weight=1)

        # Plot area
        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.add_tooltip(self.canvas.get_tk_widget(), "Scroll to zoom, click and drag to pan the graph")

        # Variables for panning
        self.pan_start = None
        self.original_limits = None  # To store original limits for reset

        # Bind mouse events for interactivity
        self.canvas.get_tk_widget().bind("<MouseWheel>", self.zoom)
        self.canvas.get_tk_widget().bind("<Button-1>", self.start_pan)
        self.canvas.get_tk_widget().bind("<B1-Motion>", self.pan)
        self.canvas.get_tk_widget().bind("<ButtonRelease-1>", self.end_pan)

        # Make the container responsive
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)
        self.container.rowconfigure(2, weight=1)

    def add_tooltip(self, widget, text):
        """Add a tooltip to a widget."""
        tooltip = tk.Toplevel(self.root)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+1000+1000")
        label = tk.Label(tooltip, text=text, background="#ffffe0", relief='solid', borderwidth=1,
                        font=('Helvetica', 10), padx=5, pady=3)
        label.pack()

        def show_tooltip(event):
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + 20
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def hide_tooltip(event):
            tooltip.withdraw()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
        tooltip.withdraw()

    def zoom(self, event):
        """Handle mouse wheel zoom in/out centered at the mouse position."""
        if not self.ax:
            return

        # Get current axis limits
        x_lim = self.ax.get_xlim()
        y_lim = self.ax.get_ylim()

        # Get mouse position in data coordinates
        x_data, y_data = self.ax.transData.inverted().transform((event.x, event.y))

        # Zoom factor (scroll up = zoom in, scroll down = zoom out)
        zoom_factor = 1.2 if event.delta < 0 else 1 / 1.2

        # Calculate new limits centered at the mouse position
        new_x_width = (x_lim[1] - x_lim[0]) * zoom_factor
        new_y_width = (y_lim[1] - y_lim[0]) * zoom_factor

        # Compute the proportion of the mouse position relative to the current limits
        x_ratio = (x_data - x_lim[0]) / (x_lim[1] - x_lim[0])
        y_ratio = (y_data - y_lim[0]) / (y_lim[1] - y_lim[0])

        # Set new limits
        new_x_min = x_data - new_x_width * x_ratio
        new_x_max = x_data + new_x_width * (1 - x_ratio)
        new_y_min = y_data - new_y_width * y_ratio
        new_y_max = y_data + new_y_width * (1 - y_ratio)

        self.ax.set_xlim(new_x_min, new_x_max)
        self.ax.set_ylim(new_y_min, new_y_max)

        self.canvas.draw()

    def start_pan(self, event):
        """Start panning by recording the initial mouse position."""
        self.pan_start = (event.x, event.y)

    def pan(self, event):
        """Handle panning by shifting the axis limits based on mouse movement."""
        if not self.pan_start:
            return

        # Get current axis limits
        x_lim = self.ax.get_xlim()
        y_lim = self.ax.get_ylim()

        # Calculate movement in pixels
        dx = event.x - self.pan_start[0]
        dy = event.y - self.pan_start[1]

        # Convert pixel movement to data coordinates
        transform = self.ax.transData.inverted()
        (x_data_start, y_data_start) = transform.transform(self.pan_start)
        (x_data_current, y_data_current) = transform.transform((event.x, event.y))
        dx_data = x_data_current - x_data_start
        dy_data = y_data_current - y_data_start

        # Update axis limits
        # Horizontal panning (left/right) remains the same
        self.ax.set_xlim(x_lim[0] - dx_data, x_lim[1] - dx_data)
        # Vertical panning (up/down) is reversed
        self.ax.set_ylim(y_lim[0] + dy_data, y_lim[1] + dy_data)

        self.canvas.draw()

        # Update pan start position
        self.pan_start = (event.x, event.y)

    def end_pan(self, event):
        """End panning by resetting the pan start position."""
        self.pan_start = None

    def validate_date(self, date_str):
        """Validate if the date string is in YYYY-MM-DD format."""
        date_str = date_str.strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def detect_anomalies(self, df):
        df['Z-Score'] = zscore(df['Close'])
        threshold = 2
        anomalies = df[abs(df['Z-Score']) > threshold]
        return anomalies

    def predict_stock(self):
        ticker = self.ticker_entry.get().strip().upper()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        forecast_days = int(self.forecast_days.get())

        # Debug: Print the raw date strings to inspect their format
        print(f"Raw Start Date: '{start_date}'")
        print(f"Raw End Date: '{end_date}'")

        # Normalize date strings: replace '/' with '-' to match expected format
        start_date = start_date.strip().replace("/", "-")
        end_date = end_date.strip().replace("/", "-")

        # Debug: Print the normalized date strings
        print(f"Normalized Start Date: '{start_date}'")
        print(f"Normalized End Date: '{end_date}'")

        # Input validation
        if not ticker:
            messagebox.showerror("Error", "Please enter a valid stock ticker.")
            return

        # Validate date format
        if not self.validate_date(start_date) or not self.validate_date(end_date):
            messagebox.showerror("Error", "Please enter valid dates in YYYY-MM-DD format.")
            return

        # Parse dates
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        # Check if start date is before end date
        if start_date_obj >= end_date_obj:
            messagebox.showerror("Error", "Start date must be before end date.")
            return

        # Check if end date is in the future (current date is May 02, 2025)
        current_date = datetime(2025, 5, 2)  # Hardcoded as per instructions
        if end_date_obj > current_date:
            messagebox.showerror("Error", "End date cannot be in the future. Please select a date on or before May 02, 2025.")
            return

        self.predict_button.config(state="disabled")
        self.root.config(cursor="wait")

        try:
            # Fetch stock data
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if df.empty:
                raise ValueError("No data found for the given ticker and date range.")
            df = df[['Close']].dropna()

            # Detect anomalies in historical data
            anomalies = self.detect_anomalies(df)

            # Prepare data for Prophet
            prophet_df = df[['Close']].reset_index()
            prophet_df.columns = ['ds', 'y']

            # Initialize and fit Prophet model
            model = Prophet(daily_seasonality=True)
            model.fit(prophet_df)

            # Create future dates
            future_dates = model.make_future_dataframe(periods=forecast_days)

            # Make predictions
            forecast = model.predict(future_dates)

            # Clear previous results
            for item in self.result_tree.get_children():
                self.result_tree.delete(item)
            for item in self.anomaly_tree.get_children():
                self.anomaly_tree.delete(item)

            # Display forecast results
            forecast_next = forecast.tail(forecast_days)
            for _, row in forecast_next.iterrows():
                self.result_tree.insert("", "end", values=(
                    row['ds'].strftime("%Y-%m-%d"),
                    f"${row['yhat']:.2f}",
                    f"${row['yhat_lower']:.2f}",
                    f"${row['yhat_upper']:.2f}"
                ))

            # Display detected anomalies
            for _, row in anomalies.iterrows():
                self.anomaly_tree.insert("", "end", values=(
                    row.name.strftime("%Y-%m-%d"),
                    f"${row['Close'].iloc[0]:.2f}",
                    f"{row['Z-Score'].iloc[0]:.2f}"
                ))

            # Plot the forecast and highlight anomalies
            self.ax.clear()
            self.ax.plot(prophet_df['ds'], prophet_df['y'], label='Historical Data', color='blue')
            self.ax.plot(forecast['ds'], forecast['yhat'], color='red', label='Forecast')
            self.ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], 
                                color='red', alpha=0.1, label='Confidence Interval')
            if not anomalies.empty:
                self.ax.scatter(anomalies.index, anomalies['Close'], color='green', label='Anomalies', zorder=5)
            self.ax.set_title(f'Stock Price Forecast for {ticker}', fontsize=14, pad=10)
            self.ax.set_xlabel('Date', fontsize=12)
            self.ax.set_ylabel('Price', fontsize=12)
            self.ax.legend()
            self.ax.tick_params(axis='x', rotation=45)
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch or predict stock data: {str(e)}")
        finally:
            self.predict_button.config(state="normal")
            self.root.config(cursor="")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockPredictorApp(root)
    root.mainloop()