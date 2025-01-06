import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time


# Define min and max Bid Values for Filtering
min_bid = 7
max_bid = 50

# URL of the Page
url = 'https://fragment.com/numbers?sort=price_asc&filter=auction'


while True:

    # Send an HTTP request to the Page
    response = requests.get(url)
    html = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Data Containers
    numbers = []
    bids = []
    end_times = []

    # Find the Table Rows Containing Data
    for row in soup.find_all('tr', class_='tm-row-selectable'):
        # Extract the phone number
        number = row.find('div', class_='table-cell-value tm-value').text.strip()
        
        # Extract the Bid
        bid_str = row.find('div', class_='table-cell-value tm-value icon-before icon-ton').text.strip()
        bid = float(bid_str.replace(',', ''))  # Remove commas and convert to float

        # Extract the Auction end Datetime
        end_time_tag = row.find('time', datetime=True)
        end_time = datetime.fromisoformat(end_time_tag['datetime'])
        
        # Append to Lists
        numbers.append(number)
        bids.append(bid)
        end_times.append(end_time)

    # Create a DataFrame
    data = pd.DataFrame({
        'Number': numbers,
        'Bid': bids,
        'End Time': end_times
    })

    filtered_data = data[(data['Bid'] >= min_bid) & (data['Bid'] <= max_bid)]

    # Sort the Data
    data_sorted = filtered_data.sort_values(by='End Time', ascending=True)
    # Display the Result
    print(f'{data_sorted.head(33)}\n')

    time.sleep(20 * 60)