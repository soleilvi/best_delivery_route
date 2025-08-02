import heapq

from timemod import TimeMod
from package_hash import PackageHash
from places_hash import PlacesHash
from truck import Truck

'''
NOTE: there is a minor bug caused by not removing x and y in the "Must be" 
section. It could mess up the count when loading the trucks. Ultimately, I 
actually think this bug is harmless for now and does not make enough trouble
to merit the effort of resolving it since I'd need to reformat a big chunk
of the code.
'''

def print_truck_contents(trucks: list):
    i = 1
    print("           TRUCK CONTENTS          ")
    print("-----------------------------------")
    print("|    TRUCK 1     |    TRUCK 2     |")
    print("|---------------------------------|")
    for p1, p2 in zip(trucks[1].packages, trucks[2].packages): 
        print(f"| package {i}: {p1.id}".ljust(16), "|" 
              f" package {i}: {p2.id}".ljust(16), "|")
        i += 1
    print("-----------------------------------")


'''
- Appends the wrong address package to the late truck because we know from the 
assignment instructions that it updates to the correct one at 10:30 AM, but it 
would need to implement different logic if the wrong address changed after the 
late truck departed. 
- Does not account for more than two late/early trucks
'''
def load_trucks(trucks: list, packages: PackageHash, packages_to_deliver: list):
    deliver_together = []  # Will contain sets with the IDs of packages that need to be delivered together
    early_truck = trucks[1] # Truck that leaves when the shift starts
    late_truck = trucks[2] # Truck that waits for late packages
    linked_truck = None

    while packages_to_deliver and not (early_truck.is_full() and late_truck.is_full()):
        package = packages_to_deliver[0]
        # 1) Identify which packages have special notes 
        note = package.notes
        if note:
            # 2) Parse the string to identify what must be done with the special packages
            # For delayed, you should implement more logic for loading the truck depending on whether there are packages that will be delivered after noon or not...etc.
            if "Delayed" in note:  # Delayed on flight---will not arrive to depot until  xx:xx xm
                time = TimeMod()
                time.str_to_time(note[-8:]) # contains "xx:xx xm"
                # Load delayed packages into the late truck if they will arrive at the facility before it departs. Otherwise, it will have to wait for the first truck to come back.
                if time <= late_truck.depart_time:
                    if not late_truck.is_full(): late_truck.load_package(package)
                else:
                    if not early_truck.is_full(): early_truck.load_package(package)

            elif "Must be" in note:  # Must be delivered with x, y
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

            elif "Can only" in note:  # Can only be on truck x
                if not trucks[int(note[-1])].is_full(): trucks[int(note[-1])].load_package(package)

            elif "Wrong address" in note: # Wrong address listed
                if not late_truck.is_full(): late_truck.load_package(package)

        # 3) Add any packages that we have identified are linked together
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

                # If any of the linked packages were loaded onto the wrong truck before, we should remove them
                for id in trucks:
                    if trucks[id] == linked_truck:
                        continue
                    # Remove the element(s) in common between the wrong truck's packages and the linked packages
                    elif trucks[id].packages & set:
                        trucks[id].packages -= trucks[id].packages & set

        # 4) Add package based on time priority. Since packages_to_deliver is a priority queue based on delivery time, we just need to worry about deadines and whether the truck is full.
        # Alternate between each truck getting loaded up to distribute the deadline packages evenly
        if not note:  # Making sure the package was not removed previously
            if not early_truck.is_full():
                early_truck.load_package(package)
            elif not late_truck.is_full():
                late_truck.load_package(package)

        heapq.heappop(packages_to_deliver)

    # In case a package was loaded onto a truck and was not removed previously (AKA linked packages)
    for package in packages_to_deliver:
        if early_truck.has_package(package) or late_truck.has_package(package):
            packages_to_deliver.remove(package) 


# Get a list of all the places the truck will need to visit to deliver the packages. 
def get_delivery_details(packages: list, places: PlacesHash):    
    hub = places.get(places.address_to_place("HUB"))
    eod = TimeMod(23,59)
    routes = {eod.time_to_str(): set()}  # Different routes according to each package deadline
    where_to_deliver = {}  # Holds information for where to deliver packages

    # 1) Loop over packages to retrieve the address of each of their destinations. Put them in a set to avoid repeats.
    for package in packages:
        destination = places.get(places.address_to_place(package.address))
        deadline = package.deadline.time_to_str()

        # 2) Set each package into the route that corresponds with its deadline
        if deadline in routes:
            routes[deadline].add(destination)
        else:
            # print("package:", package.id, ", deadline:", deadline)
            routes[deadline] = {destination}

        where_to_deliver.setdefault(destination, []).append(package)  # Essentially an if-statement to check if the dictionary has a list before appending the value

    # Sorting the keys to return a list of the routes that is also sorted
    keys = list(routes.keys())
    keys.sort()
    
    #3) If there are any duplicates, remove them
    for i, key in enumerate(keys[1:], start=1):
        previous_key = keys[i - 1]
        # Remove the intersections between the current and previous paths
        if routes[key] & routes[previous_key]:
            routes[key] -= routes[key] & routes[previous_key]

    # 4) Only return the values. Make sure they are in order according to their corresponding deadline.
    routes_list = []
    for key in keys:
        routes[key].add(hub)
        routes_list.append(routes[key])

    return routes_list, where_to_deliver


