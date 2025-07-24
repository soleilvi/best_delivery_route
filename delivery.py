import heapq

from timemod import TimeMod
from package_hash import PackageHash
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
                if time.is_less_than(late_truck.depart_time) or time.is_equal_to(late_truck.depart_time):
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
            for package in set:
                if early_truck.has_package(package):
                    early_truck.load_packages(set)
                    deliver_together.remove(set)
                    break
                elif late_truck.has_package(package):
                    late_truck.load_packages(set)
                    deliver_together.remove(set)
                    break

        # 4) Add package based on time priority. Since packages_to_deliver is a priority queue based on delivery time, we just need to worry about whether the truck is full.
        if not note:  # Making sure the package was not removed previously
            if not early_truck.is_full():
                early_truck.load_package(package)
            elif not late_truck.is_full():
                late_truck.load_package(package) 

        heapq.heappop(packages_to_deliver)


# Choosing paths taking into account delivery deadlines and packages that need to be linked together
def choose_delivery_route(packages: list):
    special_packages = set()
    
    # 3) Implement the special instructions that come with the packages
    # 4) Return the paths for each truck 
    

# Show update messages and track time with this
def deliver_packages(route: dict, distances: list, truck: Truck):
    time = TimeMod()
    current_node = 0
    previous_node = -1
    next_node = route[current_node][0]
    total_distance = 0
    
    while next_node != 0:
        # 1) Add distance to total_distance
        total_distance +=  distances[current_node][next_node]

        # 2) Unload packages

        # 3) Translate distance to time
        time.distance_to_time(total_distance, truck.SPEED)

        # 4) Show message
        print(f"Delivered package (package_id) (on time, late, etc) to (place) at {time.time_to_str}")

        # 5) Reconnect nodes
        previous_node = current_node
        current_node = next_node
        for destination in route[current_node]:
            if destination != previous_node:
                next_node = destination
                break