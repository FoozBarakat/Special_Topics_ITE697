import sqlite3
import pandas as pd
import random
import string

# Connect to the existing database
conn = sqlite3.connect('internet_speed_data.db')

# Read the existing table into a DataFrame
df_existing = pd.read_sql_query("SELECT * FROM data", conn)

# Create a new table
conn.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY, name TEXT, country TEXT, speed_id INTEGER)''')

# Generate random names and countries
names = [''.join(random.choices(string.ascii_uppercase, k=5)) for _ in range(len(df_existing))]
countries = [''.join(random.choices(string.ascii_uppercase, k=5)) for _ in range(len(df_existing))]

# Insert data into the new table
for i in range(len(df_existing)):
    conn.execute(f"INSERT INTO users (name, country, speed_id) VALUES ('{names[i]}', '{countries[i]}', {i + 1})")

# Commit changes to the database
conn.commit()

# Read the new table into a DataFrame
df_new = pd.read_sql_query("SELECT * FROM users", conn)

# Join the tables
df_merged = pd.merge(df_existing, df_new, left_on='id', right_on='speed_id', how='inner')

# Display the merged DataFrame
print(df_merged.head())

# Close the connection
conn.close()
