# Sumar 10 a una variable existente, luego multiplicar por argumento en otra lambda
sumar10 = lambda x: x + 10
multiplicar = lambda x, y: x * y

resultado = multiplicar(sumar10(5), 2)
print(resultado)