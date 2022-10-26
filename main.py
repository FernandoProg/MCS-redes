import numpy as np
import itertools as it

matrix_incid = np.genfromtxt('./dataset/matrix_incid_6_9.csv', delimiter=',') # Importacion de la matriz de incidencia
vector_conf = np.genfromtxt('./dataset/vector_conf_6_9.csv', delimiter=',')   # Importacion del vector de confiabilidad

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

def matrix_incid_to_matrix_connect():               # Conversion de matriz de incidencia a matriz de conectividad
    num_rows, num_cols = matrix_incid.shape
    matrix_connect = np.zeros((num_rows, num_rows)) # Creamos una matriz de conectividad con 0s del tamaño de filas de la matriz de incidencia
    for i in range(num_cols):
        pos = np.where(matrix_incid[:, i] == 1)     # Buscamos las posiciones por columna que sean 1 y estas son asignadas en la matriz de conectividad con el numero del enlace
        matrix_connect[pos[0][0]][pos[0][1]] = i + 1
        matrix_connect[pos[0][1]][pos[0][0]] = i + 1
    return matrix_connect

def firstCombination():                                 # Obtenemos las primeras MCS
    firstRow = ""
    LastRow = ""
    values = []
    for i in range(0, len(matrix_connect)):             # La primera y ultima combinacion son los valores de las columnas en la primera y ultima fila respectivamente distintos de 0
        if matrix_connect[0][i] != 0:
            firstRow += str(int(matrix_connect[0][i]))
        if matrix_connect[-1][i] != 0:
            LastRow += str(int(matrix_connect[-1][i]))
    if firstRow != LastRow:                             # Si las combinaciones son distintas retornamos ambas, en caso contraria solo una es agregada
        values.append(firstRow)
        values.append(LastRow)
    else:
        values.append(firstRow)
    return values

def isCombination(element):         # Preguntamos si la combinacion es valida o no segun las reglas de la generacion de componentes entre nodos de interes
    sumFirstRow = 0
    if len(element) > 1:
        sumLastColumn = False
    else:
        sumLastColumn = True
    for i in range(len(element)):   # Recorremos la combinacion y en sumFirstRow sumamos las columnas de la primera fila y en sumLastColumn buscamos si la ultima columna de las filas presentan algun 0
        sumFirstRow += matrix_connect[0][int(element[i])]
        if matrix_connect[int(element[i])][-1] == 0:
            sumLastColumn = True
    if sumFirstRow == 0 or not sumLastColumn:   # La combinacion es descartada si hay solo 0s en la primera fila o no se encontro ningun 0 en la ultima columna
        return False
    else:
        return True

def toCombination(element):                 # Convertimos las combinaciones a MCS
    newElement = "0"
    MyElement = ""
    for k in element:                       # Creamos un string con las combinaciones y le antepones la posicion 0 
        newElement = newElement + str(k)
    for i in range(len(matrix_connect)):    # Se agregan al MCS las filas y columnas de la combinacion que sean distintos de 0
        if str(i) in newElement:
            for j in range(len(matrix_connect)):
                if str(j) not in newElement and matrix_connect[i][j] != 0: 
                    MyElement += str(int(matrix_connect[i][j]))
    return MyElement

def combinations():                                 # Obtenemos las combinaciones entre 2 y el largo de la matriz de conectividad
    values = np.arange(1, len(matrix_connect)-1)
    val = []
    list_combinations = list()
    for i in range(len(values) + 1):                # Creamos las combinaciones de orden 1 hasta el tamaño de la matriz de conectividad - 2
        list_combinations += list(it.combinations(values, i))
    for i in list_combinations:                     # Revisamos que la combinacion sea valida con el metodo explicado anteriormente
        if isCombination(i):
            val.append(toCombination(i))
    return val

def inclusionexclusion(sets):       # Aplicamos el metodo de inclusion exclusion
    sum = 0
    i = 0
    list_combinations = list()
    for i in range(len(sets)+1):    # Combinamos los MCS de orden 1 hasta el largo de MCS y los almacenamos en list_combinations
        list_combinations = list(it.combinations(sets, i))
        for j in list_combinations:
            if len(j) > 0:
                value = ""
                for k in j:
                    for l in k:     # Creamos un string con los valores de la combinacion de MCS y eliminamos los repetidos
                        value += str(l)
                    value = ''.join(set(value))
                mult = 1
                for k in range(len(value)): # Multiplicamos 1 menos la probabilidad en el vector de confiabilidad
                    mult *= (1-vector_conf[int(value[k])-1])
                if i % 2 == 0:              # En caso de de ser una combinacion de orden par se resta, en caso contrario se suma
                    sum -= mult
                else:
                    sum += mult
        if i == 1:                  # Las cotas son 1 menos la sumatoria actual, la confiabilidad es 1 menos la sumatoria final 
            print("Primera cota inferior: ", 1 - sum)
        elif i == 2:
            print("Primera cota superior: ", 1 - sum)
        elif i == 3:
            print("Segunda cota inferior: ", 1 - sum)
        elif i == 4:
            print("Segunda cota superior: ", 1 - sum)
    return 1 - sum

print("Cantidad de nodos: ", matrix_incid.shape[0])
print("Cantidad de enlaces: ", matrix_incid.shape[1])

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

print("Cantidad de nodos post reduccion SP: ", matrix_incid.shape[0])
print("Cantidad de enlaces post reduccion SP: ", matrix_incid.shape[1])
matrix_connect = matrix_incid_to_matrix_connect()   # Convertimos la matriz de incidencia a una de conectividad
myList = combinations()                             # Creamos las combinaciones entre 2 y el largo de la matriz - 2, ademas de convertirlos en MCS
for i in firstCombination():
    if i not in myList:                             # Agregamos las combinaciones de la primera y ultima fila
        myList.append(i)
print("Cantidad de MCS post reduccion SP: ", len(myList))
print("Confiabilidad: ", inclusionexclusion(myList))