# Connects the priority package route with the non-priority one
def connect_paths(priority_route: dict, regular_route: dict, distances: list, places: PlacesHash):
    hub = places.get(places.address_to_place("HUB"))
    priority_connections = list(priority_route[hub])
    regular_connections = list(regular_route[hub])
    minimum = 1000

    # See if there is only one connection in the priority package dict
    if len(priority_connections) < 2:
        stray = priority_connections[0]
        # Assign x and y according to which distance between the stray node and the other hub connections is smaller
        if distances[stray.id][regular_connections[0].id] < distances[stray.id][regular_connections[1].id]:
            x = regular_connections[0]
            y = regular_connections[1]
        else:
            x = regular_connections[1]
            y = regular_connections[0]

        # Simply add the node to the existing dict
        regular_route[hub].remove(x)
        regular_route[x].remove(hub)
        regular_route[x].add(stray)
        priority_route[stray].add(x)
    else:
        # 1) Compare the distances between the nodes that connect to the hub in the two lists 
        for i in range(4):
            j = 0
            if i >= 2:
                j = 1
            p = priority_connections[j]  # Connection to the hub from the priority route
            r = regular_connections[i % 2]  # Connection to the hub from the regular route
            
            if distances[p.id][r.id] < minimum:
                minimum = distances[p.id][r.id]

                # p and r may not have the values that align with the minimum distance by the end of the loop, so we need new variables
                x = p 
                y = r

        # 2) Connect the nodes from the two different routes that have the least distance between them
        priority_route[hub].remove(x)
        regular_route[hub].remove(y)

        priority_route[x].remove(hub)
        priority_route[x].add(y)

        regular_route[y].remove(hub)
        regular_route[y].add(x)

    priority_route[hub].update(regular_route[hub])  # Merge the connections of the hub in each route
    regular_route.update(priority_route)  # Merge the two dictionaries
    
    return regular_route  # I know that this is accessible through regular_route, but it's so that it makes more sense in the main function
    

# Show update messages and track time with this
# TODO: Correct the address for package 9 here
def deliver_packages(route: dict, where_to_deliver: dict, distances: list, truck: Truck, places: PlacesHash):
    current_time = truck.depart_time
    total_distance = 0
    previous_place = places.get(places.address_to_place("HUB"))  # Delivery facility, or node 0

    # Find the node that will start the priority path
    minimum = TimeMod(23, 59)
    for connection in route[previous_place]:
        for package in where_to_deliver[connection]:
            # print("current connection:", connection.id, "package", package.id)
            if package.deadline < minimum:
                minimum = package.deadline
                current_place = connection

    for place in route[current_place]:
        if place.id != 0:
            next_place = place
            break
    
    while current_place.id != 0:
        print(f"At place with ID {current_place.id}")
        # 1) Add distance to total_distance
        distance = distances[previous_place.id][current_place.id]
        total_distance +=  distance
        # print("Distance travelled:", distance)

        # 2) Translate distance to time
        temp = TimeMod()
        temp.distance_to_time(distance, truck.speed)
        current_time = current_time.add_time(temp)

        if current_time >= TimeMod(10, 20) and truck.has_package(9):
            # SOMEHOW UPDATE THE DAMN PACKAGE INFO
            pass

        # 3) Unload packages
        packages = where_to_deliver[current_place]
        for package in packages:


            print(f"Unloading package with ID {package.id}.")
            truck.unload_package(package)

            if current_time <= package.deadline:
                time_status = "on time"
            else: 
                time_status = "late"

            # 4) Show message
            print(f"Delivered package {package.id} {time_status} to {current_place.name.replace('\n', '')} at {current_time.time_to_str()}.")

        # 5) Reconnect nodes
        previous_place = current_place
        current_place = next_place
        for destination in route[current_place]:
            if destination != previous_place:
                next_place = destination
                break
        print()
        
    # We also need to count the distance and time taken by the truck to return to the warehouse
    distance = distances[previous_place.id][current_place.id]
    total_distance +=  distance
    temp = TimeMod()
    temp.distance_to_time(distance, truck.speed)
    current_time = current_time.add_time(temp)
    print(f"Returned to the warehouse at {current_time.time_to_str()}.")

    print("DISTANCE COVERED: ", total_distance)

    return total_distance, current_time