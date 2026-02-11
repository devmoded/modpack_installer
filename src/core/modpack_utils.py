import requests
import zipfile
import io
import shutil
import tempfile

from typing import Callable
from pathlib import Path

class ModpackUtils:
    def __init__(self, modpack_info: dict[str, str], status_callback: Callable):
        self.name = modpack_info.get('name', '')
        self.source = modpack_info.get('source', '')
        self.mc_version = modpack_info.get('mc_version', '')
        self.modloader = modpack_info.get('modloader', '')
        self.status = status_callback

        self.modpack_temp = None
        self.modpack_content_path = None

    def _download_and_extract(self):
        # Скачивание сборки и сохранение в оперативную память
        try:
            response = requests.get(self.source)
            response.raise_for_status()
        except requests.HTTPError as e:
             self.status(f"Ошибка при скачивании сборки: {e}")
        else:
            zip_bytes = io.BytesIO(response.content)

            # Создание временного каталога
            self.modpack_temp = tempfile.TemporaryDirectory()
            self.modpack_content_path = Path(self.modpack_temp.name)

            # Извлечение содержимого zip во временный каталог
            try:
                with zipfile.ZipFile(zip_bytes) as zf:
                    zf.extractall(self.modpack_content_path)
            except zipfile.BadZipFile:
                self.status("Ошибка: архив повреждён")
            except OSError as e:
                self.status(f"Ошибка записи на диск: {e}")
            else:
                self.status(f"Cборка '{self.name}' успешно скачана и распакована в {self.modpack_content_path}")

    def _cleanup(self):
        # Очистка временного каталога
        if self.modpack_temp:
            self.modpack_temp.cleanup()
            self.modpack_temp = None
            self.modpack_content_path = None
            self.status('Временный каталог удалён')

    def self_install(self):
        self.status(f"Начата установка сборки '{self.name}'")
        self._download_and_extract()

        self._cleanup()
        self.status('Готово')
