import yfinance as yf
import pandas as pd
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


def plot_bollinger_bands(data):
    # Create a new window for the plot
    window = tk.Toplevel()
    window.title('Bollinger Bands Analysis')

    # Create a Figure and set its size
    figure = Figure(figsize=(8, 6), dpi=100)

    # Create a subplot within the Figure
    subplot = figure.add_subplot(111)

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

    # Create a canvas for the Figure
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()

    # Add the canvas to the window
    canvas.get_tk_widget().pack()


def analyze_stock():
    ticker = entry.get()

    # Perform Bollinger Bands analysis
    data = calculate_bollinger_bands(ticker)

    # Plot the Bollinger Bands
    plot_bollinger_bands(data)


# Create the main window
window = tk.Tk()
window.title('Stock Analysis Tool')

# Create a label and an entry for the stock ticker
label = tk.Label(window, text='Enter Stock Ticker:')
label.pack()

entry = tk.Entry(window)
entry.pack()

# Create a button to analyze the stock
button = tk.Button(window, text='Analyze', command=analyze_stock)
button.pack()

# Start the main GUI loop
tk.mainloop()
