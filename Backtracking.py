import time

import pandas as pd
import numpy as np


class Backtracking:
    # atributo que contendrá el grafo en cuestion
    dato = pd.DataFrame(
        columns=[
            'X',
            'Y',
            'marcado'
        ]
    )

    # constructor del grafo
    def __init__(self, nodos):
        # el par (nodos,2) da las dimensiones del array que generará numpy (fila,col)
        puntosAleatorios = pd.DataFrame(
            np.random.randint(0, 50, (nodos, 2)),
            columns=['X', 'Y']
        )
        # la columna marcado funciona para ver si el nodo en cuestion ya fue visitado
        grafo = puntosAleatorios.assign(marcado=False)
        self.dato = grafo


    def existe_en_dataframe(self, df, data):
        query = "X == " + str(data['X']) + " and Y == " + str(data['Y'])
        return len(df.query(query)) >= 1


    def distancia(self, punto1, punto2):
        return np.sqrt(np.power(punto1[0] - punto2[0], 2) + np.power(punto1[1] - punto2[1], 2))


    def search(self, ruta_optima, ruta, grafo, inicio):
        for h in range(0, len(grafo)):
            punto = {"X": grafo.iloc[h].X, "Y": grafo.iloc[h].Y}
            if (not self.existe_en_dataframe(ruta['ruta'], punto)):
                ruta['ruta'] = ruta['ruta'].append(punto, ignore_index=True)
                ruta['distancia'] += self.distancia(ruta['ruta'].iloc[-1], ruta['ruta'].iloc[-2])
                ruta_optima = self.search(ruta_optima, ruta, grafo, inicio)
                ruta['distancia'] -= self.distancia(ruta['ruta'].iloc[-1], ruta['ruta'].iloc[-2])
                ruta['ruta'] = ruta['ruta'].drop([len(ruta['ruta']) - 1], axis=0)

        # conectar con el primer punto solo si la ruta ya fue totalmente recorrida
        if (len(ruta['ruta']) == len(grafo)):
            punto = {"X": grafo.iloc[inicio].X, "Y": grafo.iloc[inicio].Y}
            ruta['ruta'] = ruta['ruta'].append(punto, ignore_index=True)
            ruta['distancia'] += self.distancia(ruta['ruta'].iloc[-1], ruta['ruta'].iloc[-2])

        if (ruta['distancia'] <= ruta_optima['distancia'] and len(ruta['ruta']) == (len(grafo) + 1)):
            if (ruta['distancia'] < ruta_optima['distancia']):

                ruta_optima['ruta'] = [ruta['ruta'].copy()]
                ruta_optima['distancia'] = ruta['distancia']

            elif (ruta['distancia'] == ruta_optima['distancia']):

                ruta_optima['ruta'].append(ruta['ruta'].copy())
                ruta_optima['distancia'] = ruta['distancia']

        if (len(ruta['ruta']) == (len(grafo) + 1)):
            # borrar la conexion con el inicio
            ruta['distancia'] -= self.distancia(ruta['ruta'].iloc[-1], ruta['ruta'].iloc[-2])
            ruta['ruta'] = ruta['ruta'].drop([len(ruta['ruta']) - 1], axis=0)

        return ruta_optima


    def backtracking(self, dataframe, inicio):
        ruta = {
            'ruta': pd.DataFrame(columns=['X', 'Y']),
            'distancia': 0
        }
        ruta_optima = {
            'ruta': [],
            'distancia': np.inf
        }
        ruta['ruta'] = ruta['ruta'].append({'X': dataframe.iloc[inicio].X, 'Y': dataframe.iloc[inicio].Y},
                                           ignore_index=True)
        return self.search(ruta_optima, ruta, dataframe, inicio)