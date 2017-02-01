import numpy as np

arr = [
   [[1, 1, 1],[2, 2, 2],[3, 3, 3]], [[4, 4, 4],[5, 5, 5],[6, 6, 6]]
]
a = np.array(arr)
print(a)
# print([[sum(rgbArr) for rgbArr in col] for col in arr])
d = np.dot(a[:3], [.3, .6, .1])
print(d)