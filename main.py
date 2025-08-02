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

distance_graph = load_distance_graph(places)

total_distance_travelled = 0
j = 0
while packages_to_deliver:
    if trucks[1].is_empty() and trucks[2].is_empty():
        load_trucks(trucks, package_hash, packages_to_deliver)
        print_truck_contents(trucks)
    truck = trucks[(j % 2) + 1]  # Alternating between trucks
    route_info = get_delivery_details(truck.packages, places_hash)
    where_to_unload = route_info[1]

    routes = []
    for i, route in enumerate(route_info[0]):
        routes.append(christofides(route, distance_graph, places_hash))

    if len(routes) > 1:
        for i in range(1, len(routes)):
            if i == 1:
                full_route = connect_paths(routes[i - 1], routes[i], distance_graph, places_hash)
            else:
                full_route = connect_paths(routes[i], full_route, distance_graph, places_hash)
    else:
        full_route = routes[0]

    # Uncomment to see the graph that represents the route the truck will take. 
    # print(f"TRUCK {truck.id} ROUTE:")
    # for place in full_route:
    #     print(f"{place.id}: ", end="")
    #     for i, p in enumerate(full_route[place]):
    #         if i < len(full_route[place]) - 1:
    #             print(f"{p.id}, ", end="")
    #         else:
    #             print(p.id)

    print(f"TRUCK {truck.id} DELIVERY:")
    update_info = deliver_packages(full_route, where_to_unload, distance_graph, truck, places_hash)
    total_distance_travelled += update_info[0]
    truck.depart_time = update_info[1]

    j += 1

print(f"TOTAL DISTANCE: {total_distance_travelled} miles")
