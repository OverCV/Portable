# views/productos.py
import flet as ft

from frontend.enums.routes import Routes

from backend.data.managers.csv_manager import CSVManager
from backend.app.services.productos import (
    get_productos,
    add_producto,
)


def mostrar_404(page: ft.Page, data_manager: CSVManager):
    productos_list = ft.ListView(
        spacing=10,
        padding=20,
        expand=True,
    )

    view = ft.View(
        Routes.NOT_FOUND,
        [
            ft.AppBar(
                title=ft.Text('Ooops (404 Error)... 🤷‍♂️🤷‍♀️'),
                center_title=True,
                actions=[
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        tooltip='Sitio desconocido',
                        # on_click=handle_add_producto,
                    ),
                ],
            ),
            productos_list,
        ],
    )

    page.update()
    return view
