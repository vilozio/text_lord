import requests
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = True
        self.data = []

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'script' or tag == 'style':
            self.recording = False
        else:
            self.recording = True

    def handle_data(self, data):
        if self.recording and not data.isspace():
            self.data.append(data)


r = requests.get("http://money.cnn.com/2017/03/10/technology/elon-musk"
                 "-australia-energy/index.html?iid=INTL_SPC")

parser = MyHTMLParser()
parser.feed(r.text)
parser.close()

longest = parser.data[0]
for line in parser.data:
    if len(line) > len(longest):
        longest = line


f = open('news.txt', 'w')
[f.write(line + '\n') for line in parser.data]
f.close()
