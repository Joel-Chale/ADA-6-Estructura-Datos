from collections import deque


class Nodo:
    """Representa cada elemento (nodo) del Árbol Binario de Búsqueda."""

    def __init__(self, dato: int):
        self.dato: int = dato
        self.izquierdoPtr: Nodo | None = None
        self.derechoPtr: Nodo | None = None


class Arbol:
    """Implementación de la clase Árbol Binario de Búsqueda y sus operaciones."""

    def __init__(self):
        # Constructor: inicializa la raíz con valor nulo
        self.__raizPtr: Nodo | None = None

    def esVacio(self) -> bool:
        """Verifica si la raíz del árbol apunta a vacío."""
        return self.__raizPtr is None

    def regresaRaiz(self) -> Nodo | None:
        """Regresa la referencia al nodo raíz del árbol."""
        return self.__raizPtr

    def insertar(self, valor: int) -> None:
        """Método envoltorio para insertar desde la raíz."""
        self.__raizPtr = self.insertarNodo(valor, self.__raizPtr)

    def insertarNodo(self, valor: int, nodoPtr: Nodo | None) -> Nodo:
        """Crea un nuevo nodo y lo inserta de forma recursiva en su posición ABB."""
        if nodoPtr is None:
            nodoPtr = Nodo(valor)
        elif valor < nodoPtr.dato:
            nodoPtr.izquierdoPtr = self.insertarNodo(valor, nodoPtr.izquierdoPtr)
        elif valor > nodoPtr.dato:
            nodoPtr.derechoPtr = self.insertarNodo(valor, nodoPtr.derechoPtr)
        return nodoPtr

    def muestraAcostado(self, nivel: int, nodoPtr: Nodo | None) -> None:
        """Muestra el árbol en forma horizontal con la raíz a la izquierda."""
        if nodoPtr is None:
            return
        self.muestraAcostado(nivel + 1, nodoPtr.derechoPtr)
        print("    " * nivel + str(nodoPtr.dato))
        self.muestraAcostado(nivel + 1, nodoPtr.izquierdoPtr)

    def graficarArbol(self, nodoPtr: Nodo | None) -> None:
        """Grafica el árbol completo de forma vertical en consola."""
        if nodoPtr is None:
            return

        h = self.altura(nodoPtr)
        filas = h * 2 - 1
        columnas = (2 ** h) * 3
        lienzo = [[" " for _ in range(columnas)] for _ in range(filas)]

        def llenar_lienzo(nodo: Nodo | None, x: int, y: int, desplazamiento: int) -> None:
            if nodo is None:
                return
            etiqueta = str(nodo.dato)
            inicio = max(0, x - len(etiqueta) // 2)
            for idx, ch in enumerate(etiqueta):
                if inicio + idx < columnas:
                    lienzo[y][inicio + idx] = ch

            if nodo.izquierdoPtr is not None and y + 1 < filas:
                lienzo[y + 1][max(0, x - desplazamiento // 2)] = "/"
                llenar_lienzo(
                    nodo.izquierdoPtr, x - desplazamiento, y + 2, max(2, desplazamiento // 2)
                )
            if nodo.derechoPtr is not None and y + 1 < filas:
                lienzo[y + 1][min(columnas - 1, x + desplazamiento // 2)] = "\\"
                llenar_lienzo(
                    nodo.derechoPtr, x + desplazamiento, y + 2, max(2, desplazamiento // 2)
                )

        llenar_lienzo(nodoPtr, columnas // 2, 0, max(2, columnas // 4))
        for fila in lienzo:
            linea = "".join(fila).rstrip()
            if linea:
                print(linea)

    def busqueda(self, x: int, nodoPtr: Nodo | None) -> bool:
        """Busca el valor 'x' de manera recursiva dentro del ABB."""
        if nodoPtr is None:
            return False
        elif x < nodoPtr.dato:
            return self.busqueda(x, nodoPtr.izquierdoPtr)
        elif x > nodoPtr.dato:
            return self.busqueda(x, nodoPtr.derechoPtr)
        else:
            return True

    def buscaMenor(self, nodoPtr: Nodo | None) -> Nodo | None:
        """Regresa el nodo con el dato menor del árbol o subárbol."""
        if nodoPtr is None:
            return None
        while nodoPtr.izquierdoPtr is not None:
            nodoPtr = nodoPtr.izquierdoPtr
        return nodoPtr

    def buscaMayor(self, nodoPtr: Nodo | None) -> Nodo | None:
        """Regresa el nodo con el dato mayor del árbol o subárbol."""
        if nodoPtr is None:
            return None
        while nodoPtr.derechoPtr is not None:
            nodoPtr = nodoPtr.derechoPtr
        return nodoPtr

    def eliminarPorPredecesor(self, x: int) -> None:
        """Método envoltorio para eliminar usando el predecesor en InOrden."""
        self.__raizPtr = self.eliminarPredecesor(x, self.__raizPtr)

    def eliminarPredecesor(self, x: int, nodoPtr: Nodo | None) -> Nodo | None:
        """Elimina el nodo con dato 'x'; si tiene dos hijos, sustituye por el predecesor."""
        if nodoPtr is None:
            return None

        if x < nodoPtr.dato:
            nodoPtr.izquierdoPtr = self.eliminarPredecesor(x, nodoPtr.izquierdoPtr)
        elif x > nodoPtr.dato:
            nodoPtr.derechoPtr = self.eliminarPredecesor(x, nodoPtr.derechoPtr)
        else:
            # Caso 1: Nodo sin hijos (hoja)
            if nodoPtr.izquierdoPtr is None and nodoPtr.derechoPtr is None:
                return None
            # Caso 2: Nodo con un solo subárbol hijo
            elif nodoPtr.izquierdoPtr is None:
                return nodoPtr.derechoPtr
            elif nodoPtr.derechoPtr is None:
                return nodoPtr.izquierdoPtr
            # Caso 3: Nodo con dos subárboles hijo (mayor del subárbol izquierdo)
            else:
                mayor = self.buscaMayor(nodoPtr.izquierdoPtr)
                nodoPtr.dato = mayor.dato
                nodoPtr.izquierdoPtr = self.eliminarPredecesor(
                    mayor.dato, nodoPtr.izquierdoPtr
                )
        return nodoPtr

    def eliminarPorSucesor(self, x: int) -> None:
        """Método envoltorio para eliminar usando el sucesor en InOrden."""
        self.__raizPtr = self.eliminarSucesor(x, self.__raizPtr)

    def eliminarSucesor(self, x: int, nodoPtr: Nodo | None) -> Nodo | None:
        """Elimina el nodo con dato 'x'; si tiene dos hijos, sustituye por el sucesor."""
        if nodoPtr is None:
            return None

        if x < nodoPtr.dato:
            nodoPtr.izquierdoPtr = self.eliminarSucesor(x, nodoPtr.izquierdoPtr)
        elif x > nodoPtr.dato:
            nodoPtr.derechoPtr = self.eliminarSucesor(x, nodoPtr.derechoPtr)
        else:
            # Caso 1: Nodo sin hijos (hoja)
            if nodoPtr.izquierdoPtr is None and nodoPtr.derechoPtr is None:
                return None
            # Caso 2: Nodo con un solo subárbol hijo
            elif nodoPtr.izquierdoPtr is None:
                return nodoPtr.derechoPtr
            elif nodoPtr.derechoPtr is None:
                return nodoPtr.izquierdoPtr
            # Caso 3: Nodo con dos subárboles hijo (menor del subárbol derecho)
            else:
                menor = self.buscaMenor(nodoPtr.derechoPtr)
                nodoPtr.dato = menor.dato
                nodoPtr.derechoPtr = self.eliminarSucesor(
                    menor.dato, nodoPtr.derechoPtr
                )
        return nodoPtr

    def preOrden(self, nodoPtr: Nodo | None) -> None:
        """Recorrido en PreOrden: raíz -> izquierdo -> derecho."""
        if nodoPtr is None:
            return
        print(f"{nodoPtr.dato}", end=" - ")
        self.preOrden(nodoPtr.izquierdoPtr)
        self.preOrden(nodoPtr.derechoPtr)

    def inOrden(self, nodoPtr: Nodo | None) -> None:
        """Recorrido en InOrden: izquierdo -> raíz -> derecho."""
        if nodoPtr is None:
            return
        self.inOrden(nodoPtr.izquierdoPtr)
        print(f"{nodoPtr.dato}", end=" - ")
        self.inOrden(nodoPtr.derechoPtr)

    def postOrden(self, nodoPtr: Nodo | None) -> None:
        """Recorrido en PostOrden: izquierdo -> derecho -> raíz."""
        if nodoPtr is None:
            return
        self.postOrden(nodoPtr.izquierdoPtr)
        self.postOrden(nodoPtr.derechoPtr)
        print(f"{nodoPtr.dato}", end=" - ")

    def recorridoNiveles(self, nodoPtr: Nodo | None) -> None:
        """Recorre el árbol por niveles (amplitud) utilizando una cola."""
        if nodoPtr is None:
            return

        colaAuxiliar: deque[Nodo] = deque()
        colaAuxiliar.append(nodoPtr)

        while colaAuxiliar:
            nodoAuxiliar = colaAuxiliar.popleft()
            print(f"{nodoAuxiliar.dato}", end=" - ")

            if nodoAuxiliar.izquierdoPtr is not None:
                colaAuxiliar.append(nodoAuxiliar.izquierdoPtr)
            if nodoAuxiliar.derechoPtr is not None:
                colaAuxiliar.append(nodoAuxiliar.derechoPtr)

    def altura(self, nodoPtr: Nodo | None) -> int:
        """Obtiene la altura (número máximo de niveles; árbol vacío = 0, raíz = 1)."""
        if nodoPtr is None:
            return 0
        alturaIzq = self.altura(nodoPtr.izquierdoPtr)
        alturaDer = self.altura(nodoPtr.derechoPtr)
        return max(alturaIzq, alturaDer) + 1

    def contarHojas(self, nodoPtr: Nodo | None) -> int:
        """Obtiene la cantidad de nodos hoja (nodos sin hijos) del árbol."""
        if nodoPtr is None:
            return 0
        if nodoPtr.izquierdoPtr is None and nodoPtr.derechoPtr is None:
            return 1
        return self.contarHojas(nodoPtr.izquierdoPtr) + self.contarHojas(nodoPtr.derechoPtr)

    def contarNodos(self, nodoPtr: Nodo | None) -> int:
        """Obtiene la cantidad total de nodos del árbol."""
        if nodoPtr is None:
            return 0
        return (
            self.contarNodos(nodoPtr.izquierdoPtr)
            + self.contarNodos(nodoPtr.derechoPtr)
            + 1
        )

    def arbolEspejo(self, nodoPtr: Nodo | None) -> Nodo | None:
        """Genera una copia reflejada (espejo) del árbol."""
        if nodoPtr is None:
            return None
        nodoEspejo = Nodo(nodoPtr.dato)
        nodoEspejo.izquierdoPtr = self.arbolEspejo(nodoPtr.derechoPtr)
        nodoEspejo.derechoPtr = self.arbolEspejo(nodoPtr.izquierdoPtr)
        return nodoEspejo

    def esCompleto(self, nodoPtr: Nodo | None) -> bool:
        """Determina si el árbol binario es completo mediante recorrido por niveles."""
        if nodoPtr is None:
            return True

        colaAuxiliar: deque[Nodo] = deque([nodoPtr])
        nodoNoLleno = False

        while colaAuxiliar:
            nodoAuxiliar = colaAuxiliar.popleft()

            if nodoAuxiliar.izquierdoPtr is not None:
                if nodoNoLleno:
                    return False
                colaAuxiliar.append(nodoAuxiliar.izquierdoPtr)
            else:
                nodoNoLleno = True

            if nodoAuxiliar.derechoPtr is not None:
                if nodoNoLleno:
                    return False
                colaAuxiliar.append(nodoAuxiliar.derechoPtr)
            else:
                nodoNoLleno = True

        return True

    def esLleno(self, nodoPtr: Nodo | None) -> bool:
        """Determina recursivamente si todos los nodos tienen 0 o 2 hijos."""
        if nodoPtr is None:
            return True
        if nodoPtr.izquierdoPtr is None and nodoPtr.derechoPtr is None:
            return True
        if nodoPtr.izquierdoPtr is not None and nodoPtr.derechoPtr is not None:
            return self.esLleno(nodoPtr.izquierdoPtr) and self.esLleno(nodoPtr.derechoPtr)
        return False

    def eliminarArbol(self) -> None:
        """Libera todos los nodos del árbol y restablece la raíz a None."""
        self.__raizPtr = self.podarArbol(self.__raizPtr)

    def podarArbol(self, nodoPtr: Nodo | None) -> None:
        """Elimina recursivamente en PostOrden los nodos del árbol."""
        if nodoPtr is None:
            return None
        nodoPtr.izquierdoPtr = self.podarArbol(nodoPtr.izquierdoPtr)
        nodoPtr.derechoPtr = self.podarArbol(nodoPtr.derechoPtr)
        return None


def menu() -> None:
    print("\n" + "=" * 55)
    print("        ÁRBOL BINARIO DE BÚSQUEDA (ABB) - MENÚ")
    print("=" * 55)
    print(" [1]  Insertar elemento")
    print(" [2]  Mostrar árbol completo acostado (raíz a la izquierda)")
    print(" [3]  Graficar árbol completo")
    print(" [4]  Buscar un elemento en el árbol")
    print(" [5]  Recorrer el árbol en PreOrden")
    print(" [6]  Recorrer el árbol en InOrden")
    print(" [7]  Recorrer el árbol en PostOrden")
    print(" [8]  Eliminar un nodo del árbol (PREDECESOR)")
    print(" [9]  Eliminar un nodo del árbol (SUCESOR)")
    print(" [10] Recorrer el árbol por niveles (Amplitud)")
    print(" [11] Altura del árbol")
    print(" [12] Cantidad de hojas del árbol")
    print(" [13] Cantidad de nodos del árbol")
    print(" [14] Mostrar árbol espejo acostado")
    print(" [15] Revisar si es un árbol binario completo")
    print(" [16] Revisar si es un árbol binario lleno")
    print(" [17] Eliminar el árbol (Podar)")
    print(" [0]  Salir")
    print("=" * 55)


def main() -> None:
    arbolEnteros = Arbol()

    while True:
        menu()
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("\nError: Ingrese un número entero válido.")
            continue

        raizArbolPtr = arbolEnteros.regresaRaiz()

        if opcion == 0:
            arbolEnteros.eliminarArbol()
            print("\nPrograma finalizado.")
            break

        elif opcion == 1:
            try:
                valor = int(input("\nIngrese valor entero a insertar: "))
                arbolEnteros.insertar(valor)
                print(f"Elemento {valor} procesado.")
            except ValueError:
                print("\nError: Debe ingresar un número entero.")

        elif opcion in range(2, 18) and arbolEnteros.esVacio():
            print("\nEl árbol está vacío.")

        elif opcion == 2:
            print("\nÁrbol acostado con la raíz a la izquierda:\n")
            arbolEnteros.muestraAcostado(0, raizArbolPtr)

        elif opcion == 3:
            print("\nGráfico del árbol completo:\n")
            arbolEnteros.graficarArbol(raizArbolPtr)

        elif opcion == 4:
            try:
                x = int(input("\nIngrese valor entero a buscar: "))
                if arbolEnteros.busqueda(x, raizArbolPtr):
                    print(f"\nElemento {x} ha sido encontrado en el árbol.")
                else:
                    print(f"\nElemento {x} no encontrado.")
            except ValueError:
                print("\nError: Debe ingresar un número entero.")

        elif opcion == 5:
            print("\nRecorrido en PreOrden: ", end="")
            arbolEnteros.preOrden(raizArbolPtr)
            print("FIN")

        elif opcion == 6:
            print("\nRecorrido en InOrden: ", end="")
            arbolEnteros.inOrden(raizArbolPtr)
            print("FIN")

        elif opcion == 7:
            print("\nRecorrido en PostOrden: ", end="")
            arbolEnteros.postOrden(raizArbolPtr)
            print("FIN")

        elif opcion == 8:
            try:
                x = int(input("\nIngrese valor a eliminar (Predecesor): "))
                if arbolEnteros.busqueda(x, raizArbolPtr):
                    arbolEnteros.eliminarPorPredecesor(x)
                    print(f"Elemento {x} eliminado usando Predecesor.")
                else:
                    print(f"El elemento {x} no existe en el árbol.")
            except ValueError:
                print("\nError: Debe ingresar un número entero.")

        elif opcion == 9:
            try:
                x = int(input("\nIngrese valor a eliminar (Sucesor): "))
                if arbolEnteros.busqueda(x, raizArbolPtr):
                    arbolEnteros.eliminarPorSucesor(x)
                    print(f"Elemento {x} eliminado usando Sucesor.")
                else:
                    print(f"El elemento {x} no existe en el árbol.")
            except ValueError:
                print("\nError: Debe ingresar un número entero.")

        elif opcion == 10:
            print("\nRecorrido por niveles (Amplitud): ", end="")
            arbolEnteros.recorridoNiveles(raizArbolPtr)
            print("FIN")

        elif opcion == 11:
            print(f"\nAltura del árbol: {arbolEnteros.altura(raizArbolPtr)}")

        elif opcion == 12:
            print(f"\nCantidad de hojas del árbol: {arbolEnteros.contarHojas(raizArbolPtr)}")

        elif opcion == 13:
            print(f"\nCantidad de nodos del árbol: {arbolEnteros.contarNodos(raizArbolPtr)}")

        elif opcion == 14:
            print("\nÁrbol espejo acostado:\n")
            raizEspejo = arbolEnteros.arbolEspejo(raizArbolPtr)
            arbolEnteros.muestraAcostado(0, raizEspejo)

        elif opcion == 15:
            if arbolEnteros.esCompleto(raizArbolPtr):
                print("\nEl árbol ES un árbol binario completo.")
            else:
                print("\nEl árbol NO es un árbol binario completo.")

        elif opcion == 16:
            if arbolEnteros.esLleno(raizArbolPtr):
                print("\nEl árbol ES un árbol binario lleno.")
            else:
                print("\nEl árbol NO es un árbol binario lleno.")

        elif opcion == 17:
            arbolEnteros.eliminarArbol()
            print("\nEl árbol ha sido eliminado (podado) por completo.")

        else:
            print("\nOpción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()