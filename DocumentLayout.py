HSTEP, VSTEP = 13, 18
LINEBREAK = 26
from BlockLayout import BlockLayout
class DocumentLayout:
    def __init__(self, node, width):
        self.GLOBAL_WIDTH = width
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.node = node
        self.parent = None
        self.children = []
    def layout(self):
        child = BlockLayout(self.node, self, None)
        self.children.append(child)
        self.width = self.GLOBAL_WIDTH - (2 * HSTEP)
        self.x = HSTEP
        self.y = VSTEP
        child.layout()
        self.height = child.height

    def paint(self):
        return []
