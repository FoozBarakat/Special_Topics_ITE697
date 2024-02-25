import datetime
import subprocess
import csv
import pandas as pd

# Define column names
column_names = ['Date & Time', 'Ping (ms)', 'Download (Mbit/s)', 'Upload (Mbit/s)']

# Create an empty DataFrame with the specified column names
df = pd.DataFrame(columns=column_names)

# Save the DataFrame to a CSV file with headers
df.to_csv('./internet_speed_data.csv', sep='\t', index=False)

def speedtest():
    speedtest_cmd = "speedtest-cli --simple"
    process = subprocess.Popen(speedtest_cmd.split(), stdout=subprocess.PIPE)
    process_output = process.communicate()[0].split()
    date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    ping = process_output[1].decode('utf-8')
    download = process_output[4].decode('utf-8')
    upload = process_output[7].decode('utf-8')
    return date_time, ping, download, upload

def save_to_csv(data, filename):
    with open(filename + '.csv', 'a', newline='') as f:
        wr = csv.writer(f, delimiter='\t')
        wr.writerow(data)

for i in range(5):  # Generate 5 rows of data
    speedtest_output = speedtest()
    save_to_csv(speedtest_output, 'internet_speed_data')

# Read the CSV file with the specified column names
df = pd.read_csv('./internet_speed_data.csv', sep='\t')

# Split the 'Date & Time' column into separate 'Date' and 'Time' columns
df[['Date', 'Time']] = df['Date & Time'].str.split(' ', n=1, expand=True)

# Drop the original 'Date & Time' column
df.drop(columns=['Date & Time'], inplace=True)

# Reorder the columns to place 'Date' and 'Time' as the first columns
cols = df.columns.tolist()
cols = cols[-2:] + cols[:-2]
df = df[cols]

# Save the modified DataFrame to a new CSV file
df.to_csv('./updated_internet_speed_data.csv', index=False)