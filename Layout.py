HSTEP, VSTEP = 13, 28
LINEBREAK = 26
import tkinter
import tkinter.font
from Text import Text
from Element import Element
FONTS = {}
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
         
class Layout:
    def __init__(self, tokens, width):
        self.width = width
        self.display_list = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.line = []
        self.size = 12
        self.weight = "normal"
        self.style = "roman"
        self.recurse(tokens)
        self.flush()

    def open_tag(self, tag):
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        elif tag == "br":
            self.flush()
    
    def word(self, word):
        font = get_font(self.size, self.weight, self.style)
        w = font.measure(word)
        if self.cursor_x + w >= self.width - HSTEP - 20:
                self.flush()  
        if word == "\n":
            self.cursor_x = HSTEP
            self.cursor_y += LINEBREAK
            return
        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + font.measure(" ")

    def close_tag(self, tag):
        if tag == "/i":
            self.style = "roman"
        elif tag == "/b":
            self.weight = "normal"
        elif tag == "/small":
            self.size += 2
        elif tag == "/big":
            self.size -= 4
        elif tag == "/p":
            self.flush()
            self.cursor_y += VSTEP
    
    def flush(self):
        if not self.line: return
        metrics = [font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = HSTEP
        self.line = []
    
    def recurse(self, tree):
        if isinstance(tree, Text):
            for word in tree.text.split():
                self.word(word)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close_tag(tree.tag)