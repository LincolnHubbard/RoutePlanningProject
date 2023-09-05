import datetime
import Hash
import Package
from Locations import loadLocationData, getLocationIndex, getDistanceBetween, loadDistanceValues, distance_matrix
from Package import loadPackageData
from Truck import Truck, returnTruckToHub


# truck_1.getDeliveryStatus(packages, time)2
# truck_2.getDeliveryStatus(packages, time)
# truck_3.getDeliveryStatus(packages, time)

# Returns the delivery status for ALL packages
# Time complexity of O(n)
def getDeliveryStatusAtTime(time):
    for i in range(1, 41):
        Package.getPackageInfoAtTime(packages.search(i), time)


# The implementation of the nearest neighbor algorithm
# *** Time complexity of O(n*m) ***
# Implementation based on code provided by Dr Cemal Tepe as provided by WGU staff, cited below
# Tepe, C. (2022). C950 - Webinar-2 - Getting Greedy, who moved my data - Complete Python Code.
# https://srm--c.vf.force.com/apex/coursearticle?Id=kA03x000000e1g4CAA
def simulateDeliveries(truck):
    truck_route = {}  # This dictionary will store location indexes and lists of associated packages
    current_address = 0  # Trucks should always be leaving from the WGUPS hub at index 0
    delivery_address = None  # Needs to be initialized here in order to remove it from truck_route later

    # First all the addresses for the packages the truck needs to deliver, store them in truck_route
    for package in truck.packages:
        index = getLocationIndex(package.address, locations)
        if index not in truck_route:
            truck_route[index] = [package]  # Create a list to handle multiple packages at one address
        else:
            # If this code is reached, then there is more than one package to be delivered to this address
            truck_route[index].append(package)

    # Then find the package with the closest delivery address, and don't stop until the truck is empty
    while truck.isTruckEmpty() is not True:
        min_distance = float('inf')  # Has to be reset everytime a new address needs to be chosen

        # Iterate through all packages left to deliver and find the closest delivery address
        for address, pack_list in truck_route.items():
            distance = getDistanceBetween(address, current_address)  # 'current_address' refers to the truck's location
            if min_distance > distance > 0:
                min_distance = distance
                delivery_address = address

        # Retrieve the packages that need to be delivered at this address
        if delivery_address is not None:  # Check to make sure delivery address actually has a value
            packages_to_deliver = truck_route[delivery_address]
            # Deliver each package individually (In real life drivers scan each package separately when dropping off)
            for package in packages_to_deliver:
                truck.deliverPackage(package, min_distance)
                min_distance = 0  # If more packages are being delivered at this address, don't add more miles to truck

        # Set the truck's current location to the delivery address, then remove it from the route
        current_address = delivery_address
        truck_route.pop(delivery_address)

    # Once the truck is empty, take it back home. This NEEDS to be called so that the return trip is calculated
    # in the mileage for the truck
    if truck.isTruckEmpty():
        returnTruckToHub(truck, current_address)


packages = Hash.ChainingHashTable()  # Create the table of packages, and populate it with the data from the CSV file
loadPackageData('package_file.csv', packages)

# Create a dictionary of locations and load in data from the related CSV file
locations = {}
loadLocationData('location_file.csv', locations)
# Load in values for the distance matrix
loadDistanceValues('distance_values.csv', distance_matrix)

# Create each truck object and assign departure times
# The following resource was referenced when working with datetime values
# Python Software Foundation. (2002). Datetime — Basic Date and Time Types — Python 3.7.2 Documentation.
# Python.org. https://docs.python.org/3/library/datetime.html
truck_1 = Truck('Truck 1', datetime.timedelta(hours=9, minutes=5))
truck_2 = Truck('Truck 2', datetime.timedelta(hours=8))
truck_3 = Truck('Truck 3', datetime.timedelta(hours=10, minutes=30))  # Leaves after truck 2 returns @ 10:27

# Assign packages by ID to the manifest list for each truck
truck_1.manifest.extend([1, 2, 6, 7, 25, 26, 28, 29, 30, 31, 32, 33, 40])
truck_2.manifest.extend([3, 5, 12, 13, 14, 15, 16, 18, 19, 20, 21, 34, 36, 37, 38, 39])
truck_3.manifest.extend([4, 8, 9, 10, 11, 17, 22, 23, 24, 27, 35])

# Actually load the packages onto each truck
truck_1.loadPackages(packages)
truck_2.loadPackages(packages)
truck_3.loadPackages(packages)

# Simulate deliveries (In other words, call the nearest neighbor algorithm)
simulateDeliveries(truck_1)
simulateDeliveries(truck_2)
# Update address for package 9. Happens before truck 3 departs @ 10:30AM, after truck 2 returns @ 10:27
package_9 = packages.search(9)
package_9.address = '410 S State St'
package_9.zip = 84111
simulateDeliveries(truck_3)

# Calculate total mileage to display on the main menu
total = truck_1.mileage + truck_2.mileage + truck_3.mileage

# Loop for the main menu
while True:
    print('-' * 50)
    print('         WGUPS ROUTING PROGRAM MAIN MENU')
    print('Total mileage: ' + str(total))  # TOTAL MILEAGE WILL BE PRINTED HERE
    print('-' * 50)
    print('Press 1 to search for a package by ID')
    print('Press 2 to view delivery status at a specific time')
    print('Press 3 to quit program')
    user_input = input()
    if user_input == '1':
        # Allow user to search for a package by ID
        while True:
            id_to_search = int(input('Please enter the package ID: \n'))
            print(packages.search(id_to_search))
            return_input = input('Return to menu? Y/N\n')
            if return_input.lower() == 'y':
                break
            elif return_input.lower() == 'n':
                print('Goodbye')
                quit()
            else:
                print('Invalid input, please try again\n')
    elif user_input == '2':
        # Allow user to display ALL package statuses at a specific time
        while True:
            time_input = input("Enter time (hours:minutes): \n")
            # Extracting time values from input happens in this try-catch block in case user input is invalid
            try:
                hours, minutes = map(int, time_input.split(':'))
                print('Press 1 to view all packages, or 2 to view a specific package:')
                selection_choice = int(input())
                if selection_choice == 1:
                    getDeliveryStatusAtTime(datetime.timedelta(hours=hours, minutes=minutes))
                elif selection_choice == 2:
                    id_to_search = int(input('Please enter the package ID: \n'))
                    pack_buffer = packages.search(id_to_search)
                    Package.getPackageInfoAtTime(pack_buffer, datetime.timedelta(hours=hours, minutes=minutes))
            except ValueError:
                print('Invalid input, please try again')
            # Ask user if they would like to return to the main menu
            return_input = input('Return to menu? Y/N\n')
            if return_input.lower() == 'y':
                break
            elif return_input.lower() == 'n':
                print('Goodbye')
                quit()
            else:
                print('Invalid input, please try again')
    elif user_input == '3':
        # Let user quit out of program and break the loop
        print('Goodbye')
        quit()
    else:
        # Will keep being called until the user inputs a valid value
        print('Invalid input, please try again')
