"""
Contains the functions that handle anything relating to the delivery route and 
packages that go in each truck.
"""

import heapq
from itertools import zip_longest

from classes.timemod import TimeMod
from classes.package_hash import PackageHash
from classes.places_hash import PlacesHash
from classes.truck import Truck


def print_truck_contents(trucks: list):
    """Formats the contents of the trucks and prints their contents."""

    i = 1
    print("           TRUCK CONTENTS          ")
    print("-----------------------------------")
    print("|    TRUCK 1     |    TRUCK 2     |")
    print("|---------------------------------|")
    for p1, p2 in zip_longest(trucks[1].packages, trucks[2].packages): 
        p1_str = f"package {i}: {p1.id}" if p1 is not None else " " 
        p2_str = f"package {i}: {p2.id}" if p2 is not None else " "
        print(f"| {p1_str.ljust(14)} | {p2_str.ljust(14)} |")
        i += 1
    print("-----------------------------------")


def load_trucks(trucks: list, packages: PackageHash, packages_to_deliver: list):
    """Loads package objects into each truck's packages attribute.

    Packages are loaded into each truck according to their delivery deadline 
    and the instructions outlined in their delivery notes. Since WGUPS can 
    only use two trucks at a time in Salt Lake City, I set one to be the 
    "early" truck that leaves when the shift starts, and the other one to be 
    the "late" truck that leaves after the delayed packages arrive to the 
    facility. Notes are given priority over the delivery deadline when 
    deciding into which truck a package should be loaded since some packages 
    need to be loaded into a specific truck. Packages that need to be 
    delivered together ("linked" packages) are put together in a set and later 
    put into whichever truck is first identified as having one of the linked 
    packages.
    
    As it is, this function does not account for having more than two trucks 
    in use, so future developers would have to heavily edit this function to 
    make it work with their trucks if they plan to use more than two at a 
    time. In addition, "wrong address" packages are simply added to the late 
    truck because it's the assignment that specifies when the address will 
    change, not any document that we can parse. The logic for this would need 
    to change if the time at which the address gets updated appeared in a 
    document we could parse.
    """

    # deliver_together will contain sets with the IDs of the linked packages.
    deliver_together = [] 
    early_truck = trucks[1]
    late_truck = trucks[2]
    linked_truck = None

    while packages_to_deliver and not (early_truck.is_full() 
                                       and late_truck.is_full()):
        package = packages_to_deliver[0]
        # 1) Identify which packages have special notes and parse their string 
        #    to identify what must be done with them.
        note = package.notes
        if note:
            # Delayed on flight---will not arrive to depot until hh:mm XM
            if "Delayed" in note:
                time = TimeMod()
                time.str_to_time(note[-8:]) # contains "hh:mm XM"

                # The reason why we check the early truck first is because it 
                # arrives back to the facility before the late truck. Delayed 
                # packages will never arrive to the facility before the start 
                # of the shift, so they are initially loaded into the late 
                # truck. However, once the trucks arrive back to the facility, 
                # their departure time is updated. Checking the early truck 
                # first prevents the late truck from having to go out to 
                # deliver a single package.
                if time <= early_truck.depart_time:
                    if not early_truck.is_full(): 
                        early_truck.load_package(package)
                else:
                    if not late_truck.is_full(): 
                        late_truck.load_package(package)

            # Must be delivered with x, y
            elif "Must be" in note: 
                x = packages.get_through_id(int(note[-6:-4]))
                y = packages.get_through_id(int(note[-2:]))
                if deliver_together:
                    for set in deliver_together:
                        if (x in set) or (y in set) or (package in set):
                            set.add(package)
                            set.add(x)
                            set.add(y)
                        else:
                            deliver_together.append({package, x, y})
                else: 
                    deliver_together.append({package, x, y})

            # Can only be on truck x
            elif "Can only" in note:
                if not trucks[int(note[-1])].is_full(): 
                    trucks[int(note[-1])].load_package(package)

            # Wrong address listed
            elif "Wrong address" in note:
                if not late_truck.is_full(): late_truck.load_package(package)

        # 3) Add any packages that we have identified are linked together.
        for set in deliver_together:
            if linked_truck is None:
                for package in set:
                    if early_truck.has_package(package):
                        early_truck.load_packages(set)
                        deliver_together.remove(set)
                        linked_truck = early_truck
                        break
                    elif late_truck.has_package(package):
                        late_truck.load_packages(set)
                        deliver_together.remove(set)
                        linked_truck = late_truck
                        break
            elif not linked_truck.is_full():
                linked_truck.load_packages(set)

                # Remove any linked packages that were previously loaded into 
                # the wrong truck.
                for id in trucks:
                    if trucks[id] == linked_truck:
                        continue

                    # Remove the element(s) in common between the wrong 
                    # truck's packages and the linked packages.
                    elif trucks[id].packages & set:
                        trucks[id].packages -= trucks[id].packages & set

        # 4) Add package based on time priority. Since packages_to_deliver is 
        #    a priority queue based on delivery time, we just need to worry 
        #    about deadines and whether the truck is full. Alternate between 
        #    each truck getting loaded up to distribute the deadline packages 
        #    evenly.
        if not note:  # Making sure the package was not loaded previously.
            if not early_truck.is_full():
                early_truck.load_package(package)
            elif not late_truck.is_full():
                late_truck.load_package(package)

        heapq.heappop(packages_to_deliver)

    # In case a package was loaded onto a truck and was not removed
    # previously (AKA linked packages).
    for package in packages_to_deliver:
        if early_truck.has_package(package) or late_truck.has_package(package):
            packages_to_deliver.remove(package) 


