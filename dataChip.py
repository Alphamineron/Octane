from colorama import init, Fore

class Primitive_Bookmark(object):
    def __init__(self):
        self.name = ""
        self.url = ""
        self.time = ""

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


class UseCase(object):
    """
        docstring for UseCase
        ID Format: UC<USERCODE>XXXXX
    """
    def __init__(self):
        self.ID = None          # NoneID invalidates the object, equivalent to deleting it
        pass



class Todo(object):
    """
        docstring for Todo
        ID Format: T<USERCODE>XXXXX
    """
    def __init__(self):
        self.ID = None          # NoneID invalidates the object, equivalent to deleting it
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
        self.ID = None          # NoneID invalidates the object, equivalent to deleting it
        self.heading = ""
        self.description = ""
        self.list = []      # List of Todo Objects IDs
        pass

"""
    ID : Unique ID of the Chip Object
    img : Web Scraped image related to the chip, extacted from the url
"""

class Chip(Primitive_Bookmark):
    """
        docstring for Chip
        ID Format: C<USERCODE>XXXXX
    """
    def __init__(self):
        super()
        self.ID = None          # NoneID invalidates the chip, equivalent to deleting it
        self.description = ""
        self.img = None         # LFS
        self.cache = None       # LFS
        self.TodoList = []   # List of TodoSections Objects IDs
        self.starred = False

        self.source = []        # Is it from Medium? Is it from Youtube
        self.kind = []          # Is this a video, article, or image? What kind of content this represents
        self.tags = []          # List of Strings
        self.useCases = []      # List of UseCase Objects IDs
        self.topics = []        # List of Topics that the Chip's contents fall into
        self.phaseID = None     # Color Hex Value
        self.status = None      # 4-State Value: Done - In_Progress - ToDo - None(N/A)

        self.collectionIDs = None
        self.folderID = None

    def inherit(self, p_bm):
        self.name = p_bm.name
        self.url = p_bm.url
        self.time = p_bm.time


def iterPrimitiveBookmarks(limit):
    for i in range(limit):
        p_bm = Primitive_Bookmark()
        p_bm.name = "Test_" + str(i)
        p_bm.url = "https://www.test" + str(i) + ".com"
        p_bm.time = "DateTimeObject_" + str(i)
        yield p_bm

def test_initPrimitiveBookmarks(limit, show=False):
    try:
        for p_bm in iterPrimitiveBookmarks(limit):
            chip = Chip()
            chip.inherit(p_bm)
            if show:
                chip.show()

        print("initPBm - Initialization of "+ str(limit) +" chips: True")
    except Exception as e:
        print("Error encountered in test_initPrimitiveBookmarks()")

def main():
    test_initPrimitiveBookmarks(10000)





if __name__ == '__main__':
    # import msgpack
    #
    # # Define data
    # data = {'a list': [1, 42, 3.141, 1337, 'help'],
    #         'a string': 'bla',
    #         'another dict': {'foo': 'bar',
    #                          'key': 'value',
    #                          'the answer': 42}}
    #
    # # Write msgpack file
    # with open('data.msgpack', 'wb') as outfile:
    #     msgpack.packb(data, outfile)
    #
    # # Read msgpack file
    # with open('data.msgpack', "rb") as data_file:
    #     # data_loaded = json.load(data_file)
    #     data_loaded = msgpack.unpack(data_file)
    #
    # print(data)
    # print(data_loaded)
    main()
