from django.shortcuts import render
import sys
import os

# importar arbol.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from arbol import Nodo


def buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    nodos_visitados = []
    nodos_frontera = []

    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)

    while len(nodos_frontera) != 0:
        nodo = nodos_frontera[0]
        nodos_visitados.append(nodos_frontera.pop(0))

        if nodo.get_datos() == solucion:
            return nodo
        else:
            dato_nodo = nodo.get_datos()
            lista_hijos = []

            for un_hijo in conexiones.get(dato_nodo, []):
                hijo = Nodo(un_hijo)
                hijo.set_padre(nodo)
                lista_hijos.append(hijo)

                if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)

            nodo.set_hijos(lista_hijos)

    return None


conexiones = {
    'jiloyork': {'celaya', 'cdmx', 'queretaro'},
    'sonora': {'zacatecas', 'sinaloa'},
    'guanajuato': {'aguascalientes'},
    'oaxaca': {'queretaro'},
    'sinaloa': {'celaya', 'sonora', 'jiloyork'},
    'queretaro': {'tamaulipas', 'zacatecas', 'sinaloa', 'jiloyork', 'oaxaca'},
    'celaya': {'jiloyork', 'sinaloa'},
    'zacatecas': {'sonora', 'monterrey', 'queretaro'},
    'monterrey': {'zacatecas', 'sinaloa'},
    'tamaulipas': {'queretaro'},
    'cdmx': {'jiloyork'},
    'aguascalientes': {'guanajuato'}
}


def index(request):
    resultado = None

    if request.method == "POST":
        inicio = request.POST.get("inicio").lower()
        fin = request.POST.get("fin").lower()

        nodo_solucion = buscar_solucion_BFS(conexiones, inicio, fin)

        if nodo_solucion:
            camino = []
            nodo = nodo_solucion

            while nodo.get_padre() is not None:
                camino.append(nodo.get_datos())
                nodo = nodo.get_padre()

            camino.append(inicio)
            camino.reverse()
            resultado = camino
        else:
            resultado = "No se encontró ruta"

    return render(request, "vuelos/index.html", {"resultado": resultado})