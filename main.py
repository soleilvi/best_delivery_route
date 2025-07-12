import csv
from package import Package
from place import Place
from christophides import *

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

# keep in mind that the size of the list should be adjusted to the average number of packages if adjusting for another city
def load_package_hash(package_list, hash_list):
    for package in package_list:
        key = int(package.id)
        index = (key - 1) % len(hash_list)  # Division method for hashing
        
        # Initialize with the package if the bucket is empty
        if hash_list[index] is None:
            hash_list[index] = [package]

        # Collision handling (chaining)
        else:
            hash_list[index].append(package)

# assumes that any address apart from the hub starts with either 3 or 4 number digits 
# depending on how many collisions there are in your data set, you may want to use the first 3 digits or the last 3 digits. 
def load_places_hash(place_list, hash_list):
    for place in place_list:
        key = ''.join(num for num in place.address[:4] if num.isdigit()) # Extract the first 3 digits of the address as a key. The first digit is a space.
        if key == '':  # This is for the hub 
            key = 0
        else:
            key = int(key)
            
        index = key % len(hash_list)  # Division method for hashing
        
        # Initialize with the place if the bucket is empty
        if hash_list[index] is None:
            hash_list[index] = [place]

        # Collision handling (chaining)
        else:
            # print("collision detected")  # for determining index insertion method
            hash_list[index].append(place)

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


package_hash = [None] * 35  # Set the size of the hash table to the average number of packages + 5
places_hash = [None] * 1000 

packages = load_package_data('./data/package_data.csv')
places = load_distance_data('./data/distance_data.csv')

distance_graph = load_distance_graph(places)

# print("GRAPH")
# for row in distance_graph:
#     print(row)

mst = get_mst(len(places), distance_graph)
mpm = get_mpm(mst, distance_graph)
# merged = merge_graphs(mst, mpm)

# mst.sort()
# mpm.sort()
# merged.sort()

print(mst)
print(f"mst size: {len(mst)}")
print(mpm)
# print(f"mpm size: {len(mpm)}")
# print(merged)
# print(f"merged size: {len(merged)}")

# final = simplify_edges(distance_graph, merged)

# for place in places:
#     print(f'Id: {place.id}, Name: {place.name}, Address: {place.address}')

# Print packages hash
# load_package_hash(packages, package_hash)
# for i, bucket in enumerate(package_hash):
#     if bucket is not None:
#         if isinstance(bucket, list):
#             for package in bucket:
#                 print(f"Hash Index: {i}, Package ID: {package.id}, Address: {package.address}, City: {package.city}, State: {package.state}, Zip: {package.zip}, Deadline: {package.deadline}, Weight: {package.weight}, Notes: {package.notes}")
#         else:
#             print(f"Hash Index: {i}, Package ID: {bucket.id}, Address: {bucket.address}, City: {bucket.city}, State: {bucket.state}, Zip: {bucket.zip}, Deadline: {bucket.deadline}, Weight: {bucket.weight}, Notes: {bucket.notes}")
#     else:
#         print(f"Hash Index: {i} is empty.")

# Print places hash
# for i, bucket in enumerate(places_hash):
#     if bucket is not None:
#         for place in bucket:
#             print(f'in bucket. Index = {i}')
#             print(f'Id: {place.id}, Name: {place.name}, Address: {place.address}')