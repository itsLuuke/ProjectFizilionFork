# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Init file which loads all of the modules """
from userbot import LOGS, NO_LOAD

not_loaded = []


def __list_all_modules():
    import glob
    from os.path import basename, dirname, isfile

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    for a in NO_LOAD:
        if a in all_modules:
            not_loaded.append(a)
            all_modules.remove(a)
    return all_modules


ALL_MODULES = sorted(__list_all_modules())
LOGS.info("Modules to load: %s", str(ALL_MODULES))
LOGS.info("Not loading: %s", str(not_loaded))
__all__ = ALL_MODULES + ["ALL_MODULES"]
