import requests
import zipfile
import io
import shutil
import tempfile

from typing import Callable
from pathlib import Path

from core.launcher import Launcher
from core.locations import get_modpacks_location
from config import END_MESSAGE

class ModpackUtils:
    def __init__(self, modpack_info: dict[str, str], status_callback: Callable, launcher_type: str):
        self.modpack_info = modpack_info
        self.name = modpack_info.get('name', '')
        self.version = modpack_info.get('version', '')
        self.source = modpack_info.get('source', '')
        self.status = status_callback
        self.launcher_type = launcher_type
        try:
            modpacks_location = get_modpacks_location(self.launcher_type)
        except RuntimeError as e:
            self.status(e)
        else:
            self.modpack_location = modpacks_location / self.name

        self.modpack_temp = None
        self.modpack_temp_path = None

    def _download_and_extract(self):
        # Скачивание сборки и сохранение в оперативную память
        if not self.source:
            self.status('Поле \'source\' в информации о сборке не найдено')
            return
        try:
            self.status('Скачивание сборки начато')
            response = requests.get(self.source)
            response.raise_for_status()
        except requests.HTTPError as e:
            self.status(f"Ошибка при скачивании сборки: {e}")
        else:
            self.status('Скачивание сборки завершено')
            zip_bytes = io.BytesIO(response.content)

            # Создание временного каталога
            self.modpack_temp = tempfile.TemporaryDirectory()
            self.modpack_temp_path = Path(self.modpack_temp.name)
            # self.modpack_temp_path = Path('~/downloads/modpack_inst_sprrp_test').expanduser()

            # Извлечение содержимого zip во временный каталог
            try:
                with zipfile.ZipFile(zip_bytes) as zf:
                    zf.extractall(self.modpack_temp_path)
            except zipfile.BadZipFile:
                self.status("Ошибка: архив повреждён")
            except OSError as e:
                self.status(f"Ошибка записи на диск: {e}")
            else:
                # TODO добавить проверку на отсутствие файлов в self.modpack_content_path

                github_subdir = next(dir for dir in self.modpack_temp_path.iterdir() if dir.is_dir())
                for item in github_subdir.iterdir():
                    shutil.move(item, self.modpack_temp_path / item.name)

                github_subdir.rmdir()
                self.status(f"Cборка '{self.name}' успешно скачана и распакована в {self.modpack_temp_path}")

    def _save_version_in_file(self):
        if self.modpack_temp_path:
            version_file = self.modpack_temp_path / 'modpack_version'
            if self.version:
                version_file.write_text(self.version)
                self.status('Версия сборки сохранена в файл \'modpack_version\'')

    def _get_version_from_file(self) -> str | None:
        version_file = self.modpack_location / self.name / 'modpack_version'
        return version_file.read_text().strip()

    def _is_actual(self) -> bool:
        installed_version = self._get_version_from_file()
        # Улучшить механизм проверки версии
        return True if installed_version == self.version else False

    def _is_installed(self) -> bool:
        return True if self.modpack_location.exists() else False

    def _cleanup(self):
        # Очистка временного каталога
        if self.modpack_temp:
            self.status('Очистка начата')
            self.modpack_temp.cleanup()
            self.modpack_temp = None
            self.modpack_temp_path = None
            self.status('Временный каталог удалён')
            self.status('Очистка завершена')

    def _full_install(self):
        self._download_and_extract()
        self._save_version_in_file()

        if self.modpack_temp_path is not None:
            launcher = Launcher(
                self.status, self.modpack_temp_path,
                self.modpack_info, self.launcher_type
            )
            launcher.install_modpack()

        self._cleanup()

    def install_selected(self):
        self.status(f"Проверка существования сборки '{self.name}'")
        if self._is_installed():
            self.status('Проверка актуальности установленной сборки')
            if self._is_actual():
                self.status('Установленная версия сборки актуальна')
                return
            else:
                self.status('Установленная версия сборки не актуальна')
        self.status('Начата установка сборки')
        self._full_install()
        self.status(END_MESSAGE)

    # Для проверок функционала или дебага
    def print_selected(self):
        print(self.modpack_info)
        self.status(END_MESSAGE)
