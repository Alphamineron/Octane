import codecs
import os

import parser_Medium as MP
import parser_netscapeHTML as NP
import controller_buku

EXPORT_FILE_PATH = "./temp/browserExport.html"
DIRECTORY_IN_STR = "Dump/Data/medium-export/bookmarks/"


def GET_BrowserExports():
    controller_buku.run(ERASE_BEFORE_INIT = False, EXPORT_FILE_PATH = EXPORT_FILE_PATH)

    parser = NP.netscapeHTMLparser()
    with codecs.open(EXPORT_FILE_PATH, 'r', 'utf-8') as fin:
        str = fin.read()
    parser.feed(str)
    # return parser.bookmarks, parser.count
    # for bookmark in parser.bookmarks:
        # bookmark.show()


def GET_MediumExports():
    parser = MP.MediumParser()

    directory = os.fsencode(DIRECTORY_IN_STR)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".html"):
            filepath = os.path.join(DIRECTORY_IN_STR, filename)

            print("Parsing", filepath)
            with codecs.open(filepath, 'r', 'utf-8') as fin:
                str = fin.read()

            parser.feed(str)
            continue
        else:
            continue
    print("Objects Parsed: ", parser.count)


    # for bookmark in parser.bookmarks:
    #     bookmark.show()
if __name__ == '__main__':
    GET_BrowserExports()
    GET_MediumExports()
