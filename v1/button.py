from cmu_112_graphics import *

class Button:
    # x and y refer to the top left corner
    # response passes in the function that is called when the button is 
    # pressed
    # if the future, make the option for rectangular buttons
    def __init__(self, app, size, x, y, response, isActive, images, mode):
        self.app = app
        self.size = size
        self.x = x
        self.y = y
        self.response = response
        self.isActive = isActive
        self.images = images
        self.mode = mode

    # check if it has been clicked
    def checkClicked(self,x,y,app):
        x1 = self.x - self.size
        x2 = self.x + self.size
        y1 = self.y - self.size
        y2 = self.y + self.size

        # if it has
        if (x >= x1 and x <= x2) and (y >= y1 and y <= y2):
            # do the response and set itself to active
            self.response(self.app)
            #self.isActive = True
            return True
        return False

    # draw the buttons using the image based on whether it is active
    def drawButton(self, app, canvas):
        if (self.isActive):
            canvas.create_image(self.x + self.size//2, self.y + self.size//2, 
            image=ImageTk.PhotoImage(self.images[1]))
        else:
            canvas.create_image(self.x + self.size//2, self.y + self.size//2, 
            image=ImageTk.PhotoImage(self.images[0]))

#class SizeButton(Button):
#    def __init__(self, sizeX, sizeY):
#
