import copy
import uuid

from colorama import init, Fore
import colorama
import pprint

USERCODE = "0000"
PROJECT_NAME = "BMM"

class Primitive_Bookmark(object):
    def __init__(self):
        self.name = ""
        self.url = ""
        self.time = ""
        self.source = []        # Is it from Medium? Is it from Youtube

    def show(self):
        init(autoreset = True)
        name = "\n" + Fore.WHITE + self.name + Fore.RESET
        time = "\n| " + Fore.GREEN + self.time + Fore.RESET
        url = "\n>\t" + Fore.BLUE + self.url
        print(name + time + url)
        print("=========================================================\n")

    def flush(self):
        self.name = ""
        self.url = ""
        self.time = ""
        self.source = []


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
        self.time = p_bm.time
        self.source = copy.deepcopy(p_bm.source)

    def serialize(self):
        return  {
                    "ID" : self.ID,
                    "name" : self.name,
                    "url" : self.url,
                    "time" : self.time,
                    "description" : self.description,
                    "starred" : self.starred,
                    "tags" : self.tags,
                    "source" : self.source,
                    "kind" : self.kind,
                    "UseCases" : self.useCases,
                    "topics" : self.topics,
                    "phaseID" : self.phaseID,
                    "status" : self.status,
                }










def generatePrimitiveBookmarks(limit):
    for i in range(limit):
        p_bm = Primitive_Bookmark()
        p_bm.name = "Test_" + str(i)
        p_bm.url = "https://www.test" + str(i) + ".com"
        p_bm.time = "DateTimeObject_" + str(i)
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
