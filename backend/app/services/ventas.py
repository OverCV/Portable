# backend/app/services/ventas.py

from backend.data.manager import Manager
from datetime import datetime
from typing import List, Dict


def get_ventas(data_manager: Manager):
    return data_manager.get_data('ventas')


def add_venta(data_manager: Manager, venta: Dict, productos: List[Dict]):
    # Crear la venta principal
    venta_id = len(data_manager.get_data('ventas')) + 1
    venta['id'] = venta_id
    venta['fecha_venta'] = datetime.now().isoformat()

    # Guardar la venta en la base de datos
    data_manager.add_data('ventas', venta)

    # Registrar cada producto de la venta en 'venta_productos'
    for producto in productos:
        print(f'{producto=}')
        venta_producto = {
            'id_venta': venta_id,
            'id_producto': producto['id'],
            'cantidad': producto['cantidad'],
        }
        data_manager.add_data('venta_productos', venta_producto)

    return venta
