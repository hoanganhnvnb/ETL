import os
import importlib

from pathlib import Path

PATH_PROJECT = 'bankofcanada'

def get_root_path(file=__file__):
    path = os.path.dirname(os.path.abspath(file))
    return path

def get_model_name(name:str):
    return 'models.' + name.replace("\\", ".").replace("/", ".")

def get_model(mode:str=None, process_type:str=None):
    if not mode or not process_type:
        return None

    module_name = get_model_name(process_type)
    module = importlib.import_module(module_name)
    class_name = mode.capitalize() + 'Model' + process_type.capitalize()
    class_object = getattr(module, class_name)
    return class_object()