#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
data = pd.read_csv('housing_market.csv')

# Group the data by state and calculate the median home price for each state
state_median_prices = data.groupby('State')['2023-04-30'].median()

# Sort the data by median home price in descending order
state_median_prices = state_median_prices.sort_values(ascending=False)

# Create a bar chart to visualize the data
plt.bar(state_median_prices.index, state_median_prices.values)
plt.xticks(rotation=90)
plt.xlabel('State')
plt.ylabel('Median Home Price ($)')
plt.title('Median Home Prices by State')
plt.show()
