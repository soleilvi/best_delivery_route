from christophides import *

distances1 = [[0, 1, 6, 3],
              [1, 0, 5, 4],
              [6, 5, 0, 8],
              [3, 4, 8, 0]]

distances2 = [[0, 2, 3, 3, 0, 0, 0],
              [2, 0, 4, 0, 3, 0, 0],
              [3, 4, 0, 5, 1, 6, 0],
              [3, 0, 5, 0, 0, 7, 10],
              [0, 3, 1, 0, 0, 8, 11],
              [0, 0, 6, 7, 8, 0, 9],
              [0, 0, 0, 10, 11, 9, 0]]

graph2 = {0: [1, 2, 3],
          1: [0, 2, 4],
          2: [0, 1, 3, 4, 5],
          3: [0, 2, 5, 6],
          4: [1, 2, 5, 6],
          5: [2, 3, 4, 6],
          6: [3, 4, 5]}

# pee = {}
# for i in range(5):
#     pee[i] = []
# print(pee)
# length = 5
# heck = {i:[] for i in range(length)}
# print(heck)


mst1 = get_mst(4, distances1)
print("MST 1:")
print(mst1)

mst2 = get_mst(7, distances2)
print("MST 2:")
print(mst2)

mpm1 = get_mpm(mst1, distances1)
print("MPM 1")
print(mpm1)

mpm2 = get_mpm(mst2, distances2)
print("MPM 2")
print(mpm2)