from pathlib import Path
from typing import Callable

from core.installers.tlinstaller import TlInstaller

class Launcher:
    def __init__(
        self, status_callback: Callable, modpack_content_path: Path,
        modpack_info: dict[str, str], launcher_type: str
    ):
        self.status = status_callback
        self.modpack_content_path = modpack_content_path
        self.modpack_name = modpack_info.get('name', '')
        self.modpack_mc_version = modpack_info.get('mc_version', '')
        self.modpack_modloader = modpack_info.get('modloader', '')

        self.launcher_type = launcher_type
        self.installers: dict[str, type[TlInstaller]] = {
            'tl': TlInstaller
        }

    def install_modpack(self):
        installer_cls = self.installers.get(self.launcher_type)
        if not installer_cls:
            self.status('Ошибка: Неизвестный ID лаунчера')
            return

        # TODO: Поработать над изменением на raise и последующую работу с логгером
        if not self.modpack_content_path.exists():
            self.status('Ошибка: Временный путь с содержимым сборки не существует!')
            return
        installer = installer_cls(
            self.status, self.modpack_content_path,
            self.modpack_name, self.modpack_mc_version, self.modpack_modloader
        )
        installer.install_modpack()
