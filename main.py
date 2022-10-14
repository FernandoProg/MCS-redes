import numpy as np

matrix_incid = np.genfromtxt('./dataset/matrix_incid_5_7.csv', delimiter=',') # Importacion de la matriz de incidencia
vector_conf = np.genfromtxt('./dataset/vector_conf_5_7.csv', delimiter=',')   # Importacion del vector de confiabilidad

def parallel():                             # Funcion para ver nodos paralelos
    num_rows, num_cols = matrix_incid.shape # Se almacena el numero de filas y columnas respectivamente
    for i in range(num_cols):               # Se comparan las columnas de la mas a la izquierda
        for j in range(i+1, num_cols):      # con las demas que se encuentra a su derecha
            column1 = matrix_incid[:, i]    # Se guarda la columna izquierda
            column2 = matrix_incid[:, j]    # Se guarda una columna derecha 
            equal = column1 == column2      # En equal se ve si cada uno de sus valores son iguales, retornando True o False segun corresponda
            if(equal.all()):                # Se consulta si todos los valores de equal son verdaderos, en caso afirmativo estamos ante 2 columnas identicas
                return i, j                 # Retornamos las posiciones de las columnas que son iguales
    return None, None                       # En caso contrario retornamos None para identificar que no se encontraron columnas paralelas

def serie():                                # Funcion para ver nodos en serie
    num_rows, num_cols = matrix_incid.shape # Se almacena el numero de filas y columnas respectivamente
    for i in range(1, num_rows-1):          # Recorremos las filas a excepcion de la primera y la ultima
        row = matrix_incid[i, :]            # Almacenamos la fila en la variable row
        if np.sum(row) == 2:                # Vemos si el grado de la fila es 2
            index = []
            index.append(i)                 # Guardamos el indice de la fila de grado 2
            for j in range(0, num_cols):    # recorremos las columnas
                if row[j] == 1:             # Como es de grado 2, buscamos las columnas que en la posicion de la fila sea 1
                    index.append(j)         # Agregamos estas posiciones a la lista index
            return index                    # Retornamos la lista de indices
    return None                             # En caso contrario retornamos None para identificar que no se encontraron enlaces en serie

def matrix_incid_to_matrix_connect():
    num_rows, num_cols = matrix_incid.shape
    matrix_connect = np.zeros((num_rows, num_rows))
    for i in range(num_cols):
        pos = np.where(matrix_incid[:, i] == 1)
        matrix_connect[pos[0][0]][pos[0][1]] = i + 1
        matrix_connect[pos[0][1]][pos[0][0]] = i + 1
    return matrix_connect

def firstCombination():
    firstRow = ""
    LastRow = ""
    values = []
    for i in range(0, len(matrix_connect)):
        if matrix_connect[0][i] != 0:
            firstRow += str(int(matrix_connect[0][i]))
        if matrix_connect[-1][i] != 0:
            LastRow += str(int(matrix_connect[-1][i]))
    if firstRow != LastRow:
        values.append(firstRow)
        values.append(LastRow)
    else:
        values.append(firstRow)
    values = np.array(values)
    return values

def isCombination(element):
    sumFirstRow = 0
    if len(element) > 1:
        sumLastColumn = False
    else:
        sumLastColumn = True
    for i in range(len(element)):
        sumFirstRow += matrix_connect[0][int(element[i])]
        if matrix_connect[int(element[i])][-1] == 0:
            sumLastColumn = True
    if sumFirstRow == 0 or not sumLastColumn:
        return False
    else:
        return True

def toCombination(element):
    newElement = ""
    element = "0" + element
    for i in range(len(matrix_connect)):
        if str(i) in element:
            for j in range(len(matrix_connect)):
                if str(j) not in element and matrix_connect[i][j] != 0: 
                    newElement += str(int(matrix_connect[i][j]))
    return newElement

def combinations(paso):
    values = []
    for i in range(1, len(matrix_connect)-1):
        number = ""
        if paso > 1:
            for j in range(i, len(matrix_connect)):
                if len(number) < paso:
                    number += str(j)
                else:
                    if isCombination(number):
                        values.append(toCombination(number))
                    number = number.rstrip(number[-1])
                    number += str(j)
        else:
            number += str(i)
            if isCombination(number):
                values.append(toCombination(number))
    values = np.array(values)
    return values

def inclusionexclusion(sets):
    sum = 0
    for i in range(1, len(sets)):
        newSet = combinateSets(sets, i)
        # print(newSet)
        for j in newSet:
            mult = 1
            for k in range(len(j)):
                mult *= (1-vector_conf[int(j[k])-1])
            if i % 2 == 0:
                sum -= mult
            else:
                sum += mult
    return 1 - sum

def combinateSets(sets, paso):
    flag = False
    for i in range(len(sets) + 1):
        if flag:
            i -= 1
        flag = False
        number = ""
        values = []
        for j in range(i, len(sets)):
            if len(number) < paso:
                number += str(j)
            else:
                comb = ""
                print(number)
                for k in range(len(number)):
                    comb += sets[int(number[k])]
                values.append(''.join(set(comb)))
                number = number.rstrip(number[-1])
                flag = True
                number += str(j)
        return values

while 1:                        # Inicio del bucle
    isParallel = parallel()     # Consultamos si hay enlaces en paralelo
    isSerie = serie()           # Consultamos si hay enlaces en serie
    if isParallel[0] != None:   # Si encontramos paralelos estos deberian retornar posiciones en vez de None
        matrix_incid = np.delete(matrix_incid, isParallel[0], axis=1)                                   # Eliminamos la columna que se encuentra mas a la izquierda
        vector_conf[isParallel[1]] = 1-(1-vector_conf[isParallel[0]])*(1-vector_conf[isParallel[1]])    # Reemplazamos la nuevo confiabilidad en el vector por el lado derecho
        vector_conf = np.delete(vector_conf, isParallel[0], axis=0)                                     # Eliminamos la confiabilidad en el vector por el lado izquierdo
    elif isSerie != [] and isSerie != None:                                                     # Si hay enlaces en serie deberia retornar una lista de indices en vez de None
        matrix_incid = np.delete(matrix_incid, isSerie[0], axis=0)                              # Eliminamos la fila de la matriz
        matrix_incid_t = matrix_incid.T                                                         # Creamos la transpuesta para futuras operaciones
        matrix_incid_t[isSerie[1]] = matrix_incid_t[isSerie[1]] + matrix_incid_t[isSerie[2]]    # Guardamos en una fila de la transpuesta la suma de ambas filas, que son las equivalentes a las columnas de nuestra matriz
        matrix_incid = matrix_incid_t.T                                                         # Igualamos la matriz a la transpuesta de la transpuesta
        matrix_incid = np.delete(matrix_incid, isSerie[2], axis=1)                              # Eliminamos la columna en la que no sobreescribimos el nuevo enlace
        vector_conf[isSerie[1]] = vector_conf[isSerie[1]]*vector_conf[isSerie[2]]               # Reemplazamos la nuevo confiabilidad en el vector por el lado izquierdo
        vector_conf = np.delete(vector_conf, isSerie[2], axis=0)                                # Eliminamos la confiabilidad en el vector por el lado derecho
    else:                       # De no haberse encontrado enlaces en serie ni en paralelo, el bucle se termina
        break

matrix_connect = matrix_incid_to_matrix_connect()
print(matrix_connect)
print(vector_conf)
myList = firstCombination()
for i in range(1, len(matrix_connect)-2):
    myList = np.append(myList, combinations(i))
print("MCS: ", myList)
ans = inclusionexclusion(myList)
print(ans)
