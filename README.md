# Lógica del algoritmo
El algoritmo empieza simplificando la red a través de métodos SP, una vez hecho esto se procede a crear una matriz de conectividad con la matriz de incidencia.
Luego buscamos las combinaciones entre 2 y el número de columnas de la matriz que respeten las reglas para el método de generar componentes entre nodos de interés, estos son sonvertidos a MCS a través de las filas y columnas con las reglas del método y luego se utiliza el método de inclusién exclusión para calcular su confiabilidad.

# Consideraciones del algoritmo

## Entradas del algoritmo
1. Matriz de incidencia
2. Vector de confiabilidad

## Reducciones SP
Las reducciones SP aplicadas son las mismas usadas en la tarea 1. Vease [aquí](https://github.com/FernandoProg/ConfiabilidadRedes.git) para mayor información (Link en privado, para solicitar ser colaborador hablar por interno)

## Convertir la matriz de incidencia a una matriz de conectividad
Para esta conversión se busca por columna las posiciones de la matriz de incidencia que sean iguales a 1. Estas equivalen a nuestras posiciones fila columna en la matriz de conectividad, dejandole el número del enlace más uno por valor.

## Busqueda de MCS
1. Buscamos todas las combinaciones entre los números 2 y n-1 con n el número de columnas de la matriz de conectividad, que a su vez satisfagan las siguientes reglas:
- Eliminamos la columna o la combinación de columnas que en su primera fila presenten solo 0
- Eliminamos la combinación de filas que en su última columna presenten solo valores distintos de 0
2. Convertir las combinaciones restantes en MCS con la matriz de conectividad aplicando las siguientes relgas:
- Las filas a utilizar son la primera y las que contemplen las respectivas combinaciones
- Las columnas a utilizar no pueden ser la primera ni ninguna de las contempladas en las respectivas combinaciones

## Principio de inclusión exclusión
1. Se crean las combinaciones desde primer orden entre los MCS hasta el número de elementos que este traiga
2. Para cada combinatoria se multiplica 1 menos el valor de la probabilidad que tenemos en el vector de confiabilidad
3. Las combinatorias de orden impar se suman, mientras que las de orden impar se restan
4. La confiabilidad final se obtiene de restar 1 menos el valor obtenido anteriormente

## Intervalos de confiabilidad
Para los primeros cuatro intervalos se resta 1 menos la sumatoria obtenida hasta ese momento.

# Relacion entre el valor de confiabilidad 1 y 2
A medida que avanzamos en los intervalos, estos se vuelven más cercanos al valor de confiabilidad real, debido a que el principio de inclusión exclusión para los MCS dice que para probabilidades altas sucede este efecto.