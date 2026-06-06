#!/usr/bin/env python3
# coding: utf-8


"""
Helper module for loading external data.
"""


import inspect
import importlib

from typing import (
    Callable,
)


def _preload_module_data(data_name):
    mod = importlib.import_module(data_name)
    if not hasattr(mod, "load"):
        raise AttributeError(f"module {mod} has no attribute 'load'")

    return mod.load()


def _module_name(full_name: str) -> str:
    return full_name.split(".")[-1]


def _get_caller_module_name(index=1) -> str:
    stack = inspect.stack()
    caller_frame = stack[index]         # 0: current frame
    caller_module = inspect.getmodule(caller_frame[0])
    full_name = caller_module.__name__  # e.g. "problems.p0022"
    return _module_name(full_name)


def _default_data_handler(raw: str) -> list[str]:
    print("default data handler called")
    return raw.splitlines()

class _DataLoader:
    """
    Helper class for loading external data.
    """

    def __init__(self):
        self.cache = None

    def reset(self):
        """
        Reset cache.
        """
        self.cache = None

    def preload(self, module_name):
        """
        Preload data from problem of specified module.
        """
        if len(module_name) <= 0:
            return None

        with open(f"data/{module_name}.txt", encoding="utf-8") as f:
            raw = f.read()

        self.cache = raw
        return raw

    def try_preload(self, module_name):
        """
        Preload data from problem of specified module.
        """
        try:
            return self.preload(module_name)

        except FileNotFoundError:
            return None

    def load(self):
        """
        Load data dynamically from problem of calling module or preloaded cache.
        """
        if self.cache is not None:
            return self.cache

        caller_module_name = _get_caller_module_name(3)
        return self.preload(caller_module_name)


_data_loader = _DataLoader()


def load(handler: Callable[[str], list[str]] | None = None):
    """
    Load data dynamically from problem of calling module or preloaded cache.
    """
    data = _data_loader.load()
    if handler is not None:
        data = handler(data)

    return data


def preload(data_name):
    """
    Preload data from problem of specified module.
    """
    return _data_loader.preload(data_name)


def try_preload(data_name):
    """
    Preload data from problem of specified module.
    """
    if len(data_name) <= 0:
        return None

    return _data_loader.try_preload(data_name)


def reset():
    """
    Reset cache.
    """
    _data_loader.reset()
