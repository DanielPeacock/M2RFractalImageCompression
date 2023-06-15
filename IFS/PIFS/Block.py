class Block:
    def __init__(self, bot_left, width, height):
        self.bot_left = bot_left
        self.width = width
        self.height = height
     

    def contains(self, point):
        x, y = point[0], point[1]
        rect_x, rect_y = self.bot_left[0], self.bot_left[1]
        
        return not ((x < rect_x or x > (rect_x + self.width)) or (y < rect_y or y > (rect_y + self.height)))
        
