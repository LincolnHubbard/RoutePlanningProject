# Implementation based on code provided by Dr Cemal Tepe as provided by WGU staff, cited below
# Tepe, C. (2022). C950 - Webinar-1 - Let’s Go Hashing - Complete Python Code.
# https://srm--c.vf.force.com/apex/coursearticle?Id=kA03x000000e1fuCAA
class ChainingHashTable:
    # Only 10 buckets really necessary for 40 packages, but this can easily be changed to support more packages
    def __init__(self, size=10):
        self.table = []
        # Create an empty list in each bucket
        for i in range(size):
            self.table.append([])

    # Only called by the loadPackageData function in 'Package.py'
    def insert(self, item, key):
        bucket = hash(key) % len(self.table)  # Generate hash value from key
        bucket_list = self.table[bucket]  # Get the list from that 'bucket'

        # Update key if it is in the bucket's list
        for key_index in bucket_list:
            if key_index[0] == key:
                key_index[1] = item
                return True

        # Otherwise add package to the end of the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Will return the package if it is found, or None if it is not
    def search(self, key):
        # First find the bucket + list where the key would be
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Iterate through this bucket list to find the item
        for key_index in bucket_list:
            if key_index[0] == key:
                return key_index[1]  # Finally return the package

        # If the code reaches this point, the package was not found
        return None

    def remove(self, key):
        # Find our bucket + list to remove the package from
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # If found, then remove the package
        for key_index in bucket_list:
            if key_index[0] == key:
                bucket_list.remove([key_index[0], key_index[1]])
