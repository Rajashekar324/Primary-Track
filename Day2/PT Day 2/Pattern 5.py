row=int(input("Enter the row size for the Z pattern: "))
for i in range(row):
    for j in range(row):
        if i==0 or i==row-1:
            print("*",end=" ")
        elif j==row-i-1:
            print("*", end=" ")
        else:
            print(" ",end=" ")
    print()