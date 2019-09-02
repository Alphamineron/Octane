import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import pathlib

# Imports for Data File Handling
try: import cPickle as pickle
except ModuleNotFoundError: import pickle
import json

# Imports for utilities
from utils.spinner import Spinner
from copy import deepcopy
import colorama
import pprint
from prettytable import PrettyTable


from dataChip import Chip, generatePrimitiveBookmarks
try: import importer
except ModuleNotFoundError as e: from . import importer


# Fetching Defined Project-Scoped Config Constants
from config import PROJECT_NAME, CHIPS_BIN, CHIPS_JSON


def drop_deletions(removedData):
    return False, []

def accept_deletions(removedData):
    return True, removedData

def selective_deletion(removedData):
    dataArr = deepcopy(removedData)
    for data in dataArr:
        colorama.init(autoreset = True)
        print(colorama.Fore.WHITE + colorama.Back.RED + "\n<=================================>")
        data.show()
        print(colorama.Fore.WHITE + colorama.Back.RED + "<=================================>")
        choice = input("To Save? (Y/N): ")
        if(choice.lower() == 'y'):
            for item in removedData:
                if(item.url == data.url):
                    removedData.remove(item)
                    break

    choice = input("To you wish to continue? (Press 'E' to exit): ")
    if(choice.lower() == 'e'):
        cancel_import(removedData)

    return True, removedData

def cancel_import(_):
    print("Import Cancelled on User Request...")
    exit()

def get_menuCLI(newData, removedData, lenExistingData):
    colorama.init(autoreset = True)
    print(colorama.Fore.WHITE + colorama.Back.GREEN + "\n<Import Status ===================================================================================================>")
    # print("New Data: ", newData)
    # print("Removed Data: ", removedData)
    table = PrettyTable()
    table.field_names = ["New Data Received", "Existing Data pior import", "Existing Data Removal Pending", "Total Data after import"]
    table.add_row([str(len(newData))+" Objects", str(lenExistingData)+" Objects", str(len(removedData))+" Objects", str(len(newData) + (lenExistingData - len(removedData)))+u" \u00B1 "+str(len(removedData))+" Objects"])
    print(table)
    print(colorama.Fore.WHITE + colorama.Back.GREEN + "<=================================================================================================================>")
    # print("New Data Received: \n", len(newData), "Objects")
    # print("Existing Data pior import: \n", lenExistingData, "Objects")
    # print("Existing Data Removal Pending: \n", len(removedData), "Objects")
    # print("Total Data after import: ", len(newData) + (lenExistingData - len(removedData)), u"\u00B1", len(removedData), "Objects")
    print("\nSelect an option to deal with the merge conflict:")
    print("1. Drop deletion request (Doesn't Delete the \"removed\" objs from your system)")
    print("2. Accept deletions request")
    print("3. View Deleted Chips to Selectively Decide")
    print("Any other key to cancel Import Completely")
    choice = input(">>> ")
    switcher = {
        1: drop_deletions,
        2: accept_deletions,
        3: selective_deletion,
    }
    # Get the function from switcher dictionary
    try:
        delete = switcher.get(int(choice), cancel_import)
    except ValueError as e:
        delete = cancel_import

    return delete(removedData)

def Verify_Data_Integrity(newData):
    if not os.path.exists(CHIPS_JSON):
        return newData
    oldData = JSON.loadObjects(CHIPS_JSON)  # Serialized Data in form of dict
    oldDataUn = []    # Unserialized Data in form of <class 'dataChip.Chip'> objects
    oLen = len(oldData)
    nLen = len(newData)
    eLen = oLen     # Storing only for printing purposes
    i, j = (0, 0)

    for chipDict in oldData:     # Need to unserialize it for compatibility
        oldDataUn.append(Chip.unserialize(chipDict))

    while(i < oLen):
        j = 0
        while(j < nLen):
            if(newData[j].url == oldDataUn[i].url):
                del newData[j]
                del oldDataUn[i]
                oLen -= 1
                nLen -= 1
                j -= 1
                i -= 1
                break
            j += 1
        i += 1

    if(len(oldDataUn) > 0):  # Avoid showing the Menu if there aren't any objects with deletion requests pending
        delete, dataToBeRemoved = get_menuCLI(newData, oldDataUn, eLen)
    else:
        delete = False

    CHIPSDict = JSON.loadObjects(CHIPS_JSON)  # Serialized Data in form of dict
    CHIPS = []  # Unserialized Data in form of <class 'dataChip.Chip'> objects
    for chipDict in CHIPSDict:     # Need to unserialize it for compatibility
        CHIPS.append(Chip.unserialize(chipDict))

    if(delete):
        for chip in dataToBeRemoved:
            for i, C in enumerate(CHIPS):
                if(chip.url == C.url):
                    del CHIPS[i]
                    break;

    for chip in newData:
        CHIPS.append(chip)
    return CHIPS


