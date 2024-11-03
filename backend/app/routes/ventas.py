# backend/routes/ventas.py

from backend.app.services.ventas import (
    add_venta,
    get_ventas,
    calcular_total_venta,
    filtrar_productos_con_stock,
)


def registrar_venta(data_manager, venta_data, productos_venta):
    """Función que maneja el registro de una venta completa."""
    return add_venta(data_manager, venta_data, productos_venta)


def obtener_ventas(data_manager):
    return get_ventas(data_manager)


def obtener_total_venta(productos_venta):
    return calcular_total_venta(productos_venta)


def obtener_productos_disponibles(data_manager):
    productos = data_manager.get_data('productos')
    return filtrar_productos_con_stock(productos)
