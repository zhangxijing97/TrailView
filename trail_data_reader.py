import csv

def read_trail_data(file_path):
    trails = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Assuming the CSV has columns like 'TrailName', 'Location', 'Difficulty', etc.
            header = next(reader)  # Skip the header row
            for row in reader:
                trail = dict(zip(header, row))
                trails.append(trail)
        return trails
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

# Specify the path to the CSV file
csv_file_path = 'California_Coastal_Trail_(CCT)_.csv'

# Read trail data from the CSV file
trail_data = read_trail_data(csv_file_path)

# Display the first few trails as a test
for trail in trail_data[:5]:
    print(trail)
