# task3
import numpy as np
a = np.arange(1, 25).reshape(2, 3, 4)
print("Original Array:")
print(a)
print("Shape:", a.shape)
print("\nElements greater than 10:")
print(a[a > 10])
even_count = np.sum(a % 2 == 0)
print("\nNumber of even elements:", even_count)
a[a < 10] = 0
print("\nArray after replacing values < 10 with 0:")
print(a)