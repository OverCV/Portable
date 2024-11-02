# views/productos.py
import flet as ft

from frontend.enums.routes import Routes

from backend.data.managers.csv_manager import CSVManager
from backend.app.services.productos import (
    get_productos,
    add_producto,
)


def mostrar_inicio(page: ft.Page, data_manager: CSVManager):
    productos_list = ft.ListView(
        spacing=10,
        padding=20,
        expand=True,
    )

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
            productos_list,
        ],
    )

    page.update()
    return view

    # def refresh_productos():
    #     productos_list.controls = [create_producto_card(p) for p in get_productos(data_manager)]
    #     page.update()

    # def create_producto_card(producto: dict) -> ft.Card:
    #     return ft.Card(
    #         content=ft.Container(
    #             content=ft.Column(
    #                 [
    #                     ft.ListTile(
    #                         leading=ft.Icon(ft.icons.INVENTORY),
    #                         title=ft.Text(producto['nombre'], size=16),
    #                         subtitle=ft.Text(
    #                             f"Precio: ${producto['precio']} - Stock: {producto['cantidad']}"
    #                         ),
    #                     ),
    #                     ft.Row(
    #                         [
    #                             ft.IconButton(
    #                                 icon=ft.icons.EDIT,
    #                                 tooltip='Editar',
    #                                 # on_click=lambda e: edit_producto(producto),
    #                             ),
    #                             ft.IconButton(
    #                                 icon=ft.icons.DELETE,
    #                                 tooltip='Eliminar',
    #                                 # on_click=lambda e: delete_producto(producto),
    #                             ),
    #                         ],
    #                         alignment=ft.MainAxisAlignment.END,
    #                     ),
    #                 ]
    #             ),
    #             padding=10,
    #         ),
    #     )

    # refresh_productos()
