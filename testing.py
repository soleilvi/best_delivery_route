from christophides import *

graph1 = [[0, 1, 6, 3],
          [1, 0, 5, 4],
          [6, 5, 0, 8],
          [3, 4, 8, 0]]

graph2 = [[0, 2, 3, 3, 0, 0, 0],
          [2, 0, 4, 0, 3, 0, 0],
          [3, 4, 0, 5, 1, 6, 0],
          [3, 0, 5, 0, 0, 7, 0],
          [0, 3, 1, 0, 0, 8, 0],
          [0, 0, 6, 7, 8, 0, 9],
          [0, 0, 0, 0, 0, 9, 0]]

mst = get_mst(4, graph1)
print("MST 1:")
print(mst)

mst = get_mst(7, graph2)
print("MST 2:")
print(mst)