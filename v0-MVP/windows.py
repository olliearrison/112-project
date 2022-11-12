from cmu_112_graphics import *

# draw the windows
def drawWindows(app, canvas):
    drawTopWindow(app, canvas)
    drawSideBar(app, canvas)

# draw the top
def drawTopWindow(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height//15,
    fill = '#181818', outline = '#181818')

# draw the side
def drawSideBar(app, canvas):
    sideBarMargin = app.height//5
    canvas.create_rectangle(0,sideBarMargin,app.height//15,
    app.height-sideBarMargin,
    fill = '#181818', outline = '#181818')


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

    # resets all other buttons
    def resetAllElse(self, app):
        self.isActive = True
        for button in app.mainButtons:
            if self != button:
                button.isActive = False

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
            self.isActive = True
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


class Slider:
    # the amount variable should be changed to represent 0-255
    def __init__(self, app, sizeX, sizeY, slideSize, x, y, response, isActive, 
    amount):
        self.app = app
        self.sizeX = sizeX # 10
        self.sizeY = sizeY # 60
        self.slideSize = slideSize
        self.x = x # 20
        self.y = y # app.height/2 - 90
        self.response = response
        self.isActive = isActive
        self.amount = amount

    # num is 0-255
    def setAmount(self, num):
        bound1 = self.y - self.sizeY + self.slideSize
        bound2 = self.y + self.sizeY - self.slideSize
        den = bound2 - bound1
        adjust = num/255
        self.amount = bound2 - (den*adjust)
        
    # get the percent location from the slider
    def getPercent(self):
        bound1 = self.y - self.sizeY + self.slideSize
        bound2 = self.y + self.sizeY - self.slideSize
        den = bound2 - bound1
        num = den - (self.amount - bound1)
        return num/den

    # draw the slider
    def drawSlider(self, app, canvas):

        # draw the larger piece
        canvas.create_rectangle(self.x - self.sizeX, self.y - self.sizeY,
                            self.x + self.sizeX, self.y + self.sizeY,
                            fill = "#252525", outline = "#252525")
        
        # draw the small, movable piece
        canvas.create_rectangle(self.x - self.sizeX, self.amount - self.slideSize,
                            self.x + self.sizeX, self.amount + self.slideSize,
                            fill = "#868686", outline = "#868686")

    # move the slider
    def dragSlider(self, app, event):

        # calculate the bound
        bound1 = self.y - self.sizeY + self.slideSize
        bound2 = self.y + self.sizeY - self.slideSize

        # if it is active, move the amount to the right place
        if self.isActive:
            if (event.y < bound1):
                self.amount = bound1
            elif (event.y > bound2):
                self.amount = bound2
            else:
                self.amount = event.y
        
        # return the most recent value
        lastValue = int(self.getPercent() * 255)
        return lastValue

    # check whether the slider has been clicked
    def checkClicked(self, x, y, app):
        x1 = self.x
        x2 = self.x + self.sizeX
        y1 = self.y - self.sizeY + self.slideSize
        y2 = self.y + self.sizeY - self.slideSize

        if (x >= x1 and x <= x2) and (y >= y1 and y <= y2):
            self.isActive = True
            return True
        return False

        
    
