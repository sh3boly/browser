from tkinter import Canvas
SCROLLBAR_WIDTH = 15
SCROLLBAR_HEIGHT = 40
PADDING = 5
class ScrollBar:
    def __init__(self, screen_width, screen_height, canvas: Canvas):
        self.x0 = screen_width - SCROLLBAR_WIDTH - PADDING
        self.y0 = screen_height + PADDING
        self.x1 = screen_width - PADDING
        self.y1 = screen_height + SCROLLBAR_HEIGHT + PADDING
        print("HERE")
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, tags="scrollbar")
    
    def update(self, canvas: Canvas, y_end, y_screen_end, screen_height, screen_width):
        canvas.delete("scrollbar")
        
        relative_height = min(screen_height - 2 * PADDING, (y_screen_end / y_end) * screen_height)
        
        self.y1 = relative_height + PADDING
        self.y0 = relative_height  - SCROLLBAR_HEIGHT + PADDING
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, tags="scrollbar")
    
                
        

