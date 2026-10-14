import logging
import os
import platform
import shutil
from pathlib import Path

logger = logging.getLogger("YACC")

class EmptyName(Exception):
    pass

def get_platform_path():
    pltfrm = platform.system()
    if pltfrm == "Linux":
        path = os.path.join(os.path.expanduser("~"), ".config/YACC/")
    elif pltfrm == "Windows":
        path = os.path.join(os.getenv("LOCALAPPDATA", "YACC/"))

    return path

def get_sets():
    path = os.path.join(get_platform_path(), "crosshairs/")
    sets = []
    for dir in os.listdir(path):
        sets.append(dir)  # noqa: PERF402

    return sets

def get_xhairs(set):
    path = os.path.join(get_platform_path(), "crosshairs/", set, "materials/vgui/replay/thumbnails/")
    xhairs = []
    for file in os.listdir(path):
        filename = file
        if filename.endswith(".vtf"):
            xhairs.append(file[:-4])
        else:
            pass

    return xhairs


def import_xhairs(name, src):
    if name == "":
        raise EmptyName("Name cannot be empty")

    path = os.path.join(get_platform_path(), "crosshairs/")
    os.makedirs(os.path.join(path, name), exist_ok=False)
    shutil.copytree(src, os.path.join(path, name), dirs_exist_ok=True)

def copy_cfg(path):
    def_cfg = Path("./config/config.default.toml")
    
    if os.path.exists(f"{path}/config.toml"):
        return
    shutil.copy(def_cfg, path)
    os.rename(f"{path}/config.default.toml", f"{path}/config.toml")
    logger.info(f"Created configuration file at {path}")
    

def create_dirs():
    path = get_platform_path()
    os.makedirs(os.path.join(path, "crosshairs/"), exist_ok=True)
    copy_cfg(path)

    return path