import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# Imports for Data File Handling
try: import cPickle as pickle
except ModuleNotFoundError: import pickle
import json

from dataChip import Chip, generatePrimitiveBookmarks
import importer

import colorama
import pprint

PROJECT_NAME = "BMM"
CHIPS_BIN = "data/chips.bin"
CHIPS_JSON = "data/chips.json"


def generateChips(limit):
    for pbm in generatePrimitiveBookmarks(limit):
        chip = Chip(pbm)
        yield chip

def generateChipsfromImport():
    for p_bm in importer.generateImports():
        chip = Chip()
        chip.inherit(p_bm)
        yield chip

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
        raise TypeError(repr(obj) + " is not JSON serializable")

    @staticmethod
    def storeObjects(filename, iterable = None, objectsList = None):
        """
            Stores objects into JSON using json.dump and modified encoder (JSON.encoder)

            Arguments:
            `filename` : File to use for writing objects (String)
            `objectsList` : List of Objects to be written to the file
            `iterable` : Any iterable object, such as lists, tuples or generators, that can return the object to be written to file on call of __next__()
        """
        if not os.path.exists("data/"):     # TODO: Refactor the code to reduce the no. of args, using type check
            os.mkdir("data")

        with open(filename, "w") as fout:
            if iterable and objectsList is None:      # When a iterable is passed
                chips = []      # Required due to JSON's storage restrictions (One JSON object per file)
                for chip in iterable:
                    chips.append(chip)
                json.dump(chips, fout, indent=4, default=JSON.encoder)

            elif objectsList and iterable is None:      # When a list of objects is passed
                json.dump(objectsList, fout, indent=4, default=JSON.encoder)

            else:
                raise AttributeError("Objects' source not parsable! (Expected 2 arguments got one or more)")

    @staticmethod
    def loadObjects(filename):
        with open(filename, "r") as fin:
            data = json.load(fin)
            return data


if __name__ == '__main__':
    colorama.init(autoreset = True)
    print(colorama.Fore.WHITE + colorama.Back.RED + 'Warning! This script is to be run internally by ' + PROJECT_NAME + ' scripts, direct use might lead to unexpected behaviour\n')
    # PICKLE.storeObjects(CHIPS_BIN, generateChipsfromImport())  # Should be handled from the main.py or app.py

    JSON.storeObjects(CHIPS_JSON, generateChipsfromImport())

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(JSON.loadObjects(CHIPS_JSON))
