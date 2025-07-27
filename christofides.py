import heapq

# TODO: would it be good to make a dictionary that includes the distance as well as the node...?

# Calculate the minimum spanning tree (MST) using Prim's algorithm
def get_mst(nodes_list, distance_graph):
    current_node = 0  # Starting node for the MST
    visited_nodes = set()
    possible_paths = []
    mst = {node.id:[] for node in nodes_list}  # An MST includes all the nodes in the graph. Initialize all the nodes in a dictionary without any connections.
    
    # while we don't have connections between all the nodes. We don't actually need to visit all the nodes for all the nodes to be included.
    while len(visited_nodes) < len(nodes_list) - 1:
        visited_nodes.add(current_node)
        print(f"Current node: {current_node}")

        # get the distances stored in the current node
        for destination in mst:
            distance = distance_graph[current_node][destination]
            # do not add nodes connected to themselves or without paths
            if distance != 0 and destination not in visited_nodes:
                # print(destination)
                possible_paths.append([distance, current_node, destination])

        heapq.heapify(possible_paths)  # the first element will always contain the smallest element

        # print(possible_paths)
        print(visited_nodes)
        print(f"visited nodes length: {len(visited_nodes)} vs., nodes list length: {len(nodes_list)}")

        # origin = possible_paths[0][1]
        # destination = possible_paths[0][2]
        # while destination in visited_nodes:
        #     # print(possible_paths)
        #     heapq.heappop(possible_paths)
        #     if possible_paths:
        #         origin = possible_paths[0][1]
        #         destination = possible_paths[0][2]

        while possible_paths:
            origin = possible_paths[0][1]
            destination = possible_paths[0][2]
            if origin == 6:
                print(f"dest: {destination}, distance: {possible_paths[0][0]}")
            if destination not in visited_nodes:
                break
            heapq.heappop(possible_paths)
        
        # draw a path between the two nodes that can be accessed through either of them
        print(f"adding destination {destination}")
        mst[origin].append(destination)
        mst[destination].append(origin)

        if not possible_paths:
            break

        current_node = destination
        heapq.heappop(possible_paths)
        
    return mst


# Find the minimum weight perfect matching 
def get_mpm(node_graph, distance_graph):
    uneven_nodes = set()  # Nodes with an odd number of edges connecting to them
    bijection = []
    node_distances = []

    # 1) Identify nodes with odd-degree edges 
    for node in node_graph:
        if len(node_graph[node]) % 2 == 1:
            uneven_nodes.add(node)

    # 2) Get distances of each of those nodes
    unseen = uneven_nodes.copy()  # Prevents adding the same path originating from a different node
    for origin in uneven_nodes:
        unseen.remove(origin)
        for destination in unseen:
            distance = distance_graph[origin][destination]
            if distance != 0:
                node_distances.append((distance, origin, destination))

    heapq.heapify(node_distances)

    # 3) Match nodes according to the minimum distance between them
    while uneven_nodes:
        start_node = node_distances[0][1]
        end_node = node_distances[0][2]
    
        # Do not match nodes we already have to satisfy 
        if start_node in uneven_nodes and end_node in uneven_nodes:
            bijection.append((start_node, end_node))
            uneven_nodes.remove(start_node)
            uneven_nodes.remove(end_node)
        
        heapq.heappop(node_distances)

    return bijection


# Merge the MST and MPM (finding an Eulerian tour). MST is a dictionary, MPM is a tuple list.
def merge_graphs(mst, mpm): 
    merged = mst.copy()
    for node_pair in mpm:
        a = node_pair[0]
        b = node_pair[1]

        if b not in mst[a]:
            merged[a].append(b)
        if a not in merged[b]:
            merged[b].append(a)    
        
    return merged


def remove_single_edge_nodes(node_graph, distance_graph):
    distances = []

    for node in node_graph:
        # If a node only has one connection, connect it to the node with the shortest distance between them
        if len(node_graph[node]) == 1:
            for destination in node_graph:
                distance = distance_graph[node][destination]
                if distance != 0:
                    distances.append([distance, destination])

            heapq.heapify(distances)
            heapq.heappop(distances)  # Remove 0
            print("Heapq distances: ", distances)

            destination = distances[0][1]

            # Verify that we're not just adding the same connection twice
            print("the one single connection:", node_graph[node][0])
            while destination == node_graph[node][0]:
                heapq.heappop(distances)
            node_graph[node].append(destination)
            node_graph[destination].append(node)

            distances = []


# For making the hamiltonian tour
def is_disjoint(node_connection_dict, current_node, complete_node_count):
    visited_nodes = set()
    unvisited_nodes = node_connection_dict[current_node].copy()  # stack
    print("unvisited nodes: ", unvisited_nodes)
    
    while unvisited_nodes:
        if current_node in visited_nodes:
            pass
        else:
            for destination in node_connection_dict[current_node]:
                if destination not in visited_nodes:
                    unvisited_nodes.append(destination)

        visited_nodes.add(current_node)
        current_node = unvisited_nodes.pop()

    print("visited nodes: ", visited_nodes)
    print(complete_node_count)
    return len(visited_nodes) != complete_node_count


