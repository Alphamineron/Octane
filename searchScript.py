import json
from tqdm import tqdm


def mapstruct(d, key, intend):
    print("", "    " * intend, "|-", key)

def foo(d, key):
    if(isinstance(d[key], dict)):
        for k in d[key].keys():
            if(k == "type"):
                print("Type Found: ", d[key]["type"])


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
            for d in l:
                for k in d.keys():
                    if(k == "type"):
                        print("Type Found: ", d["type"])


        # Recursive Digging
        if(isinstance(val, dict)):
            digD(val, intend+1, func)
        if(isinstance(val, list)):
            digL(val, intend+1, func)


def main():
    with open('chrome-exports/Bookmarks', 'r', encoding='utf8') as inf:
        workingData = json.load(inf)
        # Start Digging...
        digD(workingData)

if __name__ == "__main__":
    main();
