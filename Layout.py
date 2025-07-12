HSTEP, VSTEP = 13, 18
LINEBREAK = 26
import tkinter
import tkinter.font
from Text import Text
from Tag import Tag
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
        for tok in tokens:
            self.token(tok)
        self.flush()
    
    def word(self, word):
        font = tkinter.font.Font(
                            size=self.size,
                            weight=self.weight,
                            slant=self.style,
                        )
        w = font.measure(word)
        if word == "\n":
            self.cursor_x = HSTEP
            self.cursor_y += LINEBREAK
            return
        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + font.measure(" ")
        if self.cursor_x + w >= self.width - HSTEP - 20:
            self.flush()  

    def token(self, tok):
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
                self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
    