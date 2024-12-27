import sqlite3
import os
from colorama import init, Fore, Back, Style
# Se importa la libreria de colorama que luego de instlar y aplicar, modificará la apariencia en la que se muestra la salida de la ejecución del código
init(autoreset=True)

# Aqui abajo se definen los diferentes estilos que se aplicarán, para no tener que detallarlo nuevamente dentro de cada instrucción
estilo_titulo = Fore.MAGENTA + Back.WHITE
estilo_menu = Style.BRIGHT + Fore.MAGENTA
estilo_aviso = Back.GREEN + Fore.RED
estilo_alerta = Back.RED + Fore.BLACK + Style.BRIGHT
estilo_exito = Back.GREEN + Fore.BLACK + Style.BRIGHT


conexion = sqlite3.connect("./base-de-datos-final-productos.db") # se conecta a la base de datos de SQLite
cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT NOT NULL,
                stock INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT NOT NULL)''') # se crea las base de datos si no existe
conexion.close()

def agregar_producto(nombre, descripcion, stock, precio, categoria): # Se crea/define la función
    datos = [nombre, descripcion, stock, precio, categoria]
    conexion = sqlite3.connect("./base-de-datos-final-productos.db") # Aqui se conecta la función a la base de datos
    cursor = conexion.cursor()    
    cursor.execute("INSERT INTO productos (nombre, descripcion, stock, precio, categoria) VALUES (?, ?, ?, ?, ?)", datos)
    conexion.commit() # pasa los valores
    print(f"Producto {nombre} agregado con éxito") # Imprime el producto agregado
    conexion.close() # cierra la conexión con la base de datos

def mostrar_productos(productos = 0, unico_producto = False): # Se crea/define la función
    if productos == 0:
        conexion = sqlite3.connect("./base-de-datos-final-productos.db") # Aqui se conecta la función a la base de datos
        cursor = conexion.cursor() # declara el cursor
        cursor.execute("SELECT * FROM productos") # trae los datos
        resultados = cursor.fetchall() # trae los datos y los guarda dentro de la variable como un a lista        
        for registro in resultados: # itera los resultados de la lista que trajo
            print("ID:", registro[0], "Nombre:", registro[1], "Descripcion:", registro[2], "Stock:", registro[3], "Precio:", registro[4], "Categoria", registro[5])
        conexion.close() # cierra la conexión con la base de datos
    else:
        if unico_producto:
            print("ID:", productos[0], "Nombre:", productos[1], "Descripcion:", productos[2], "Stock:", productos[3], "Precio:", productos[4], "Categoria", productos[5])
        else:
            for registro in productos:
                print("ID:", registro[0], "Nombre:", registro[1], "Descripcion:", registro[2], "Stock:", registro[3], "Precio:", registro[4], "Categoria", registro[5])
        
def actualizar_producto(): # Se crea/define la función
    mostrar_productos()
    codigo = 0
    while codigo <= 0:
        try:
            codigo = int(input("Ingrese el codigo del producto que desea modificar")) # solicita datos al usuario
            if codigo <=0:
                print("Ingrese un numero mayor que 0")
        except ValueError:
            print("Ingrese un numero")
            codigo = 0
    nombre = input("Ingrese el nuevo nombre del producto") # solicita datos al usuario
    descripcion = input("Ingrese la nueva descripcion del producto") # solicita datos al usuario
    stock = 0
    while stock <= 0:
        try:
            stock = int(input("Ingrese el nuevo stock")) # solicita datos al usuario
            if stock <0:
                print("Ingrese un numero mayor que 0") 
        except ValueError:
            print("Ingrese un numero")
            stock = 0
    precio = 0
    while precio <= 0:
        try:
            precio = int(input("Ingrese el nuevo precio")) # solicita datos al usuario
            if precio <= 0:
                print("Ingrese un numero mayor que 0")
        except ValueError:
            print("Ingrese un numero")
            precio = 0
    categoria = input("Ingrese la nueva categoria")
    conexion = sqlite3.connect("./base-de-datos-final-productos.db") # Aqui se conecta la función a la base de datos
    cursor = conexion.cursor()
    
    cursor.execute('''UPDATE productos SET nombre = ?, descripcion = ?, stock = ?, precio = ?, categoria = ? WHERE id = ?''', (nombre, descripcion, stock, precio, categoria, codigo))
    conexion.commit()
    conexion.close() # cierra la conexión con la base de datos
    mostrar_productos() # Se ejecuta la función

def eliminar_producto(): # Se crea/define la función
    mostrar_productos() # Se ejecuta la función
    codigo = 0 # Se asigna valor 0 al codigo para que entre al while
    while codigo <= 0:
        try:
            codigo = int(input("Ingrese el codigo del producto que desea eliminar"))
            if codigo <=0:
                print(estilo_aviso + "Ingrese un numero mayor que 0") # se imprime y aplica el estilo de colorama designado al inicio dentro de "estilo_aviso" 
        except ValueError:
            print(estilo_aviso + "Ingrese un numero")
            codigo = 0
    try: 
        with sqlite3.connect("./base-de-datos-final-productos.db") as cursor: 
            cursor.execute("DELETE FROM productos WHERE id = ?", (codigo, ))
            print(estilo_alerta + "Producto eliminado") # se imprime y aplica el estilo de colorama designado al inicio dentro de "estilo_alerta" 
    except ValueError:
        print("Codigo incorrecto")

def reporte_bajo_stock(): # Se crea/define la función
    valor_bajo = 0
    while valor_bajo <= 0:
        try:
            valor_bajo = int(input(estilo_menu + "Ingrese la cantidad minima de stock"))
            if valor_bajo <=0:
                print(estilo_aviso + "Ingrese un numero mayor que 0")
        except ValueError:
            print(estilo_aviso + "Ingrese un numero")
            valor_bajo = 0
    conexion = sqlite3.connect("./base-de-datos-final-productos.db") # Aqui se conecta la función a la base de datos
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE stock <= ?",(valor_bajo,))
    resultados = cursor.fetchall()
    if len(resultados) > 0:
        print(resultados)
        mostrar_productos(resultados)
    else:
        print(estilo_exito + "No hay productos con bajo stock")
    conexion.close()
        
def buscar_producto_por_nombre():  # Se crea/define la función
    nombre = input("Ingrese el nombre del producto a buscar: ").capitalize()
    conexion = sqlite3.connect("./base-de-datos-final-productos.db") # Aqui se conecta la función a la base de datos
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = ?",(nombre,))
    #contador = cursor.fetchone()[0]
    resultados = cursor.fetchone()
    #print(resultados)
    if resultados != None:
        mostrar_productos(resultados, True)
    else:
        print("Registro no encontrado")
    conexion.close() # cierra la conexión con la base de datos

def mostrar_menu():
    print(estilo_titulo + "Gestión del inventario PFI")
    print(estilo_menu + "1. Agregar producto")
    print(estilo_menu + "2. Mostrar todos los productos")
    print(estilo_menu + "3. Actualizar producto")
    print(estilo_menu + "4. Eliminar producto")
    print(estilo_menu + "5. Reporte de bajo stock")
    print(estilo_menu + "6. Buscar producto")
    print(estilo_menu + "7. Salir")

def main(): # Se crea/define la función Menú
    menu = True
    while menu:
        mostrar_menu()
        opcion = input("Ingrese la opcion deseada: ")
        if opcion == "1":
            #nombre, descripcion, stock, precio, categoria
            nombre = input("Ingrese el nombre del producto: ").capitalize() # con "capitalize"se pasan con su primer carácter en mayúsculas y el resto en minúsculas los valores ingresados por el usuario 
            descripcion = input("Descripcion: ").capitalize() # con "capitalize"se pasan con su primer carácter en mayúsculas y el resto en minúsculas los valores ingresados por el usuario
            stock = 0
            while stock <= 0:
                try:
                    stock = int(input("Cantidad: "))
                    if stock <=0:
                        print(estilo_aviso + "Ingrese un numero mayor que 0")
                except ValueError:
                    print(estilo_aviso + "Ingrese un numero")
                    stock = 0
            precio = 0
            while precio <= 0:
                try:
                    precio = int(input("Precio: "))
                    if precio <=0:
                        print(estilo_aviso + "Ingrese un numero mayor que 0")
                except ValueError:
                    print(estilo_aviso + "Ingrese un numero")
                    precio = 0
            categoria = input("Categoria: ").capitalize()
            agregar_producto(nombre, descripcion, stock, precio, categoria)
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            reporte_bajo_stock()
        elif opcion == "6":
            buscar_producto_por_nombre()
        elif opcion == "7":
            menu = False
        else:
            print(estilo_alerta + "Opcion incorrecta\n")

main()