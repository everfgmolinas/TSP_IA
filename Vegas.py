import time

import pandas as pd
import numpy as np


class Vegas:
    # atributo que contendrá el grafo en cuestion
    dato = pd.DataFrame(
        columns=[
            'X',
            'Y',
            'marcado'
        ]
    )
    # atributo que contendrá el camino solución hallado
    caminoSolucion = pd.DataFrame(
        columns=[
            'X',
            'Y'
        ]
    )

    # constructor del grafo
    def __init__(self, nodos):
        # el par (nodos,2) da las dimensiones del array que generará numpy (fila,col)
        puntosAleatorios = nodos.copy()
        # la columna marcado funciona para ver si el nodo en cuestion ya fue visitado
        grafo = puntosAleatorios.assign(marcado=False)
        self.dato = grafo


    # funcion que retorna un dataframe con los nodos del grafo
    def nodos(self):
        return self.dato[['X','Y']]


    # funcion encargada de marcar o desmarcar un nodo en espcífico
    def marcar(self, x, y, value):
        self.dato['marcado'].loc[(self.dato['X'] == x) & (self.dato['Y'] == y)] = value


    # funcion encargada de agregar un nodo al camino solucion
    def agregarCamino(self, x, y):
        self.caminoSolucion = self.caminoSolucion.append({'X': x, 'Y': y}, ignore_index=True)


    # funcion encargada de eliminar un camino mal puesto
    def eliminarUltimoCamino(self):
        self.caminoSolucion.drop(self.caminoSolucion.tail(1).index, inplace=True)


    # funcion que construirá la solución
    def vegas(self, tiempoInicio, x, y, longCamino):
        # condicion verdadera indica solucion hallada
        if (longCamino == self.nodos().shape[0] - 1):
            # marcar el nodo visitado
            self.marcar(x, y, True)
            #puntosAleatorios['marcado'].loc[(puntosAleatorios['X'] == x) & (puntosAleatorios['Y'] == y)] = True
            # retornamos una lista que contiene el nodo final accedido
            return [x, y]
        else:
            # obviamos el nodo actual en la búsqueda de vecinos
            query = "X != @x and Y != @y and marcado == False"
            # obtenemos los vecinos disponibles
            vecinos = self.dato.query(query)[['X', 'Y']]
            # print(f'VECINOS DE {x},{y} hay: {len(vecinos.index)}')
            # print(vecinos)
            # print('ELEGIBLES: ')
            # print(vecinos.index)
            # si todavia hay vecinos por recorrer
            if (len(vecinos.index) >= 1):
                # centinela para el ciclo mientras
                res = None
                while (res == None):
                    # obtenemos el menor índice entre los vecinos
                    minimoIndice = 0
                    # obtenemos el mayor índice entre los vecinos
                    maximoIndice = len(vecinos.index.values)
                    # elegimos un nodo vecino disponible de manera aleatoria
                    indice = np.random.randint(minimoIndice, maximoIndice)
                    # print(f'ALEATORIO: {indice}')
                    # marcar el nodo actual
                    # puntosAleatorios['marcado'].loc[(puntosAleatorios['X'] == x) & (puntosAleatorios['Y'] == y)] = True
                    self.marcar(x, y, True)
                    # llamada recursiva
                    res = self.vegas(tiempoInicio, vecinos.iloc[indice]['X'], vecinos.iloc[indice]['Y'], longCamino + 1)
                    if (res == None):
                        tiempoActual = time.time()
                        if (tiempoActual - tiempoInicio >= 60):
                            quit()
                    # cuando la respuesta ya no es None
                    else:
                        # se agrega de forma provisoria el camino
                        # camino.append({'X': res[0], 'Y': res[1]}, ignore_index=True)
                        self.agregarCamino(res[0], res[1])
                        return [x, y]
            # ya no hay vecinos por visitar y el algoritmo aun no hay terminado
            else:
                # eliminamos el último nodo agregado al camino
                # camino.drop(camino.tail(1).index, inplace=True)
                self.eliminarUltimoCamino()
                return None