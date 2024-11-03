# backend/app/services/ventas.py

from datetime import datetime
from backend.data.manager import Manager
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
        venta_producto = {
            'id_venta': venta_id,
            'id_producto': producto['id'],
            'cantidad': producto['cantidad'],
        }
        data_manager.add_data('venta_productos', venta_producto)

        # Actualizar el stock del producto
        nuevo_stock = int(producto['stock']) - producto['cantidad']
        producto_actualizado = {
            'id': producto['id'],
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'stock': str(nuevo_stock),
        }
        put_producto(data_manager, producto['id'], producto_actualizado)

    return venta


def calcular_total_venta(productos_venta: list[dict]) -> float:
    """Calcula el total de la venta en base a la lista de productos."""
    return sum(venta['precio'] * venta['cantidad'] for venta in productos_venta)


def filtrar_productos_con_stock(productos: list[dict]) -> list[dict]:
    """Filtra productos con stock disponible."""
    return [producto for producto in productos if int(producto['stock']) > 0]
