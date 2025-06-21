# Calculate the minimum spanning tree (MST) using Prim's algorithm
def get_mst(places_list):
    current_node = 0  # Starting node for the MST
    visited_nodes = [False] * len(places_list)  # Each index in the list represents a different place. Once it is visited, it turns into True.
    possible_paths = []
    mst = [0]

    while len(mst) < len(places_list):  # while mst is not full 
        visited_nodes[current_node] = True

        # get the distances stored in the current node
        for i, distance in enumerate(places_list[current_node].distances):
            if visited_nodes[i] is False:  # optimize algorithm a bit by excluding paths to nodes we have already visited 
                possible_paths.append([float(distance), i])
        # get the rest of the distances from the column that corresponds to the ID number of the current node
        for i in range(current_node + 1, len(places_list)):
            if visited_nodes[i] is False:
                possible_paths.append([float(places_list[i].distances[current_node]), i])

        possible_paths.sort(reverse=True, key=lambda sub_list: sub_list[0])  # sorting from greatest distance to smallest according to the first element (edge weight) of each sub-list
        # print(possible_paths)

        destination = possible_paths[-1][1]
        is_new_node = False  # the destination is a node in visited_nodes
        while not is_new_node:
            # if the node we are visiting is not already in the MST graph
            if visited_nodes[destination] is False:
                current_node = destination
                mst.append(destination)
                possible_paths.pop()
                is_new_node = True 
            # if the node we are visiting has already been visited 
            else:
                possible_paths.pop()
                destination = possible_paths[-1][1]
        
        # print(f'mst after: {mst}')
        # print(f'current node: {current_node}')

    return mst
