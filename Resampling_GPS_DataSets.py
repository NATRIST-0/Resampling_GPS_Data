# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 08:17:06 2024

@author: GAYRARD
"""

import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic

data = pd.read_excel(r"C:\Users\GAYRARD\Desktop\flight_test.xlsx")
drone_data = pd.read_excel(r"C:\Users\GAYRARD\Desktop\flight_test_drone_data.xlsx") 

drone_data['date'] = pd.to_datetime(drone_data['timestamp(ms)'], unit='ms')
drone_data.set_index('date', inplace=True)
resampled_data = drone_data.resample('512.6ms').mean()

# Convert GPS coordinates
resampled_data['GPS.Lat'] = resampled_data['GPS,Lat'] * 10**-8
resampled_data['GPS.Lng'] = resampled_data['GPS,Lng'] * 10**-8

lat = resampled_data['GPS.Lat']
lon = resampled_data['GPS.Lng']
alt = resampled_data['GPS,Alt']

# Initialize empty lists to store x, y and z
x3 = []
y3 = []
z3 = []

# Get the start point and start altitude
start_point = (lat.iloc[0], lon.iloc[0])
start_alt = alt.iloc[0]

# Append the start point
x3.append(0)
y3.append(0)
z3.append(start_alt)

# Calculate x and y coordinates relative to the start point
for i in range(1, len(lat)):
    current_point = (lat.iloc[i], lon.iloc[i])
    x3.append(geodesic(start_point, (lat.iloc[i], start_point[1])).meters)
    y3.append(geodesic(start_point, (start_point[0], lon.iloc[i])).meters)
    z3.append(alt.iloc[i])
    
# Make those empty lists in DataFrame
df_x3 = pd.DataFrame(x3)
df_y3 = pd.DataFrame(y3)
df_z3 = pd.DataFrame(z3)

X1 = data['X1 (m)']

print(len(df_x3))
print(len(X1))

###PLOT
fig, ax1 = plt.subplots()

ax1.plot(resampled_data["timestamp(ms)"], df_x3, label='X3 (m)', color='crimson')
ax1.set_ylabel('X3 (m)', color='red')
ax1.set_xlabel('TimeStamps (ms)')

# ax2 = ax1.twinx()
# ax2.spines['right'] 
# ax2.plot(resampled_data["timestamp(ms)"], X1, label='X1 (m)', color='steelblue')
# ax2.set_ylabel('X1 (m)', color='blue')

fig.patch.set_linewidth(5)
fig.patch.set_edgecolor('slategrey')
plt.title('X drone vs X garmin from speed')
plt.show()

