from flask import Flask, request, render_template
import requests
import csv
from datetime import datetime, timedelta

app = Flask(__name__)

def fetch_stock_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    time_series = data.get('Time Series (Daily)', {})
    return time_series

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, values in data.items():
            writer.writerow({
                'date': date,
                'open': values['1. open'],
                'high': values['2. high'],
                'low': values['3. low'],
                'close': values['4. close'],
                'volume': values['5. volume']
            })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    api_key = 'your_alpha_vantage_api_key'  # Replace with your Alpha Vantage API key
    symbol = request.form['symbol']
    
    data = fetch_stock_data(symbol, api_key)
    if data:
        filename = f'stockdata_{symbol}.csv'
        save_to_csv(data, filename)
        
        # Prepare data for the last 7 days
        sorted_dates = sorted(data.keys(), reverse=True)[:7]
        last_week_data = {date: data[date] for date in sorted_dates}
        
        return render_template('stock_data.html', symbol=symbol, stock_data=last_week_data)
    else:
        return f"Failed to fetch data for {symbol}. Please check the stock symbol and try again."

if __name__ == "__main__":
    app.run(debug=True)
