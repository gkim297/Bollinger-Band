import yfinance as yf
import pandas as pd
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calculate_bollinger_bands(ticker, interval):
    # Fetch data from Yahoo Finance
    data = yf.download(ticker, interval=interval)

    # Calculate Bollinger Bands
    data['SMA'] = data['Close'].rolling(window=20).mean()
    data['STD'] = data['Close'].rolling(window=20).std()
    data['Upper'] = data['SMA'] + 2 * data['STD']
    data['Lower'] = data['SMA'] - 2 * data['STD']

    # Identify buy and sell positions
    data['Buy'] = data['Close'] > data['Upper']
    data['Sell'] = data['Close'] < data['Lower']

    return data


def update_bollinger_bands(ticker, interval):
    # Clear previous plot
    subplot.clear()

    # Perform Bollinger Bands analysis
    data = calculate_bollinger_bands(ticker, interval)

    # Plot the stock prices
    subplot.plot(data['Close'], label='Close Price')

    # Plot the Bollinger Bands
    subplot.plot(data['Upper'], label='Upper Band')
    subplot.plot(data['Lower'], label='Lower Band')

    # Plot buy and sell positions
    buy_positions = data[data['Buy']].index
    sell_positions = data[data['Sell']].index

    subplot.plot(buy_positions, data.loc[buy_positions, 'Close'], 'g^', markersize=8, label='Buy')
    subplot.plot(sell_positions, data.loc[sell_positions, 'Close'], 'rv', markersize=8, label='Sell')

    # Add labels and title to the plot
    subplot.set_xlabel('Date')
    subplot.set_ylabel('Price')
    subplot.set_title('Bollinger Bands Analysis')

    # Add a legend to the plot
    subplot.legend()

    # Redraw the canvas
    canvas.draw()


def analyze_stock():
    ticker = entry.get()
    interval = timeframe.get()

    # Update the Bollinger Bands plot
    update_bollinger_bands(ticker, interval)


def resize_event(event):
    subplot.set_position([0.1, 0.1, 0.8, 0.8])  # Set initial position
    canvas.draw()


def scroll_event(event):
    if event.button == 'up':
        subplot.set_position(subplot.get_position() + [0, 0, 0, 0.1])  # Increase height
    elif event.button == 'down':
        subplot.set_position(subplot.get_position() - [0, 0, 0, 0.1])  # Decrease height
    canvas.draw()


# Create the main window
window = tk.Tk()
window.title('Stock Analysis Tool')

# Create a label and an entry for the stock ticker
label = tk.Label(window, text='Enter Stock Ticker:', font=('Arial', 12))
label.pack(pady=10)

entry = tk.Entry(window, font=('Arial', 12))
entry.pack(pady=5)

# Create a label and a dropdown menu for timeframe selection
timeframe_label = tk.Label(window, text='Select Timeframe:', font=('Arial', 12))
timeframe_label.pack(pady=5)

timeframe = tk.StringVar(window)
timeframe.set('1d')  # Default timeframe selection

timeframe_dropdown = tk.OptionMenu(window, timeframe, '1m', '2m', '5m', '15m', '30m', '60m', '90m',
                                   '1h', '1d', '5d', '1wk', '1mo', '3mo')
timeframe_dropdown.config(font=('Arial', 12))
timeframe_dropdown.pack(pady=5)

# Create a Figure and set its size
figure = Figure(figsize=(8, 6), dpi=100)

# Create a subplot within the Figure
subplot = figure.add_subplot(111)

# Create a canvas for the Figure
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.get_tk_widget().pack(pady=10)

# Bind the resize and scroll events to the canvas
canvas.mpl_connect('resize_event', resize_event)
canvas.mpl_connect('scroll_event', scroll_event)

# Create a button to analyze the stock
button = tk.Button(window, text='Analyze', font=('Arial', 12), command=analyze_stock)
button.pack(pady=5)

# Start the main GUI loop
window.mainloop()
