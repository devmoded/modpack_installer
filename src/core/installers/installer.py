from abc import ABC, abstractmethod

class Installer(ABC):
    @abstractmethod
    def _init_modpack(self):
        pass

    @abstractmethod
    def install_modpack(self):
        pass
