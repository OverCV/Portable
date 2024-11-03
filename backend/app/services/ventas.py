# backend/app/services/ventas.py

from backend.data.manager import Manager
from datetime import datetime


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

        # Actualizar el stock del producto en el archivo 'productos'
        productos_data = data_manager.get_data('productos')
        producto_actual = next((p for p in productos_data if int(p['id']) == producto['id']), None)

        if producto_actual:
            nuevo_stock = int(producto_actual['cantidad']) - producto['cantidad']
            if nuevo_stock < 0:
                raise ValueError(f"Stock insuficiente para el producto {producto_actual['nombre']}")

            # Actualizar el producto con el nuevo stock
            producto_actual['cantidad'] = str(
                nuevo_stock
            )  # Convertimos a string para guardar en CSV
            data_manager.put_data('productos', producto['id'], producto_actual)

    return venta
