from backend.data.manager import Manager


def get_ventas(data_manager: Manager):
    return data_manager.get_data('ventas')


def add_venta(data_manager: Manager, venta: dict):
    return data_manager.add_data('ventas', venta)
