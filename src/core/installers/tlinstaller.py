from pathlib import Path
from typing import Callable

from core.installers.installer import Installer

class TlInstaller(Installer):
    def __init__(
        self, status_callback: Callable, modpack_content_path: Path,
        modpacks_location: Path,
        modpack_name: str, modpack_mc_version: str, modpack_modloader: str
    ):
        self.status = status_callback
        self.name = modpack_name
        self.mc_version = modpack_mc_version
        self.modloader = modpack_modloader

        self.modpack_path = modpacks_location / self.name

    def _init_modpack(self):
        # TODO: Механизм инициализации сборки
        pass

    def install_modpack(self):
        self._init_modpack()
        # TODO: Установка сборки
