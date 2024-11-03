# backend/app/services/ventas.py

from backend.data.manager import Manager
from datetime import datetime
from backend.app.services.productos import put_producto


def get_ventas(data_manager: Manager):
    return data_manager.get_data('ventas')


def add_venta(data_manager: Manager, venta: dict, productos: list[dict]):
    # Crear la venta principal
    venta_id = len(data_manager.get_data('ventas')) + 1
    venta['id'] = venta_id
    venta['fecha_venta'] = datetime.now().isoformat()

    # Guardar la venta en la base de datos
    data_manager.add_data('ventas', venta)

    # Registrar cada producto de la venta en 'venta_productos' y actualizar stock
    for producto in productos:
        # Guardar el producto de la venta en 'venta_productos'
        venta_producto = {
            'id_venta': venta_id,
            'id_producto': producto['id'],
            'cantidad': producto['cantidad'],
        }
        data_manager.add_data('venta_productos', venta_producto)

        # Calcular el nuevo stock sin volver a validar (asumimos que ya se verificó)
        nuevo_stock = int(producto['stock']) - producto['cantidad']

        # Crear un diccionario actualizado para el producto
        producto_actualizado = {
            'id': producto['id'],
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'stock': str(nuevo_stock)  # Convertir a string para guardar en CSV
        }

        # Actualizar el stock del producto en el archivo CSV usando `put_producto`
        put_producto(data_manager, producto['id'], producto_actualizado)

    return venta
