# Calculate the minimum spanning tree (MST) using Prim's algorithm
# TODO: implement graph
def get_mst(places_list):
    current_node = 0  # Starting node for the MST
    visited_nodes = [False] * len(places_list)  # Each index in the list represents a different place. Once it is visited, it turns into True.
    possible_paths = []
    mst = []

    while len(mst) < len(places_list) - 1:  # while mst is not full 
        visited_nodes[current_node] = True

        # get the distances stored in the current node
        for i, distance in enumerate(places_list[current_node].distances):
            if visited_nodes[i] is False:  # optimize algorithm a bit by excluding paths to nodes we have already visited 
                possible_paths.append((float(distance), current_node, i))
        # get the rest of the distances from the column that corresponds to the ID number of the current node
        for i in range(current_node + 1, len(places_list)):
            if visited_nodes[i] is False:
                possible_paths.append((float(places_list[i].distances[current_node]), current_node, i))

        possible_paths.sort(reverse=True, key=lambda sub_list: sub_list[0])  # sorting from greatest distance to smallest according to the first element (edge weight) of each sub-list
        # print(possible_paths)

        destination = possible_paths[-1][2]
        is_new_node = False  # the destination is a node in visited_nodes
        while not is_new_node:
            # if the node we are visiting is not already in the MST graph
            if visited_nodes[destination] is False:
                mst.append((possible_paths[-1][1], destination))
                current_node = destination
                possible_paths.pop()
                is_new_node = True 
                
            # if the node we are visiting has already been visited 
            else:
                possible_paths.pop()
                destination = possible_paths[-1][2]
        
        # print(f'mst after: {mst}')
        # print(f'current node: {current_node}')

    return mst


# find the minimum weight perfect matching 
def get_mpm(node_graph, distance_graph):
    uneven_nodes = set()  # Holds nodes that have uneven edges connecting to them
    bijection = []
    node_distances = []

    # 1) Identify nodes with odd-degree edges 
    for row in node_graph:
        # Only repeats twice
        for node in row:
            if node not in uneven_nodes:
                uneven_nodes.add(node)
            else:
                uneven_nodes.remove(node)

    # 2) Get distances of each of those nodes
    for node in uneven_nodes:
        for i, distance in enumerate(distance_graph[node]):
            if i in uneven_nodes and distance != 0.0:
                node_distances.append((distance, node, i))

    node_distances.sort(reverse=True, key=lambda tuple: tuple[0])
    # print(node_distances)

    # 3) Match nodes according to the minimum distance between them
    while uneven_nodes:
        # distance = node_distances[-1][0]
        start_node = node_distances[-1][1]
        end_node = node_distances[-1][2]
    
        # Do not match nodes we already have to satisfy 
        if start_node in uneven_nodes and end_node in uneven_nodes:
            # print(f'Distance ({distance}) between {start_node} and {end_node}')
            bijection.append((start_node, end_node))
            uneven_nodes.remove(start_node)
            uneven_nodes.remove(end_node)
            # print(uneven_nodes)
        
        # Two pops because the node distances are repeated
        node_distances.pop()
        node_distances.pop()

    return bijection


# Merge the MST and MPM (finding an Eulerian tour)
def merge_graphs(long_graph, short_graph):
    merged_graph = set()

    # In case the graphs are accidentally switched around 
    if len(long_graph) < len(short_graph):
        placeholder = long_graph
        long_graph = short_graph
        short_graph = placeholder

    for node_pair in long_graph:
        merged_graph.add(node_pair)
    for node_pair in short_graph:
        a = node_pair[0]
        b = node_pair[1]

        # Prevents duplicate edges that have the nodes switched around
        if (b, a) not in merged_graph:
            merged_graph.add(node_pair)
        
    return list(merged_graph)


# For making the hamiltonian tour
def is_disjoint(node_connection_dict, current_node, complete_node_count):
    nodes_in_graph = {current_node}
    circuit_completed = False
    next_node = -1
    connecting_nodes_in_graph = 0

    while not circuit_completed:
        for connecting_node in node_connection_dict[current_node]:
            # delete once finished
            # print(f"current node: {current_node}, connecting node: {connecting_node}, next node: {next_node}")
            # print(nodes_in_graph)
            
            if connecting_node in nodes_in_graph:
                connecting_nodes_in_graph += 1
            else:
                next_node = connecting_node

            # We have visited both nodes, which means that it's a complete circuit
            if connecting_nodes_in_graph == len(node_connection_dict[current_node]):
                circuit_completed = True
                break

            nodes_in_graph.add(connecting_node)
        current_node = next_node
        connecting_nodes_in_graph = 0

    return len(nodes_in_graph) != complete_node_count


# Make a hamiltonian tour out of the Eulerian tour
def simplify_edges(distance_graph, eulerian_graph):
    # Dictionary instead of a 2D array since reading the nodes won't be in order -> rows are not in the correct order 
    # Will have the 26 entries in it
    node_connections = {}
    nodes_over_two_edges = set()

    # 1) Iterate over the list, append each destination node to a list that goes in a dictionary with the start node as the key
    # REMOVE EDGES HERE???? Wouldn't work since the indexes would get all messed up 
    for node_pair in eulerian_graph:
        a = node_pair[0]
        b = node_pair[1]

        if a in node_connections:
            node_connections[a].add(b)
            if len(node_connections[a]) > 2: 
                nodes_over_two_edges.add(a)

        # Initialize the node in the dictionary 
        else:
            node_connections[a] = {b}

        # a and b not being in the dictionary are not mutually exclusive events
        if b in node_connections:
            node_connections[b].add(a)
            if len(node_connections[b]) > 2: 
                nodes_over_two_edges.add(b)
        else:
            node_connections[b] = {a}

    # 2) Get the distances between all the destination nodes
    new_paths = []
    while nodes_over_two_edges:
        node = nodes_over_two_edges.pop()
        # node_edges = []
        min_distance = 100000  # arbitrarily large number that I doubt a city could contain in miles
        path = None

        # Getting the distances from the distance graph according to the intersection between the node and the destination node
        for start_node in node_connections[node]:
            for end_node in node_connections[node]:
                distance = distance_graph[start_node][end_node]
                if start_node != end_node:
                    # Connect the minimum distance and prevent selecting an already existing connection
                    if distance < min_distance and end_node not in node_connections[start_node]:
                        min_distance = distance
                        path = (start_node, end_node)

        # # delete
        print(f"node: {node}")
        # print(min_distance)
        # print(distance_graph[node])

        # 3) Replace [(n, x), (n, y)] with [(x, y)]
        # Reconnecting node 1
        node_connections[path[0]].remove(node)
        node_connections[path[0]].add(path[1])

        # Reconnecting node 2
        node_connections[path[1]].remove(node)
        node_connections[path[1]].add(path[0])

        # Removing node 1 and 2 from the current node's destination list
        node_connections[node].remove(path[0])
        node_connections[node].remove(path[1])

        new_paths.append(path)  # For the final graph

        # printing dict, delete once done
        for key in node_connections:
            print(f"key: {key}, end points: {node_connections[key]}")
        print(nodes_over_two_edges)
                
        # 5) Repeat until the current start node only has two distances (add the node to the set again if the length is still over 2)
        if len(node_connections[node]) > 2:
            nodes_over_two_edges.add(node)

    print(is_disjoint(node_connections, 10, len(distance_graph)))