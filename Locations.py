import csv

# Most functions pertaining to location and distance data are located here

# This 2D list will act as a matrix to hold distance values for the program. Global variable
distance_matrix = []


# Loads the location data from the CSV file
# Time complexity: O(n)
def loadLocationData(location_file, location_dict):
    with open(location_file) as location_data:
        location_data = csv.reader(location_data, delimiter=',')
        for row in location_data:
            key = row[0]
            label = row[2]
            location_dict[key] = label


# Retrieves the index of the given address in the location data. Used for looking up values in distance matrix
# Time complexity: O(n)
def getLocationIndex(address, location_dict):
    for location_index in location_dict:
        location_address = location_dict[location_index].split('(')[0].strip()
        if address == location_address:
            return location_index


# Loads the distance data from the CSV file
# Time complexity: O(n)
def loadDistanceValues(file_name, matrix):
    with open(file_name) as distance_data:
        distance_data = csv.reader(distance_data, delimiter=',')
        for row in distance_data:
            distance_row = [float(cell) if cell != '' else 0.0 for cell in row]
            matrix.append(distance_row)


# Calculates the distance between the given indexes (which represent addresses
# Time complexity: O(1)
def getDistanceBetween(destination, source):
    source_idx = int(source)  # Make sure we are working with integer values
    destination_idx = int(destination)
    if source_idx == 26:  # The destination and source need to be swapped, since the distance_matrix is 27 x 26
        temp = destination_idx
        destination_idx = source_idx
        source_idx = temp
    distance = float(distance_matrix[destination_idx][source_idx])
    # If the distance wasn't found, swap the indexes. This works because the values are bidirectional
    if distance == 0 or distance is None:
        distance = float(distance_matrix[source_idx][destination_idx])

    return distance
