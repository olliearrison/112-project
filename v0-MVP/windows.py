from cmu_112_graphics import *

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
    def __init__(self, app, size, x, y, response, isActive, images, mode):
        self.app = app
        self.size = size
        self.x = x
        self.y = y
        self.response = response
        self.isActive = isActive
        self.images = images
        self.mode = mode

    def resetAllElse(self, app):
        self.isActive = True
        for button in app.mainButtons:
            if self != button:
                button.isActive = False

    def checkClicked(self,x,y,app):
        x1 = self.x
        x2 = self.x + self.size
        y1 = self.y
        y2 = self.y + self.size

        if (x >= x1 and x <= x2) and (y >= y1 and y <= y2):
            print("Button do thingos")
            self.response(self.app)
            self.isActive = True
            return True
        return False
            # self.image = self.getImage(app)

    def drawButton(self, app, canvas):
        #canvas.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,
        #fill = '#161212', outline = '#161212')
        if (self.isActive):
            canvas.create_image(self.x + self.size//2, self.y + self.size//2, 
            image=ImageTk.PhotoImage(self.images[1]))
        else:
            canvas.create_image(self.x + self.size//2, self.y + self.size//2, 
            image=ImageTk.PhotoImage(self.images[0]))


class Slider:
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

    def getPercent():
        print("return percent")

    def drawSlider(self, app, canvas):

        #
        canvas.create_rectangle(self.x - self.sizeX, self.y - self.sizeY,
                            self.x + self.sizeX, self.y + self.sizeY,
                            fill = "#252525", outline = "#252525")
        
        #
        canvas.create_rectangle(self.x - self.sizeX, self.amount - self.slideSize,
                            self.x + self.sizeX, self.amount + self.slideSize,
                            fill = "#868686", outline = "#868686")

    def dragSlider(self, app, event):

        bound1 = self.y - self.sizeY + self.slideSize
        bound2 = self.y + self.sizeY - self.slideSize

        if self.isActive:
            if (event.y < bound1):
                self.amount = bound1
            elif (event.y > bound2):
                self.amount = bound2
            else:
                self.amount = event.y


    # difference is a construct
    # comparitive difference
    # emergence of a conciousness comes from interactions within the brain
    # photo vs exist

        
    
