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
        # print(matrix_incid[:, i])
        # print(np.where(matrix_incid[:, i] == 1))
        pos = np.where(matrix_incid[:, i] == 1)
        matrix_connect[pos[0][0]][pos[0][1]] = 1
        matrix_connect[pos[0][1]][pos[0][0]] = 1
    return matrix_connect

def combinations(paso):
    num_rows, num_cols = matrix_connect.shape
    numbers = np.arange(2,num_rows)
    for i in range(2, num_rows):
        for j in range(paso):
            number = i
            for k in range(i, num_rows):
            
                
    print(numbers)
    return None

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

print("Matriz de incidencia: ", matrix_incid)     # Mostramos la matriz de incidencia resultante
print("Vector de confiabilidad: ", vector_conf)  # Mostramos el vector de confiabilidad resultante

matrix_connect = matrix_incid_to_matrix_connect()
paso = 1
initial_node = '0'
end_node = '4'
actualList = combinations(paso)
print(actualList)