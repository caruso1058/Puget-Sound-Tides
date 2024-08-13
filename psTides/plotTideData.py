import json
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.dates as mdates

# Load data from the JSON file
with open('tide_data.json', 'r') as f:
    data = json.load(f)

# Extract dates and heights from the data
dates = []
heights = []

for prediction in data['predictions']:
    # Convert time to datetime object for better plotting
    date = datetime.strptime(prediction['t'], '%Y-%m-%d %H:%M')
    height = float(prediction['v'])
    dates.append(date)
    heights.append(height)

# Convert dates to numbers for interpolation
dates_num = mdates.date2num(dates)
heights = np.array(heights)

# Smooth the curve
spline = make_interp_spline(dates_num, heights, k=3)
dates_smooth = np.linspace(dates_num.min(), dates_num.max(), 500)
heights_smooth = spline(dates_smooth)

# Plot the smoothed data
plt.figure(figsize=(12, 6))
plt.plot(mdates.num2date(dates_smooth), heights_smooth, label='Tide Height (MLLW)')
plt.title('Tide Predictions')
plt.xlabel('Date')
plt.ylabel('Height (Feet)')
plt.xticks(rotation=45)
plt.grid(True)

# Add labels for the high and low points
for i, height in enumerate(heights):
    if i == 0 or i == len(heights) - 1:
        continue
    if heights[i-1] < height > heights[i+1] or heights[i-1] > height < heights[i+1]:
        plt.annotate(f'{height:.2f} ft', (dates[i], height), textcoords="offset points", xytext=(0,10), ha='center')

plt.tight_layout()

# Save the plot as an image
plt.savefig('tide_plot.png')

# Show the plot
plt.show()
