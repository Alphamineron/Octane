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

class Chip(Primitive_Bookmark):
    """
        docstring for Chip
        ID Format: C<USERCODE>XXXXX
    """
    def __init__(self):
        super()
        self.ID = None          # NoneID invalidates the chip, equivalent to deleting it
        self.title = self.name
        self.description = ""
        self.img = None         # LFS
        self.cache = None       # LFS
        self.tags = []          # List of Strings
        self.useCases = []      # List of UseCase Objects IDs
        self.phaseID = None     # Color Hex Value
        self.status = None      # 4-State Value - Done - In_Progress - ToDo - None(N/A)
        self.TodoList = False   # List of TodoSections Objects IDs
        pass
