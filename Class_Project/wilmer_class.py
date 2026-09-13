# Programación de una cuadrícula interactiva con selección de círculos mediante coordenadas

FILAS = 8
COLUMNAS = 8


# Solicita al usuario el tamaño de la cuadrícula
def solicitar_datos_cuadricula():
    while True:
        try:
            filas = int(input("Ingrese el número de filas mínimo 8: "))
            columnas = int(input("Ingrese el número de columnas mínimo 8: "))

            if filas >= 8 and columnas >= 8:
                return filas, columnas
            else:
                print("Por favor, ingrese valores desde 8 en adelante.")

        except ValueError:
            print("Entrada inválida. Debe ingresar números enteros.")


# Crea una cuadrícula según el número de filas y columnas
def crear_cuadricula(filas, columnas):
    cuadricula = []

    for fila in range(filas):
        fila_actual = []

        for columna in range(columnas):
            fila_actual.append("○")

        cuadricula.append(fila_actual)

    return cuadricula


# Muestra la cuadrícula en la consola
def mostrar_cuadricula(cuadricula):
    columnas = len(cuadricula[0])

    print()
    print("    ", end="")

    for columna in range(columnas):
        numero_columna = columna + 1
        print(numero_columna, end="   ")

    print()

    print("   ", end="")

    for columna in range(columnas):
        print("---", end=" ")

    print()

    for fila in range(len(cuadricula)):
        numero_fila = fila + 1
        if fila < 9:
            print(numero_fila, end=" | ")
        else:
            print(numero_fila, end="| ")

        for columna in range(columnas):
            circulo = cuadricula[fila][columna]
            print(circulo, end="   ")

        print()

    print()


# Permite seleccionar una coordenada
def seleccionar_coordenada(cuadricula, coordenadas):
    try:
        filas = len(cuadricula)
        columnas = len(cuadricula[0])

        x = int(input(f"Ingrese la coordenada X (1-{columnas}): "))
        y = int(input(f"Ingrese la coordenada Y (1-{filas}): "))

        if x < 1 or x > columnas or y < 1 or y > filas:
            print("Coordenada inválida.")
            print(f"X debe estar entre 1 y {columnas}.")
            print(f"Y debe estar entre 1 y {filas}.")
            return

        cuadricula[y - 1][x - 1] = "●"

        coordenada = (x, y)

        if coordenada not in coordenadas:
            coordenadas.append(coordenada)
            print(f"Coordenada ({x},{y}) seleccionada.")
        else:
            print(f"La coordenada ({x},{y}) ya estaba seleccionada.")

    except ValueError:
        print("Entrada inválida. Debe ingresar números.")


# Muestra las coordenadas seleccionadas
def mostrar_coordenadas(coordenadas):
    if len(coordenadas) == 0:
        print("No hay coordenadas seleccionadas.")
        return

    print()
    print("Coordenadas seleccionadas:")

    for coordenada in coordenadas:
        x = coordenada[0]
        y = coordenada[1]

        print("X:", x, "Y:", y)


# Reinicia la cuadrícula
def reiniciar(cuadricula, coordenadas):
    filas = len(cuadricula)
    columnas = len(cuadricula[0])

    for fila in range(filas):
        for columna in range(columnas):
            cuadricula[fila][columna] = "○"

    coordenadas.clear()

    print("La cuadrícula ha sido reiniciada.")


# Controla el menú principal
def menu():
    filas = FILAS
    columnas = COLUMNAS

    cuadricula = crear_cuadricula(filas, columnas)
    coordenadas = []

    while True:
        mostrar_cuadricula(cuadricula)

        print("Opciones:")
        print("1. Ingresar tamaño de la cuadrícula")
        print("2. Seleccionar coordenada")
        print("3. Ver coordenadas seleccionadas")
        print("4. Reiniciar cuadrícula")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            filas, columnas = solicitar_datos_cuadricula()

            cuadricula = crear_cuadricula(filas, columnas)

            coordenadas.clear()

            print()
            print("Se creó una nueva cuadrícula.")
            print("Filas:", filas)
            print("Columnas:", columnas)

        elif opcion == "2":
            seleccionar_coordenada(cuadricula, coordenadas)

        elif opcion == "3":
            mostrar_coordenadas(coordenadas)

        elif opcion == "4":
            reiniciar(cuadricula, coordenadas)

        elif opcion == "5":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


# Inicia el programa
menu()
