# import pandas as pd

# mydataset={
#     'cars': ["BMW", "Volvo", "Ford"],
#     'passings': [3, 7, 2]
# }
# vr=pandas.DataFrame(mydataset)
# print(vr)

#pandas series  
# a=pandas.Series([1,2,3,4,5])
# print(a)

#accesing value from series
# a=pandas.Series([1,2,3,4,5])
# print(a[0])

#labels
# mv=pd.Series([1,2,3,4,5], index=["a","b","c","d","e"])
# print(mv)

#accesing value from series using label
# mv=pd.Series([1,2,3,4,5], index=["a","b","c","d","e"])
# print(mv["c"])

#dataframe
# mydataset={
#     'name': ["John", "Anna", "Peter"],
#     'age': [24, 13, 53],
#     'city': ["New York", "Paris", "Berlin"]
# }
# df=pd.DataFrame(mydataset)
# print(df)
# # print(df.loc[0])
# print(df.loc[[0,1]])

#named indexing
# df=pd.DataFrame(mydataset, index=["first", "second", "third"])
# print(df.loc["first"])
# print(df.loc[["first", "second"]])

#load files into pandas dataframe
# df=pd.read_csv("data.csv")
# print(df)
