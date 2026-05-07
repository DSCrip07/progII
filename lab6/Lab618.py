def contador(maximo):
    i = 1
    while i <= maximo:
        yield i
        i += 1

for num in contador(5):
    print(num)