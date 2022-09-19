import pandas as pd
import numpy as np


class Opt:
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
        puntosAleatorios = nodos.copy()
        # la columna marcado funciona para ver si el nodo en cuestion ya fue visitado
        grafo = puntosAleatorios.assign(marcado=False)
        self.dato = grafo


    def existe_en_dataframe(self, df, data):
        query = "X == " + str(data['X']) + " and Y == " + str(data['Y'])
        return len(df.query(query)) >= 1


    def invertir(self, dataframe, inicio, fin):
        """
        Invierte desde inicio + 1, hasta fin
        """
        return pd.concat([dataframe.iloc[:inicio + 1], dataframe[inicio + 1:fin + 1:][::-1], dataframe.iloc[fin + 1:]])

    def distancia2(self, punto1, punto2):
        return np.power(punto1[0] - punto2[0], 2) + np.power(punto1[1] - punto2[1], 2)

    def puntos_mas_cercanos2(self, df, df2, punto_inicial):
        """Determina los siguientes puntos más cercanos con respecto al punto_inicial,
        si no encuentra un punto se retorna el mismo.

        Parameters
        ----------
          df : Dataframe de puntos totales
          df2 : Dataframe de puntos ya utilizados
          punto_inicial : punto a partir de donde se busca el siguiente punto

        Returns
        ----------

          array de df.row : array de puntos mas cercanos
          int : longitud con el punto mas cercano o numpy.inf
        """

        # longitud infinita
        min_lenght = np.inf

        # el siguiente punto más cercano es si mismo
        next = [punto_inicial]

        for index, row in df.iterrows():
            # no debe de existir en el segundo dataframe y debe de ser una longitud menor a la
            # longitud minima
            if (self.existe_en_dataframe(df2, row) != True and self.distancia2(row, punto_inicial) <= min_lenght):
                if (self.distancia2(row, punto_inicial) < min_lenght):
                    next = [row]
                    min_lenght = self.distancia2(row, punto_inicial)
                else:
                    next.append(row)

        # retorna el punto y la longitud
        return next, min_lenght

    def distancia(self, punto1, punto2):
        return np.sqrt(np.power(punto1[0] - punto2[0], 2) + np.power(punto1[1] - punto2[1], 2))

    def puntos_mas_cercanos(self, df, df2, punto_inicial):
        """Determina los siguientes puntos más cercanos con respecto al punto_inicial,
        si no encuentra un punto se retorna el mismo.

        Parameters
        ----------
          df : Dataframe de puntos totales
          df2 : Dataframe de puntos ya utilizados
          punto_inicial : punto a partir de donde se busca el siguiente punto

        Returns
        ----------

          array de df.row : array de puntos mas cercanos
          int : longitud con el punto mas cercano o numpy.inf
        """

        # longitud infinita
        min_lenght = np.inf

        # el siguiente punto más cercano es si mismo
        next = [punto_inicial]

        for index, row in df.iterrows():
            # no debe de existir en el segundo dataframe y debe de ser una longitud menor a la
            # longitud minima
            if (self.existe_en_dataframe(df2, row) != True and self.distancia(row, punto_inicial) <= min_lenght):
                if (self.distancia(row, punto_inicial) < min_lenght):
                    next = [row]
                    min_lenght = self.distancia(row, punto_inicial)
                else:
                    next.append(row)

        # retorna el punto y la longitud
        return next, min_lenght

    def opt2_local(self, ruta, fin):
        """optimizacion local por 2opt,

        Parameters
        ----------
        ruta : ruta la cual optimizar
        fin: hasta que punto hacer la optimizacion

        Returns
        ----------

        ruta optimizada
        """
        foundImprovement = True

        # mientras se encuentre una optmimizacion se vuelve a analizar desde el principio debido a un cambio de ruta
        while (foundImprovement):
            foundImprovement = False;

            # desde el inicio hasta el final
            for i in range(fin - 1):

                # calcular la mejora de distancia si se incercambia dos aristas
                lengthDelta = - self.distancia2(ruta['ruta'].iloc[i], ruta['ruta'].iloc[i + 1]) - self.distancia2(
                    ruta['ruta'].iloc[fin], ruta['ruta'].iloc[fin + 1]) + self.distancia2(ruta['ruta'].iloc[i],
                                                                                    ruta['ruta'].iloc[fin]) + self.distancia2(
                    ruta['ruta'].iloc[i + 1], ruta['ruta'].iloc[fin + 1])

                # si la distancia es negativa, significa una mejora
                if (lengthDelta < 0):
                    # invertimos la ruta entre "i+1" e "fin"
                    ruta['ruta'] = self.invertir(ruta['ruta'], i, fin)

                    # aplicamos la mejora de la ruta
                    ruta['distancia'] += lengthDelta;

                    # anuncimamos un cambio en la ruta
                    foundImprovement = True;
        return ruta

    def ruta2Optima(self, dataframe, inicio):
        # realizar una copia para no afectar al original
        dataframeCP = dataframe.copy()

        # crear un diccionario
        ruta = {
            'ruta': pd.DataFrame(columns=['X', 'Y']),  # dataframe de puntos que representan el orden del recorrido
            'distancia': 0
        }

        # agregamos el punto inicial
        ruta['ruta'] = ruta['ruta'].append({'X': dataframeCP.iloc[inicio].X, 'Y': dataframeCP.iloc[inicio].Y},
                                           ignore_index=True)

        # mientras no haya un punto sin visitar
        while len(ruta['ruta']) != len(dataframe):

            # obtener puntos mas cercanos
            puntos_siguientes, distancia_sig = self.puntos_mas_cercanos2(dataframeCP, ruta['ruta'], ruta['ruta'].iloc[-1])

            # array de heuristicas
            heuristicas = []

            # generar heuristicas por cada punto posible
            for punto in puntos_siguientes:
                # nuevo se hace una copia del estado actual
                ruta_cp = ruta.copy()

                # se agrega el punto cercano al estado obteniendo asi el siguiente estado a analizar
                ruta_cp['ruta'] = ruta_cp['ruta'].append({'X': punto.X, 'Y': punto.Y}, ignore_index=True)
                ruta_cp['distancia'] += distancia_sig

                # se calcula la conveniencia del estado de acuerto a la heuristica 2opt y se agrega a las heuristicas
                heuristicas.append(self.opt2_local(ruta_cp, len(ruta_cp['ruta']) - 2))

            # la mejor heuristica es aquella que se desconoce
            heuristica = np.inf

            # buscar por cada heuristica
            for ruta_2opt in heuristicas:

                # la heuristica es mejor que la que  tenemos
                if (ruta_2opt['distancia'] < heuristica):
                    # actualizamos el valor de la heuristica
                    heuristica = ruta_2opt['distancia']

                    # esa heuristica sera nuestro proximo estado
                    ruta = ruta_2opt

        # conectar con el inicio
        ruta['ruta'] = ruta['ruta'].append({'X': ruta['ruta'].iloc[0].X, 'Y': ruta['ruta'].iloc[0].Y},
                                           ignore_index=True)
        ruta['distancia'] += self.distancia2(ruta['ruta'].iloc[-1], ruta['ruta'].iloc[-2])

        # aplicar la optimizacion al volver al inicio
        return self.opt2_local(ruta, len(ruta_cp['ruta']) - 2)