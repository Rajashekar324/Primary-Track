row=int(input("Enter the row size for the reverse Z pattern: "))
for i in range(row):
    for j in range(row):
        if i==0 or i==row-1:
            print("*",end=" ")
        elif j==i:
            print("*", end=" ")
        else:
            print(" ",end=" ")
    print()