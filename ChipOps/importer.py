import sys
import codecs
import os

import parser_Medium as MP
import parser_netscapeHTML as NP
import controller_buku

from utils.spinner import Spinner

# Fetching Defined Project-Scoped Config Constants
from config import BROWSER_EXPORT_FILE, MEDIUM_DIR


def GET_BrowserExports(exportFile = BROWSER_EXPORT_FILE, mute = True):
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

def generateImports():
    """
        Generator for iterating through combined exports from browsers and medium files

        Yields:
        `dataChip.Primitive_Bookmark`
    """
    sys.stdout.write("\n> Auto-Importing bookmarks: ")   # TODO: Add the config setup check before this for paths
    with Spinner():
        b_1, c_1 = GET_BrowserExports()
        b_2, c_2 = GET_MediumExports()
    print(c_1 + c_2, "objects imported")

    b_1.extend(b_2)
    yield from b_1
