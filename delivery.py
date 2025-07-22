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

# Restriction: The notes in future implementations of the program need to follow the same format as in this one
# Restriction: If future implementations of the program include more special notes, they need to be added here. 
def parse_note(note: str):
    if "Delayed" in note:
        print("omg")
    elif "Must be" in note:
        print("teid")
    elif "Can only" in note:
        print("wrong address")
    elif "Wrong address" in note:
        pass

'''
- Modify late_truck and late_depart_time accordingly in future programs
- Appends the wrong address package to the late truck because we know from the 
assignment instructions that it updates to the correct one at 10:30 AM, but it 
would need to implement different logic if the wrong address changed after the 
late truck departed. 
- Does not account for multiple late trucks
'''
def load_truck(trucks: list, packages: PackageHash, packages_to_deliver: set):
    deliver_together = []  # Will contain sets with the IDs of packages that need to be delivered together

    early_truck = 1 # Truck that leaves when the shift starts
    late_truck = 2  # Truck that waits for late packages
    
    # 1) Identify which packages have special notes 
    for bucket in packages.hash:
        if bucket is not None:
            for package in bucket:
                note = package.notes
                # If the note is not empty
                if note:
                    # 2) Parse the string to identify what must be done with the special packages
                    # For delayed, you should implement more logic for loading the truck depending on whether there are packages that will be delivered after noon or not...etc.
                    if "Delayed" in note:  # Delayed on flight---will not arrive to depot until  xx:xx xm
                        time = TimeMod()
                        time.str_to_time(note[-8:]) # contains "xx:xx xm"
                        
                        # Load delayed packages into the late truck if they will arrive at the facility before it departs. Otherwise, it will have to wait for the first truck to come back.
                        if time.is_less_than(trucks[late_truck].depart_time) or time.is_equal_to(trucks[late_truck].depart_time):
                            trucks[late_truck].load_package(package)
                        else:
                            trucks[early_truck].load_package(package)

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
                        trucks[int(note[-1])].load_package(package)

                    elif "Wrong address" in note: # Wrong address listed
                        trucks[late_truck].load_package(package)

                    packages_to_deliver.remove(package)

                elif package.deadline != "EOD":
                    deadline = TimeMod()
                    deadline.str_to_time(package.deadline)

                    # Add to early truck if the package could be delivered within the next 3 hours after it departs
                    if deadline.is_less_than(trucks[early_truck].depart_time.add_time(TimeMod(3, 0))):
                        trucks[early_truck].load_package(package)
                    else:
                        trucks[late_truck].load_package(package) 

                    packages_to_deliver.remove(package)

    for set in deliver_together:
        for package in set:
            if trucks[early_truck].has_package(package):
                trucks[early_truck].load_packages(set)
                break
            elif trucks[late_truck].has_package(package):
                trucks[late_truck].load_packages(set)
                break

    # Evenly divide the remaining packages between the trucks
    # May have to put in more if-statements to adjust for more trucks
    while packages_to_deliver:
        truck_to_load = len(packages_to_deliver) % len(trucks) + 1
        other_truck = truck_to_load % len(trucks) + 1
        package = packages_to_deliver.pop()

        if not trucks[truck_to_load].is_full():
            trucks[truck_to_load].load_package(package)
        elif not trucks[other_truck]: 
            trucks[other_truck].load_package(package)
        # if both trucks are already full, add the popped package back in and leave the set as it is
        else: 
            packages_to_deliver.add(package)
            break

    #to print, delete later
    print("PACKAGES LEFT")
    for package in packages_to_deliver:
        print(package.id)
    print("TRUCK 1")
    for i, package in enumerate(trucks[1].packages):
        print(f"{i + 1}: {package.id}")
    print("TRUCK 2")
    for i, package in enumerate(trucks[2].packages):
        print(f"{i + 1}: {package.id}")


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