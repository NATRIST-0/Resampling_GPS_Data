import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Load data
data = pd.read_excel(r"C:\Users\GAYRARD\Desktop\flight_test.xlsx")
drone_data = pd.read_excel(r"C:\Users\GAYRARD\Desktop\flight_test_drone_data.xlsx")

# Convert timestamps to datetime and set as index
drone_data['date'] = pd.to_datetime(drone_data['timestamp(ms)'], unit='ms')
drone_data.set_index('date', inplace=True)

# Calculate total duration in seconds
total_duration = (drone_data.index[-1] - drone_data.index[0]).total_seconds()

# Calculate new resampling frequency
num_points = len(data['X1 (m)'])
new_frequency = total_duration / num_points

# Resample the data using the new frequency
resampled_data = drone_data.resample('0.512s').mean()

# Convert GPS coordinates
resampled_data['GPS,Lat'] = resampled_data['GPS,Lat'] * 10**-8
resampled_data['GPS,Lng'] = resampled_data['GPS,Lng'] * 10**-8

# Drop rows with NaN values in the relevant columns
resampled_data = resampled_data.dropna(subset=['GPS,Lat', 'GPS,Lng', 'GPS,Alt'])

lat = resampled_data['GPS,Lat']
lon = resampled_data['GPS,Lng']
alt = resampled_data['GPS,Alt']

# Initialize lists for storing x, y, and z coordinates
x3 = [0]
y3 = [0]
z3 = [alt.iloc[0]]

# Get the start point coordinates
start_point = (lat.iloc[0], lon.iloc[0])

# Calculate x and y coordinates relative to the start point
for i in range(1, len(lat)):
    current_point = (lat.iloc[i], lon.iloc[i])
    if pd.notna(current_point[0]) and pd.notna(current_point[1]):
        x3.append(geodesic(start_point, (lat.iloc[i], start_point[1])).meters)
        y3.append(geodesic(start_point, (start_point[0], lon.iloc[i])).meters)
        z3.append(alt.iloc[i])

# Create DataFrames for x, y, and z coordinates
df_x3 = pd.DataFrame(x3, columns=['X3'])
df_y3 = pd.DataFrame(y3, columns=['Y3'])
df_z3 = pd.DataFrame(z3, columns=['Z3'])

# Extract X1 data for plotting
X1 = data['X1 (m)']

# Ensure resampled_data and X1 have the same length
if len(resampled_data) > len(X1):
    resampled_data = resampled_data.iloc[:len(X1)]
    print('X1 trimmed')
elif len(X1) > len(resampled_data):
    X1 = X1.iloc[:len(resampled_data)]

print("len(df_x3)",len(df_x3))
print("len(X1)",len(X1))


fig, ax1 = plt.subplots()

ax1.plot(resampled_data.index, df_x3, label='X3 (m)', color='crimson')
ax1.set_ylabel('X3 (m)', color='red')
ax1.set_xlabel('Timestamp (ms)')

ax2 = ax1.twinx()
ax2.spines['right']
ax2.plot(resampled_data.index, -X1, label='X1 (m)', color='steelblue')
ax2.set_ylabel('X1 (m)', color='steelblue')

fig.patch.set_linewidth(5)
fig.patch.set_edgecolor('slategrey')
plt.title('X drone vs X garmin from speed')

line1, = ax1.plot(resampled_data.index, df_x3, label='X3 (m)', color='crimson')
line2, = ax2.plot(resampled_data.index, -X1, label='X1 (m)', color='steelblue')
lines = [line1, line2]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='upper right')

plt.show()
