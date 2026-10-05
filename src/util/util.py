import logging
import os
import platform
import shutil
from pathlib import Path

logger = logging.getLogger("YACC")

class EmptyName(Exception):
    pass

def import_xhairs(name, src):
    if name == "":
        raise EmptyName("Name cannot be empty")

    pltfrm = platform.system()
    if pltfrm == "Linux":
        path = os.path.join(os.path.expanduser("~"), ".config/YACC/crosshairs")
    elif pltfrm == "Windows":
        path = os.path.join(os.getenv("LOCALAPPDATA", "YACC/crosshairs"))

    os.makedirs(os.path.join(path, name), exist_ok=False)
    shutil.copytree(src, os.path.join(path, name), dirs_exist_ok=False)

def copy_cfg(path):
    def_cfg = Path("./config/config.default.toml")
    
    if os.path.exists(f"{path}/config.toml"):
        return
    shutil.copy(def_cfg, path)
    os.rename(f"{path}/config.default.toml", f"{path}/config.toml")
    logger.info(f"Created configuration file at {path}")
    

def create_dirs():
    pltfrm = platform.system()
    if pltfrm == "Linux":
        path = os.path.join(os.path.expanduser("~"), ".config/YACC/")
    elif pltfrm == "Windows":
        path = os.path.join(os.getenv("LOCALAPPDATA", "YACC/"))

    os.makedirs(os.path.join(path, "crosshairs/"), exist_ok=True)
    copy_cfg(path)

    return path