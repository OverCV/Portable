# views/productos.py
import flet as ft

from frontend.enums.routes import Routes

from backend.data.managers.csv_manager import CSVManager


def mostrar_inicio(page: ft.Page, data_manager: CSVManager):

    view = ft.View(
        Routes.HOME,
        [
            ft.AppBar(
                title=ft.Text('Inicio'),
                center_title=True,
                actions=[
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        tooltip='Agregar historia',
                        # on_click=handle_add_producto,
                    ),
                ],
            ),
        ],
    )

    page.update()
    return view