import numpy as np
import csv
from collections import defaultdict
from datetime import datetime


# Load the CSV data into Numpy array
def csv_into_array (csv_file):    
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        
        # Read the header
        header = next(reader) 
        
        # Data lines
        for row in reader:
            data.append(row)
    
    # Convert data to a numpy array
    data_array = np.array(data)
    
    # print (data_array.shape)
    # print (data_array[:, 0].dtype)
    # print (data_array[:, 1].dtype)
    
    return data_array, header

def max_temp_day(data_array, header):
    
    # Extract the city columns (London, Tokyo, Sydney, Cairo, Rio)
    cities = header[1:]  # Skip the 'Date' column
    dates = data_array[:, 0]  # Extract the Date column
    
    # Initialize a dictionary to store results
    max_temp_dict = {}
    
    # Iterate over each city to find the max temperature and corresponding day
    for i, city in enumerate(cities):
        
        # Temp for the current city : from string to float
        temps = data_array[:, i + 1].astype(float)
        
        # Find the index of the maximum temperature
        max_temp_index = np.argmax(temps)
        
        # Get the date and temperature of the max temperature day
        max_temp_day = dates[max_temp_index]
        max_temp = temps[max_temp_index]
        
        # Store the result in the dictionary
        max_temp_dict[city] = (max_temp_day, max_temp)
    
    return max_temp_dict


def monthly_avg_temp(data_array, header):
    
    # Extract city names from header
    cities = header[1:]
    
    # date column
    dates = data_array[:, 0]
    
    # Initialize a nested dictionary: month -> city -> list of temps
    monthly_avg_dict = {}

    for i, date_str in enumerate(dates):
        # Convert date string to datetime object
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        month = date_obj.strftime('%Y-%m')
        
        # Initialize inner dict for month if not exists
        if month not in monthly_avg_dict:
            monthly_avg_dict[month] = {}
        
        for j, city in enumerate(cities):
            temp = float(data_array[i, j + 1])
            
            # Initialize list for city if not exists
            if city not in monthly_avg_dict[month]:
                monthly_avg_dict[month][city] = []
            
            # Append the temperature
            monthly_avg_dict[month][city].append(temp)

    # Compute average temperatures
    avg_temp_dict = {}
    for month, city_data in monthly_avg_dict.items():
        avg_temp_dict[month] = {}
        for city, temps in city_data.items():
            avg_temp_dict[month][city] = np.mean(temps)
    
    return avg_temp_dict

def count_5day_hot_streaks(data_array, header):
    
    # Identify cities list and the date column
    cities = header[1:]
    dates = data_array[:, 0]
    
    # Check monthly averages
    monthly_averages = monthly_avg_temp(data_array, header)
    
    # Initialize result dictionary
    hot_streak_counts = {city: 0 for city in cities}
    
    num_rows = data_array.shape[0]
    
    for i in range(num_rows - 4):  # For each 5-day window
        
        # Get 5 consecutive date strings and convert to month keys
        window_dates = [dates[i + k] for k in range(5)]
        month_keys = [datetime.strptime(d, '%d-%m-%Y').strftime('%Y-%m') for d in window_dates]
        
        # Count how many times each month appears in the window
        month_counts = {}
        for month in month_keys:
            month_counts[month] = month_counts.get(month, 0) + 1
        
        # Pick the dominant month (the one with most days)
        dominant_month = max(month_counts, key=month_counts.get)
        
        # For each city, compare all 5 temps to the monthly average
        for j, city in enumerate(cities):
            temps = [float(data_array[i + k, j + 1]) for k in range(5)]
            monthly_avg = monthly_averages[dominant_month][city]
            
            if all(temp > monthly_avg for temp in temps):
                hot_streak_counts[city] += 1
    
    return hot_streak_counts


csv_file = 'city_temperature.csv'

# Get the Header and Data from CSV
data_array, header = csv_into_array(csv_file)

# Find Max temp for each city
max_temp_result = max_temp_day(data_array, header)
print("Max Temperature : ", max_temp_result)

# Find Monthly average
monthly_averages = monthly_avg_temp(data_array, header)
print("Monthly Average : ", monthly_averages)

# Number of hot streaks
hot_streaks = count_5day_hot_streaks(data_array, header)
print("Number of Hot streaks : ", hot_streaks)

