"""Contains all the functions that come together to perform the Christofides 
algorithm.

The Christofides algorithm finds an efficient solution to the travelling 
salesman problem that guarantees that any path it generates will be at most 
3/2 the length of the most optimal path. It can only be used with graphs that 
fulfill the triangle inequality, which states that a direct path between two 
nodes is always shorter (or weighs less) than the path taken by traversing 
through a third node. Since the graphs used in this program emulate distances 
in a city, they should always fulfill th  triangle inequality. At a worst-case 
scenario, this algorithm will have a runtime of O(n^3), where n is the number 
of nodes in the input graph. 

The Christofides algorithm has the following steps:
1) Find the minimum spanning tree (MST) of the input graph
2) Make a separate graph containing all the nodes that have an odd number of 
   edges in the MST.
3) Find the minimum-weight perfect matching (MPM) of the sub-graph containing 
   the nodes with the odd number of edges.
4) Combine the MST and MPM in such a way that each node has an even number of 
   edges. Duplicate paths between nodes are fine (multigraph).
5) Make a Eulerian circuit out of the merged graph.
6) Make a Hamiltonian circiut out of the Eulerian circuit by removing edges 
   between vertices that are visited more than once.

In reality, this program uses a pseudo-Christofides algorithm. It merges the 
MST and MPM, but it does not ensure that the nodes in its merged result have 
an even number of edges nor does it find a Eulerian circuit for the graph. 
Instead, it prunes the paths and builds the Hamiltonian circuit in a single 
function. It runs more like this:
1) Find the minimum spanning tree (MST) of the input graph
2) Identify all the nodes that have an odd number of edges in the MST.
3) Find the minimum-weight perfect matching (MPM) of the nodes with the odd 
   number of edges.
4) Combine the MST and MPM.
5) Make a Hamiltonian circiut out of the merged graph by reconnecting the 
   edges of each node until all of them have exactly two edges. Ensure that 
   the graph is not disjoint every time the edges are reconnected.

This pseudo-Christofides algorithm still has a worst-case runtime of O(n^3).
"""

import heapq

def get_mst(nodes_list, distance_graph, places):
    """Calculate the minimum spanning tree (MST) using Prim's algorithm.
    
    The minimum spanning tree of a graph links together all of its nodes using 
    the edges with the smallest weight. Nodes have at least one path 
    connecting them to another node, and it does not matter if they have more 
    than two. 
    
    The steps of Prim's algorithm are:
    1) Start from an arbitrary node in the graph.
    2) Add the node to a "visited" list.
    3) Compare the weight of all the edges of the nodes in the visited list.
    4) Choose the edge with the smallest weight, given that it isn't connected 
       to a node we have already visited.
    5) Repeat 2-4 until all of the nodes in the graph are in the MST.
    """
    
    current_node = places.get(places.address_to_place("HUB"))  # Node 0
    visited_nodes = set()
    possible_paths = []
    # An MST includes all the nodes in the graph. Initialize all the nodes in
    # a dictionary without any connections.
    mst = {node:set() for node in nodes_list}
    
    # "While we don't have connections between all the nodes." We don't 
    # actually need to visit all the nodes for all of them to be included.
    while len(visited_nodes) < len(nodes_list) - 1:
        visited_nodes.add(current_node)

        # Get the distances stored in the current node.
        for destination in mst:
            distance = distance_graph[current_node.id][destination.id]
            # Do not add nodes connected to themselves or without paths.
            if distance != 0 and destination not in visited_nodes:
                possible_paths.append([distance, current_node, destination])

         # Convert the list into a priority queue: the first element will 
         # always contain the smallest element.
        heapq.heapify(possible_paths)

        while possible_paths:
            origin = possible_paths[0][1]
            destination = possible_paths[0][2]
            if destination not in visited_nodes:
                break
            heapq.heappop(possible_paths)
        
        # Draw a path between the two nodes. The path can be accessed through 
        # either of them.
        mst[origin].add(destination)
        mst[destination].add(origin)

        if not possible_paths:
            break

        current_node = destination
        heapq.heappop(possible_paths)
        
    return mst


