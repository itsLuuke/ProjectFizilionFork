from userbot import LOGS


def __list_all_modules():
    import glob
    from os.path import basename, dirname, isfile

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    return [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]


CUSTOM_MODULES = sorted(__list_all_modules())
LOGS.info("Custom Modules to load: %s", str(CUSTOM_MODULES))
__all__ = CUSTOM_MODULES + ["ALL_MODULES"]
