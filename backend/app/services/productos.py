from backend.data.manager import Manager


def get_productos(data_manager: Manager) -> list[dict]:
    return data_manager.get_data('productos')


def add_producto(data_manager: Manager, producto: dict):
    return data_manager.add_data('productos', producto)


def put_producto(data_manager: Manager, id_producto: dict, nuevo_producto: dict):
    return data_manager.put_data(
        'productos',
        id_producto,
        nuevo_producto,
    )


def delete_producto(data_manager: Manager, id_producto: dict):
    return data_manager.delete_data('productos', id_producto)
