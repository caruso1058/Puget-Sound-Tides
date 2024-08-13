from flask import Flask, render_template
import matplotlib.pyplot as plt
import json
from datetime import datetime
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.dates as mdates

app = Flask(__name__)

def plot_tide_chart():
    with open('tide_data.json', 'r') as f:
        data = json.load(f)

    dates = []
    heights = []

    for prediction in data['predictions']:
        date = datetime.strptime(prediction['t'], '%Y-%m-%d %H:%M')
        height = float(prediction['v'])
        dates.append(date)
        heights.append(height)

    dates_num = mdates.date2num(dates)
    heights = np.array(heights)

    spline = make_interp_spline(dates_num, heights, k=3)
    dates_smooth = np.linspace(dates_num.min(), dates_num.max(), 500)
    heights_smooth = spline(dates_smooth)

    plt.figure(figsize=(12, 6))
    plt.plot(mdates.num2date(dates_smooth), heights_smooth, label='Tide Height (MLLW)')
    plt.title('Tide Predictions')
    plt.xlabel('Date and Time')
    plt.ylabel('Height (Feet)')
    plt.xticks(rotation=45)
    plt.grid(True)

    for i, height in enumerate(heights):
        if i == 0 or i == len(heights) - 1:
            continue
        if heights[i-1] < height > heights[i+1] or heights[i-1] > height < heights[i+1]:
            plt.annotate(f'{height:.2f} ft', (dates[i], height), textcoords="offset points", xytext=(0,10), ha='center')

    plt.tight_layout()
    plt.savefig('static/tide_plot.png')
    plt.close()

@app.route('/')
def index():
    plot_tide_chart()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
