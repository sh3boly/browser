from URL import URL
from Text import Text
from Tag import Tag
from scrollbar import ScrollBar
from Layout import Layout
import time
import tkinter
WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLLSTEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack(fill='both', expand=1)
        self.scrollbar = ScrollBar(WIDTH, HEIGHT, self.canvas)
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.mousewheel)
        self.window.bind("<Button-4>", self.mousewheel)
        self.window.bind("<Button-5>", self.mousewheel)
        self.window.bind("<Configure>", self.resize)
    
    def resize(self, e):
        global HEIGHT, WIDTH
        HEIGHT = e.height
        WIDTH = e.width
        self.display_list = Layout(self.tokens, WIDTH).display_list
        self.draw()

    def mousewheel(self, e):

        if e.delta >= 120 or e.num == 4:
            self.scroll -= SCROLLSTEP
            if self.scroll < 0:
                self.scroll = 0
            self.draw()
        if e.delta <= -120 or e.num == 5:
            if self.scroll + SCROLLSTEP >= self.max_scroll:
                return
            self.scroll += SCROLLSTEP
            self.draw()


    def scrolldown(self, e):
        if self.scroll + SCROLLSTEP >= self.max_scroll:
            return
        self.scroll += SCROLLSTEP
        self.draw()
    def scrollup(self, e):
        self.scroll -= SCROLLSTEP
        if self.scroll < 0:
            self.scroll = 0
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        y_screen_end = float('inf')
        y_end = float('-inf')
        for x, y, c, f in self.display_list:
            if y > self.scroll + HEIGHT: 
                y_end = max(y_end, y)
                y_screen_end = min(y_screen_end, y)
                continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text = c, font=f)
        self.max_scroll = y_end + 50
        self.scrollbar.update(y_end = y_end, y_screen_end = y_screen_end, screen_height= HEIGHT, screen_width= WIDTH, canvas = self.canvas)

    def load(self, url, httpVersion = "1.1", browser = "Chrome"):
        body, view_source, _ = url.request(httpVersion, browser)
        tokens = lex(body, view_source)
        self.tokens = tokens
        self.display_list = Layout(tokens, WIDTH).display_list
        self.draw()
            

def lex(body, view_source):
    out = []
    buffer = ""
    in_tag = False
    i = 0
    if view_source:
        text = body
        return text
    while i < len(body):
        c = body[i]
        if body[i:i+4] == "&lt;":
            buffer += "<"
            i += 3
        elif body[i:i+4] == "&gt;":
            buffer += ">"
            i += 3
        elif c == "<":
            in_tag = True
            if buffer: out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        elif not in_tag:
            buffer += c
        i += 1
        if not in_tag and buffer:
            out.append(Text(buffer))
    return out



if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
    # import sys
    # if len(sys.argv) < 2:
    #     start_time = time.time()
    #     load(URL())
    #     first_time = time.time()
    #     load(URL())
    #     cached_time = time.time()

    # elif len(sys.argv) == 2:
    #     start_time = time.time()
    #     load(URL(sys.argv[1]))
    #     first_time = time.time()
    #     load(URL(sys.argv[1]))
    #     cached_time = time.time()


    # else:
    #     load(URL(sys.argv[1]), sys.argv[2], sys.argv[3])
    #     load(URL(sys.argv[1]))
        
    # print("Normal time: ", first_time - start_time)
    # print("Cached time: ", cached_time - first_time)