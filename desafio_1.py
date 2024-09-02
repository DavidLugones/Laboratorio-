import json

class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.__nombre = nombre
        self.__precio = precio
        self.__cantidad = cantidad

    def __str__(self):
        return f"{self.__nombre}: ${self.__precio} ({self.__cantidad} disponibles)"

    def actualizar_precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = nuevo_precio

    def actualizar_cantidad(self, nueva_cantidad):
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = nueva_cantidad

    def to_dict(self):
        return {
            'nombre': self.__nombre,
            'precio': self.__precio,
            'cantidad': self.__cantidad
        }

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['nombre'], dict_data['precio'], dict_data['cantidad'])

class ProductoElectronico(Producto):
    def __init__(self, nombre, precio, cantidad, marca):
        super().__init__(nombre, precio, cantidad)
        self.__marca = marca

    def __str__(self):
        return f"{self._Producto__nombre} ({self.__marca}): ${self._Producto__precio} ({self._Producto__cantidad} disponibles)"

    def to_dict(self):
        data = super().to_dict()
        data['marca'] = self.__marca
        return data

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['nombre'], dict_data['precio'], dict_data['cantidad'], dict_data['marca'])

class ProductoAlimenticio(Producto):
    def __init__(self, nombre, precio, cantidad, fecha_caducidad):
        super().__init__(nombre, precio, cantidad)
        self.__fecha_caducidad = fecha_caducidad

    def __str__(self):
        return f"{self._Producto__nombre}: ${self._Producto__precio} ({self._Producto__cantidad} disponibles, caduca el {self.__fecha_caducidad})"

    def to_dict(self):
        data = super().to_dict()
        data['fecha_caducidad'] = self.__fecha_caducidad
        return data

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['nombre'], dict_data['precio'], dict_data['cantidad'], dict_data['fecha_caducidad'])

class Inventario:
    def __init__(self, archivo):
        self.__archivo = archivo
        self.__productos = []

    def cargar_productos(self):
        try:
            with open(self.__archivo, 'r') as f:
                data = json.load(f)
                for item in data:
                    if item.get('tipo') == 'electronico':
                        producto = ProductoElectronico.from_dict(item)
                    elif item.get('tipo') == 'alimenticio':
                        producto = ProductoAlimenticio.from_dict(item)
                    else:
                        producto = Producto.from_dict(item)
                    self.__productos.append(producto)
        except FileNotFoundError:
            print("El archivo no fue encontrado. Se inicializa un inventario vacío.")
            self.__productos = []
        except json.JSONDecodeError:
            print("Error al decodificar el archivo JSON. Asegúrate de que el formato sea correcto.")
            self.__productos = []

    def guardar_productos(self):
        try:
            with open(self.__archivo, 'w') as f:
                data = [producto.to_dict() for producto in self.__productos]
                json.dump(data, f, indent=4)
        except IOError:
            print("Error al intentar guardar los productos en el archivo.")

    def agregar_producto(self, producto):
        self.__productos.append(producto)
        self.guardar_productos()

    def eliminar_producto(self, nombre):
        for producto in self.__productos:
            if producto._Producto__nombre == nombre:
                self.__productos.remove(producto)
                self.guardar_productos()
                return True
        return False

    def buscar_producto(self, nombre):
        for producto in self.__productos:
            if producto._Producto__nombre == nombre:
                return producto
        return None

    def actualizar_producto(self, nombre, nuevo_producto):
        for i, producto in enumerate(self.__productos):
            if producto._Producto__nombre == nombre:
                self.__productos[i] = nuevo_producto
                self.guardar_productos()
                return True
        return False

def main():
    inventario = Inventario('productos.json')
    inventario.cargar_productos()

    while True:
        print("\nMenú de Inventario")
        print("1. Agregar Producto")
        print("2. Buscar Producto")
        print("3. Actualizar Producto")
        print("4. Eliminar Producto")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio del producto: "))
            cantidad = int(input("Cantidad del producto: "))
            tipo = input("Tipo (electronico/alimenticio): ")
            if tipo == 'electronico':
                marca = input("Marca: ")
                producto = ProductoElectronico(nombre, precio, cantidad, marca)
            elif tipo == 'alimenticio':
                fecha_caducidad = input("Fecha de caducidad: ")
                producto = ProductoAlimenticio(nombre, precio, cantidad, fecha_caducidad)
            else:
                producto = Producto(nombre, precio, cantidad)
            inventario.agregar_producto(producto)
            print("Producto agregado.")

        elif opcion == '2':
            nombre = input("Nombre del producto a buscar: ")
            producto = inventario.buscar_producto(nombre)
            if producto:
                print("Producto encontrado:", producto)
            else:
                print("Producto no encontrado.")

        elif opcion == '3':
            nombre = input("Nombre del producto a actualizar: ")
            nuevo_precio = float(input("Nuevo precio: "))
            nueva_cantidad = int(input("Nueva cantidad: "))
            producto = inventario.buscar_producto(nombre)
            if producto:
                producto.actualizar_precio(nuevo_precio)
                producto.actualizar_cantidad(nueva_cantidad)
                inventario.actualizar_producto(nombre, producto)
                print("Producto actualizado.")
            else:
                print("Producto no encontrado.")

        elif opcion == '4':
            nombre = input("Nombre del producto a eliminar: ")
            if inventario.eliminar_producto(nombre):
                print("Producto eliminado.")
            else:
                print("Producto no encontrado.")

        elif opcion == '5':
            print("Saliendo de la aplicación.")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
