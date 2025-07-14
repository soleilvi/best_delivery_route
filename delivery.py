from timemod import TimeMod
from truck import Truck

# Choosing paths taking into account delivery deadlines and packages that need to be linked together
def choose_path():
    pass

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
        time.distance_to_time(total_distance, truck.speed)

        # 4) Show message
        print(f"Delivered package (package_id) (on time, late, etc) to (place) at {time.format_time}")

        # 5) Reconnect nodes
        previous_node = current_node
        current_node = next_node
        for destination in route[current_node]:
            if destination != previous_node:
                next_node = destination
                break