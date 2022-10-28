from cmu_112_graphics import *

def drawWindows(app, canvas):
    drawTopWindow(app, canvas)
    drawSideBar(app, canvas)
    drawButton(app, canvas, app.width - 150, app.height - 40, app.height//15)
    drawButton(app, canvas, app.width, app.height, app.height//15)

def drawTopWindow(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height//15,
    fill = '#181818', outline = '#181818')

def drawSideBar(app, canvas):
    sideBarMargin = app.height//5
    canvas.create_rectangle(0,sideBarMargin,app.height//15,
    app.height-sideBarMargin,
    fill = '#181818', outline = '#181818')

def drawButton(app, canvas, x, y, size):
    canvas.create_rectangle(x,y,x+size,y+size,
        fill = '#161212', outline = '#161212')

"""
class Button(object):
    # x and y refer to the top left corner
    # response passes in the function that is
    # if the future, make the option for rectangular buttons
    def __init__(self, size, x, y, response):
        #self.image = image
        #self.activeImage = image
        self.size = size
        self.x = x
        self.y = y
        self.response = response

    def clickButton():
        return 42

    def drawButton(self, app, canvas):
        canvas.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,
        fill = '#161212', outline = '#161212')
"""
