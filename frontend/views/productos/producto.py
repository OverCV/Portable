# views/productos.py
import flet as ft
from backend.data.managers.json_manager import DataManager


def create_productos(page: ft.Page, data_manager: DataManager):
    def handle_add_producto(e):
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo Producto"),
            content=ft.Column(
                [
                    ft.TextField(
                        label="Nombre", ref=(nombre_ref := ft.Ref[ft.TextField]())
                    ),
                    ft.TextField(
                        label="Precio",
                        keyboard_type=ft.KeyboardType.NUMBER,
                        ref=(precio_ref := ft.Ref[ft.TextField]()),
                    ),
                    ft.TextField(
                        label="Cantidad",
                        keyboard_type=ft.KeyboardType.NUMBER,
                        ref=(cantidad_ref := ft.Ref[ft.TextField]()),
                    ),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    "Cancelar", on_click=lambda _: setattr(modal, "open", False)
                ),
                ft.TextButton("Guardar", on_click=lambda _: save_producto()),
            ],
        )

        def save_producto():
            nuevo_producto = {
                "nombre": nombre_ref.current.value,
                "precio": float(precio_ref.current.value),
                "cantidad": int(cantidad_ref.current.value),
            }
            data_manager.add_producto(nuevo_producto)
            modal.open = False
            page.update()
            refresh_productos()

        page.dialog = modal
        modal.open = True
        page.update()

    def refresh_productos():
        productos_list.controls = [
            create_producto_card(p) for p in data_manager.get_productos()
        ]
        page.update()

    def create_producto_card(producto: dict) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.INVENTORY),
                            title=ft.Text(producto["nombre"], size=16),
                            subtitle=ft.Text(
                                f"Precio: ${producto['precio']} - Stock: {producto['cantidad']}"
                            ),
                        ),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    tooltip="Editar",
                                    # on_click=lambda e: edit_producto(producto),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip="Eliminar",
                                    # on_click=lambda e: delete_producto(producto),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                padding=10,
            ),
        )

    productos_list = ft.ListView(
        spacing=10,
        padding=20,
        expand=True,
    )

    view = ft.View(
        "/productos",
        [
            ft.AppBar(
                title=ft.Text("Productos"),
                center_title=True,
                actions=[
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        tooltip="Agregar Producto",
                        on_click=handle_add_producto,
                    ),
                ],
            ),
            productos_list,
        ],
    )

    refresh_productos()
    return view