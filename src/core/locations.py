from pathlib import Path
from platformdirs import user_data_path

minecraft_path = user_data_path('.minecraft', roaming=True)

launchers = {
    'tl': minecraft_path / 'versions'
}

def get_modpacks_location(launcher_type: str) -> Path:
    modpacks_location = launchers.get(launcher_type)

    if not modpacks_location:
        raise RuntimeError('Невозможно установить раположение каталога со сборками')

    if not modpacks_location.exists():
        raise RuntimeError(f"Каталог {modpacks_location} не существует")

    return modpacks_location
