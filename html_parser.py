from html.parser import HTMLParser
import copy
import codecs

class MediumBookmark(object):
    def __init__(self):
        self.name = ""
        self.url = ""
        self.time = ""

    def show(self):
        str = self.name + "\n| " + self.time + "\n\t" + self.url
        print("\n=======================================")
        print(str)

    def flush(self):
        self.name = ""
        self.url = ""
        self.time = ""

class MediumParser(HTMLParser):
    mdm = MediumBookmark()  # For Internal Use Only

    def __init__(self):
        HTMLParser.__init__(self)

        self.count = 0
        self.bookmarks = []

    def handle_starttag(self, tag, attrs):
        self.tag = tag
        # print(tag)
        try:
            if(attrs[1][0] == "href"):
                MediumParser.mdm.url = attrs[1][1]
        except: pass


    def handle_endtag(self, tag):
        if(tag == "li"):
            self.bookmarks.append(copy.deepcopy(MediumParser.mdm))
            self.count += 1
            MediumParser.mdm.flush()
        self.tag = ""

    def handle_data(self, data):
        if(self.tag == "a"):
            MediumParser.mdm.name = data

        elif(self.tag == "time"):
            MediumParser.mdm.time = data


with codecs.open("medium-export/bookmarks/bookmarks-0001.html", 'r', 'utf-8') as fin:
    str = fin.read()

parser = MediumParser()
parser.feed(str)

print("Objects Parsed: ", parser.count)
for bookmarks in parser.bookmarks:
    bookmarks.show()
