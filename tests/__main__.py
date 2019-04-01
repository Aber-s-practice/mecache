import os
import sys
import importlib

from . import SELF_PATH

sys.path.append(os.path.dirname(SELF_PATH))

for each in os.listdir(SELF_PATH):
    path = os.path.join(SELF_PATH, each)
    if os.path.isfile(path) and each.split(".")[-1] == "py":
        importlib.import_module("."+each.split(".")[0], __package__)
