from xml.sax import ContentHandler

from model.entity import Book


class SaxHandler(ContentHandler):

    def __init__(self):
        super().__init__()
        self.books = []

    def startElement(self, name, attrs):
        if name == "book":
            self.books.append(Book(*attrs.values()))
