from delivery import *

packages_to_deliver = {1, 2, 3, 4, 5, 6, 7, 8}
trucks = {1: Truck(1, TimeMod(8, 0)), 2: Truck(2, TimeMod(9, 30))}

length = 4

while packages_to_deliver:
        truck_to_load = len(packages_to_deliver) % length + 1
        package = packages_to_deliver.pop()
        print(f"truck to load {truck_to_load}")
        print(f"other: {truck_to_load % length + 1}")
        # if not trucks[truck_to_load].is_full():
        #     trucks[truck_to_load].load_package(package)
        # elif not trucks[(truck_to_load + 1) + 1]: 
        #     trucks[(truck_to_load + 1) + 1].load_package(package)