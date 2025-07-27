import csv
import heapq

from package import Package
from place import Place
from truck import Truck
from places_hash import PlacesHash
from package_hash import PackageHash
from timemod import TimeMod

from christofides import *
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
            new_package = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
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
packages_to_deliver = []

for package in packages:
    packages_to_deliver.append(package)
heapq.heapify(packages_to_deliver)  # Priority queue that sorts the packages by deadline.
# for package in packages_to_deliver:
#     print(package.id, package.deadline.time_to_str())

distance_graph = load_distance_graph(places)
# Print distance table
print("    ", end="")
for i, row in enumerate(distance_graph):
    if i < len(distance_graph) - 2:
        print(i, " ", end="")
    else:
        print(i, " ")
for i, row in enumerate(distance_graph):
    print(i, ": ", row)

load_trucks(trucks, package_hash, packages_to_deliver)
# print_truck_contents(trucks)
truck1_route = get_delivery_route(trucks[1].packages, places_hash)

# for place in truck1_route:
#     print(f'Id: {place.id}, Name: {place.name}, Address: {place.address}')
    
chris = christofides(truck1_route, distance_graph)
print("CHRISTOFIDES")
for node in chris[0]:
    print(f"{node}: {chris[0][node]}")
print(f"Weight: {chris[1]}")

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
