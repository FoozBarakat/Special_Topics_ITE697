import pandas as pd
import numpy as np

# List of cities in Libya
cities = [
    "Tripoli", "Benghazi", "Misrata", "Tobruk", "Sabha",
    "Zuwara", "Derna", "Sirte", "Zliten", "Al Khums",
    "Ghat", "Murzuq", "Waddan", "Jalu", "Ghadames",
    "Tarhuna", "Mizdah", "Awjilah", "Nalut", "Ubari"
]

# Create a DataFrame with 1000 rows and four columns (City, Ping, Download, Upload) filled with random values
data = {
    'City': np.random.choice(cities, 1000),
    'Ping (ms)': np.random.randint(1, 100, 1000),
    'Download (Mbit/s)': np.random.randint(1, 100, 1000),
    'Upload (Mbit/s)': np.random.randint(1, 100, 1000)
}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('internet_speed.csv', index=False)

# Display the DataFrame
print(df)
