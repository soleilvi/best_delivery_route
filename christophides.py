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
                possible_paths.append([float(distance), current_node, i])
        # get the rest of the distances from the column that corresponds to the ID number of the current node
        for i in range(current_node + 1, len(places_list)):
            if visited_nodes[i] is False:
                possible_paths.append([float(places_list[i].distances[current_node]), current_node, i])

        possible_paths.sort(reverse=True, key=lambda sub_list: sub_list[0])  # sorting from greatest distance to smallest according to the first element (edge weight) of each sub-list
        # print(possible_paths)

        destination = possible_paths[-1][2]
        is_new_node = False  # the destination is a node in visited_nodes
        while not is_new_node:
            # if the node we are visiting is not already in the MST graph
            if visited_nodes[destination] is False:
                mst.append([possible_paths[-1][1], destination])
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
                node_distances.append([distance, node, i])

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
            bijection.append([start_node, end_node])
            uneven_nodes.remove(start_node)
            uneven_nodes.remove(end_node)
            # print(uneven_nodes)
        
        # Two pops because the node distances are repeated
        node_distances.pop()
        node_distances.pop()

    return bijection

# Merge the MST and MPM
def merge_graphs(graph1, graph2):
    pass
