import yfinance as yf
import pandas as pd
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import numpy as np


def calculate_bollinger_bands(ticker):
    # Fetch data from Yahoo Finance
    data = yf.download(ticker, period='1y')

    # Calculate Bollinger Bands
    data['SMA'] = data['Close'].rolling(window=20).mean()
    data['STD'] = data['Close'].rolling(window=20).std()
    data['Upper'] = data['SMA'] + 2 * data['STD']
    data['Lower'] = data['SMA'] - 2 * data['STD']

    # Identify buy and sell positions
    data['Buy'] = data['Close'] > data['Upper']
    data['Sell'] = data['Close'] < data['Lower']

    return data


def calculate_head_and_shoulders(ticker):
    # Fetch data from Yahoo Finance
    data = yf.download(ticker, period='1y')

    # Find potential head and shoulders pattern
    pattern = np.where(
        (data['Close'].shift(-2) < data['Close'].shift(-1)) &
        (data['Close'].shift(-2) < data['Close']) &
        (data['Close'].shift(2) < data['Close'].shift(1)) &
        (data['Close'].shift(2) < data['Close'])
    )

    return data, pattern


def calculate_double_top_and_bottom(ticker):
    # Fetch data from Yahoo Finance
    data = yf.download(ticker, period='1y')

    # Find potential double top and double bottom patterns
    double_top_pattern = np.where(
        (data['High'].shift(-1) < data['High']) &
        (data['High'].shift(1) < data['High']) &
        (data['Low'].shift(-1) > data['Low']) &
        (data['Low'].shift(1) > data['Low'])
    )

    double_bottom_pattern = np.where(
        (data['High'].shift(-1) < data['High']) &
        (data['High'].shift(1) < data['High']) &
        (data['Low'].shift(-1) > data['Low']) &
        (data['Low'].shift(1) > data['Low'])
    )

    return data, double_top_pattern, double_bottom_pattern


def calculate_triangles(ticker):
    # Fetch data from Yahoo Finance
    data = yf.download(ticker, period='1y')

    # Find potential ascending, descending, and symmetrical triangles
    ascending_triangle = np.where(
        (data['High'].shift(-2) < data['High'].shift(-1)) &
        (data['High'].shift(-2) < data['High']) &
        (data['Low'].shift(-2) < data['Low'].shift(-1)) &
        (data['Low'].shift(-2) < data['Low'])
    )

    descending_triangle = np.where(
        (data['High'].shift(-2) > data['High'].shift(-1)) &
        (data['High'].shift(-2) > data['High']) &
        (data['Low'].shift(-2) > data['Low'].shift(-1)) &
        (data['Low'].shift(-2) > data['Low'])
    )

    symmetrical_triangle = np.where(
        ((data['High'].shift(-2) < data['High'].shift(-1)) & (data['High'].shift(-2) < data['High']) &
         (data['Low'].shift(-2) > data['Low'].shift(-1)) & (data['Low'].shift(-2) < data['Low'])) |
        ((data['High'].shift(-2) > data['High'].shift(-1)) & (data['High'].shift(-2) > data['High']) &
         (data['Low'].shift(-2) < data['Low'].shift(-1)) & (data['Low'].shift(-2) > data['Low']))
    )

    return data, ascending_triangle, descending_triangle, symmetrical_triangle


def calculate_flags_and_pennants(ticker):
    # Fetch data from Yahoo Finance
    data = yf.download(ticker, period='1y')

    # Find potential flag and pennant patterns
    flags = np.where(
        (data['Close'].shift(-1) > data['Close']) &
        (data['Close'].shift(1) > data['Close']) &
        (data['High'].shift(-1) > data['High']) &
        (data['High'].shift(1) > data['High']) &
        (data['Low'].shift(-1) < data['Low']) &
        (data['Low'].shift(1) < data['Low'])
    )

    pennants = np.where(
        (data['Close'].shift(-1) < data['Close']) &
        (data['Close'].shift(1) < data['Close']) &
        (data['High'].shift(-1) > data['High']) &
        (data['High'].shift(1) > data['High']) &
        (data['Low'].shift(-1) < data['Low']) &
        (data['Low'].shift(1) < data['Low'])
    )

    return data, flags, pennants


def calculate_cup_and_handle(ticker):
    # Fetch data from Yahoo Finance
    data = yf.download(ticker, period='1y')

    # Find potential cup and handle pattern
    pattern = np.where(
        (data['Close'] > data['Close'].shift(-1)) &
        (data['Close'].shift(-1) > data['Close'].shift(-2)) &
        (data['Close'].shift(-2) > data['Close'].shift(-3)) &
        (data['Close'].shift(-3) > data['Close'].shift(-4)) &
        (data['Close'].shift(-4) < data['Close'].shift(-5))
    )

    return data, pattern


def calculate_wedges(ticker):
    # Fetch data from Yahoo Finance
    data = yf.download(ticker, period='1y')

    # Find potential ascending and descending wedges
    ascending_wedge = np.where(
        (data['High'].shift(-2) < data['High'].shift(-1)) &
        (data['High'].shift(-2) < data['High']) &
        (data['Low'].shift(-2) < data['Low'].shift(-1)) &
        (data['Low'].shift(-2) < data['Low'])
    )

    descending_wedge = np.where(
        (data['High'].shift(-2) > data['High'].shift(-1)) &
        (data['High'].shift(-2) > data['High']) &
        (data['Low'].shift(-2) > data['Low'].shift(-1)) &
        (data['Low'].shift(-2) > data['Low'])
    )

    return data, ascending_wedge, descending_wedge


