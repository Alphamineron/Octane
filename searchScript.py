import json
from tqdm import tqdm


def mapstruct(d, key, intend):
    print("", "    " * intend, "├", key)

def foo(d, key = True):
    if(key == "name"):
        print("F: Name Found: ", d[key])

    if(key == "type"):
        print("F: Type Found: ", d[key], "\n")




def digD(d, intend = 1, func = mapstruct):
    for key in d.keys():    # Loop to step inside the heirarchy

        if(func == mapstruct):
            func(d, key, intend)
        else:
            func(d, key)

        # Recursive Digging
        if(isinstance(d[key], dict)):
            digD(d[key], intend+1, func)
        if(isinstance(d[key], list)):
            digL(d[key], intend+1, func)

def digL(l, intend, func = mapstruct, index = True):
    for i, val in enumerate(l):    # Loop to step inside the heirarchy

        if(index == True and func == mapstruct):
            print("    " * intend, "--" + "[" + str(i+1) + "]")
        else:           # REMOVE THIS
            pass


        # Recursive Digging
        if(isinstance(val, dict)):
            digD(val, intend+1, func)
        if(isinstance(val, list)):
            digL(val, intend+1, func)


def main():
    with open('Dump/Data/chrome-exports/BookmarksC', 'r', encoding='utf8') as inf:
        workingData = json.load(inf)
        # Start Digging...
        digD(workingData, func = foo)

if __name__ == "__main__":
    main();