def get_delivery_details(packages: list, places: PlacesHash):
    """Determines which places the truck needs to visit to deliver all of its 
    packages. 
    
    Gets the delivery address information from each package to know which 
    places the truck needs to visit to deliver all its packages. To ensure 
    that each package is delivered on time, it groups the places it needs to 
    visit according to the package deadlines. Later on, we find the most 
    efficient route for each of these groups and assemble them together to 
    make the full route. This function returns a tuple with a list of the 
    routes and a dictionary that helps tie each package to a Place object.
    """

    hub = places.get(places.address_to_place("HUB"))
    eod = TimeMod(23,59)
    routes = {eod.time_to_str(): set()}  # Each deadline gets its own route
    where_to_deliver = {}  # Key = delivery place, values = list of packages

    # 1) Loop over packages to retrieve the address of each of their 
    #    destinations. Put them in a set to avoid repeats.
    for package in packages:
        destination = places.get(places.address_to_place(package.address))
        deadline = package.deadline.time_to_str()

        # 2) Set each package into the route that corresponds with its 
        #    deadline.
        if deadline in routes:
            routes[deadline].add(destination)
        else:
            routes[deadline] = {destination}

        where_to_deliver.setdefault(destination, []).append(package)

    # Sorting the keys so that routes_list is also sorted based on package 
    # deadlines, despite routes_list not having that information.
    keys = list(routes.keys())
    keys.sort()
    
    #3) If there are any duplicates, remove them.
    for i, key in enumerate(keys[1:], start=1):
        previous_key = keys[i - 1]
        # Remove the intersections between the current and previous paths
        if routes[key] & routes[previous_key]:
            routes[key] -= routes[key] & routes[previous_key]

    # 4) Only return the values of the dictionary.
    routes_list = []
    for key in keys:
        routes[key].add(hub)
        routes_list.append(routes[key])

    return routes_list, where_to_deliver


def connect_paths(route1: dict, route2: dict, distances: list, 
                  places: PlacesHash):
    """Connects the routes with different delivery deadlines together.
    
    After each of the groups in routes_list returned by get_delivery_details() 
    are put through christofides(), they need to be connected together to make 
    up the full route for the delivery. We do this by finding the shortest 
    path between the nodes that need to be reconnected (the hub and two of the 
    places to which it is connected). If there is only one place connected to 
    the hub in one of the groups, simply integrate it into the larger route. 
    This function returns the merged route.
    """
    
    hub = places.get(places.address_to_place("HUB"))
    r1_connections = list(route1[hub])
    r2_connections = list(route2[hub])
    minimum = 1000

    # 1) Determine whether there is only one connection in either of the 
    #    routes
    if len(r1_connections) < 2:
        stray = r1_connections[0]
        # Assign x and y according to which distance between the stray node 
        # and the other hub connections is smaller.
        if (distances[stray.id][r2_connections[0].id] 
            < distances[stray.id][r2_connections[1].id]):
            x = r2_connections[0]
            y = r2_connections[1]
        else:
            x = r2_connections[1]
            y = r2_connections[0]

        # Simply add the node to the existing dict.
        route2[hub].remove(x)
        route2[x].remove(hub)
        route2[x].add(stray)
        route1[stray].add(x)

    elif len(r2_connections) < 2:
        stray = r2_connections[0]
        if (distances[stray.id][r1_connections[0].id] 
            < distances[stray.id][r1_connections[1].id]):
            x = r1_connections[0]
            y = r1_connections[1]
        else:
            x = r1_connections[1]
            y = r1_connections[0]

        route1[hub].remove(x)
        route1[x].remove(hub)
        route2[x].add(stray)
        route2[stray].add(x)
        
    # 2) If not, compare the distances between the nodes that connect to the 
    #    hub in the two lists.
    else:
        for i in range(4):
            j = 0
            if i >= 2:
                j = 1
            r1 = r1_connections[j]      # Connection to the hub from route1
            r2 = r2_connections[i % 2]  # Connection to the hub from route2
            
            if distances[r1.id][r2.id] < minimum:
                minimum = distances[r1.id][r2.id]

                # r1 and r2 may not have the values that align with the 
                # minimum distance by the end of the loop, so we need new 
                # variables.
                x = r1 
                y = r2

        # 2) Connect the nodes from the two different routes that have the 
        #    least distance between them.
        route1[hub].remove(x)
        route2[hub].remove(y)

        route1[x].remove(hub)
        route1[x].add(y)

        route2[y].remove(hub)
        route2[y].add(x)

    # Merge the connections of the hub in each route
    route1[hub].update(route2[hub])
    # Merge the two dictionaries
    route2.update(route1)
    
    return route2
    

