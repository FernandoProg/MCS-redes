import numpy as np

matrix_connect = np.genfromtxt('./dataset/matrizConectividad55.csv', delimiter=',')
initial_node = '0'
end_node = '4'

def camino(actualList):
    num_rows, num_cols = matrix_connect.shape
    myList = []
    for i in range(len(actualList)):
        element = int(actualList[i][-1])
        for j in range(num_cols):
            if matrix_connect[element][j] != 0:
                if len(''.join(set(actualList[i] + str(j)))) == len(actualList[i])+1:
                    myList.append(actualList[i] + str(j))
    return myList

principalList = []
actualList = []
actualList.append(initial_node)
while 1:
    actualList = camino(actualList)
print(actualList)