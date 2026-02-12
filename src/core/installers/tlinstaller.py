from pathlib import Path
from typing import Callable
from platformdirs import user_data_path

from installers.installer import Installer

class TlInstaller(Installer):
    def __init__(
        self, status_callback: Callable, modpack_content_path: Path,
        modpack_name: str, modpack_mc_version: str, modpack_modloader: str
    ):
        self.status = status_callback
        self.name = modpack_name
        self.mc_version = modpack_mc_version
        self.modloader = modpack_modloader

        minecraft_path = user_data_path('.minecraft', roaming=True)
        self.modpack_path = minecraft_path / 'versions' / self.name

    def _init_modpack(self):
        # TODO: Механизм инициализации сборки
        pass

    def install_modpack(self):
        self._init_modpack()
        # TODO: Установка сборки
