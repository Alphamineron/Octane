from html.parser import HTMLParser
import copy
import codecs
from tqdm import tqdm

class WebBookmark(object):
    def __init__(self):
        self.name = ""
        self.url = ""

    def show(self):
        str = self.name + "\n|\t" + self.url
        print("\n=======================================")
        print(str)

    def flush(self):
        self.name = ""
        self.url = ""

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
    if(input("Would you like to compare a Buku Export file and Chrome Export File? (Y/N): ") == "Y"):

        bukuPar = netscapeHTMLparser()

        with codecs.open("Dump/Data/BukuBookmarks.html", 'r', 'utf-8') as fin:
            str = fin.read()

        bukuPar.feed(str)

        print("Buku Objects Parsed: ", bukuPar.count)   # Buku Objects Parsed: 1305
        # for bookmark in bukuPar.bookmarks:
        #     bookmark.show()


        BPar = netscapeHTMLparser()

        with codecs.open("Dump/Data/bookmarks_11_06_2019.html", 'r', 'utf-8') as fin:
            str = fin.read()

        BPar.feed(str)

        print("Chrome Objects Parsed: ", BPar.count)    # Chrome Objects Parsed: 1314


        extraBM = []

        for b1 in tqdm(BPar.bookmarks):
            found = False
            for b2 in tqdm(bukuPar.bookmarks):
                if (b1.url == b2.url):
                    found = True
            if found is False:
                print("Extra Found!")
                extraBM.append(copy.deepcopy(b1))

        print("\n>>> Scan Completed!")  # Somehow, Chrome is exporting duplicates,
                                        # as the extraBM list is empty in the end...
    else:
        print("\nNo other functionality implemented yet... Exiting")
