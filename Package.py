import csv
from enum import Enum


# The following resource was referenced when implementing enum class
# Python Software Foundation. (2002). enum — Support for enumerations — Python 3.7.2 Documentation.
# Python.org. https://docs.python.org/3/library/enum.html
class PackageStatus(Enum):
    AT_HUB = 'AT_HUB'
    IN_TRANSIT = 'IN_TRANSIT'
    DELIVERED = 'DELIVERED'


class Package:

    def __init__(self, id, addr, city, state, zip, deadline, weight, notes):
        self.package_id = id
        self.address = addr
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.special_notes = notes
        self.status = PackageStatus.AT_HUB
        self.time_delivered = None
        self.depart_time = None

    # Override __str__ function so that the actual values are printed instead of raw pointers
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.package_id, self.address, self.city, self.state, self.zip,
            self.deadline, self.time_delivered, self.weight, self.special_notes, self.status.value)


# Loads all the data for each package from the CSV file
# Time complexity: O(n)
def loadPackageData(file_name, package_table):
    with open(file_name) as package_data:
        package_data = csv.reader(package_data, delimiter=',')
        next(package_data)  # Remove if not skipping the header
        for package in package_data:
            pId = int(package[0])
            pAddr = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDl = package[5]
            pWeight = package[6]
            pNotes = package[7]

            package = Package(pId, pAddr, pCity, pState, pZip, pDl, pWeight, pNotes)

            package_table.insert(package, pId)


# Prints the delivery status of a SINGLE package at the given time
# Time complexity O(1)
def getPackageInfoAtTime(package, time):
    if time < package.depart_time or time == package.depart_time:
        if package.package_id == 9:
            package.address = '300 State St'
        package.status = PackageStatus.AT_HUB
        print(package)
        #print(' Package #' + str(package.package_id) + ' AT HUB. DELIVERY ADDRESS: ' + package.address)
    elif package.depart_time < time < package.time_delivered:
        if package.package_id == 9:
            package.address = '410 S State St'
            package.zip = 84111
        package.status = PackageStatus.IN_TRANSIT
        print(package)
        #print(' Package #' + str(package.package_id) + ' IN TRANSIT')
    elif time > package.time_delivered:
        if package.package_id == 9:
            package.address = '410 S State St'
            package.zip = 84111
        package.status = PackageStatus.DELIVERED
        print(package)
        #print(' Package #' + str(package.package_id) + ' DELIVERED AT ' + str(package.time_delivered),
              #'TO ' + package.address)
