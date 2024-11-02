from backend.data.manager import Manager


def get_productos(data_manager: Manager):
    return data_manager.get_data('productos')


def add_producto(data_manager: Manager, producto: dict):
    return data_manager.add_data('productos', producto)
