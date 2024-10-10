from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


class ServerHandlersManager:
    def __init__(self):
        self.__supported_handlers = self.get_handlers()

        self.get_host: Callable[[], str | None] | None = None
        self.get_mac_address: Callable[[], str | None] | None = None
        self.toggle_wlan: Callable[[bool], None] | None = None
        self.is_wlan_active: Callable[[], bool] | None = None

    def setup_handler(self, name: str, handler: Callable):
        if name in self.__supported_handlers:
            setattr(self, name, handler)

    def get_handlers(self) -> list[str]:
        return [
            "get_host",
            "get_mac_address",
            "toggle_wlan",
            "is_wlan_active"
        ]
