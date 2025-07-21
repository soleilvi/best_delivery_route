import csv
from package import Package
from place import Place
from truck import Truck
from package_hash import PackageHash
from places_hash import PlacesHash
from christophides import *
from delivery import *

# You need one truck to leave late to wait for the packages that are late. Truck 1 is the "early" truck, while truck 2 is the "late" truck.
# Send the other one to deliver all the packages 

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

def load_distance_data(file_path):
    places = []
    place_id = 0
    distances_counter = 1  # represents how many distances are associated with each place in distance_data

    with open(file_path, 'r') as file:
        data = csv.reader(file, delimiter=',')

        # Skip the next 8 lines of the CSV file
        for num in range(8):
            next(data) 

        for row in data:
            new_place = Place(place_id, row[0], row[1])
            
            for i in range(distances_counter):
                new_place.distances.append(row[i + 2])  # + 1 for the row, and another +1 to compensate for the fact that i starts at 0

            # print(new_place.id, new_place.distances)
            places.append(new_place)
            distances_counter += 1
            place_id += 1
    return places

# The distance graph needs to be a symmetric graph 
def load_distance_graph(place_list):
    graph = []
    for place in place_list:
        row = [float(distance) for distance in place.distances]

        # Loading the rest of the distances from the column that corresponds to the place ID
        for destination in place_list[place.id + 1:]:
            row.append(float(destination.distances[place.id]))
        graph.append(row)
    
    return graph


package_hash = PackageHash(45) # keep in mind that the size of the list should be adjusted to the average number of packages if adjusting for another city
places_hash = PlacesHash(1000)

packages = load_package_data('./data/package_data.csv')
places = load_distance_data('./data/distance_data.csv')
trucks = {1: Truck(1, TimeMod(8, 0)), 2: Truck(2, TimeMod(9, 30))}

package_hash.load(packages)
places_hash.load(places)
packages_to_deliver = set()

for package in packages:
    packages_to_deliver.add(package)

distance_graph = load_distance_graph(places)

load_truck(trucks, len(trucks), package_hash, packages_to_deliver)
# print(package_hash)
# chris= christophides(len(places), distance_graph)

# for place in places:
#     print(f'Id: {place.id}, Name: {place.name}, Address: {place.address}')

# # Print packages hash
# for i, bucket in enumerate(package_hash.hash):
#     if bucket is not None:
#         if isinstance(bucket, list):
#             for package in bucket:
#                 print(f"Hash Index: {i}, Package ID: {package.id}, Address: {package.address}, City: {package.city}, State: {package.state}, Zip: {package.zip}, Deadline: {package.deadline}, Weight: {package.weight}, Notes: {package.notes}")
#         else:
#             print(f"Hash Index: {i}, Package ID: {bucket.id}, Address: {bucket.address}, City: {bucket.city}, State: {bucket.state}, Zip: {bucket.zip}, Deadline: {bucket.deadline}, Weight: {bucket.weight}, Notes: {bucket.notes}")
#     else:
#         print(f"Hash Index: {i} is empty.")
# # Ensure get() works
# for package in packages:
#     pee = package_hash.get(package)
#     print(pee.id)

# # Print places hash
# for i, bucket in enumerate(places_hash.hash):
#     if bucket is not None:
#         for place in bucket:
#             print(f'in bucket. Index = {i}')
#             print(f'Id: {place.id}, Name: {place.name}, Address: {place.address}')
# # Ensure get() works
# for place in places:
#     pee = places_hash.get(place)
#     print(pee.id)