def get_mpm(node_graph: dict, distance_graph: list):
    """Find the minimum-weight perfect matching of the nodes with uneven edges 
    from the input graph.

    A matching is a set of edges in a graph where no two edges in the set are 
    adjacent to each other. This means that no edge in the set can share a 
    node. A perfect matching is a matching that includes all the nodes in the 
    graph. The graph for which this function finds the perfect matching is a 
    graph containing all of the nodes in the MST with an uneven number of 
    edges connecting to them. Therefore, the expected input for this function 
    is the result of the MST.
    """
    
    uneven_nodes = set()  # Nodes with an odd number of edges/paths.
    bijection = []
    node_distances = []

    # 1) Identify nodes with odd-degree edges.
    for node in node_graph:
        if len(node_graph[node]) % 2 == 1:
            uneven_nodes.add(node)

    # 2) Get the distances of each of those nodes.
    unseen = uneven_nodes.copy()  # Prevents path duplicates.
    for origin in uneven_nodes:
        unseen.remove(origin)
        for destination in unseen:
            distance = distance_graph[origin.id][destination.id]
            if distance != 0:
                node_distances.append((distance, origin, destination))

    heapq.heapify(node_distances)

    # 3) Match nodes according to the minimum distance between them.
    while uneven_nodes:
        start_node = node_distances[0][1]
        end_node = node_distances[0][2]
    
        # Do not match nodes we have already matched.
        if start_node in uneven_nodes and end_node in uneven_nodes:
            bijection.append((start_node, end_node))
            uneven_nodes.remove(start_node)
            uneven_nodes.remove(end_node)
        
        heapq.heappop(node_distances)

    return bijection


def merge_graphs(mst: dict, mpm: list): 
    """Merge the MST and MPM."""
    
    merged = mst.copy()
    # Adding the MPM to the MST
    for node_pair in mpm:
        a = node_pair[0]
        b = node_pair[1]

        if b not in mst[a]:
            merged[a].add(b)
        if a not in merged[b]:
            merged[b].add(a)    
        
    return merged


def is_disjoint(node_connection_dict, current_node, complete_node_count):
    """Checks if the input graph is disjoint.
    
    A graph is disjoint when it has at least one node that is not connected to 
    the rest of the graph. It is not possible to access all the nodes in the 
    graph when starting its traversal at an arbitrary node. This is a helper 
    function for simplify_edges().
    """

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


def reconnect_nodes(node_connection_dict, n, x, y):
    """Removes unnecessary edges between nodes by reconnecting the 
    destinations of node n to each other instead of n.

    For nodes that have more than two connections, we want to make a direct 
    path between its connections by replacing [(n, x), (n, y)] with [(x, y)]. 
    This is a helper function for simplify_edges().
    """

    n_is_even = len(node_connection_dict[n]) % 2 == 0
    x_is_even = len(node_connection_dict[x]) % 2 == 0
    y_is_even = len(node_connection_dict[y]) % 2 == 0

    if n_is_even:
        node_connection_dict[x].remove(n)
        node_connection_dict[x].add(y)

        node_connection_dict[y].remove(n)
        node_connection_dict[y].add(x)

        node_connection_dict[n].remove(x)
        node_connection_dict[n].remove(y)
    
    # For nodes with uneven edges, we just want to remove one edge
    else:
        # Prevents reconnecting nodes that are already fine
        connections = node_connection_dict[n].copy()
        while x_is_even and y_is_even and connections:
            connections.remove(x)
            connections.remove(y)
            y =  connections.pop()
            y_is_even = len(node_connection_dict[y]) % 2 == 0

        node_connection_dict[x].add(y)
        node_connection_dict[y].add(x)

        if x_is_even:
            node_connection_dict[x].remove(n)
            node_connection_dict[n].remove(x)
        # No need to check if they're both uneven since we would use the same 
        # behavior anyway.
        else: 
            node_connection_dict[y].remove(n)
            node_connection_dict[n].remove(y)