def calculate_gaps(ticker):
    # Fetch data from Yahoo Finance
    data = yf.download(ticker, period='1y')

    # Calculate price differences between consecutive days
    price_diff = data['Close'].diff()

    # Find potential gap patterns
    breakaway_gaps = np.where((price_diff > 0) & (price_diff.shift(-1) > 0))
    exhaustion_gaps = np.where((price_diff < 0) & (price_diff.shift(-1) < 0))
    runaway_gaps = np.where((price_diff > 0) & (price_diff.shift(-1) < 0))

    return data, breakaway_gaps, exhaustion_gaps, runaway_gaps


def plot_pattern(data, pattern):
    # Create a new window for the plot
    window = tk.Toplevel()
    window.title('Pattern Analysis')

    # Create a Figure and set its size
    figure = Figure(figsize=(8, 6), dpi=100)

    # Create a subplot within the Figure
    subplot = figure.add_subplot(111)

    # Plot the stock prices
    candlestick_ohlc(subplot, data[['Date', 'Open', 'High', 'Low', 'Close']].values, width=0.6,
                     colorup='green', colordown='red')
    subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
    subplot.xaxis.set_major_locator(mpl_dates.DayLocator())

    # Highlight the pattern on the plot
    subplot.plot(data.iloc[pattern]['Date'], data.iloc[pattern]['Close'], 'bo', markersize=8)

    # Add labels and title to the plot
    subplot.set_xlabel('Date')
    subplot.set_ylabel('Price')
    subplot.set_title('Pattern Analysis')

    # Rotate the x-axis tick labels for better visibility
    figure.autofmt_xdate()

    # Create a canvas for the Figure
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()

    # Add the canvas to the window
    canvas.get_tk_widget().pack()


def analyze_stock():
    ticker = entry.get()
    pattern = pattern_var.get()

    if pattern == 'Bollinger Bands':
        # Perform Bollinger Bands analysis
        data = calculate_bollinger_bands(ticker)

        # Plot the Bollinger Bands
        plot_bollinger_bands(data)
    elif pattern == 'Head and Shoulders':
        # Perform Head and Shoulders pattern analysis
        data, pattern = calculate_head_and_shoulders(ticker)

        # Plot the pattern
        plot_pattern(data, pattern)
    elif pattern == 'Double Top and Double Bottom':
        # Perform Double Top and Double Bottom pattern analysis
        data, double_top_pattern, double_bottom_pattern = calculate_double_top_and_bottom(ticker)

        # Plot the patterns
        plot_pattern(data, double_top_pattern)
        plot_pattern(data, double_bottom_pattern)
    elif pattern == 'Triangles':
        # Perform Triangles pattern analysis
        data, ascending_triangle, descending_triangle, symmetrical_triangle = calculate_triangles(ticker)

        # Plot the patterns
        plot_pattern(data, ascending_triangle)
        plot_pattern(data, descending_triangle)
        plot_pattern(data, symmetrical_triangle)
    elif pattern == 'Flags and Pennants':
        # Perform Flags and Pennants pattern analysis
        data, flags, pennants = calculate_flags_and_pennants(ticker)

        # Plot the patterns
        plot_pattern(data, flags)
        plot_pattern(data, pennants)
    elif pattern == 'Cup and Handle':
        # Perform Cup and Handle pattern analysis
        data, pattern = calculate_cup_and_handle(ticker)

        # Plot the pattern
        plot_pattern(data, pattern)
    elif pattern == 'Wedges':
        # Perform Wedges pattern analysis
        data, ascending_wedge, descending_wedge = calculate_wedges(ticker)

        # Plot the patterns
        plot_pattern(data, ascending_wedge)
        plot_pattern(data, descending_wedge)
    elif pattern == 'Gaps':
        # Perform Gaps pattern analysis
        data, breakaway_gaps, exhaustion_gaps, runaway_gaps = calculate_gaps(ticker)

        # Plot the patterns
        plot_pattern(data, breakaway_gaps)
        plot_pattern(data, exhaustion_gaps)
        plot_pattern(data, runaway_gaps)


# Create the main window
window = tk.Tk()
window.title('Stock Analysis Tool')
window.geometry('300x300')

# Create a label and an entry for the stock ticker
label = tk.Label(window, text='Enter Stock Ticker:')
label.pack()

entry = tk.Entry(window)
entry.pack()

# Create a dropdown menu for pattern selection
pattern_var = tk.StringVar(window)
pattern_var.set('Bollinger Bands')
pattern_label = tk.Label(window, text='Select Pattern:')
pattern_label.pack()

pattern_menu = tk.OptionMenu(window, pattern_var,
                             'Bollinger Bands',
                             'Head and Shoulders',
                             'Double Top and Double Bottom',
                             'Triangles',
                             'Flags and Pennants',
                             'Cup and Handle',
                             'Wedges',
                             'Gaps')
pattern_menu.pack()

# Create a button to analyze the stock
button = tk.Button(window, text='Analyze', command=analyze_stock)
button.pack()

# Start the main GUI loop
tk.mainloop()
