import sys
import os
import json
import pathlib

reset_config = {
    "PROJECT_NAME": "Octane",
    "CHIPS_BIN": "data/chips.bin",
    "CHIPS_JSON": "data/chips.json",
    "FOLDERTREE_JSON": "data/folderTree.json",
    "__GC_DB": "",
    "__CR_DB": "",
    "__MF_DB": "",
    "BROWSER_EXPORT_FILE": "",
    "MEDIUM_DIR": "",
    "DATASET_URL": "",
    "USERCODE": "0000",
    "__IMPORT_GC": False,
    "__IMPORT_CR": False,
    "__IMPORT_MEDIUM": False,
    "__CONFIGinit": False
}

def storeConfig():
    path = pathlib.Path("config.json")
    with path.open("w") as fout:
        json.dump(CONFIG, fout, indent=4)


try:
    path = pathlib.Path("config.json")
    with path.open() as config_file:
        CONFIG = json.load(config_file)
except FileNotFoundError as e:
    CONFIG = reset_config
    storeConfig()
    path = pathlib.Path("config.json")
    full_path = path.absolute()
    my_path = full_path.as_posix()
    print("\nConfig Created! \nEdit the config.json to your preferences \nFile Location -> " + my_path)
    exit()


PROJECT_NAME = CONFIG["PROJECT_NAME"]
CHIPS_BIN = CONFIG["CHIPS_BIN"]
CHIPS_JSON = CONFIG["CHIPS_JSON"]
FOLDERTREE_JSON = CONFIG["FOLDERTREE_JSON"]
BROWSER_EXPORT_FILE = CONFIG["BROWSER_EXPORT_FILE"]
MEDIUM_DIR = CONFIG["MEDIUM_DIR"]
DATASET_URL = CONFIG["DATASET_URL"]
USERCODE = CONFIG["USERCODE"]
__GC_DB = CONFIG["__GC_DB"] # Chrome Browser's Bookmarks Database Path
__CR_DB = CONFIG["__CR_DB"] # Chromium Browser's Bookmarks Database Path
__MF_DB = CONFIG["__MF_DB"] # Firefox Browser's Bookmarks Database Path [NOT SUPPORTED]
__IMPORT_GC = CONFIG["__IMPORT_GC"]
__IMPORT_CR = CONFIG["__IMPORT_CR"]
__IMPORT_MEDIUM = CONFIG["__IMPORT_MEDIUM"]


def fetchDBPaths_Linux():
    CONFIG["__GC_DB"] = "~/.config/google-chrome/Default/Bookmarks"
    CONFIG["__CR_DB"] = "~/.config/chromium/Default/Bookmarks"

def fetchDBPaths_Mac():
    CONFIG["__GC_DB"] = "~/Library/Application Support/Google/Chrome/Default/Bookmarks"
    CONFIG["__CR_DB"] = "~/Library/Application Support/Chromium/Default/Bookmarks"

def fetchDBPaths_Win():
    username = os.getlogin()
    CONFIG["__GC_DB"] = ("C:/Users/{}/AppData/Local/Google/Chrome/User Data/"
                         "Default/Bookmarks".format(username))
    CONFIG["__CR_DB"] = ("C:/Users/{}/AppData/Local/Chromium/User Data/"
                         "Default/Bookmarks".format(username))

def fetchDBPaths():
    if sys.platform.startswith(("linux", "freebsd", "openbsd")):
        fetchDBPaths_Linux()
    elif sys.platform == "darwin":
        fetchDBPaths_Mac()
    elif sys.platform == "win32":
        fetchDBPaths_Win()
    else:
        print("\n{} is not supported yet.".format(sys.platform))
        print("\nUnable to fetch Browsers' Bookmarks' Database Paths.")
        print("Supported Browser Formats:")
        print("1) Chrome")
        print("2) Chromium")
        print(("\nIf you believe that python is functional on your OS, Manually "
                "enter the paths in config.json within the project repository"))


def initCONFIG():
    if CONFIG["__CONFIGinit"] == False:
        try:
            print("Initializing config.json")
            fetchDBPaths()
            # __CONFIGinit: Denotes whether the config file has been
            #               initialized or not (To avoid undefined behaviour)
            CONFIG["__CONFIGinit"] = True   # Default Value: FALSE
            storeConfig()
        except Exception as e:
            CONFIG["__CONFIGinit"] = False
            storeConfig()
            raise e
    else:
        print("config.json already initialized!")


if __name__ == '__main__':
    initCONFIG()
