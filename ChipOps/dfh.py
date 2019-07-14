import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# Imports for Data File Handling
try: import cPickle as pickle
except ModuleNotFoundError: import pickle

from dataChip import Chip
import importer

import colorama

PROJECT_NAME = "BMM"
CHIPS_FILE = "data/chips.bin"


def generateChipsfromImport():
    for p_bm in importer.generateImports():
        chip = Chip()
        chip.inherit(p_bm)
        yield chip


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

def loadObjects(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

class JSON(object):
    def __init__(self):
        pass

    @staticmethod
    def encoder(self, obj):
        """
            Usage: `json.dumps(obj, default=JSON.encoder)`
        """
        if isinstance(obj, Chip):
            return obj.serialize()
        raise TypeError(repr(obj) + " is not JSON serializable")


if __name__ == '__main__':
    colorama.init(autoreset = True)
    print(colorama.Fore.WHITE + colorama.Back.RED + 'Warning! This script is to be run internally by ' + PROJECT_NAME + ' scripts, direct use might lead to unexpected behaviour\n')
    # storeObjects(CHIPS_FILE, generateChipsfromImport())  # Should be handled from the main.py or app.py
