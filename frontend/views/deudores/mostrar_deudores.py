# views/productos.py
import flet as ft

from frontend.enums.routes import Routes

from backend.data.managers.csv_manager import CSVManager



def mostrar_deudores(page: ft.Page, data_manager: CSVManager):
    productos_list = ft.ListView(
        spacing=10,
        padding=20,
        expand=True,
    )

    view = ft.View(
        Routes.DEUDORES,
        [
            ft.AppBar(
                title=ft.Text('Quiénes me deben ⚖️👩‍⚖️📜💰'),
                center_title=True,
                actions=[
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        tooltip='Agregar historia',
                        # on_click=handle_add_producto,
                    ),
                ],
            ),
            productos_list,
        ],
    )

    page.update()
    return view
