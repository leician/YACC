import logging
import os
import platform

import tomli
import tomli_w

from util.util import create_dirs


class Config:
    def __init__(self):
        self.logger = logging.getLogger("YACC")
        self.path = os.path.join(create_dirs(), "config.toml")
        self.os = platform.system()

    def read_config(self):
        with open(self.path, "rb") as f:
            cfg = tomli.load(f)
            return cfg

    def write_config(self, section, key, value):
        cfg = self.read_config()
        cfg[section][key] = value
        with open(self.path, "wb") as f:
            tomli_w.dump(cfg, f)