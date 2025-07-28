import heapq

# TODO: would it be good to make a dictionary that includes the distance as well as the node...?

# Calculate the minimum spanning tree (MST) using Prim's algorithm
def get_mst(nodes_list, distance_graph):
    current_node = 0  # Starting node for the MST
    visited_nodes = set()
    possible_paths = []
    mst = {node.id:set() for node in nodes_list}  # An MST includes all the nodes in the graph. Initialize all the nodes in a dictionary without any connections.
    
    # while we don't have connections between all the nodes. We don't actually need to visit all the nodes for all the nodes to be included.
    while len(visited_nodes) < len(nodes_list) - 1:
        visited_nodes.add(current_node)

        # get the distances stored in the current node
        for destination in mst:
            distance = distance_graph[current_node][destination]
            # do not add nodes connected to themselves or without paths
            if distance != 0 and destination not in visited_nodes:
                possible_paths.append([distance, current_node, destination])

        heapq.heapify(possible_paths)  # the first element will always contain the smallest element

        while possible_paths:
            origin = possible_paths[0][1]
            destination = possible_paths[0][2]
            if destination not in visited_nodes:
                break
            heapq.heappop(possible_paths)
        
        # draw a path between the two nodes that can be accessed through either of them
        mst[origin].add(destination)
        mst[destination].add(origin)

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
            merged[a].add(b)
        if a not in merged[b]:
            merged[b].add(a)    
        
    return merged


# For making the hamiltonian tour
def is_disjoint(node_connection_dict, current_node, complete_node_count):
    visited_nodes = set()
    unvisited_nodes = list(node_connection_dict[current_node]) # stack
    
    while unvisited_nodes:
        if current_node in visited_nodes:
            pass
        else:
            for destination in node_connection_dict[current_node]:
                if destination not in visited_nodes:
                    unvisited_nodes.append(destination)

        visited_nodes.add(current_node)
        current_node = unvisited_nodes.pop()

    return len(visited_nodes) != complete_node_count


# For nodes that have more than two connections, we want to make a direct path between its connections by replacing [(n, x), (n, y)] with [(x, y)]
def reconnect_nodes(node_connection_dict, n, x, y):
    n_is_even = len(node_connection_dict[n]) % 2 == 0
    x_is_even = len(node_connection_dict[x]) % 2 == 0

    if n_is_even:
        node_connection_dict[x].remove(n)
        node_connection_dict[x].add(y)

        node_connection_dict[y].remove(n)
        node_connection_dict[y].add(x)

        node_connection_dict[n].remove(x)
        node_connection_dict[n].remove(y)
    
    # For nodes with uneven edges, we just want to remove one edge
    else:
        node_connection_dict[x].add(y)
        node_connection_dict[y].add(x)
        if x_is_even:
            node_connection_dict[x].remove(n)
            node_connection_dict[n].remove(x)
        else:  # Even if they're both uneven, nothing would change with this result
            node_connection_dict[y].remove(n)
            node_connection_dict[n].remove(y)


# Make a hamiltonian tour out of the Eulerian tour
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
        destination_nodes = list(node_connections[node])
        destination_node_distances = []
        n = len(destination_nodes)
        i = n - 1

        # Getting the distance between each destination node 
        for start_node in destination_nodes:
            # Prevent revisiting the same path several times and make runtime slightly faster with [(n-i):]
            for end_node in destination_nodes[(n-i):]:
                destination_node_distances.append((distance_graph[start_node][end_node], start_node, end_node))  # Distance between start and end nodes
            i -= 1

        heapq.heapify(destination_node_distances)

        # 3) Remove extra paths from the origin node by reconnecting those paths to the destinations with the smallest distance between them
        tried_pairs = set()
        while destination_node_distances:
            start_node = destination_node_distances[0][1]
            end_node = destination_node_distances[0][2]

            pair = tuple(sorted((start_node, end_node)))  # Since edge weights don't depend on which node it starts on
            if pair in tried_pairs:
                heapq.heappop(destination_node_distances)
            tried_pairs.add(pair)

            original_paths = {
                "node": node_connections[node].copy(),
                "start": node_connections[start_node].copy(),
                "end": node_connections[end_node].copy()
            }

            if node != start_node and node != end_node and start_node != end_node:
                reconnect_nodes(node_connections, node, start_node, end_node)

                # Undo changes if disjoint, break if the reconnection was successful
                if is_disjoint(node_connections, start_node, len(node_connections)):
                    node_connections[node] = original_paths["node"]
                    node_connections[start_node] = original_paths["start"]
                    node_connections[end_node] = original_paths["end"]
                else:
                    break 
        
            else:
                print("Skipping invalid or duplicate node pair")
                print(f"The destinations of said pair: {destination_node_distances}")

            heapq.heappop(destination_node_distances)

        # 5) Repeat until the current start node only has two distances (add the node to the set again if the length is still over 2)
        if len(node_connections[node]) > 2:
            nodes_over_two_edges.add(node)

    return node_connections

# Add up the distance of all the paths in the graph to get the weight. Only works with hamiltonian tour graphs.
def get_graph_weight(graph, distance_graph):
    visited = set()
    node = 0
    node_with_end_connection = -1
    weight = 0

    while len(visited) < len(graph):
        visited.add(node)
        connections = list(graph[node])
        destination = connections[0]
        if destination == 0: node_with_end_connection = node
               
        if destination in visited:
            destination = connections[1]
            if destination == 0: node_with_end_connection = node

        if destination in visited:
            break

        weight += distance_graph[node][destination]
        node = destination

    weight += distance_graph[0][node_with_end_connection]
                
    return weight


def christofides(node_number, distance_graph):
    mst = get_mst(node_number, distance_graph)
    mpm = get_mpm(mst, distance_graph)
    eulerian = merge_graphs(mst, mpm)
    best_path = simplify_edges(distance_graph, eulerian)
    weight = get_graph_weight(best_path, distance_graph)

    return (best_path, weight)