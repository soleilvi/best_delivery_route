'''
Student ID: 011029940
Created by Soleil Vivero Rivera on August 2nd, 2025
'''

import csv
import heapq

from classes.package import Package
from classes.place import Place
from classes.truck import Truck
from classes.places_hash import PlacesHash
from classes.package_hash import PackageHash
from classes.timemod import TimeMod

from christofides import *
from delivery import *

def load_package_data(file_path: str):
    """Returns a list of Package objects initialized from a csv file."""
    
    packages = []

    with open(file_path, 'r') as file:
        data = csv.reader(file, delimiter=',')

        # Skip the next 8 lines of the CSV file.
        for num in range(8):
            next(data) 

        for row in data:
            new_package = Package(int(row[0]), row[1], row[2], row[3], 
                                  row[4], row[5], row[6], row[7])
            packages.append(new_package)
    return packages


def load_distance_data(file_path: str):
    """Returns a list of Place objects initialized from a csv file."""
    places = []
    place_id = 0
    # Represents how many distances are associated with each place in 
    # distance_data.
    distances_counter = 1

    with open(file_path, 'r') as file:
        data = csv.reader(file, delimiter=',')

        # Skip the next 8 lines of the CSV file.
        for num in range(8):
            next(data) 

        for row in data:
            new_place = Place(place_id, row[0], row[1])
            
            for i in range(distances_counter):
                # + 1 for the row, and another +1 to compensate for the fact 
                # that i starts at 0.
                new_place.distances.append(row[i + 2])

            places.append(new_place)
            distances_counter += 1
            place_id += 1
    return places


def load_distance_graph(place_list: list):
    """Makes a symmetric 2D matrix from the distance attribute of each place 
    in the list."""
    
    graph = []
    for place in place_list:
        row = [float(distance) for distance in place.distances]

        # Loading the rest of the distances from the column that corresponds 
        # to the place ID
        for destination in place_list[place.id + 1:]:
            row.append(float(destination.distances[place.id]))
        graph.append(row)
    
    return graph


# Keep in mind that the size of each hash should be adjusted according to the 
# average number of packages delivered in a day and the types of addresses 
# that come up most frequently.
package_hash = PackageHash(45)  # Average number of packages in a day + 5.
places_hash = PlacesHash(1000)  # Could be 100 depending on collisions.

packages = load_package_data('./data/package_data.csv')
places = load_distance_data('./data/distance_data.csv')
trucks = {1: Truck(1, TimeMod(8, 0)), 2: Truck(2, TimeMod(9, 30))}

package_hash.load(packages)
places_hash.load(places)
distance_graph = load_distance_graph(places)

# Making a priority queue that sorts the packages by their deadline.
packages_to_deliver = []
for package in packages:
    packages_to_deliver.append(package)
heapq.heapify(packages_to_deliver)

total_distance_travelled = 0
j = 0
while packages_to_deliver:
    if trucks[1].is_empty() and trucks[2].is_empty():
        load_trucks(trucks, package_hash, packages_to_deliver)
        print_truck_contents(trucks)

    # Alternate between trucks each time the loop repeats. We're concentrating
    # on one delivery at a time, even if the trucks are technically delivering
    # packages at the same time.
    truck = trucks[(j % 2) + 1]

    route_info = get_delivery_details(truck.packages, places_hash)
    where_to_unload = route_info[1]

    # This separates the routes into chunks according to each package 
    # deadline. For each group of packages with the same deadline, it will get 
    # the best route for just that group and put it in a list.
    routes = []
    for i, route in enumerate(route_info[0]):
        routes.append(christofides(route, distance_graph, places_hash))

    # Now we join each deadline group together, making the full route.
    if len(routes) > 1:
        for i in range(1, len(routes)):
            if i == 1:
                full_route = connect_paths(routes[i - 1], routes[i], 
                                           distance_graph, places_hash)
            else:
                full_route = connect_paths(routes[i], full_route, 
                                           distance_graph, places_hash)
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
    update_info = deliver_packages(full_route, where_to_unload, 
                                   distance_graph, truck, places_hash)
    total_distance_travelled += update_info[0]
    truck.depart_time = update_info[1]

    print("Total distance covered by all trucks: "
          f"{total_distance_travelled} miles.\n")

    j += 1

