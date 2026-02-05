# task2
import numpy as np
a = np.arange(1, 25).reshape(2, 3, 4)
print(a[0])
print(a[-1])
print(a[0, 1, 2])
print(a[:, 0, :])
print(a[:, -1, :])