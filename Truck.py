import datetime
import Package
from Locations import getDistanceBetween


class Truck:
    # Time complexity: O(1)
    def __init__(self, truck_name, depart_time):
        self.truck_name = truck_name
        self.packages = []  # Packages currently on the truck
        self.manifest = []  # Packages the truck should depart with
        self.depart_time = depart_time  # Should be set when calling constructor
        self.current_time = depart_time  # Used to track delivery times
        self.mileage = 0

    # Override __str__ method so that the truck ID prints instead of a raw pointer value. For debugging purposes
    def __str__(self):
        return "%s" % self.truck_name

    # Time complexity: O(1)
    def isTruckEmpty(self):
        return not self.packages

    # Time complexity: O(n)
    def printRemainingPackages(self):  # for debugging purposes
        pack_strings = []
        for p in self.packages:
            pack_strings.append(str(p))

        print(pack_strings)

    # Time complexity: O(n)
    # Loads all packages from the manifest onto the truck
    def loadPackages(self, package_table):
        for package_id in self.manifest:
            package = package_table.search(package_id)
            package.depart_time = self.depart_time
            self.packages.append(package)

    # Deliver the package, removing it from the truck's inventory and updating mileage + time
    # Time complexity: O(n)
    def deliverPackage(self, package_to_deliver, distance):
        delivery_success = False
        # Find the package we are delivering in the truck's inventory
        for package in self.packages:
            if package.package_id == package_to_deliver.package_id:
                package.status = Package.PackageStatus.DELIVERED  # Set the package's delivery status
                self.packages.remove(package)
                delivery_success = True
                break  # Break out of for loop since we found the package

        # Update the truck's mileage and current time
        self.mileage += distance
        self.current_time += datetime.timedelta(minutes=(distance / 18) * 60)
        package_to_deliver.time_delivered = self.current_time

        # Mostly for debugging purposes, if this prints then the method needs to be fixed
        if delivery_success is False:
            print('Package ID', package_to_deliver.package_id, 'NOT FOUND ON', self.truck_name)

    # Print the delivery status of ALL packages the truck delivered
    # Time complexity: O(n)
    def getDeliveryStatus(self, package_list, time):
        package_statuses = []
        # Search the MANIFEST, not the inventory
        for package_id in self.manifest:
            package = package_list.search(package_id)
            if time < self.depart_time or time == self.depart_time:
                package_statuses.append(' Package #' + str(package.package_id) + ' AT HUB')
            elif self.depart_time < time < package.time_delivered:
                package_statuses.append(' Package #' + str(package.package_id) + ' IN TRANSIT')
            elif time > package.time_delivered:
                package_statuses.append(
                    ' Package #' + str(package.package_id) + ' DELIVERED AT ' + str(package.time_delivered))

        # Print both truck name and package statuses to make the output clearer to the user
        print(self.truck_name, package_statuses)


# This method is necessary to include the truck's return trip in its total mileage and return time
def returnTruckToHub(truck, current_address):
    # 0 can be passed in as the destination since it will always be returning back to the hub
    distance = getDistanceBetween(0, current_address)
    truck.mileage += distance
    truck.current_time += datetime.timedelta(minutes=(distance / 18) * 60)
