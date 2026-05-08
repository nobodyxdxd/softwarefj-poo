from cliente import Cliente

try:

    cliente1 = Cliente("Juan", "juan@gmail.com")

    print(cliente1.mostrar_info())

except Exception as e:

    print("Error:", e)