from copy import deepcopy
import colorama

def get_oldData():
    return ['a', 'b', 'c', 'd']

def drop_deletions(removedData):
    return False, []

def accept_deletions(removedData):
    return True, removedData

def selective_deletion(removedData):
    dataArr = deepcopy(removedData)
    for data in dataArr:
        colorama.init(autoreset = True)
        print(colorama.Fore.WHITE + colorama.Back.RED + "\n<=================================>")
        print(data)
        print(colorama.Fore.WHITE + colorama.Back.RED + "<=================================>")
        choice = input("To Save? (Y/N): ")
        if(choice.lower() == 'y'):
            removedData.remove(data)

    return True, removedData

def cancel_import(_):
    print("Import Cancelled on User Request...")
    exit()

def get_menuCLI(newData, removedData):
    colorama.init(autoreset = True)
    print(colorama.Fore.WHITE + colorama.Back.GREEN + "\n<Import Status>")
    # print("New Data: ", newData)
    # print("Removed Data: ", removedData)
    print("New Data Received: \n", len(newData), "Objects")
    print("Existing Data Removed : \n", len(removedData), "Objects")
    print("\nSelect an option to deal with the merge conflict:")
    print("1. Drop deletion request (Doesn't Delete the \"removed\" objs from your system)")
    print("2. Accept deletions request")
    print("3. View Deleted Chips to Selectively Decide")
    print("Any other key to cancel Import Completely")
    choice = input(">>> ")
    switcher = {
        1: drop_deletions,
        2: accept_deletions,
        3: selective_deletion,
    }
    # Get the function from switcher dictionary
    try:
        delete = switcher.get(int(choice), cancel_import)
    except ValueError as e:
        delete = cancel_import

    return delete(removedData)

def Verify_Data_Integrity(newData):
    oldData = get_oldData()
    oLen = len(oldData)
    nLen = len(newData)
    i, j = (0, 0)

    while(i < oLen):
        j = 0
        while(j < nLen):
            if(newData[j] == oldData[i]):
                del newData[j]
                del oldData[i]
                oLen -= 1
                nLen -= 1
                j -= 1
                i -= 1
                break
            j += 1
        i += 1


    delete, dataToBeRemoved = get_menuCLI(newData, oldData)
    CHIPS = get_oldData()
    if(delete):
        for chip in dataToBeRemoved:
            for i, C in enumerate(CHIPS):
                if(chip == C):
                    del CHIPS[i]
                    break;
    for chip in newData:
        CHIPS.append(chip)
    return CHIPS

newData = ['a', 'd', 'e', 'f', 'g', 'h', 'i']
print("Existing Data: ", get_oldData())
print("Input Data: ", newData)
CHIPS = Verify_Data_Integrity(deepcopy(newData))
print("Final Data: ", CHIPS)

# print("\n\n\n", isinstance(exit, _sitebuiltins.Quitter))
