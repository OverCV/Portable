import flet as fl

# from backend.api.enums.routes import Routes
from frontend.models.inventory import Portalapp
from backend.constants.application import __MAIN__


def main() -> None:
    """Application initializer."""
    app: Portalapp = Portalapp()
    fl.app(target=app.main)


if __name__ == __MAIN__:
    main()
