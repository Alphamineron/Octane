import codecs
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import parser_Medium as MP
import parser_netscapeHTML as NP
# import parser_Browser as BP  {INSIDE generateChipImports()}
from dataChip import Chip
import controller_buku

from utils.spinner import Spinner

# Fetching Defined Project-Scoped Config Constants
from config import BROWSER_EXPORT_FILE, MEDIUM_DIR, __GC_DB, __CR_DB, __IMPORT_GC, __IMPORT_CR, __IMPORT_MEDIUM


def GET_BrowserExports(exportFile = BROWSER_EXPORT_FILE, mute = True, buku = False):
    if buku:
        controller_buku.run(ERASE_BEFORE_INIT = False, EXPORT_FILE_PATH = exportFile, mute = mute)

    parser = NP.netscapeHTMLparser()
    with codecs.open(exportFile, 'r', 'utf-8') as fin:
        str = fin.read()
    parser.feed(str)
    return parser.bookmarks, parser.count


def GET_MediumExports(dirString = MEDIUM_DIR, mute = True):
    parser = MP.MediumParser()  # Parser not local to loop, Stores data from all files

    directory = os.fsencode(dirString)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".html"):
            filepath = os.path.join(dirString, filename)

            if not mute: print("Parsing", filepath)
            with codecs.open(filepath, 'r', 'utf-8') as fin:
                str = fin.read()
            parser.feed(str)
            continue
        else:
            continue
    if not mute: print("\n\t Medium Bookmarks:", parser.count, "exported")
    return parser.bookmarks, parser.count

def generateImportsfromExports():
    """
        Generator for iterating through combined exports from browsers and medium files

        Yields:
        `dataChip.Primitive_Bookmark`
    """
    sys.stdout.write("\n> Auto-Importing bookmarks: ")   # TODO: Add the config setup check before this for paths
    with Spinner():
        b_1, c_1 = GET_BrowserExports(buku = True)
        b_2, c_2 = GET_MediumExports()
    print(c_1 + c_2, "objects imported")

    b_1.extend(b_2)
    yield from b_1


def generateChipImports():
    """
        Generator for iterating through imports from browsers and medium files

        Yields:
        `dataChip.Chip`
    """
    import parser_Browser as BP  # import needs to be removed otherwise
                                # if parser_Browser.py is to be run alone

    sys.stdout.write("\n> Auto-Importing bookmarks: ")   # TODO: Add the config setup check before this for paths
    with Spinner():
        if(__IMPORT_GC):
            try:
                for chips in BP.import_from_Browser("Google Chrome", __GC_DB, BP.jsonMiner, mute = True):
                    yield chips
            except FileNotFoundError as e:
                print("Issue Encountered: ", e, " > ", __GC_DB)

        if(__IMPORT_CR):
            try:
                for chips in BP.import_from_Browser("Chromium", __CR_DB, BP.jsonMiner, mute = True):
                    yield chips
            except FileNotFoundError as e:
                print("Issue Encountered: ", e, " > ", __CR_DB)

        if(__IMPORT_MEDIUM):
            try:
                mediumB, _ = GET_MediumExports()
                for p_bm in mediumB:
                    yield Chip(p_bm)
            except FileNotFoundError as e:
                print("Issue Encountered: ", e, " > ", MEDIUM_DIR)

    # yield from mediumB
