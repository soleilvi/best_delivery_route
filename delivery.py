from timemod import TimeMod
from package_hash import PackageHash
from truck import Truck

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
def load_truck(trucks: list, number_of_trucks: int, packages: PackageHash, packages_to_deliver: set):
    # deliver_together = {}
    # print(packages_to_deliver)
    deliver_together = []  # Will contain sets with the IDs of packages that need to be delivered together

    early_truck = 1 # Truck that leaves when the shift starts
    late_truck = 2  # Truck that waits for late packages
    
    # 1) Identify which packages have special notes 
    for i, bucket in enumerate(packages.hash):
        if bucket is not None:
            for package in bucket:
                note = package.notes
                print(f"currently on: {package.id}")
                # If the note is not empty
                if note:
                    print(note)
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
                        # 1) What if it isn't in the hash anymore? 
                        x = packages.get_through_id(int(note[-6:-4]))
                        y = packages.get_through_id(int(note[-2:]))
                        # x = int(note[-6:-4])
                        # y = int(note[-2:]) 

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

                        # for truck in trucks.values():
                        #     if truck.has_package(x):
                        #         print(f"This is x: {x}")
                        #         truck.load_package(package)
                        #         truck.load_package(y)
                        #         packages_to_deliver.remove(package)
                        #         packages_to_deliver.remove(package.get_through_id(y))
                        #     elif truck.has_package(y):
                        #         print(f"This is y: {y}")
                        #         truck.load_package(package)
                        #         truck.load_package(x)
                        #         packages_to_deliver.remove(package)
                        #         packages_to_deliver.remove(package.get_through_id(x))

                        # Link each package together in a dictionary. setdefault removes the need to use an if-statement to check if the key is in the dictionary.
                        # deliver_together.setdefault(package, set()).update({x, y})
                        # deliver_together.setdefault(x, set()).update({package, y})
                        # deliver_together.setdefault(y, set()).update({package, x})

                        # if p_id = 

                    elif "Can only" in note:  # Can only be on truck x
                        trucks[int(note[-1])].load_package(package)

                    elif "Wrong address" in note: # Wrong address listed
                        trucks[late_truck].load_package(package)

                    packages_to_deliver.remove(package)

                elif package.deadline != "EOD":
                    deadline = TimeMod()
                    deadline.str_to_time(package.deadline)
                    # truck_to_load = 0
                    # acceptable = trucks[early_truck].add_time(3, 0)

                    # Add to early truck if the package could be delivered within the next 3 hours after it departs
                    if deadline.is_less_than(trucks[early_truck].depart_time.add_time(TimeMod(3, 0))):
                        trucks[early_truck].load_package(package)
                        # truck_to_load = early_truck
                    else:
                        trucks[late_truck].load_package(package) 
                        # truck_to_load = late_truck

                    # if package in deliver_together:
                    #     trucks[truck_to_load].load_packages(deliver_together[package])
                    #     deliver_together.remove(package)

                    packages_to_deliver.remove(package)

    # delete
    for i, set in enumerate(deliver_together):
        print(f"deliver together set {i + 1}: {set}")
    
    for set in deliver_together:
        for package in set:
            print(f"deliver together package: {package.id}")
            if trucks[early_truck].has_package(package):
                trucks[early_truck].load_packages(set)
                break
            elif trucks[late_truck].has_package(package):
                trucks[late_truck].load_packages(set)
                break

        # for truck in trucks.values():
        #     print(f"package: {package.id}")
        #     if truck.has_package(packages.get(package)):
        #         for dependent_package in deliver_together[package]:
        #             truck.load_package(packages.get(package))
        #             deliver_together[dependent_package].remove(package)
        #             packages.remove(dependent_package)
            # if packages[package_id] is not None:  # Remove this too
            #     if truck.has_package(packages[package_id][0]):  # TODO: Later replace this with a get_package() function from the hash, oh god
            #         for dependent_package_id in deliver_together[package_id]:
            #             if packages[dependent_package_id] is not None:
            #                 truck.load_package(packages[dependent_package_id][0])  # This one too
            #                 deliver_together[dependent_package_id].remove(package_id)
            #                 packages[dependent_package_id].remove(packages[dependent_package_id][0]) # And this one
            #                 if not packages[dependent_package_id]:
            #                     packages[dependent_package_id] = None                
    
    #to print, delete later
    for package in packages_to_deliver:
        print(package.id)
    print("TRUCK 1")
    for package in trucks[1].packages:
        print(package.id)
    print("TRUCK 2")
    for package in trucks[2].packages:
        print(package.id)

    # # Evenly divide the remaining packages between the trucks
    # len(packages) % number_of_trucks:
    #     if not trucks[i].is_full():
    #         trucks[i].packages.append(package)


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