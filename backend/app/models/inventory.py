import flet as fl
from backend.data.managers.csv_manager import CSVManager
from frontend.views.productos.producto import create_productos
from backend.app.enums.routes import Routes


class InventoryApp:
    def __init__(self):
        self.data_manager = CSVManager()

    async def main(self, page: fl.Page):
        page.title = 'Inventory App'
        page.theme_mode = fl.ThemeMode.LIGHT
        page.window.width = 400
        page.window.height = 800

        # Bottom Navigation
        nav_rail = fl.NavigationBar(
            selected_index=0,
            destinations=[
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
            ],
            on_change=self.navigation_changed,
        )

        # Router
        async def route_change(e):
            page.views.clear()
            route = e.route

            if route == Routes.PRODUCTOS:
                page.views.append(
                    create_productos(page, self.data_manager),
                )

            # Agregar la barra de navegación a todas las vistas
            page.views[-1].navigation_bar = nav_rail
            page.update()

        page.on_route_change = route_change
        page.go(Routes.PRODUCTOS)  # Ruta inicial

    async def navigation_changed(self, e: fl.Page):
        routes = [Routes.PRODUCTOS]
        e.page.go(routes[e.control.selected_index])
