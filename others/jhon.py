import flet as fl
from flet import (
    View,
    Page,
    AppBar,
    ElevatedButton,
    Text,
    RouteChangeEvent,
    ViewPopEvent,
    CrossAxisAlignment,
    MainAxisAlignment,
)

def main(page: Page) -> None:
    page.title = "Learning application"

    def route_change(e: RouteChangeEvent) -> None:
        page.views.append(
            View(
                route="/",
                controls=[
                    AppBar(title=Text("Inicio"), bgcolor="blue"),
                    Text(value="Inicio", size=30),
                    ElevatedButton(
                        text="Ir a ventas", on_click=lambda _: page.go("/ventas")
                    ),
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=26,
            )
        )

        if page.route == "/ventas":
            page.views.append(
                View(
                    route="/ventas",
                    controls=[
                        AppBar(title=Text("Mis ventas"), bgcolor="red"),
                        Text(value="Ventas", size=30),
                        ElevatedButton(text="Volver", on_click=lambda _: page.go("/")),
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26,
                )
            )
        page.update()

    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)



if __name__ == "__main__":
    fl.app(target=main)
