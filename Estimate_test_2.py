import numpy as np

data = np.array([1,-2,3,-4,5])

bools = np.dot(data[0:len(data) - 1], data[1:len(data)])

array = []
array.append(bools)

result = []
zc = [0]
for i in array:
    if i <= 0:
        result.append(1)
    else:
        result.append(0)
    
    zc[0] = sum(result)

print(zc)