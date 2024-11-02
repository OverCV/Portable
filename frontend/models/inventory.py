import flet as fl
from backend.data.managers.csv_manager import CSVManager
from frontend.enums.routes import Routes

from frontend.views.productos.registro_producto import create_productos
from frontend.views.ventas.registro_venta import create_ventas
from frontend.views.home.inicio import mostrar_inicio
from frontend.views.deudores.mostrar_deudores import mostrar_deudores
from frontend.views.not_found import mostrar_404

from frontend.enums.config import conf


class InventoryApp:
    def __init__(self):
        self.data_manager = CSVManager()

    async def main(self, page: fl.Page):
        page.title = conf.APP_NAME
        page.theme_mode = fl.ThemeMode.LIGHT
        page.window.height = conf.get_window_height()
        page.window.width = conf.get_window_width()

        # Bottom Navigation #
        nav_rail = fl.NavigationBar(
            selected_index=0,
            destinations=[
                fl.NavigationBarDestination(
                    icon=fl.icons.HOME_OUTLINED,
                    selected_icon=fl.icons.HOME_FILLED,
                    label='Inicio',
                ),
                fl.NavigationBarDestination(
                    icon=fl.icons.INVENTORY_2_OUTLINED,
                    selected_icon=fl.icons.INVENTORY_2,
                    label='Productos',
                ),
                fl.NavigationBarDestination(
                    icon=fl.icons.SHOPPING_CART_OUTLINED,
                    selected_icon=fl.icons.SHOPPING_CART,
                    label='Ventas',
                ),
                fl.NavigationBarDestination(
                    icon=fl.icons.PEOPLE_OUTLINED,
                    selected_icon=fl.icons.PEOPLE,
                    label='Deudores',
                ),
                fl.NavigationBarDestination(
                    icon=fl.icons.QUERY_STATS_OUTLINED,
                    selected_icon=fl.icons.QUERY_STATS_ROUNDED,
                    label='Reportes',
                ),
            ],
            on_change=self.navigation_changed,
        )

        # Router
        async def route_change(e: fl.RouteChangeEvent):
            page.views.clear()
            route = e.route

            print(f'{route=}')

            all_routes = {
                Routes.HOME: mostrar_inicio,
                Routes.PRODUCTOS: create_productos,
                Routes.VENTAS: create_ventas,
                Routes.DEUDORES: mostrar_deudores,
            }

            page.views.append(
                all_routes[route](
                    page,
                    self.data_manager,
                )
                if route in all_routes
                else mostrar_404(page, self.data_manager)
            )

            # Agregar la barra de navegación a todas las vistas
            page.views[-1].navigation_bar = nav_rail
            page.update()

        page.on_route_change = route_change
        #! Ruta inicial !#
        page.go(Routes.HOME)

    async def navigation_changed(self, e: fl.Page):
        added_routes = [
            Routes.HOME,
            Routes.PRODUCTOS,
            Routes.VENTAS,
            Routes.DEUDORES,
            Routes.REPORTES,
        ]
        e.page.go(added_routes[e.control.selected_index])
