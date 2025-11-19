#!/usr/bin/env python3 faang.py

# This code is an script that generates data from the last 5 days of some tickers and then create a plot with them.
# By Ignacio Riboldi



import yfinance as yf # To get Tickers data from yfinance
from datetime import datetime # For timestamp in the file name
import os # Folder manipulation
import pandas as pd # Data manipulation
import matplotlib.pyplot as plt


def get_data(period="5d"):
    tickers = ["AAPL", "META", "AMZN", "NFLX", "GOOG"]
    data_frames = []
    
    for symbol in tickers:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        data['Ticker'] = symbol  # Add a column to identify the ticker
        data_frames.append(data)
    
    # Combine all data into a single DataFrame
    combined_data = pd.concat(data_frames)
    
    # Reset index so Date becomes a column
    combined_data.reset_index(inplace=True)
    
    # Create folder if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}.csv"
    filepath = os.path.join("data", filename)
    
    # Save to CSV
    combined_data.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")
    
    return combined_data

# Example usage
df = get_data()

def plot_data():
    # Folders
    data_folder = "data"
    plots_folder = "plots"

    # First, we make sure that plots folder exist so we don't get error https://www.w3schools.com/python/ref_os_makedirs.asp
    os.makedirs(plots_folder, exist_ok=True)

    data_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]
    if not data_files: # In case it doesn't find any file, print a message.
        print("No data files found in the data folder.")
        return

    latest_file = max(data_files, key=os.path.getmtime) # Returns the time of the last modification of the file (considering it might be the last one)

    # Load data
    df = pd.read_csv(latest_file)

    # Convert date column to datetime
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Grouping by date, ticker and Close price
    for ticker, group in df.groupby("Ticker"):
        plt.plot(group["Date"], group["Close"], label=ticker)

        # Adding label with the last close value
        for x, y in zip(group["Date"], group["Close"]):
            plt.text(x, y, f"{y:.2f}", fontsize=8, ha="center", va="bottom", rotation=45)

    # Format the plot
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title(datetime.now().strftime("%Y-%m-%d"))  # current date as title
    plt.legend()
    plt.grid(True)
    plt.tight_layout() 

    # Save the plot
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    plot_filename = os.path.join(plots_folder, f"{timestamp}.png")
    plt.savefig(plot_filename)
    plt.close()
    
    print(f"Plot has been saved: {plot_filename}")

plot_data()