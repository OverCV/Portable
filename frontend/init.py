# import flet as ft
# from data.managers.json_manager import DataManager
# from views.productos.producto import create_productos


# class InventoryApp:
#     def __init__(self):
#         self.data_manager = DataManager()

#     async def main(self, page: ft.Page):
#         page.title = "Inventory App"
#         page.theme_mode = ft.ThemeMode.LIGHT
#         page.window_width = 400
#         page.window_height = 800

#         # Bottom Navigation
#         nav_rail = ft.NavigationBar(
#             selected_index=0,
#             destinations=[
#                 ft.NavigationDestination(
#                     icon=ft.icons.INVENTORY_2_OUTLINED,
#                     selected_icon=ft.icons.INVENTORY_2,
#                     label="Productos",
#                 ),
#                 ft.NavigationDestination(
#                     icon=ft.icons.SHOPPING_CART_OUTLINED,
#                     selected_icon=ft.icons.SHOPPING_CART,
#                     label="Ventas",
#                 ),
#                 ft.NavigationDestination(
#                     icon=ft.icons.PEOPLE_OUTLINED,
#                     selected_icon=ft.icons.PEOPLE,
#                     label="Deudores",
#                 ),
#             ],
#             on_change=self.navigation_changed,
#         )

#         # Router
#         async def route_change(e):
#             page.views.clear()
#             route = e.route

#             if route == "/productos":
#                 page.views.append(
#                     create_productos(page, self.data_manager)
#                 )

#             # Agregar la barra de navegación a todas las vistas
#             page.views[-1].navigation_bar = nav_rail
#             await page.update()

#         page.on_route_change = route_change
#         await page.go("/productos")  # Ruta inicial

#     def navigation_changed(self, e):
#         routes = ["/productos"]
#         e.page.go(routes[e.control.selected_index])


# if __name__ == "__main__":
#     app = InventoryApp()
#     ft.app(target=app.main)
