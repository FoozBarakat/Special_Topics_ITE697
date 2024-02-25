import pandas as pd
import numpy as np

# List of cities in Libya
cities = [
    "Tripoli", "Benghazi", "Misrata", "Tobruk", "Sabha",
    "Zuwara", "Derna", "Sirte", "Zliten", "Al Khums",
    "Ghat", "Murzuq", "Waddan", "Jalu", "Ghadames",
    "Tarhuna", "Mizdah", "Awjilah", "Nalut", "Ubari"
]

# Create a DataFrame with at least 1000 rows and two columns (City and Value) filled with random values
data = {
    'City': np.random.choice(cities, 1000),
    'Value': np.random.choice([np.random.randint(1, 20), np.random.randint(20, 40), np.random.randint(40, 60), np.random.randint(60, 100)], 1000)
}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('libyan_cities_data.csv', index=False)

# Display the DataFrame
print(df)