# For nodes that have more than two connections, we want to make a direct path between its connections by replacing [(n, x), (n, y)] with [(x, y)]
def reconnect_nodes(node_connection_dict, n, x, y):
    print("In reconnect_nodes():", n, x, y)
    if n != x and n != y and x != y:
        node_connection_dict[x].remove(n)
        node_connection_dict[x].append(y)

        node_connection_dict[y].remove(n)
        node_connection_dict[y].append(x)

        node_connection_dict[n].remove(x)
        node_connection_dict[n].remove(y)


# Make a hamiltonian tour out of the Eulerian tour
#TODO see if you can make it work without having to copy the list constantly 
def simplify_edges(distance_graph, eulerian_graph):
    node_connections = eulerian_graph.copy()
    nodes_over_two_edges = set()

    # 1) Find which nodes have more than two paths connected to them
    for node in node_connections:
        if len(node_connections[node]) > 2:
            nodes_over_two_edges.add(node)

    # 2) Get the distances between all the destination nodes and put them in a priority queue 
    while nodes_over_two_edges:
        node = nodes_over_two_edges.pop()
        destination_nodes = node_connections[node]
        destination_node_distances = []
        n = len(destination_nodes)
        i = n - 1
        print("NODE:", node)

        # Getting the distance between each destination node 
        for start_node in destination_nodes:
            # Prevent revisiting the same path several times and make runtime slightly faster with [(n-i):]
            for end_node in destination_nodes[(n-i):]:
                print(f"node: {node}, start node: {start_node}, end node: {end_node}")
                destination_node_distances.append((distance_graph[start_node][end_node], start_node, end_node))  # Distance between start and end nodes
            i -= 1

        heapq.heapify(destination_node_distances)

        # 3) Remove extra paths from the origin node by reconnecting those paths to the destinations with the smallest distance between them
        # start_node = destination_node_distances[0][1]
        # end_node = destination_node_distances[0][2]
        # original_paths = {"node": node_connections[node].copy(), "start": node_connections[start_node].copy(), "end": node_connections[end_node].copy()}

        # reconnect_nodes(node_connections, node, start_node, end_node)

        # while is_disjoint(node_connections, start_node, len(node_connections)):
        #     node_connections[node] = original_paths["node"].copy()
        #     node_connections[start_node] = original_paths["start"].copy()
        #     node_connections[end_node] = original_paths["end"].copy()

        #     print(destination_node_distances)
        #     heapq.heappop(destination_node_distances)
        #     # if not destination_node_distances:
        #     #     break

        #     start_node = destination_node_distances[0][1]
        #     end_node = destination_node_distances[0][2]
        #     original_paths["start"] = node_connections[start_node].copy()
        #     original_paths["end"] = node_connections[end_node].copy()

        #     if node != start_node and node != end_node and start_node != end_node:
        #         print("hello why is this here??")
        #         reconnect_nodes(node_connections, node, start_node, end_node)
        #     else:
        #         heapq.heappop(destination_node_distances)
        tried_pairs = set()

        while destination_node_distances:
            start_node = destination_node_distances[0][1]
            end_node = destination_node_distances[0][2]

            pair = (start_node, end_node)
            if pair in tried_pairs:
                heapq.heappop(destination_node_distances)
                continue  # necessary?
            tried_pairs.add(pair)

            original_paths = {
                "node": node_connections[node].copy(),
                "start": node_connections[start_node].copy(),
                "end": node_connections[end_node].copy()
            }

            if node != start_node and node != end_node and start_node != end_node:
                reconnect_nodes(node_connections, node, start_node, end_node)

                if not is_disjoint(node_connections, start_node, len(node_connections)):
                    break  # Successful reconnection
                else:
                    # Undo changes if disjoint
                    node_connections[node] = original_paths["node"]
                    node_connections[start_node] = original_paths["start"]
                    node_connections[end_node] = original_paths["end"]
            else:
                print("Skipping invalid or duplicate node pair")
                print(f"The destinations of said pair: {destination_node_distances}")

            heapq.heappop(destination_node_distances)

        # 5) Repeat until the current start node only has two distances (add the node to the set again if the length is still over 2)
        if len(node_connections[node]) > 2:
            nodes_over_two_edges.add(node)

    return node_connections

# TODO: this
# Copy and paste the code in is_disjoint and just return the total distance idfk, I actually don't know what the purpose of this one is.
def get_graph_weight(graph, distance_graph):
    visited = set()
    node = 0
    node_with_end_connection = -1
    weight = 0

    while len(visited) < len(graph):
        visited.add(node)
        destination = graph[node][0]
        if destination == 0: node_with_end_connection = node
               
        if destination in visited:
            destination = graph[node][1]
            if destination == 0: node_with_end_connection = node

        # print(destination)
        if destination in visited:
            break

        weight += distance_graph[node][destination]
        node = destination

    weight += distance_graph[0][node_with_end_connection]
                
    return weight


def christofides(node_number, distance_graph):
    mst = get_mst(node_number, distance_graph)
    print("MST:", mst)
    mpm = get_mpm(mst, distance_graph)
    print(mpm)
    eulerian = merge_graphs(mst, mpm)
    remove_single_edge_nodes(eulerian, distance_graph)
    print("EULERIAN")
    for node in eulerian:
        print(node, eulerian[node])
    best_path = simplify_edges(distance_graph, eulerian)
    print("BEST PATH")
    for node in best_path:
        print(node, eulerian[node])
    weight = get_graph_weight(best_path, distance_graph)

    return (best_path, weight)