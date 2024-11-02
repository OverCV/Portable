# views/ventas.py
import flet as ft

from frontend.enums.routes import Routes

from backend.data.managers.csv_manager import CSVManager
from backend.app.services.ventas import (
    get_ventas,
    add_venta,
)


def create_ventas(page: ft.Page, data_manager: CSVManager):
    def handle_add_venta(e):
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text('Nueva Venta'),
            content=ft.Column(
                [
                    ft.TextField(
                        label='Nombre',
                        ref=(nombre_ref := ft.Ref[ft.TextField]()),
                    ),
                    ft.TextField(
                        label='Precio',
                        keyboard_type=ft.KeyboardType.NUMBER,
                        ref=(precio_ref := ft.Ref[ft.TextField]()),
                    ),
                    ft.TextField(
                        label='Cantidad',
                        keyboard_type=ft.KeyboardType.NUMBER,
                        ref=(cantidad_ref := ft.Ref[ft.TextField]()),
                    ),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton('Cancelar', on_click=lambda _: setattr(modal, 'open', False)),
                ft.TextButton('Guardar', on_click=lambda _: save_Venta()),
            ],
        )

        def save_Venta():
            nueva_venta = {
                'nombre': nombre_ref.current.value,
                'precio': float(precio_ref.current.value),
                'cantidad': int(cantidad_ref.current.value),
            }
            add_venta(data_manager, nueva_venta)
            modal.open = False
            page.update()
            refresh_ventas()

        page.dialog = modal
        modal.open = True
        page.update()

    def refresh_ventas():
        ventas_list.controls = [create_venta_card(p) for p in get_ventas(data_manager)]
        page.update()

    def create_venta_card(Venta: dict) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.INVENTORY),
                            title=ft.Text(Venta['nombre'], size=16),
                            subtitle=ft.Text(
                                f"Precio: ${Venta['precio']} - Stock: {Venta['cantidad']}"
                            ),
                        ),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    tooltip='Editar',
                                    # on_click=lambda e: edit_Venta(Venta),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip='Eliminar',
                                    # on_click=lambda e: delete_Venta(Venta),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                padding=10,
            ),
        )

    ventas_list = ft.ListView(
        spacing=10,
        padding=20,
        expand=True,
    )

    view = ft.View(
        Routes.VENTAS,
        [
            ft.AppBar(
                title=ft.Text('ventas'),
                center_title=True,
                actions=[
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        tooltip='Agregar Venta',
                        on_click=handle_add_venta,
                    ),
                ],
            ),
            ventas_list,
        ],
    )

    refresh_ventas()
    return view
