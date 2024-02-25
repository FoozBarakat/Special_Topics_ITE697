import sqlite3
import subprocess
import datetime

# Function to create the database and table
def create_database():
    # Connect to the database file
    conn = sqlite3.connect('internet_speed_data.db')
    cursor = conn.cursor()

    # Create the 'data' table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS data
                      (id INTEGER PRIMARY KEY, date TEXT, time TEXT, ping REAL, download REAL, upload REAL)''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(date, time, ping, download, upload):
    conn = sqlite3.connect('internet_speed_data.db')
    cursor = conn.cursor()

    # Insert data into the 'data' table
    cursor.execute("INSERT INTO data (date, time, ping, download, upload) VALUES (?, ?, ?, ?, ?)",
                   (date, time, ping, download, upload))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Function to query and display all data from the database
def query_data():
    conn = sqlite3.connect('internet_speed_data.db')
    cursor = conn.cursor()

    # Retrieve all rows from the 'data' table
    cursor.execute("SELECT * FROM data")
    rows = cursor.fetchall()
    
    # Print each row
    print("Query data from the database:")
    for row in rows:
        print(row)
    
    # Close the connection
    conn.close()

# Function to perform a speed test
def speedtest():
    # Run the speedtest-cli command to get speed test results
    speedtest_cmd = "speedtest-cli --simple"
    process = subprocess.Popen(speedtest_cmd.split(), stdout=subprocess.PIPE)
    process_output = process.communicate()[0].split()

    # Get the current date and time
    date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Extract ping, download, and upload speeds from the output
    ping = process_output[1].decode('utf-8')
    download = process_output[4].decode('utf-8')
    upload = process_output[7].decode('utf-8')
    
    # Return date, time, ping, download, and upload speeds as a tuple
    return date_time, ping, download, upload


# Main function to run speed tests and store results in the database
def main():
    # Create the database and table if they don't exist
    create_database()

    # Perform speed tests and insert results into the database
    for i in range(5):  # Perform 5 speed tests
        date_time, ping, download, upload = speedtest()
        date, time = date_time.split(' ')
        insert_data(date, time, ping, download, upload)

    # Query and display all data from the database
    query_data()

# Run the main function
if __name__ == "__main__":
    main()
