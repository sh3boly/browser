from URL import URL
from Text import Text
from Element import Element
from scrollbar import ScrollBar
from DocumentLayout import DocumentLayout
from CSSParser import CSSParser
import time
import tkinter
from HTMLParser import HTMLParser
WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLLSTEP = 100
INHERITED_PROPERTIES = {
    "font-size": "16px",
    "font-style": "normal",
    "font-weight": "normal",
    "color": "black",
}
def cascade_priority(rule):
    selector, body = rule
    return selector.priority
def style(node, rules):
    node.style = {}
    for property, default_value in INHERITED_PROPERTIES.items():
        if node.parent:
            node.style[property] = node.parent.style[property]
        else:
            node.style[property] = default_value
    for selector, body in rules:
        if not selector.matches(node): continue
        for property, value in body.items():
            node.style[property] = value
    if isinstance(node, Element) and "style" in node.attributes:
        pairs = CSSParser(node.attributes["style"]).body()
        for property, value in pairs.items():
            node.style[property] = value
    if node.style["font-size"].endswith("%"):
        if node.parent:
            parent_font_size = node.parent.style["font-size"]
        else:
            parent_font_size = INHERITED_PROPERTIES["font-size"]
        node_pct = float(node.style["font-size"][:-1]) / 100
        parent_px = float(parent_font_size[:-2])
        node.style["font-size"] = str(node_pct * parent_px) + "px"
    for child in node.children:
        style(child, rules)

def paint_tree(layout_object, display_list):
    display_list.extend(layout_object.paint())

    for child in layout_object.children:
        paint_tree(child, display_list)
def tree_to_list(tree, list):
    list.append(tree)
    for child in tree.children:
        tree_to_list(child, list)
    return list

DEFAULT_STYLE_SHEET = CSSParser(open("browser.css").read()).parse()

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT,
            bg = "white"
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
        self.document = DocumentLayout(self.nodes, WIDTH)
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
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
        for cmd in self.display_list:
            if cmd.top > self.scroll + HEIGHT: 
                y_end = max(y_end, cmd.top)
                y_screen_end = min(y_screen_end, cmd.top)
                continue
            if cmd.bottom < self.scroll: continue
            cmd.execute(self.scroll, self.canvas)
        self.max_scroll = y_end + 50
        self.scrollbar.update(y_end = y_end, y_screen_end = y_screen_end, screen_height= HEIGHT, screen_width= WIDTH, canvas = self.canvas)

    def load(self, url, httpVersion = "1.1", browser = "Chrome"):
        body, view_source, _ = url.request(httpVersion, browser)
        self.nodes = HTMLParser(body, view_source).parse()
        rules = DEFAULT_STYLE_SHEET.copy()
        links = [node.attributes["href"]
                for node in tree_to_list(self.nodes, [])
                if isinstance(node, Element)
                and node.tag == "link"
                and node.attributes.get("rel") == "stylesheet"
                and "href" in node.attributes]
        for link in links:
            style_url = url.resolve(link)
            body = style_url.request()
            
            rules.extend(CSSParser(body).parse())
        style(self.nodes, sorted(rules, key=cascade_priority))
        self.document = DocumentLayout(self.nodes, WIDTH)
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
        self.draw()
            

def print_tree(node, indent = 0):
        print(" " * indent, node)
        for child in node.children:
            print_tree(child, indent + 2)

if __name__ == "__main__":
    import sys
    browser = Browser()
    if len(sys.argv) < 2:
        browser.load(url = URL())
    elif len(sys.argv) == 2:
        browser.load(url = URL(sys.argv[1]))
    else:
        browser.load(url = URL(sys.argv[1]), httpVersion= sys.argv[2], browser=sys.argv[3])
    tkinter.mainloop()
