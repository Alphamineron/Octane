import copy
import uuid

from colorama import init, Fore
import colorama
import pprint

# Fetching Defined Project-Scoped Config Constants
from config import PROJECT_NAME, USERCODE

class Primitive_Bookmark(object):
    def __init__(self):
        self.name = ""
        self.url = ""
        self.date_added = ""
        self.source = []        # Is it from Medium? Is it from Youtube
        self.foldersStack = []

    def show(self):
        init(autoreset = True)
        name = "\n" + Fore.WHITE + self.name + Fore.RESET
        date_added = "\n| " + Fore.GREEN + str(self.date_added) + Fore.RESET
        url = "\n>\t" + Fore.BLUE + self.url
        print(name + date_added + url)
        print("=========================================================\n")

    def flush(self):
        self.name = ""
        self.url = ""
        self.date_added = ""
        self.source = []
        self.foldersStack = []


class Chip(Primitive_Bookmark):
    """
        docstring for Chip
        ID Format: C<USERCODE>XXXXX
    """
    def __init__(self, p_bm = None):
        super()
        if p_bm:
            self.inherit(p_bm)

        self.ID = "C" + USERCODE + str(uuid.uuid4()).replace("-", "")       # NoneID invalidates the chip, equivalent to deleting it
        self.description = ""
        self.img = None         # LFS
        self.cache = None       # LFS
        self.TodoList = []   # List of TodoSections Objects IDs
        self.starred = False

        self.tags = []          # List of Strings
        self.kind = []          # Is this a video, article, or image? What kind of content this represents
        self.useCases = []      # List of UseCase Objects IDs
        self.topics = []        # List of Topics that the Chip's contents fall into
        self.phaseID = None
        self.status = None      # 4-State Value: Done - In_Progress - ToDo - None(N/A)

        self.collectionIDs = None
        self.folderID = None

    def inherit(self, p_bm):
        self.name = p_bm.name
        self.url = p_bm.url
        self.date_added = p_bm.date_added
        self.source = copy.deepcopy(p_bm.source)
        self.foldersStack = copy.deepcopy(p_bm.foldersStack)

    def serialize(self):
        return  {
                    "ID" : self.ID,
                    "name" : self.name,
                    "url" : self.url,
                    "date_added" : self.date_added,
                    "description" : self.description,
                    "starred" : self.starred,
                    "tags" : self.tags,
                    "source" : self.source,
                    "kind" : self.kind,
                    "UseCases" : self.useCases,
                    "topics" : self.topics,
                    "phaseID" : self.phaseID,
                    "status" : self.status,
                    "folders" : self.foldersStack
                }
    @staticmethod
    def unserialize(dict):
        chip = Chip()
        chip.ID = dict["ID"]
        chip.name = dict["name"]
        chip.url = dict["url"]
        chip.date_added = dict["date_added"]
        chip.description = dict["description"]
        chip.starred = dict["starred"]
        chip.tags = dict["tags"]
        chip.source = dict["source"]
        chip.kind = dict["kind"]
        chip.useCases = dict["UseCases"]
        chip.topics = dict["topics"]
        chip.phaseID = dict["phaseID"]
        chip.status = dict["status"]
        chip.foldersStack = dict["folders"]
        return chip










def generatePrimitiveBookmarks(limit):
    for i in range(limit):
        p_bm = Primitive_Bookmark()
        p_bm.name = "Test_" + str(i)
        p_bm.url = "https://www.test" + str(i) + ".com"
        p_bm.date_added = int("1547620945" + str(i))
        yield p_bm

def test_inherit(limit, show=False):
    print("Testing Chip.inherit()")
    try:
        for p_bm in generatePrimitiveBookmarks(limit):
            chip = Chip(p_bm)
            # chip.inherit(p_bm)
            if show:
                chip.show()

        print("Initialization of "+ str(limit) +" chips: True")
    except Exception as e:
        print("Error encountered in test_inherit()")

def test_serialize(limit, show=False):
    print("Testing Chip.serialize()")
    try:
        for pbm in generatePrimitiveBookmarks(limit):
            chip = Chip(pbm)
            if show:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(chip.serialize())
                print("Serialization of "+ str(limit) +" chips: True")

    except Exception as e:
        print("Error encountered in test_serialize()")


class UseCase(object):
    """
        docstring for UseCase
        ID Format: UC<USERCODE>XXXXX
    """
    def __init__(self):
        self.ID = "UC" + USERCODE + str(uuid.uuid4()).replace("-", "")          # NoneID invalidates the object, equivalent to deleting it
        self.name = None
        self.desc = None
        self.projectIDs = []    # Projects that this UseCase is useful in
        self.phaseID = None     # Phase that this UseCase is useful for
        pass


class Todo(object):
    """
        docstring for Todo
        ID Format: T<USERCODE>XXXXX
    """
    def __init__(self):
        self.ID = "T" + USERCODE + str(uuid.uuid4()).replace("-", "")          # NoneID invalidates the object, equivalent to deleting it
        self.title = ""
        self.note = ""
        self.status = False
        pass


class TodoSection(object):
    """
        docstring for TodoSection
        ID Format: TS<USERCODE>XXXXX
    """
    def __init__(self):
        self.ID = "TS" + USERCODE + str(uuid.uuid4()).replace("-", "")          # NoneID invalidates the object, equivalent to deleting it
        self.heading = ""
        self.description = ""
        self.list = []      # List of Todo Objects IDs
        pass


if __name__ == '__main__':
    colorama.init(autoreset = True)
    print(colorama.Fore.WHITE + colorama.Back.RED + 'Warning! This script is to be run internally by ' + PROJECT_NAME + ' scripts, direct use might lead to unexpected behaviour\n')
    # test_inherit(10000)