def deliver_packages(route: dict, where_to_deliver: dict, distances: list,
                     truck: Truck, places: PlacesHash):
    """Visits each place in the delivery route, unloads the necessary 
    packages, and shows update messages at each stop.

    Once again, the logic that handles packages with a wrong address is 
    simplified because we already know which package it is and at what time 
    its address gets updated. Future developers would need to change that 
    logic if they did not know what packages have a wrong address and at what 
    time their addresses are updated.
    """

    current_time = truck.depart_time
    total_distance = 0
    previous_place = places.get(places.address_to_place("HUB"))  # Node 0
    current_place = None

    # 1) Find the node that will start the priority path (earliest deadline)
    minimum = TimeMod(23, 59)
    for i, connection in enumerate(route[previous_place]):
        for package in where_to_deliver[connection]:
            if package.deadline < minimum:
                minimum = package.deadline
                current_place = connection
        # If both connections have EOD as their deadlines
        if i == len(route[previous_place]) - 1 and current_place is None:
            current_place = connection
            
    for place in route[current_place]:
        if place.id != 0:
            next_place = place
            break
    
    # For the "wrong address" package 
    if truck.has_package(9):
        change_address = True
    else:
        change_address = False

    while current_place.id != 0:
        print(f"At place with ID {current_place.id}")
        # 2) Add distance to total_distance
        distance = distances[previous_place.id][current_place.id]
        total_distance +=  distance

        # 3) Translate distance to time
        temp = TimeMod()
        temp.distance_to_time(distance, truck.speed)
        current_time = current_time.add_time(temp)

        # Update the address of the "wrong address" package
        if current_time >= TimeMod(10, 20) and change_address:
            package_to_change = truck.get_package(9)
            old_place = places.address_to_place(package_to_change.address)
            where_to_deliver[old_place].remove(package_to_change)

            package_to_change.address = "410 S State St"
            new_place = places.address_to_place(package_to_change.address)
            where_to_deliver[new_place].append(package_to_change)
            
            change_address = False

        # 4) Unload packages
        packages = where_to_deliver[current_place]
        for package in packages:
            print(f"Unloading package with ID {package.id}.")
            truck.unload_package(package)

            if current_time <= package.deadline:
                time_status = "on time"
            else: 
                time_status = "late"

            # 5) Show message
            print(f"Delivered package {package.id} {time_status} to "
                  f"{current_place.name.replace('\n', '')} at "
                  f"{current_time.time_to_str()}.")

        # 6) Reconnect nodes
        previous_place = current_place
        current_place = next_place
        for destination in route[current_place]:
            if destination != previous_place:
                next_place = destination
                break
        print()  # Line break to make update messages look cleaner
        
    # We also need to count the distance and time taken by the truck to return 
    # to the warehouse
    distance = distances[previous_place.id][current_place.id]
    total_distance +=  distance
    temp = TimeMod()
    temp.distance_to_time(distance, truck.speed)
    current_time = current_time.add_time(temp)
    print(f"Returned to the warehouse at {current_time.time_to_str()}.")

    print(f"Distance covered by truck {truck.id}: {total_distance} miles.")

    return total_distance, current_time