# matrix=[
#     [1,2,3], # 0-qator 
#     [4,5,6], # 1-qator
#     [7,8,9] # 2-qator
# ]   #0 1 2  ustunlar


# print(matrix[0]) # o-qator # [1, 2, 3]
# print(matrix[0][0]) # 0-qator 0-ustun # 1

# total=0
# for row in matrix:
#     for element in row:
#         total+=element
# print(total) # 45 

# # 2o'lchamli matrix yaratish

# matrix=[[0]*3 for _ in range(3)]
# matrix[0][0]=1
# print(matrix)  #  [[1, 0, 0], [0, 0, 0], [0, 0, 0]]


# # qator va ustun

# matrix=[
#     [1,2,3],
#     [4,5,6]
# ]

# qator=len(matrix)
# ustun=len(matrix[0])

# for i in range(qator):
#     for j in range(ustun):
#         print(matrix[i][j])


a=[1,2,3,3,34,4]

for i in range(len(a)):
    print(a[:i+1])


