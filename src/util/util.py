import platform
import shutil
import os
from pathlib import Path
import logging

def create_cfg_dir():
    pltfrm = platform.system()
    def_cfg = Path("./config/config.default.toml")
    logger = logging.getLogger("YACC")

    if pltfrm == "Linux":
        path = os.path.join(os.path.expanduser("~"), ".config/YACC/")
        os.makedirs(path, exist_ok=True)
        try:
            if os.path.exists(f"{path}/config.toml"):
                return path
            shutil.copy(def_cfg, path)
            os.rename(f"{path}/config.default.toml", f"{path}/config.toml")
            logger.info("Created config file")
            return path
        except shutil.SameFileError:
            pass
        except PermissionError:
            pass
    elif pltfrm == "Windows":
        path = os.path.join(os.getenv("LOCALAPPDATA", "YACC/"))
        os.makedirs(path, exist_ok=True)
        try:
            if os.path.exists(f"{path}/config.toml"):
                return path
            shutil.copy(def_cfg, path)
            os.rename(f"{path}/config.default.toml", f"{path}/config.toml")
            return path
        except shutil.SameFileError:
            pass
        except PermissionError:
            pass