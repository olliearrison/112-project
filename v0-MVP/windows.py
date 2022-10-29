def drawWindows(app, canvas):
    drawTopWindow(app, canvas)
    drawSideBar(app, canvas)
    #drawButton(app, canvas, app.width - 150, app.height - 40, app.height//15)
    #drawButton(app, canvas, app.width, app.height, app.height//15)

def drawTopWindow(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height//15,
    fill = '#181818', outline = '#181818')

def drawSideBar(app, canvas):
    sideBarMargin = app.height//5
    canvas.create_rectangle(0,sideBarMargin,app.height//15,
    app.height-sideBarMargin,
    fill = '#181818', outline = '#181818')

class Button(object):
    # x and y refer to the top left corner
    # response passes in the function that is
    # if the future, make the option for rectangular buttons
    def __init__(self, app, size, x, y, response):
        #self.image = image
        #self.activeImage = image
        self.app = app
        self.size = size
        self.x = x
        self.y = y
        self.response = response

    def checkClicked(self,x,y):
        print("hi")
        if True:
            print("wow this kinda works: ", x, y)
        x1 = self.x
        x2 = self.x + self.size
        y1 = self.y
        y2 = self.y + self.size

        if (x >= x1 and x <= x2) and (y >= y1 and y <= y2):
            print("Button do thingos")
            self.response(self.app)

    def clickButton():
        return 42

    def drawButton(self, app, canvas):
        canvas.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,
        fill = '#161212', outline = '#161212')

