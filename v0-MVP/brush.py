from cmu_112_graphics import *
from coors import *

class Brush:
    # self.opacity is 0-255
    def __init__(self, brushImage, color, size, opacity, pressureOpacity,
    resultingBrush, currentStroke, active):
        self.brushImage = brushImage
        self.color = color
        self.size = size
        self.opacity = opacity
        self.pressureOpacity = pressureOpacity
        self.resultingBrush = resultingBrush
        self.currentStroke = currentStroke
        self.active = active

    def createResultingBrush(self, app, newColor, newSize):
        self.size = newSize
        adjustedSize = (self.size/20 + 1)/4
        # adjust the brush
        self.resultingBrush = app.scaleImage(self.brushImage, adjustedSize)

        self.color = newColor
        newR, newG, newB = self.color[0],self.color[1],self.color[2]#,self.color[3]
        r,g,b,a = self.resultingBrush.split()


        newA = self.pressureOpacity/255
        # sets each point on the brush to the correct value
        r = r.point(lambda i: (i + 1) * newR)
        g = g.point(lambda i: (i + 1) * newG)
        b = b.point(lambda i: (i + 1) * newB)
        a = a.point(lambda i: (i) * newA)

        # merges the values to create a final brush stamp
        self.resultingBrush = Image.merge('RGBA', (r, g, b, a))

    def startBrushStroke(self, app):
        self.active = True
        self.currentStroke = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
        (255,255,255,0))

    def brushClick(self,x ,y, layer, app):
        if not(self.active):
            self.startBrushStroke(app)
            self.addDot(x, y)
            self.afterBrushStroke(app, layer)

    def addDot(self, x, y):
        brushWidth, brushHeight = self.resultingBrush.size
        adjust = brushWidth //2
        self.currentStroke.alpha_composite(self.resultingBrush, dest = (x - adjust, y - adjust))

    def duringBrushStroke(self, app, x, y):
        if not(self.active):
            self.startBrushStroke(app)

        # if the user just pressed down the mouse
        if (app.oldX == None) or (app.oldY == None):
        # draw a dot
            self.addDot(x, y)
        # otherwise
        else:
        # draw a line
            self.drawLine(app, app.oldX, app.oldY, x, y)
        
        app.oldX = x
        app.oldY = y

    def drawLine(self, app, x1, y1, x2, y2):
        self.addDot(x2, y2)
        self.recursiveMidpoint(app, x1, y1, x2, y2)

    # recursivly fills the points between the last two coordinates with dots
    # until they are spaced less than 10 pixels apart
    def recursiveMidpoint(self, app, x1, y1, x2, y2):
        if (getDistance(x1, y1, x2, y2) < 10):
            return None
        newCoorX = (x1 + x2)//2
        newCoorY = (y1 + y2)//2
        tup = (newCoorX, newCoorY)
        app.toBeDrawn.add(tup)
        # add a point between half way and the second
        self.recursiveMidpoint(app, newCoorX, newCoorY, x2, y2)
        # add a point between the first and half way
        self.recursiveMidpoint(app, x1, y1, newCoorX, newCoorY)

    def getCurrentStroke(self):
        r,g,b,a = self.currentStroke.split()
        aChange = self.opacity
        newA = aChange/255

        # sets each point on the brush to the correct alpha value
        a = a.point(lambda i: (i) * newA)
        #r = r.point(lambda i: (i + 1) * 1)
        #g = g.point(lambda i: (i + 1) * 1)
        #b = b.point(lambda i: (i + 1) * 1)

        # merges the values to create a final brush stamp
        
        return Image.merge('RGBA', (r, g, b, a))

    def afterBrushStroke(self, app, layer):
        app.oldX = None
        app.oldY = None

        app.image1 = Image.alpha_composite(app.image1, self.getCurrentStroke())
        self.active = False
        self.currentStroke = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
        (255,255,255,0))
        

