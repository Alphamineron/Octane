import sys
import os
import json
with open("config.json") as config_file:
    CONFIG = json.load(config_file)

PROJECT_NAME = CONFIG["PROJECT_NAME"]
CHIPS_BIN = CONFIG["CHIPS_BIN"]
CHIPS_JSON = CONFIG["CHIPS_JSON"]
BROWSER_EXPORT_FILE = CONFIG["BROWSER_EXPORT_FILE"]
MEDIUM_DIR = CONFIG["MEDIUM_DIR"]
DATASET_URL = CONFIG["DATASET_URL"]
USERCODE = CONFIG["USERCODE"]
__GC_DB = CONFIG["__GC_DB"] # Chrome Browser's Bookmarks Database Path
__CR_DB = CONFIG["__CR_DB"] # Chromium Browser's Bookmarks Database Path
__MF_DB = CONFIG["__MF_DB"] # Firefox Browser's Bookmarks Database Path [NOT SUPPORTED]
__CONFIGinit = False    # Denotes whether the config file has been initialized or not (To avoid undefined behaviour)

def storeConfig():
    with open("config.json", "w") as fout:
        json.dump(CONFIG, fout, indent=4)

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


if __name__ == '__main__':
    try:
        print("Initializing config.json")
        fetchDBPaths()
        storeConfig()
        __CONFIGinit = True
        
    except Exception as e:
        __CONFIGinit = False
        print("Exception Encountered: ", e)
