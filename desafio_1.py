import json

class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return f"{self.nombre}: ${self.precio} ({self.cantidad} disponibles)"

    def actualizar_precio(self, nuevo_precio):
        self.precio = nuevo_precio

    def actualizar_cantidad(self, nueva_cantidad):
        self.cantidad = nueva_cantidad

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad
        }

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['nombre'], dict_data['precio'], dict_data['cantidad'])

class ProductoElectronico(Producto):
    def __init__(self, nombre, precio, cantidad, marca):
        super().__init__(nombre, precio, cantidad)
        self.marca = marca

    def __str__(self):
        return f"{self.nombre} ({self.marca}): ${self.precio} ({self.cantidad} disponibles)"

    def to_dict(self):
        data = super().to_dict()
        data['marca'] = self.marca
        return data

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['nombre'], dict_data['precio'], dict_data['cantidad'], dict_data['marca'])

class ProductoAlimenticio(Producto):
    def __init__(self, nombre, precio, cantidad, fecha_caducidad):
        super().__init__(nombre, precio, cantidad)
        self.fecha_caducidad = fecha_caducidad

    def __str__(self):
        return f"{self.nombre}: ${self.precio} ({self.cantidad} disponibles, caduca el {self.fecha_caducidad})"

    def to_dict(self):
        data = super().to_dict()
        data['fecha_caducidad'] = self.fecha_caducidad
        return data

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['nombre'], dict_data['precio'], dict_data['cantidad'], dict_data['fecha_caducidad'])

class Inventario:
    def __init__(self, archivo):
        self.archivo = archivo
        self.productos = []

    def cargar_productos(self):
        try:
            with open(self.archivo, 'r') as f:
                data = json.load(f)
                for item in data:
                    if item.get('tipo') == 'electronico':
                        producto = ProductoElectronico.from_dict(item)
                    elif item.get('tipo') == 'alimenticio':
                        producto = ProductoAlimenticio.from_dict(item)
                    else:
                        producto = Producto.from_dict(item)
                    self.productos.append(producto)
        except FileNotFoundError:
            self.productos = []

    def guardar_productos(self):
        with open(self.archivo, 'w') as f:
            data = [producto.to_dict() for producto in self.productos]
            json.dump(data, f, indent=4)

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.guardar_productos()

    def eliminar_producto(self, nombre):
        for producto in self.productos:
            if producto.nombre == nombre:
                self.productos.remove(producto)
                self.guardar_productos()
                return True
        return False

    def buscar_producto(self, nombre):
        for producto in self.productos:
            if producto.nombre == nombre:
                return producto
        return None

    def actualizar_producto(self, nombre, nuevo_producto):
        for i, producto in enumerate(self.productos):
            if producto.nombre == nombre:
                self.productos[i] = nuevo_producto
                self.guardar_productos()
                return True
        return False

# Crear instancia de inventario y cargar productos desde archivo
inventario = Inventario('productos.json')
inventario.cargar_productos()

# Crear nuevos productos
producto1 = ProductoElectronico('Laptop', 120000, 10, 'Lenovo')
producto2 = ProductoAlimenticio('Leche', 3.5, 50, '2024-08-31')

# Agregar productos al inventario
inventario.agregar_producto(producto1)
inventario.agregar_producto(producto2)

# Buscar un producto por nombre
producto_busqueda = inventario.buscar_producto('Laptop')

if producto_busqueda:
    print("Producto encontrado:", producto_busqueda)
else:
    print("Producto no encontrado.")

# Actualizar un producto
producto1.actualizar_cantidad(5)
inventario.actualizar_producto('Laptop', producto1)

# Eliminar un producto
inventario.eliminar_producto('Leche')

# Guardar cambios en el archivo JSON
inventario.guardar_productos()
