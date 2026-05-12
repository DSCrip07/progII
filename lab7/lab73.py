def contar_palabras_unicas(texto):
    palabras = texto.lower().split()
    return len(set(palabras))


def palabra_mas_larga(texto):
    palabras = texto.split()
    return max(palabras, key=len)


def frecuencia_caracteres(texto):

    total = 0
    letras = {}

    for c in texto.lower():

        if c != " ":

            total += 1

            if c in letras:
                letras[c] += 1
            else:
                letras[c] = 1

    print("\nFrecuencia de caracteres:")

    for letra in letras:
        porcentaje = (letras[letra] / total) * 100
        print(letra, "=", letras[letra], "-", round(porcentaje, 2), "%")


texto = input("Ingrese un texto: ")

print("\nPalabras únicas:", contar_palabras_unicas(texto))
print("Palabra más larga:", palabra_mas_larga(texto))

frecuencia_caracteres(texto)