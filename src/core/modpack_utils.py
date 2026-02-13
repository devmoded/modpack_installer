import requests
import zipfile
import io
import shutil
import tempfile

from typing import Callable
from pathlib import Path

from core.launcher import Launcher
from config import END_MESSAGE

class ModpackUtils:
    def __init__(self, modpack_info: dict[str, str], status_callback: Callable):
        self.modpack_info = modpack_info
        self.name = modpack_info.get('name', '')
        self.source = modpack_info.get('source', '')
        self.status = status_callback

        self.modpack_temp = None
        self.modpack_temp_path = None


    def _download_and_extract(self):
        # Скачивание сборки и сохранение в оперативную память
        if not self.source:
            self.status('Поле \'source\' в информации о сборке не найдено')
            return
        try:
            response = requests.get(self.source)
            response.raise_for_status()
        except requests.HTTPError as e:
            self.status(f"Ошибка при скачивании сборки: {e}")
        else:
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

    def _cleanup(self):
        # Очистка временного каталога
        if self.modpack_temp:
            self.status('Очистка начата')
            self.modpack_temp.cleanup()
            self.modpack_temp = None
            self.modpack_temp_path = None
            self.status('Временный каталог удалён')
            self.status('Очистка завершена')

    def install_selected(self, launcher_type):
        self.status(f"Начата установка сборки '{self.name}'")
        self._download_and_extract()

        if self.modpack_temp_path is not None:
            launcher = Launcher(
                self.status, self.modpack_temp_path,
                self.modpack_info, launcher_type
            )
            launcher.install_modpack()

        self._cleanup()
        self.status(END_MESSAGE)

    # Для проверок функционала или дебага
    def print_selected(self):
        print(self.modpack_info)
        self.status(END_MESSAGE)
