import heapq

# TODO: you have to sort the distances so often...would it be better to simply sort the distance graph? That would make it unable to retrieve distances in constant time. Maybe another one, then..?
# TODO: Maybe also instead of sort(), you could use heapify() (O(n) instead of O(nlogn))
# TODO: also change stuff from a 2D list to a dictionary (oh maybe not, I need a priority queue for Prim's, anyway)
# ^^ would it be good to make a dictionary that includes the distance as well as the node...?

# Calculate the minimum spanning tree (MST) using Prim's algorithm
def get_mst(nodes_in_graph, distance_graph):
    current_node = 0  # Starting node for the MST
    visited_nodes = set()
    possible_paths = []
    mst = {i:[] for i in range(nodes_in_graph)}  # An MST includes all the nodes in the graph. Initialize all the nodes in a dictionary without any connections.

    # while we have not connected all the nodes
    while len(visited_nodes) < nodes_in_graph - 1:
        # visited_nodes[current_node] = True
        visited_nodes.add(current_node)

        # get the distances stored in the current node
        for i, distance in enumerate(distance_graph[current_node]):
            # do not add nodes connected to themselves or without paths
            if distance != 0:
                possible_paths.append([distance, current_node, i])

        heapq.heapify(possible_paths)  # the first element will always contain the smallest element

        origin = possible_paths[0][1]
        destination = possible_paths[0][2]
        while destination in visited_nodes:
            heapq.heappop(possible_paths)
            origin = possible_paths[0][1]
            destination = possible_paths[0][2]
        
        # draw a path between the two nodes that can be accessed through either of them
        mst[origin].append(destination)
        mst[destination].append(origin)

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
        print(unseen)
        for destination in unseen:
            distance = distance_graph[origin][destination]
            if distance != 0:
                node_distances.append((distance, origin, destination))

    print(f"OG: {node_distances}")
    heapq.heapify(node_distances)
    print(f"1, {node_distances}")

    # 3) Match nodes according to the minimum distance between them
    while uneven_nodes:
        print(uneven_nodes)
        start_node = node_distances[0][1]
        end_node = node_distances[0][2]
    
        # Do not match nodes we already have to satisfy 
        if start_node in uneven_nodes and end_node in uneven_nodes:
            # print(f'Distance ({distance}) between {start_node} and {end_node}')
            bijection.append((start_node, end_node))
            uneven_nodes.remove(start_node)
            uneven_nodes.remove(end_node)
        
        heapq.heappop(node_distances)
        print(f"2, {node_distances}")

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
    visited_nodes = set()
    unvisited_nodes = node_connection_dict[current_node].copy()  # stack
    
    while unvisited_nodes:
        if current_node in visited_nodes:
            pass
        else:
            for destination in node_connection_dict[current_node]:
                if destination not in visited_nodes:
                    unvisited_nodes.append(destination)

        visited_nodes.add(current_node)
        current_node = unvisited_nodes.pop()

    #DELETE
    print(f"nodes in graph: {visited_nodes}, current graph count: {len(visited_nodes)}, OG graph count: 27")

    return len(visited_nodes) != complete_node_count


# For nodes that have more than two connections, we want to replace [(n, x), (n, y)] with [(x, y)]
def reconnect_nodes(node_connection_dict, n, x, y):
    node_connection_dict[x].remove(n)
    node_connection_dict[x].append(y)

    node_connection_dict[y].remove(n)
    node_connection_dict[y].append(x)

    node_connection_dict[n].remove(x)
    node_connection_dict[n].remove(y)


# Make a hamiltonian tour out of the Eulerian tour
#TODO see if you can make it work without having to copy the list constantly 
#TODO return graph (dictionary)
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
            node_connections[a].append(b)
            if len(node_connections[a]) > 2: 
                nodes_over_two_edges.add(a)

        # Initialize the node in the dictionary 
        else:
            node_connections[a] = [b]

        # a and b not being in the dictionary are not mutually exclusive events
        if b in node_connections:
            node_connections[b].append(a)
            if len(node_connections[b]) > 2: 
                nodes_over_two_edges.add(b)
        else:
            node_connections[b] = [a]

    print(f"nodes over two edges: {nodes_over_two_edges}")

    # 2) Get the distances between all the destination nodes
    new_paths = []
    while nodes_over_two_edges:
        node = nodes_over_two_edges.pop()
        destination_nodes = node_connections[node]
        destination_node_distances = []
        n = len(destination_nodes)
        i = n - 1

        print(f"current node: {node}")


        # printing dict, delete once done
        # for key in node_connections:
        #     print(f"key: {key}, end points: {node_connections[key]}")
        # print(nodes_over_two_edges)

        # Getting the distance between each destination node 
        for start_node in destination_nodes:
            # Prevent revisiting the same path several times and make runtime slightly faster with [(n-i):]
            for end_node in destination_nodes[(n-i):]:
                # print(f"start node: {start_node}, end node: {end_node}")
                destination_node_distances.append((distance_graph[start_node][end_node], start_node, end_node))  # Distance between start and end nodes
            i -= 1

        destination_node_distances.sort(reverse=True, key=lambda sub_list: sub_list[0])

        # delete
        # print(f"destination distances: {destination_node_distances}")

        # 3) Replace [(n, x), (n, y)] with [(x, y)]
        start_node = destination_node_distances[-1][1]
        end_node = destination_node_distances[-1][2]
        print(f"(out) node: {node}, start_node: {start_node}, end_node: {end_node}")
        original_paths = {"node": node_connections[node].copy(), "start": node_connections[start_node].copy(), "end": node_connections[end_node].copy()}

        reconnect_nodes(node_connections, node, start_node, end_node)

        print(node_connections[start_node])
        print(node_connections[end_node])

        # of course it's going to be disjoint, it's not getting repaired >:(
        while is_disjoint(node_connections, start_node, len(distance_graph)):
            node_connections[node] = original_paths["node"].copy()
            node_connections[start_node] = original_paths["start"].copy()
            node_connections[end_node] = original_paths["end"].copy()

            destination_node_distances.pop()

            #delete
            print(f"path: {destination_node_distances[-1]}")

            start_node = destination_node_distances[-1][1]
            end_node = destination_node_distances[-1][2]
            original_paths["start"] = node_connections[start_node].copy()
            original_paths["end"] = node_connections[end_node].copy()

            # delete
            print(f"node: {node}, start_node: {start_node}, end_node: {end_node}")
            print(f"CONNECTIONS BEFORE: node: {node_connections[node]}, start_node: {node_connections[start_node]}, end_node: {node_connections[end_node]}")

            reconnect_nodes(node_connections, node, start_node, end_node)

            # delete
            print(f"CONNECTIONS AFTER: node: {node_connections[node]}, start_node: {node_connections[start_node]}, end_node: {node_connections[end_node]}")

        new_paths.append(destination_node_distances[-1])  # For the final graph
                
        # 5) Repeat until the current start node only has two distances (add the node to the set again if the length is still over 2)
        if len(node_connections[node]) > 2:
            nodes_over_two_edges.add(node)

    print(is_disjoint(node_connections, 10, len(distance_graph)))

    # TODO: this
    # Copy and paste the code in is_disjoint and just return the total distance idfk, I actually don't know what the purpose of this one is.
    def traverse_graph():
        pass


    def christophides():
        pass