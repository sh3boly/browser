from Text import Text
from Element import Element
class HTMLParser:
    HEAD_TAGS = [
        "base", "basefont", "bgsound", "noscript",
        "link", "meta", "title", "style", "script",
        ]
    SELF_CLOSING_TAGS = [
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
        ]
    def __init__(self, body, view_source):
        self.body = body
        self.unfinished = []
        self.view_source = view_source
        
        

    def get_attributes(self, text):
        parts = text.split()
        tag = parts[0].casefold()
        attributes = {}
        for attrpair in parts[1:]:
            if "=" in attrpair:
                key, value = attrpair.split('=', 1)
                if len(value) > 2 and value[0] in ["'", "\""]:
                    value = value[1:-1]
                attributes[key.casefold()] = value
            else:
                attributes[attrpair.casefold()] = ""
        return tag, attributes
    

    def add_text(self, text):

        if text.isspace(): 
            return
        self.implicit_tags(None)
        parent = self.unfinished[-1]
        node = Text(text, parent)
        parent.children.append(node)


    def add_tag(self, tag):
        tag, attributes = self.get_attributes(tag)
        print(attributes)
        if tag.startswith("1"): return
        self.implicit_tags(tag)
        if tag.startswith("/"):
            if len(self.unfinished) == 1: return
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        elif tag in self.SELF_CLOSING_TAGS:
            parent = self.unfinished[-1]
            node = Element(tag, parent, attributes)
            parent.children.append(node)
        else:
            parent = self.unfinished[-1] if self.unfinished else None
            node = Element(tag, parent, attributes)
            self.unfinished.append(node)        
    def finish(self):
        if not self.unfinished:
            self.implicit_tags(None)
        while len(self.unfinished) > 1:
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        return self.unfinished.pop()
    def implicit_tags(self, tag):
        while True:
            open_tags = [node.tag for node in self.unfinished]
            if open_tags == [] and tag != "html":
                self.add_tag("html")
            elif open_tags == ["html"] and tag not in ["body", "head", "/html"]:
                if tag in self.HEAD_TAGS:
                    self.add_tag("head")
                else:
                    self.add_tag("body")
            elif open_tags == ["html", "head"] and tag not in ["/head"] + self.HEAD_TAGS:
                self.add_tag("/head")
            else:
                break

    def parse(self):
        text = ""
        in_tag = False
        i = 0
        if self.view_source:
            text = self.body
            return text
        print(self.body)
        while i < len(self.body):
            c = self.body[i]
            if self.body[i:i+4] == "&lt;":
                text += "<"
                i += 3
            elif self.body[i:i+4] == "&gt;":
                text += ">"
                i += 3
            elif c == "<":
                in_tag = True
                if text: self.add_text(text)
                text = ""
            elif c == ">":
                in_tag = False
                self.add_tag(text)
                text = ""
            else:
                if text == "Chris Harrelso":
                    print("Test")
                text += c
            i += 1
        if not in_tag and text:
            self.add_text(text)
        return self.finish()
