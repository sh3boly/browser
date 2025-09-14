HSTEP, VSTEP = 13, 18
LINEBREAK = 26
from DrawRect import DrawRect
from DrawText import DrawText
from Text import Text
from Element import Element
import tkinter
import tkinter.font
from CSSParser import CSSParser

def get_font(size, weight, style):
    key = (size, weight, style)
    if key not in FONTS:
         font = tkinter.font.Font(
                            size=size,
                            weight=weight,
                            slant=style,
                        ) 
         label = tkinter.Label(font=font)
         FONTS[key] = (font, label)
    return FONTS[key][0]


BLOCK_ELEMENTS = [
    "html", "body", "article", "section", "nav", "aside",
    "h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "header",
    "footer", "address", "p", "hr", "pre", "blockquote",
    "ol", "ul", "menu", "li", "dl", "dt", "dd", "figure",
    "figcaption", "main", "div", "table", "form", "fieldset",
    "legend", "details", "summary"
]
FONTS = {}

class BlockLayout:
    def __init__(self, node, parent, previous):
        self.y = None
        self.height = None
        self.x = None
        self.width = None
        self.node = node
        self.parent = parent
        self.previous = previous
        self.children = []
        self.display_list = []
    
    def layout_mode(self):
        if isinstance(self.node, Text):
            return "inline"
        elif any([isinstance(child,Element) and 
                  child.tag in BLOCK_ELEMENTS
                  for child in self.node.children]):
            return "block"
        elif self.node.children:
            return "inline"
        else:
            return "block"
    
    def layout_intermediate(self):
        previous = None
        for child in self.node.children:
            next = BlockLayout(child, self, previous)
            self.children.append(next)
            previous = next
    
    def recurse(self, tree):
        if isinstance(tree, Text):
            for word in tree.text.split():
                self.word(tree, word)
        else:
            if tree.tag == "br":
                self.flush()
            for child in tree.children:
                self.recurse(child)
            if tree.tag in BLOCK_ELEMENTS:
                self.flush()
                self.cursor_y += VSTEP
    
    def layout(self):
        self.x = self.parent.x
        self.width = self.parent.width
        if self.previous:
            self.y = self.previous.y + self.previous.height
        else:
            self.y = self.parent.y
        mode = self.layout_mode()
        if mode == "block":
            self.layout_intermediate()
            for child in self.children:
                child.layout()
            self.height = sum([child.height for child in self.children])
        else:
            self.display_list = []
            self.cursor_x = 0
            self.cursor_y = 0
            self.line = []
            self.size = 12
            self.weight = "normal"
            self.style = "roman"
            self.recurse(self.node)
            self.flush()
            self.height = self.cursor_y

    def word(self, node, word):
        color = node.style["color"]
        weight = node.style["font-weight"]
        style = node.style["font-style"]
        if style == "normal": style ="roman"
        size = int(float(node.style["font-size"][:-2]) *.75)
        font = get_font(size, weight, style)
        w = font.measure(word)
        if self.cursor_x + w >= self.width - HSTEP - 20:
                self.flush()  
        if word == "\n":
            self.cursor_x = HSTEP
            self.cursor_y += LINEBREAK
            return
        self.line.append((self.cursor_x, word, font, color))
        self.cursor_x += w + font.measure(" ")


        
    
    def flush(self):
        if not self.line: return
        metrics = [font.metrics() for x, word, font, color in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for rel_x, word, font, color in self.line:
            x = self.x + rel_x
            y = self.y + baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font, color))
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = 0
        self.line = []

    def paint(self):
        cmds = []
        bgcolor = self.node.style.get("background-color", "transparent")
        
        if bgcolor != "transparent":
            x2, y2 = self.x + self.width, self.y + self.height
            rect = DrawRect(self.x, self.y, x2, y2, bgcolor)
            cmds.append(rect)

        if self.layout_mode() == "inline":
            for x, y, word, font, color in self.display_list:
                cmds.append(DrawText(x, y, word, font, color))
        
        return cmds

        
    
    