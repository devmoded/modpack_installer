from pathlib import Path

class Launcher:
    def __init__(self):
        self.location: Path
        self.launcher_id: str # например tl, prism и так далее

    def install_modpack(self):
        """
        Псевдокод
        if tl:
            pass
        elif prism:
            pass
        elif ...
            pass
        else:
            unknown launcher_id
        """
        pass