def simplify_edges(distance_graph, merged_graph):
    """Makes a hamiltonian circuit out of the merged MST and MPM graphs.
    
    A Hamiltonian circuit is a path in a graph that visits each node exactly 
    once. For our Hamiltonian circuit, we are also adding the restriction that 
    each node needs to have exactly two edges. 
    """
    
    node_connections = merged_graph.copy()
    nodes_over_two_edges = set()

    # 1) Find which nodes have more than two paths connected to them.
    for node in node_connections:
        if len(node_connections[node]) > 2:
            nodes_over_two_edges.add(node)

    # 2) Get the distances between all the destination nodes and put them in a 
    #    priority queue.
    while nodes_over_two_edges:
        node = nodes_over_two_edges.pop()
        destination_nodes = list(node_connections[node])
        destination_node_distances = []
        n = len(destination_nodes)
        i = n - 1

        # Getting the distance between each destination node.
        for start_node in destination_nodes:
            # Prevent revisiting the same path several times and make runtime 
            # slightly faster with [(n-i):].
            for end_node in destination_nodes[(n-i):]:
                destination_node_distances.append((distance_graph
                                                   [start_node.id]
                                                   [end_node.id], 
                                                   start_node, end_node))
            i -= 1

        heapq.heapify(destination_node_distances)

        # 3) Remove extra paths from the origin node by reconnecting those 
        #    paths to the destinations with the smallest distance between 
        #    them.
        tried_pairs = set()
        while destination_node_distances:
            start_node = destination_node_distances[0][1]
            end_node = destination_node_distances[0][2]

            # Having a standard way to demonstrate start and end nodes 
            # prevents us from having to check them twice.
            pair = tuple(sorted((start_node, end_node)))

            if pair in tried_pairs:
                heapq.heappop(destination_node_distances)
            tried_pairs.add(pair)

            original_paths = {
                "node": node_connections[node].copy(),
                "start": node_connections[start_node].copy(),
                "end": node_connections[end_node].copy()
            }

            # Prevent nodes from having two paths directing them to the same 
            # destination in the dictionary.
            if (node != start_node 
                and node != end_node 
                and start_node != end_node):
                reconnect_nodes(node_connections, node, start_node, end_node)

                # Undo changes if disjoint, break if the reconnection was 
                # successful.
                if is_disjoint(node_connections, start_node, 
                               len(node_connections)):
                    node_connections[node] = original_paths["node"]
                    node_connections[start_node] = original_paths["start"]
                    node_connections[end_node] = original_paths["end"]
                else:
                    break 
        
            else:
                print("Skipping invalid or duplicate node pair")

            heapq.heappop(destination_node_distances)

        # 5) Repeat until the current start node only has two distances (add 
        #    the node back to the set if the length is still over 2).
        if len(node_connections[node]) > 2:
            nodes_over_two_edges.add(node)

    return node_connections

# Add up the distance of all the paths in the graph to get the weight. Only works with hamiltonian tour graphs.
# TODO: delete this function
def get_graph_weight(graph, distance_graph, places):
    visited = set()
    node = places.get(places.address_to_place("HUB"))
    node_with_end_connection = -1
    weight = 0

    while len(visited) < len(graph):
        visited.add(node)
        connections = list(graph[node])
        destination = connections[0]
        if destination.id == 0: node_with_end_connection = node
               
        if destination in visited:
            destination = connections[1]
            if destination.id == 0: node_with_end_connection = node

        if destination in visited:
            break

        weight += distance_graph[node.id][destination.id]
        node = destination

    weight += distance_graph[0][node_with_end_connection.id]
                
    return weight


def christofides(node_number, distance_graph, places):
    mst = get_mst(node_number, distance_graph, places)
    mpm = get_mpm(mst, distance_graph)
    merged = merge_graphs(mst, mpm)
    best_path = simplify_edges(distance_graph, merged)

    return best_path