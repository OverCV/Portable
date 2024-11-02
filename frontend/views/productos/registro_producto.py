# views/productos.py
import flet as fl

from frontend.enums.routes import Routes

from backend.data.managers.csv_manager import CSVManager
from backend.app.services.productos import (
    get_productos,
    add_producto,
)


def create_productos(page: fl.Page, data_manager: CSVManager):
    def handle_add_producto(e):
        modal = fl.AlertDialog(
            modal=True,
            title=fl.Text('Nuevo Producto'),
            content=fl.Column(
                [
                    fl.TextField(
                        label='Nombre',
                        ref=(nombre_ref := fl.Ref[fl.TextField]()),
                    ),
                    fl.TextField(
                        label='Precio',
                        keyboard_type=fl.KeyboardType.NUMBER,
                        ref=(precio_ref := fl.Ref[fl.TextField]()),
                    ),
                    fl.TextField(
                        label='Cantidad',
                        keyboard_type=fl.KeyboardType.NUMBER,
                        ref=(cantidad_ref := fl.Ref[fl.TextField]()),
                    ),
                ],
                tight=True,
            ),
            actions=[
                fl.TextButton('Cancelar', on_click=lambda _: setattr(modal, 'open', False)),
                fl.TextButton('Guardar', on_click=lambda _: save_producto()),
            ],
        )

        def save_producto():
            nuevo_producto = {
                'nombre': nombre_ref.current.value,
                'precio': float(precio_ref.current.value),
                'cantidad': int(cantidad_ref.current.value),
            }
            add_producto(data_manager, nuevo_producto)
            modal.open = False
            page.update()
            refresh_productos()

        page.dialog = modal
        modal.open = True
        page.update()

    def refresh_productos():
        productos_list.controls = [create_producto_card(p) for p in get_productos(data_manager)]
        page.update()

    def create_producto_card(producto: dict) -> fl.Card:
        return fl.Card(
            content=fl.Container(
                content=fl.Column(
                    [
                        fl.ListTile(
                            leading=fl.Icon(fl.icons.INVENTORY),
                            title=fl.Text(producto['nombre'], size=16),
                            subtitle=fl.Text(
                                f"Precio: ${producto['precio']} - Stock: {producto['cantidad']}"
                            ),
                        ),
                        fl.Row(
                            [
                                fl.IconButton(
                                    icon=fl.icons.EDIT,
                                    tooltip='Editar',
                                    # on_click=lambda e: edit_producto(producto),
                                ),
                                fl.IconButton(
                                    icon=fl.icons.DELETE,
                                    tooltip='Eliminar',
                                    # on_click=lambda e: delete_producto(producto),
                                ),
                            ],
                            alignment=fl.MainAxisAlignment.END,
                        ),
                    ]
                ),
                padding=10,
            ),
        )

    productos_list = fl.ListView(
        spacing=10,
        padding=20,
        expand=True,
    )

    view = fl.View(
        Routes.PRODUCTOS,
        [
            fl.AppBar(
                title=fl.Text('Productos'),
                center_title=True,
                actions=[
                    fl.IconButton(
                        icon=fl.icons.ADD,
                        tooltip='Agregar Producto',
                        on_click=handle_add_producto,
                    ),
                ],
            ),
            productos_list,
        ],
    )

    refresh_productos()
    return view
