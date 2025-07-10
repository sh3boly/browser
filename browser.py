from URL import URL
import time
import tkinter
WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
LINEBREAK = 26
SCROLLSTEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.mousewheel)
        self.window.bind("<Button-4>", self.mousewheel)
        self.window.bind("<Button-5>", self.mousewheel)
    def mousewheel(self, e):
        if e.delta >= 120 or e.num == 4:
            self.scroll -= SCROLLSTEP
            if self.scroll < 0:
                self.scroll = 0
            self.draw()
        if e.delta <= -120 or e.num == 5:
            self.scroll += SCROLLSTEP
            self.draw()


    def scrolldown(self, e):
        self.scroll += SCROLLSTEP
        self.draw()
    def scrollup(self, e):
        self.scroll -= SCROLLSTEP
        if self.scroll < 0:
            self.scroll = 0
        self.draw()
    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text = c)

    def load(self, url, httpVersion = "1.1", browser = "Chrome"):
        body, view_source, _ = url.request(httpVersion, browser)
        text = lex(body, view_source)
        self.display_list = layout(text)
        self.draw()
            
        
def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        if c == "\n":
            cursor_x = HSTEP
            cursor_y += LINEBREAK
            continue
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list
def lex(body, view_source):
    in_tag = False
    i = 0
    text = ""
    if view_source:
        text = body
        return text
    while i < len(body):
        c = body[i]
        if body[i:i+4] == "&lt;":
            text += "<"
            i += 3
        elif body[i:i+4] == "&gt;":
            text += ">"
            i += 3
        elif c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c
        i += 1
    return text



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