from html.parser import HTMLParser
import copy
import codecs

from utils.timeHandle import timestamp_from_MediumDate
from dataChip import Primitive_Bookmark as MediumBookmark

A_CLASS = "h-cite"
TIME_CLASS = "dt-published"

# class MediumBookmark(object):
#     def __init__(self):
#         self.name = ""
#         self.url = ""
#         self.date_added = ""
#
#     def show(self):
#         str = self.name + "\n| " + str(self.date_added) + "\n\t" + self.url
#         print("\n=======================================")
#         print(str)
#
#     def flush(self):
#         self.name = ""
#         self.url = ""
#         self.date_added = ""

class MediumParser(HTMLParser):
    mdm = MediumBookmark()  # For Internal Use Only

    def __init__(self):
        HTMLParser.__init__(self)

        self.count = 0      # No. of Bookmark Objects Collected
        self.bookmarks = []

    # @Override
    def handle_starttag(self, tag, attrs):
        self.tag = tag          # Remembering details of HTML element
        self.attrs = attrs      # the Parser is currently inside of

        try:
            for attr in attrs:                                   # -| OPTIONAL LINES: Adds
                if(attr[0] == "class" and attr[1] == A_CLASS):   # -| Rigidness in Parsing
                    for a in attrs:
                        if(a[0] == "href"):
                            MediumParser.mdm.url = a[1]
        except: pass

    # @Override
    def handle_endtag(self, tag):
        if(tag == "li"):  # </li> marks the end of a Medium Bookmark in the HTML file
            MediumParser.mdm.source.append("Medium")   # TODO: REMOVE THIS HACK (Only This Line)
            self.bookmarks.append(copy.deepcopy(MediumParser.mdm))   # DEEPCOPY required
            self.count += 1                       # to append a separated entry into the
            MediumParser.mdm.flush()             # list, so refs aren't appended instead
        self.tag = ""   # = to stack pop, using var because it's simple here.

    # @Override
    def handle_data(self, data):
        if(self.tag == "a"):
            for attr in self.attrs:                               # -| OPTIONAL LINES: Adds
                if(attr[0] == "class" and attr[1] == A_CLASS):    # -| Rigidness in Parsing
                    MediumParser.mdm.name = data

        elif(self.tag == "time"):
            for attr in self.attrs:                                # -| OPTIONAL LINES: Adds
                if(attr[0] == "class" and attr[1] == TIME_CLASS):  # -| Rigidness in Parsing
                    MediumParser.mdm.date_added = timestamp_from_MediumDate(data)




# ██████  ██ ██████  ███████ ██      ██ ███    ██ ███████
# ██   ██ ██ ██   ██ ██      ██      ██ ████   ██ ██
# ██████  ██ ██████  █████   ██      ██ ██ ██  ██ █████
# ██      ██ ██      ██      ██      ██ ██  ██ ██ ██
# ██      ██ ██      ███████ ███████ ██ ██   ████ ███████

if __name__ == '__main__':
    parser = MediumParser()

    with codecs.open("Dump/Data/medium-export/bookmarks/bookmarks-0001.html", 'r', 'utf-8') as fin:
        str = fin.read()

    parser.feed(str)

    print("Objects Parsed: ", parser.count)
    for bookmark in parser.bookmarks:
        bookmark.show()
