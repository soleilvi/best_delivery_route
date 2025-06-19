import csv
from package import Package
from place import Place

package_hash = [None] * 35  # Set the size of the hash table to the average number of packages + 5
places_hash = [None] * 36  # not sure yet

def load_package_data(file_path):
    packages = []

    with open(file_path, 'r') as file:
        data = csv.reader(file, delimiter=',')

        # Skip the next 8 lines of the CSV file
        for num in range(8):
            next(data) 

        for row in data:
            new_package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            packages.append(new_package)
    return packages

# keep in mind that the size of the list should be adjusted to the average number of packages if adjusting for another city
def load_hash(package_list, hash_list):
    for package in package_list:
        key = int(package.id)
        index = (key - 1) % len(hash_list)  # Division method for hashing
        
        # Initialize with the package if the bucket is empty
        if hash_list[index] is None:
            hash_list[index] = [package]

        # Collision handling (chaining)
        else:
            hash_list[index].append(package)

def load_distance_data(file_path):
    places = []
    counter = 0

    with open(file_path, 'r') as file:
        data = csv.reader(file, delimiter=',')

        # Skip the next 8 lines of the CSV file
        for num in range(8):
            next(data) 

        for row in data:
            new_place = Place(counter, row[0], row[1])
            places.append(new_place)
            counter += 1
    return places

packages = load_package_data('./data/package_data.csv')
places = load_distance_data('./data/distance_data.csv')

for place in places:
    print(f'Id: {place.id}, Name: {place.name}, Address: {place.address}')

# Print hash
# load_hash(packages, package_hash)
# for i, bucket in enumerate(package_hash):
#     if bucket is not None:
#         if isinstance(bucket, list):
#             for package in bucket:
#                 print(f"Hash Index: {i}, Package ID: {package.id}, Address: {package.address}, City: {package.city}, State: {package.state}, Zip: {package.zip}, Deadline: {package.deadline}, Weight: {package.weight}, Notes: {package.notes}")
#         else:
#             print(f"Hash Index: {i}, Package ID: {bucket.id}, Address: {bucket.address}, City: {bucket.city}, State: {bucket.state}, Zip: {bucket.zip}, Deadline: {bucket.deadline}, Weight: {bucket.weight}, Notes: {bucket.notes}")
#     else:
#         print(f"Hash Index: {i} is empty.")