#===============================================================================

def generateChips(limit):
    for pbm in generatePrimitiveBookmarks(limit):
        yield Chip(pbm)

def generateChipsfromImport():
    for p_bm in importer.generateImportsfromExports():
        yield Chip(p_bm)

#===============================================================================

class PICKLE(object):

    @staticmethod
    def storeObjects(filename, iterable):
        """
            Stores objects into binary form using pickle.

            Arguments:
            `filename` : File to use for writing objects (String)
            `iterable` : Any iterable object, such as lists, tuples or generators, that can return the object to be written to file on call of __next__()
        """
        if not os.path.exists("data/"):
            os.mkdir("data")

        with open(filename, 'wb') as fout:  # Overwrites any existing file.
            for obj in iterable:
                pickle.dump(obj, fout, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def loadObjects(filename):
        with open(filename, "rb") as fin:
            while True:
                try:
                    yield pickle.load(fin)
                except EOFError:
                    break


class JSON(object):

    @staticmethod
    def encoder(obj):
        """
            Usage: `json.dumps(obj, default=JSON.encoder)`
        """
        if isinstance(obj, Chip):
            return obj.serialize()
        raise TypeError(repr(obj) + " is not JSON serializable or Registered in Encoder...")

    @staticmethod
    def storeObjects(filename, iterable = None, objectsList = None, jsonObj = None):
        """
            Stores objects into JSON using json.dump and modified encoder (JSON.encoder)

            Arguments:
            `filename` : File to use for writing objects (String)
            `objectsList` : List of Objects to be written to the file (Non-Serialized)
            `iterable` : Any iterable object, such as lists, tuples or generators, that can return the object to be written to file on call of __next__()
            `jsonObj` : List of Objects to be written to the file (Serialized)
        """
        if not os.path.exists("data/"):     # TODO: Refactor the code to reduce the no. of args, using type check
            os.mkdir("data")

        if iterable and objectsList is None:      # When a iterable is passed
            chips = []      # Required due to JSON's storage restrictions (One JSON object per file)
            for chip in iterable:
                chips.append(chip)
            if isinstance(chips[0], Chip):
                chips = Verify_Data_Integrity(chips)

        path = pathlib.Path(pathlib.Path.cwd(), filename)
        with path.open("w") as fout:
            if iterable and objectsList is None:      # When a iterable is passed
                json.dump(chips, fout, indent=4, default=JSON.encoder)
            elif objectsList and iterable is None:      # When a list of objects is passed
                json.dump(objectsList, fout, indent=4, default=JSON.encoder)
            elif jsonObj and iterable is None and objectsList is None:
                json.dump(jsonObj, fout, indent=4)      # When a json object is passed directly

            else:
                raise AttributeError("Objects' source not parsable! (Expected 2 arguments got one or more)")

    @staticmethod
    def loadObjects(filename):
        path = pathlib.Path(pathlib.Path.cwd(), filename)
        with path.open() as fin:
            data = json.load(fin)
            return data


if __name__ == '__main__':
    colorama.init(autoreset = True)
    print(colorama.Fore.WHITE + colorama.Back.RED + 'Warning! This script is to be run internally by ' + PROJECT_NAME + ' scripts, direct use might lead to unexpected behaviour\n')
    # PICKLE.storeObjects(CHIPS_BIN, generateChipsfromImport())  # Should be handled from the main.py or app.py

    # JSON.storeObjects(CHIPS_JSON, generateChipsfromImport())
    JSON.storeObjects(CHIPS_JSON, importer.generateChipImports())

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(JSON.loadObjects(CHIPS_JSON))
    with Spinner():
        print("\n1st-Indent Objects loaded: ", len(JSON.loadObjects(CHIPS_JSON)))
