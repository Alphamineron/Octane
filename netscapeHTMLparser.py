from html.parser import HTMLParser
import copy
import codecs
from tqdm import tqdm
import argparse
import sys

from dataChip import Primitive_Bookmark as WebBookmark

# class WebBookmark(object):
#     def __init__(self):
#         self.name = ""
#         self.url = ""
#         self.time = ""
#
#     def show(self):
#         str = self.name + "\n|\t" + self.url
#         print("\n=======================================")
#         print(str)
#
#     def flush(self):
#         self.name = ""
#         self.url = ""
#         self.time = ""

class netscapeHTMLparser(HTMLParser):
    mdm = WebBookmark()  # For Internal Use Only

    def __init__(self):
        HTMLParser.__init__(self)

        self.count = 0      # No. of Bookmark Objects Collected
        self.bookmarks = []
        self.possibleBookmark = False;   # Flag to know if the current HTML element a bookmark

    # @Override
    def handle_starttag(self, tag, attrs):
        self.tag = tag          # Remembering details of HTML element
        self.attrs = attrs      # the Parser is currently inside of

        try:
            for a in attrs:
                if(a[0] == "href"):
                    netscapeHTMLparser.mdm.url = a[1]
                    self.possibleBookmark = True
        except: pass

    # @Override
    def handle_endtag(self, tag):
        if(tag == "a" and self.possibleBookmark == True):  # </DT> marks the end of a Bookmark in the HTML file
            self.bookmarks.append(copy.deepcopy(netscapeHTMLparser.mdm))   # DEEPCOPY required
            # to append a separated entry into the list, so refs aren't appended instead

            self.count += 1         # HOUSECLEANING
            netscapeHTMLparser.mdm.flush()
            self.possibleBookmark = False
        self.tag = ""

    # @Override
    def handle_data(self, data):
        try:
            if(self.tag == "a"):
                netscapeHTMLparser.mdm.name = data
        except Exception as e:
            pass



# ██████  ██ ██████  ███████ ██      ██ ███    ██ ███████
# ██   ██ ██ ██   ██ ██      ██      ██ ████   ██ ██
# ██████  ██ ██████  █████   ██      ██ ██ ██  ██ █████
# ██      ██ ██      ██      ██      ██ ██  ██ ██ ██
# ██      ██ ██      ███████ ███████ ██ ██   ████ ███████

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="View basic details from a Netscape format Bookmarks File (Usually exported files from popular Browsers)")
    group = argparser.add_mutually_exclusive_group()
    group.add_argument("-i", "--input",
                        help="Path of the Netscrape format HTML file",
                        type=str)

    group.add_argument("-c", "--compare",
                            help="Compare Buku and Chrome exported bookmarks files. Requires [BukuFilePath] [ChromeFilePath]. Paths can be absolute or relative to %(prog)s",
                            action="store_true")

    argparser.add_argument("-b", "--buku",
                            help="Buku's export file path",
                            required=("--compare" in sys.argv),
                            type=str,
                            default="Dump/Data/BukuBookmarks.html")

    argparser.add_argument("-ch", "--chrome",
                            help="Chrome's export file path",
                            required=("--compare" in sys.argv),
                            type=str,
                            default="Dump/Data/bookmarks_11_06_2019.html")

    args = argparser.parse_args()


    if args.compare:

        bukuPar = netscapeHTMLparser()
        with codecs.open(args.buku, 'r', 'utf-8') as fin:
            str = fin.read()
        bukuPar.feed(str)
        print("Buku Objects Parsed: ", bukuPar.count)   # Buku Objects Parsed: 1305

        BPar = netscapeHTMLparser()
        with codecs.open(args.chrome, 'r', 'utf-8') as fin:
            str = fin.read()
        BPar.feed(str)
        print("Chrome Objects Parsed: ", BPar.count)    # Chrome Objects Parsed: 1314


        extraBM = []
        duplicateBM = []

        if BPar.count > bukuPar.count:
            big = BPar
            small = bukuPar
        else:
            big = bukuPar
            small = BPar

        print("\nFinding extra items in larger list:")
        for b1 in tqdm(big.bookmarks):
            found = False
            for b2 in tqdm(small.bookmarks):
                if (b1.url == b2.url):
                    found = True

            if found is False:
                print("Extra Found!")
                extraBM.append(copy.deepcopy(b1))

        print("\n\nFinding duplicate items in larger list considering smaller list:")
        for b1 in tqdm(small.bookmarks):
            f_count = 0
            duplicates = 0
            for b2 in tqdm(big.bookmarks):
                if (b1.url == b2.url):  f_count += 1

                if f_count > 1:
                    f_count -= 1
                    duplicates += 1
                    big.bookmarks.remove(b2)

            if duplicates is not 0:
                duplicateBM.append([copy.deepcopy(b1), duplicates])

        print("\n\n>>> Scan Completed!")  # Somehow, Chrome is exporting duplicates,
                                        # as the extraBM list is empty in the end...
        print("\n\t\t ===> Scan Stats <====")
        print("Bigger List Length: ", len(big.bookmarks))
        print("Smaller List Length: ", len(small.bookmarks))
        print("\n Bigger List:")
        print("No. of Extras Found:", len(extraBM))
        if len(extraBM) is not 0:
            print("Extra Bookmarks:")
            for bm in extraBM:
                bm.show()

        print("No. of Duplicate Bookmarks Found:", len(duplicateBM))

        ch = input("Show recurring Bookmarks? (Y/N): ")

        if ch is "Y" or ch is "y":
            if len(duplicateBM) is not 0:
                print("\nDuplicate Bookmarks:\n")
                for bm in duplicateBM:
                    print(bm[0].name + "\nReplicates Found = ", bm[1], "\n|\t" + bm[0].url)
                    print("\n=======================================")



    else:
        parser = netscapeHTMLparser()
        with codecs.open(args.input, 'r', 'utf-8') as fin:
            str = fin.read()
        parser.feed(str)
        print("Objects Parsed: ", parser.count)   # Buku Objects Parsed: 1305
        for bookmark in parser.bookmarks:
            bookmark.show()
