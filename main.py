import flet as fl

# from backend.api.enums.routes import Routes
from backend.app.models.inventory import InventoryApp
from backend.constants.application import __MAIN__


def main() -> None:
    """Application initializer."""
    app: InventoryApp = InventoryApp()
    fl.app(target=app.main)


if __name__ == __MAIN__:
    main()
