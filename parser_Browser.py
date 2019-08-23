import sys
import os
import json
import uuid
import colorama
from utils.spinner import Spinner

from config import __GC_DB, FOLDERTREE_JSON, USERCODE, PROJECT_NAME
from dataChip import Chip, Primitive_Bookmark
from ChipOps.dfh import JSON
from utils.timeHandle import timestamp_from_webkit

from treelib import Tree
from treelib.exceptions import DuplicatedNodeIdError

class TreeOctane(Tree):
    def __init__(self):
        super(TreeOctane, self).__init__()

    @staticmethod
    def to_JSON():
        JSON.storeObjects(FOLDERTREE_JSON, jsonObj = json.loads(tree.to_json(with_data = True)))

    # @Override
    def to_dict(self, nid=None, key=None, sort=True, reverse=False, with_data=False):
        """Transform the whole tree into a dict."""

        saved_nidState = nid  # Used to Discrimate the "root" node, removing it from the output JSON
        nid = self.root if (nid is None) else nid
        ntag = self[nid].tag
        tree_dict = {
                    "id": self.root if (saved_nidState is None) else ("F" + USERCODE + str(uuid.uuid4()).replace("-", "")),
                    "name": ntag,
                    "children": []
                    }

        if with_data:
            tree_dict["data"] = self[nid].data

        if self[nid].expanded:
            queue = [self[i] for i in self[nid].fpointer]
            key = (lambda x: x) if (key is None) else key
            if sort:
                queue.sort(key=key, reverse=reverse)

            for elem in queue:    # Below Line is a Main Data Traffic Return point of the recursive Data Pipe (All the return statements point here)
                tree_dict["children"].append(self.to_dict(elem.identifier, with_data=with_data, sort=sort, reverse=reverse))

            if len(tree_dict["children"]) == 0:   # If No. of Children at the recursively relative current root are ZERO
                tree_dict = {
                                "id": ("F" + USERCODE + str(uuid.uuid4()).replace("-", "")),
                                "name": self[nid].tag,
                                "children": []
                            } if not with_data else {

                                "id": ("F" + USERCODE + str(uuid.uuid4()).replace("-", "")),
                                "name": ntag,
                                "children": [],
                                "data": self[nid].data
                            }

            if(tree_dict["id"] == "root"):
                return tree_dict["children"]

            return tree_dict    # This return goes to the Main Data Traffic Return Point of the calling recursive function


tree = TreeOctane()



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
        print("\nUnable to import bookmarks from {}".format(BrowserName))
        raise e


def jsonMiner(db_path):
    with open(db_path, "r") as df:
        data = json.load(df)
    roots = data["roots"]
    tree.create_node("root", "root")   # root node

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
            p_bm.time = timestamp_from_webkit(int(item["date_added"]))
            p_bm.foldersStack = foldersStack
            chip = Chip(p_bm)

            node = tree.get_node('->'.join(foldersStack))
            if node.data is None:
                node.data = []
            node.data.append(chip.ID)
            yield chip



if __name__ == '__main__':
    colorama.init(autoreset = True)
    print(colorama.Fore.WHITE + colorama.Back.RED + 'Warning! This script is to be run internally by ' + PROJECT_NAME + ' scripts, direct use might lead to unexpected behaviour\n')

    JSON.storeObjects("data/chipsTEST.json", import_from_Browser("Google Chrome", __GC_DB, jsonMiner))

    sys.stdout.write("\n> Fetching bookmarks from local file system -> ")
    with Spinner():
        print("\nObjects loaded: ", len(JSON.loadObjects("data/chipsTEST.json")))

    print("\n\n")
    tree.show(line_type="ascii-em")

    TreeOctane.to_JSON()











































    # print(entry)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(roots)
