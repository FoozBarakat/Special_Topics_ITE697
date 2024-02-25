import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # Import the module

# Load the data from the CSV file
df_compact = pd.read_csv('rpi_data_processed.csv')

# Check for NaN values in the DataFrame
print("Number of NaN values in dataframe:", df_compact.isna().sum().sum())

# Remove any rows with NaN values
df_compact = df_compact.dropna()

# Convert 'Date' and 'Time' columns to datetime objects
df_compact['Time'] = pd.to_datetime(df_compact['Time'])
df_compact['Date'] = pd.to_datetime(df_compact['Date'] + ' ' + df_compact['Time'].dt.strftime('%H:%M:%S'))

# Plot the data
fig, ax = plt.subplots(figsize=(8, 8))
ax.plot(df_compact['Date'], df_compact['Ping (ms)'], label='Ping (ms)')
ax.plot(df_compact['Date'], df_compact['Upload (Mbit/s)'], label='Upload (Mbit/s)')
ax.plot(df_compact['Date'], df_compact['Download (Mbit/s)'], label='Download (Mbit/s)')
ax.legend(loc='upper right')

# Set x-axis format to include date
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

# Add labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Speed/Time (units)')
ax.set_title('Internet Speed Over Time')

plt.xticks()
plt.show()

# Define the acceptable values
acceptable_upload = 13  # Mbit/s
acceptable_download = 88  # Mbit/s
acceptable_ping = 20  # ms

# Plot histograms
fig, ax = plt.subplots(2, 2, figsize=(10, 10))
ax[0, 0].hist(df_compact['Ping (ms)'], bins=25)
ax[0, 0].axvline(acceptable_ping, color='red', linewidth=1)
ax[0, 0].set_title('Ping (ms)')

ax[0, 1].hist(df_compact['Upload (Mbit/s)'], bins=25)
ax[0, 1].axvline(acceptable_upload, color='red', linewidth=1)
ax[0, 1].set_title('Upload (Mbit/s)')

ax[1, 0].hist(df_compact['Download (Mbit/s)'], bins=25)
ax[1, 0].axvline(acceptable_download, color='red', linewidth=1)
ax[1, 0].set_title('Download (Mbit/s)')

plt.show()

# Compute means and standard deviations
means = df_compact.mean()
stds = df_compact.std()

quote_ping = (means['Ping (ms)'], stds['Ping (ms)'])
quote_download = (means['Download (Mbit/s)'], stds['Download (Mbit/s)'])
quote_upload = (means['Upload (Mbit/s)'], stds['Upload (Mbit/s)'])

print('Average ping time: {} ± {} ms'.format(*quote_ping))
print('Average download speed: {} ± {} Mbit/s'.format(*quote_download))
print('Average upload speed: {} ± {} Mbit/s'.format(*quote_upload))
print('Distance of acceptable Ping speed from average: {:.2f} standard deviations'.format((quote_ping[0] - acceptable_ping) / quote_ping[1]))
print('Distance of acceptable Download speed from average: {:.2f} standard deviations'.format((quote_download[0] - acceptable_download) / quote_download[1]))
print('Distance of acceptable Upload speed from average: {:.2f} standard deviations'.format((quote_upload[0] - acceptable_upload) / quote_upload[1]))

# Calculate percentage of measurements below acceptable values
print('{:.2f}% of measurements are below the acceptable download speed.'.format((df_compact['Download (Mbit/s)'] < acceptable_download).mean() * 100))
print('{:.2f}% of measurements are below the acceptable upload speed.'.format((df_compact['Upload (Mbit/s)'] < acceptable_upload).mean() * 100))
print('{:.2f}% of measurements are above the acceptable ping time.'.format((df_compact['Ping (ms)'] > acceptable_ping).mean() * 100))

# Calculate percentage of measurements failing in all three criteria
all_three = ((df_compact['Ping (ms)'] > acceptable_ping) &
             (df_compact['Download (Mbit/s)'] < acceptable_download) &
             (df_compact['Upload (Mbit/s)'] < acceptable_upload)).mean() * 100
print('{:.2f}% of measurements fail in all three criteria.'.format(all_three))

# Calculate percentage of measurements failing in two out of three criteria
ping_upload = ((df_compact['Ping (ms)'] > acceptable_ping) &
               (df_compact['Upload (Mbit/s)'] < acceptable_upload)).mean() * 100
ping_download = ((df_compact['Ping (ms)'] > acceptable_ping) &
                 (df_compact['Download (Mbit/s)'] < acceptable_download)).mean() * 100
upload_download = ((df_compact['Upload (Mbit/s)'] < acceptable_upload) &
                    (df_compact['Download (Mbit/s)'] < acceptable_download)).mean() * 100

print('{:.2f}% of measurements fail in ping and upload.'.format(ping_upload))
print('{:.2f}% of measurements fail in ping and download.'.format(ping_download))
print('{:.2f}% of measurements fail in upload and download.'.format(upload_download))

# Calculate the percentage of measurements that meet all three criteria
all_three_pass = ((df_compact['Ping (ms)'] <= acceptable_ping) &
                  (df_compact['Download (Mbit/s)'] >= acceptable_download) &
                  (df_compact['Upload (Mbit/s)'] >= acceptable_upload)).mean() * 100
print('{:.2f}% of measurements meet all three criteria.'.format(all_three_pass))
