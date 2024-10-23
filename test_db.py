from mysql import connector

# Connect to the database
conn = connector.connect(
    host="localhost",
    user="pdga_rating_bot",
    password="BluePancakes1*",
    database="pdgaratingsdb"
)

# Create a cursor object
cursor = conn.cursor()

# Execute an SQL query
query = "SELECT * FROM Courses"
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()

# Display the results
for row in results:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()