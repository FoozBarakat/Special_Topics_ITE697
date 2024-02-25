import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Read the CSV file (assuming 'updated_internet_speed_data.csv' is in the same directory)
data = pd.read_csv("internet_speed.csv")

df = pd.DataFrame(data)

# Initialize dataframe df_rates
df_rates = df.drop(['Ping (ms)', 'City'], axis=1)

# Rename the download and upload columns of df_rates
lookup = {'Download (Mbit/s)': 'download_rate', 
          'Upload (Mbit/s)': 'upload_rate'}
df_rates = df_rates.rename(columns=lookup)

# Calculate ping_rate
ping_rate = 1. / df['Ping (ms)']

# Convert ping_rate to 1/seconds
ping_rate = 1000. * ping_rate

# Add a column to complete the task
df_rates['ping_rate'] = ping_rate

# Inspect the result
print(df_rates)

def scatter_view(azim, elev):
    # Init figure and axes
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Compute scatter plot
    ax.scatter(df_rates['download_rate'], df_rates['upload_rate'], df_rates['ping_rate'])
    ax.set_xlabel('D rate (Mbit/s)', fontsize=16)
    ax.set_ylabel('U rate (Mbit/s)', fontsize=16)
    ax.set_zlabel('P rate (1/s)', fontsize=16)
    
    # Specify azimuth and elevation
    ax.view_init(azim=azim, elev=elev)

    # Show plot
    plt.show()

# Draw interactive plot
scatter_view(45, 45)

# Step 1: Calculate the means
mu = df_rates.mean()

# Step 2: Calculate the Euclidean distance
euclid_sq = np.square(df_rates - mu).sum(axis=1)
euclid = np.sqrt(euclid_sq)

# Step 3: Create a histogram
fig = plt.figure(figsize=(7, 7))
plt.hist(euclid, bins=25, density=True)
plt.xlabel('Euclidean distance', fontsize=16)
plt.ylabel('Relative frequency', fontsize=16)
plt.show()

# Step 4: Compute the normalized distance
max_euclid = euclid.max()
nmd_euclid = euclid / max_euclid

# Step 5: Visualize the alarm rate
ecl_alarm_rate = []
nmd_range = np.linspace(0, 1, 400)
for nmd_decision in nmd_range:
    num_fail = (nmd_euclid > nmd_decision).sum()
    ecl_alarm_rate.append(num_fail / len(df_rates))

# Step 6: Select the decision boundary
threshold = 0.1
index, ecl_threshold = next((tpl for tpl in enumerate(ecl_alarm_rate) if tpl[1] < threshold), (0, 0))
ecl_decision = nmd_range[index]

# Step 7: Visualize the decision boundary
fig = plt.figure(figsize=(7, 7))
plt.plot(nmd_range, ecl_alarm_rate, linewidth=2)
plt.plot(ecl_decision, ecl_threshold, 'bo', markersize=11)
plt.xlabel('Normalized distance (Euclidean)', fontsize=16)
plt.ylabel('Alarm rate', fontsize=16)
plt.show()

# Step 8: Visualize the decision boundary in 3D
radius = ecl_decision * max_euclid
phi = np.linspace(0, 2 * np.pi, 300)
theta = np.linspace(0, 2 * np.pi, 300)
xs = radius * np.outer(np.sin(theta), np.cos(phi))
ys = radius * np.outer(np.sin(theta), np.sin(phi))
zs = radius * np.outer(np.cos(theta), np.ones(np.size(phi)))
ecl_xd = xs + df_rates['download_rate'].mean()
ecl_yd = ys + df_rates['upload_rate'].mean()
ecl_zd = zs + df_rates['ping_rate'].mean()

fig = plt.figure(figsize=(7, 7))
ax = Axes3D(fig)
ax.scatter(df_rates['download_rate'], df_rates['upload_rate'], df_rates['ping_rate'])
ax.plot_surface(ecl_xd, ecl_yd, ecl_zd, linewidth=0, alpha=0.25)
ax.set_xlabel('D rate (Mbit/s)', fontsize=16)
ax.set_ylabel('U rate (Mbit/s)', fontsize=16)
ax.set_zlabel('P rate (1/s)', fontsize=16)
plt.show()