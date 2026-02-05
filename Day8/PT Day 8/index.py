# numbers=[1,2,3,4,5]
# # print(numbers)

# res=[]
# for i in numbers:
#     res.append(i*10000000000000)
# print(res)


# import numpy as np
# a=np.array([1,2,3,4,5 ])
# print(a*100)

#1D array
# import numpy as np
# a=np.array([1,2,3,4,5])
# print(a)


#2D array
# import numpy as np
# a=np.array([[1,2,3],[4,5,6]])
# print(a)

#3D array-images,videos or deep learning 
# import numpy as np
# a=np.array([[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]])

# print(a.shape)

import numpy as np
# a=np.array([[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]])
# [2,2,3]
# 3layers,4rows,5columns
# b=np.ones((3,4,5))
# print(b)
# print(a.ndim)
# print(a[1,1,1])

#accessing first 2d array
# print(a[0])
# print(a[1])

#accessing first row of first 2d array
# print(a[0,0])
# print(a[0,1])

#first column of all layers
# print(a[:, :, 0])

#second column of all layers
# print(a[:, :, 1])

#second row of all layers
# print(a[:, 1, :])

#reshaping of 3d array
# b=np.arange(24)
# b=b.reshape(2,3,4)
# b.shape
# print(b)


#math operations on 3d array
# print(np.sum(a, axis=0)) #sum of all layers
# print(np.sum(a, axis=1)) #sum of all rows
# print(np.sum(a, axis=2)) #sum of all columns

#image data
# image=np.random.randint(0,225,(64,64,3))
# #meaning of 64,64,3 is 64 rows,64 columns and 3 channels(RGB)
# r=image[:,:,0] #red channel
# print(r)

