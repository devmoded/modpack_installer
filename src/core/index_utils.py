import requests
import tomli

def get_index(url: str) -> dict[str, list[dict[str, str]]]:
    response = requests.get(url)
    response.raise_for_status()
    data: dict[str, list[dict[str, str]]] = tomli.loads(response.text)
    return data

def get_modpacks_names(index: dict[str, list[dict[str, str]]] | None) -> list[str]:
    names: list[str] = []
    if index:
        modpacks: list[dict[str, str]] = index.get('modpacks', [])
        if modpacks:
            for modpack in modpacks:
                name = modpack.get('name')
                if name is not None:
                    names.append(name)
    return names

def modpack_query(index: dict[str, list[dict[str, str]]] | None, name: str) -> dict[str, str]:
    if index:
        modpacks: list[dict[str, str]] = index.get('modpacks', [])
        if modpacks:
            for modpack in modpacks:
                if modpack.get('name') == name:
                    return modpack
    return {}
