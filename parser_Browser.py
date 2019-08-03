import sys
import os
import json
import ast
import pprint
from tqdm import tqdm
from utils.spinner import Spinner

from config import __GC_DB
from dataChip import Chip, Primitive_Bookmark
from ChipOps.dfh import JSON

from treelib import Node, Tree
from treelib.exceptions import DuplicatedNodeIdError

tree = Tree()



def import_from_Browser(BrowserName, db_path, loader, mute = False):
    """
        Wrapper function that calls and handles the appropriate Bookmarks Loader
        for the given browser.
        Usage includes being passed as an encoder for ChipOps.dfh.JSON.storeObjects()

        # Parameters
        `BrowserName` : Name of the Browser ->  _(str)_
        `db_path` : Path to the Bookmarks' Database of the browser ->  _(str)_
        `loader` : Function handling the importing for the specific case ->  _(function)_

        # Returns
        `Chip` : Object of dataChip.Chip class containing bookmark name, url and
                 folder structure data

        # Examples
        >>>>>> JSON.storeObjects("data/chipsTEST.json", import_from_Browser("Google Chrome", __GC_DB, jsonMiner))

    """
    try:
        db_path = os.path.expanduser(db_path)
        if not os.path.exists(db_path):
            raise FileNotFoundError

        if not mute: sys.stdout.write("\n> Importing bookmarks from {} -> ".format(BrowserName))
        with Spinner(mute = mute):
            for bookmark in loader(db_path):
                yield bookmark

    except Exception as e:
        print("Unable to import bookmarks from {}\n".format(BrowserName))
        raise e


def jsonMiner(db_path):
    with open(db_path, "r") as df:
        data = json.load(df)
    roots = data["roots"]
    tree.create_node("Root", "root")   # root node

    for entry in roots:
        if entry == "sync_transaction_version":
            continue

        tree.create_node(roots[entry]["name"], ("root->" + roots[entry]["name"]), parent="root")
        node = tree.get_node("root->" + roots[entry]["name"])
        node.data = []

        for object in digJSONTree(roots[entry]["children"], ["root", roots[entry]["name"]]):
            # node.data.append(object.ID)  The reason this leads to error is because it's on the main
            yield object                 # data pipe, so we find duplicates of nested Chips' IDs


def createTreeNode(foldersStack):
    parentTrace = foldersStack[:-1]
    try:
        tree.create_node(foldersStack[-1], '->'.join(foldersStack), parent='->'.join(parentTrace))
    except DuplicatedNodeIdError as e:
        pass


def digJSONTree(sublist, foldersStack):
    """
        Recursive generator that fetches the bookmarks from a JSON storage
        scheme, preserving the hierarchical folder structure data.

        # Parameters
        `sublist` : List of child entries in the given folder ->  _(list)_
        `foldersStack` : Stack denoting Parent folders  ->  _(str)_

        # Returns
        `Chip` : Object of dataChip.Chip class containing bookmark name, url and
                 folder structure data
    """
    for item in sublist:
        if item["type"] == "folder":
            foldersStack.append(item["name"])
            createTreeNode(foldersStack)

            for object in digJSONTree(item["children"], foldersStack):
                yield object
            foldersStack.pop()

        elif item["type"] == "url":
            p_bm = Primitive_Bookmark()
            p_bm.name = item["name"]
            p_bm.url = item["url"]
            p_bm.foldersStack = foldersStack
            chip = Chip(p_bm)

            node = tree.get_node('->'.join(foldersStack))
            if node.data is None:
                node.data = []
            node.data.append(chip.ID)
            yield chip



if __name__ == '__main__':
    JSON.storeObjects("data/chipsTEST.json", import_from_Browser("Google Chrome", __GC_DB, jsonMiner))

    sys.stdout.write("\n> Fetching bookmarks from local file system -> ")
    with Spinner():
        print("\nObjects loaded: ", len(JSON.loadObjects("data/chipsTEST.json")))

    print("\n\n")
    tree.show(line_type="ascii-em")

    # pp = pprint.PrettyPrinter(indent=1)
    # pp.pprint(ast.literal_eval(tree.to_json()))
    JSON.storeObjects("data/folderTree.json", jsonObj = json.loads(tree.to_json()))











































    # print(entry)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(roots)
