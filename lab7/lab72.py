n = int(input("Ingrese un número par para el tamaño de la matriz: "))

if n % 2 != 0:
    print("El número debe ser par")
else:
    matriz = []

    for i in range(n):
        fila = []

        for j in range(n):
            if i == j:
                fila.append(1)
            else:
                fila.append(0)

        matriz.append(fila)

    print("\nMatriz Identidad:\n")

    for fila in matriz:
        for elemento in fila:
            print(elemento, end=" ")
        print()