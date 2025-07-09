from URL import URL
import time
import tkinter
WIDTH, HEIGHT = 800, 600


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
    def load(self, url, httpVersion = "1.1", browser = "Chrome"):
        body, view_source, _ = url.request(httpVersion, browser)
        text = lex(body, view_source)    
        for c in text:
            self.canvas.create_text(100, 100, text = c)

        

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