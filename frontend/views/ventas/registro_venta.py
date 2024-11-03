from datetime import datetime
import flet as fl

from frontend.enums.routes import Routes
from backend.data.managers.csv_manager import CSVManager
from backend.app.services.ventas import add_venta
from backend.app.services.productos import get_productos


def create_ventas(page: fl.Page, data_manager: CSVManager):
    productos = get_productos(data_manager)
    productos_venta = []
    total_venta = fl.Text(value='0', color='blue')
    devolucion_text = fl.Text('$0.00', size=16, weight=fl.FontWeight.BOLD, color=fl.colors.BLUE)

    # Crear diálogo de advertencia para monto insuficiente
    monto_insuficiente_dialog = fl.AlertDialog(
        title=fl.Text('Monto insuficiente'),
        content=fl.Text('El monto ingresado es insuficiente para realizar la venta.'),
        actions=[fl.TextButton('OK', on_click=lambda e: close_dialog())],
        open=False,
    )

    def filtrar_productos_con_stock():
        # Filtra solo los productos con stock > 0 para mostrar en el Dropdown
        return [
            fl.dropdown.Option(key=producto['id'], text=producto['nombre'])
            for producto in productos
            if int(producto['stock']) > 0
        ]

    def handle_producto_seleccionado(e):
        # Obtener el producto seleccionado
        producto_seleccionado = next((p for p in productos if p['id'] == producto_list.value), None)
        if producto_seleccionado:
            # Verificar si el producto ya está en la lista de ventas
            venta_existente = next(
                (v for v in productos_venta if v['nombre'] == producto_seleccionado['nombre']), None
            )
            if venta_existente:
                # Incrementar la cantidad solo si no excede el stock disponible
                if venta_existente['cantidad'] < int(producto_seleccionado['stock']):
                    venta_existente['cantidad'] += 1
                else:
                    page.overlay.append(
                        fl.SnackBar(
                            content=fl.Text(
                                f"Stock insuficiente para {producto_seleccionado['nombre']}"
                            ),
                            action='OK',
                        )
                    )
                    page.update()
            else:
                # Añadir el producto como nuevo si no está en la lista
                productos_venta.append(
                    {
                        'id': producto_seleccionado['id'],
                        'nombre': producto_seleccionado['nombre'],
                        'cantidad': 1,
                        'precio': float(producto_seleccionado['precio']),
                        'stock': int(producto_seleccionado['stock']),
                    }
                )
            actualizar_lista_ventas()
            actualizar_total()

    def actualizar_lista_ventas():
        ventas_list.controls.clear()

        # Agregar encabezado de la tabla
        ventas_list.controls.append(
            fl.Row(
                [
                    fl.Text('Producto', weight='bold'),
                    fl.Text('Cantidad', weight='bold'),
                    fl.Text('Precio', weight='bold'),
                ],
                alignment='spaceBetween',
            )
        )

        for venta in productos_venta:
            ventas_list.controls.append(
                fl.Row(
                    [
                        fl.Text(venta['nombre']),
                        fl.Row(
                            [
                                fl.IconButton(
                                    icon=fl.icons.REMOVE_CIRCLE_OUTLINE_ROUNDED,
                                    selected_icon=fl.icons.REMOVE_CIRCLE,
                                    on_click=lambda e, v=venta: modificar_cantidad(v, -1),
                                ),
                                fl.Text(str(venta['cantidad'])),
                                fl.IconButton(
                                    icon=fl.icons.ADD_CIRCLE_OUTLINE_ROUNDED,
                                    selected_icon=fl.icons.ADD_CIRCLE,
                                    on_click=lambda e, v=venta: modificar_cantidad(v, 1),
                                ),
                            ]
                        ),
                        fl.Text(f"{venta['precio'] * venta['cantidad']}"),
                    ],
                    alignment='spaceBetween',
                )
            )
        ventas_list.update()

    def modificar_cantidad(venta, delta):
        # Limitar el incremento de cantidad según el stock disponible
        if delta > 0 and venta['cantidad'] >= venta['stock']:
            page.overlay.append(
                fl.SnackBar(
                    content=fl.Text(f"Stock insuficiente para {venta['nombre']}"), action='OK'
                )
            )
            page.update()
            return
        venta['cantidad'] = max(1, venta['cantidad'] + delta)
        actualizar_lista_ventas()
        actualizar_total()

    def actualizar_total():
        total = sum(venta['precio'] * venta['cantidad'] for venta in productos_venta)
        total_venta.value = f'{total:.2f}'
        total_venta.update()
        calcular_devolucion(None)

    def calcular_devolucion(e):
        try:
            monto = int(monto_input.value) if monto_input.value else 0
            devolucion = monto - float(total_venta.value)
            devolucion_text.value = f'${devolucion:.2f}'

            # Cambiar el color del texto de devolución a rojo si es negativo
            if devolucion < 0:
                devolucion_text.color = fl.colors.RED
            else:
                devolucion_text.color = fl.colors.BLUE
            devolucion_text.update()
        except ValueError:
            devolucion_text.value = '$0.00'
            devolucion_text.color = fl.colors.RED
            monto_input.value = ''  # Resetear el campo si el valor no es válido
            monto_input.update()
        devolucion_text.update()

    # Lista seleccionable de productos
    producto_list = fl.Dropdown(
        label='Producto',
        hint_text='Seleccione un producto',
        options=filtrar_productos_con_stock(),
        on_change=handle_producto_seleccionado,
        expand=True,
    )

    # Lista de ventas
    ventas_list = fl.ListView(
        spacing=10,
        padding=10,
        expand=True,
    )

    # Sección de pago
    monto_input = fl.TextField(
        label='Monto… ($)',
        on_change=calcular_devolucion,
        keyboard_type=fl.KeyboardType.NUMBER,
        expand=True,
    )

    # Guardar venta con productos asociados
    def handle_vender(e):
        devolucion = float(devolucion_text.value.replace('$', ''))
        if devolucion < 0:
            # Mostrar diálogo de advertencia si la devolución es negativa
            monto_insuficiente_dialog.open = True
            page.overlay.append(monto_insuficiente_dialog)
            page.update()
            return

        if productos_venta:
            venta_data = {
                'fecha_venta': datetime.now().isoformat(),
                'ganancia': sum(v['cantidad'] * v['precio'] for v in productos_venta),
            }
            # Guardar la venta y productos asociados
            add_venta(
                data_manager,
                venta_data,
                productos_venta,
            )
            productos_venta.clear()  # Limpiar la lista de ventas después de guardar
            actualizar_lista_ventas()
            actualizar_total()
            # Mostrar snack bar de confirmación de venta
            page.overlay.append(
                fl.SnackBar(
                    content=fl.Text('Venta registrada correctamente'),
                    action='OK',
                )
            )
            page.update()
            # Actualizar el Dropdown de productos después de la venta
            producto_list.options = filtrar_productos_con_stock()
            producto_list.update()

    def close_dialog():
        monto_insuficiente_dialog.open = False
        page.update()

    # Crear vista
    view = fl.View(
        Routes.VENTAS,
        [
            fl.AppBar(title=fl.Text('Registrar venta 🛒'), center_title=True),
            fl.Container(content=producto_list, padding=10),
            fl.Divider(),
            fl.Container(content=ventas_list, expand=True),
            fl.Divider(),
            fl.Container(
                content=fl.Column(
                    [
                        fl.Row([fl.Text('Total: '), total_venta], alignment='spaceBetween'),
                        fl.Row(
                            [
                                monto_input,
                                fl.Container(width=20),  # Espaciador
                                devolucion_text,
                            ]
                        ),
                        fl.Row(
                            [
                                fl.ElevatedButton(
                                    'Vender',
                                    icon=fl.icons.ACCOUNT_BALANCE_WALLET,
                                    expand=True,
                                    # Acción de venta
                                    on_click=handle_vender,
                                )
                            ],
                            alignment='center',
                            expand=True,
                        ),
                    ]
                ),
                padding=10,
            ),
        ],
    )

    return view
