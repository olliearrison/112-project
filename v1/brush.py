from cmu_112_graphics import *
from coors import *
import random

class Brush:
    # self.opacity is 0-255
    def __init__(self, brushImage, color, size, opacity, pressureOpacity,
    resultingBrush, currentStroke, active, sizeRange, jitter = False, 
    smooth = False):
        self.brushImage = brushImage
        self.color = color
        self.size = size
        self.opacity = opacity
        self.pressureOpacity = pressureOpacity
        self.resultingBrush = resultingBrush
        self.currentStroke = currentStroke
        self.currentStrokeAdjust = None
        self.active = active
        self.sizeRange = sizeRange
        self.jitter = jitter

    # adjust the brush image so it can be directly used as a "stamp"
    def createResultingBrush(self, app, newColor, newSize):
        if app.userMode == "eraser":
            newColor = (255,255,255)
        self.size = newSize
        adjustedSize = self.sizeRange[0] + (self.sizeRange[1]-self.sizeRange[0])*self.size/100
        # adjust the brush
        self.resultingBrush = app.scaleImage(self.brushImage, adjustedSize/100)

        self.color = newColor
        newR, newG, newB = self.color[0],self.color[1],self.color[2]#,self.color[3]
        r,g,b,a = self.resultingBrush.split()


        newA = self.pressureOpacity/255
        # sets each point on the brush to the correct value
        # lambda from stackoverflow
        r = r.point(lambda i: (i + 1) * newR)
        g = g.point(lambda i: (i + 1) * newG)
        b = b.point(lambda i: (i + 1) * newB)
        a = a.point(lambda i: (i) * newA)

        # merges the values to create a final brush stamp
        self.resultingBrush = Image.merge('RGBA', (r, g, b, a))

    # refresh the currentStroke
    # set self to active
    def startBrushStroke(self, app):
        self.active = True
        self.currentStroke = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
        (255,255,255,0))

    # if doing a singular click, start brush, add dot, and add to canvas
    def brushClick(self,x ,y, layer, app):
        if not(self.active):
            self.startBrushStroke(app)
            self.addDot(x, y)
            self.afterBrushStroke(app, layer)

    # add dot with jitter if specified
    def addDot(self, x, y):
        resultingBrush = self.resultingBrush
        if self.jitter:
            resultingBrush = resultingBrush.rotate(random.randint(1,10))
        brushWidth, brushHeight = self.resultingBrush.size
        adjust = brushWidth //2
        self.currentStroke.alpha_composite(resultingBrush, dest = (x - adjust, y - adjust))

    # if the user has a last coordinate that is a part of the brush stroke
    # draw a lone, otherwise, do a dot
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

    # add a dot where the brush is
    def drawLine(self, app, x1, y1, x2, y2):
        self.addDot(x2, y2)
        self.efficientMidpoint(app, x1, y1, x2, y2)

    # choose the max distance, divide it, and add each individual dot to the set
    def efficientMidpoint(self, app, x1, y1, x2, y2):
        maxDistance = min(self.size/80,5) + 1
        distance = getDistance(x1, y1, x2, y2)
        numOfPoints = int(distance/maxDistance) + 1
        dx = (x2-x1)/numOfPoints
        dy = (y2-y1)/numOfPoints
        for i in range(1,numOfPoints):
            intX = int(x1 + dx*i)
            intY = int(y1 + dy*i)
            tup = (intX, intY)
            app.toBeDrawn.add(tup)

    # unfortunatly, this function is less efficient, so I had to get rid of this
    # recursivly fills the points between the last two coordinates with dots
    # until they are spaced less than 10 pixels apart
    def recursiveMidpoint(self, app, x1, y1, x2, y2):
        maxDistance = min(self.size/15,10) + 1
        if (getDistance(x1, y1, x2, y2) < maxDistance):
            return None
        newCoorX = (x1 + x2)//2
        newCoorY = (y1 + y2)//2
        tup = (newCoorX, newCoorY)
        app.toBeDrawn.add(tup)
        # add a point between half way and the second
        self.recursiveMidpoint(app, newCoorX, newCoorY, x2, y2)
        # add a point between the first and half way
        self.recursiveMidpoint(app, x1, y1, newCoorX, newCoorY)

    # get the current user input
    def getCurrentStroke(self):
        r,g,b,a = self.currentStroke.split()
        aChange = self.opacity
        newA = aChange/255

        # sets each point on the brush to the correct alpha value
        a = a.point(lambda i: (i) * newA)
        return Image.merge('RGBA', (r, g, b, a))

    # flatten the userinput onto the canvas
    def afterBrushStroke(self, app, layer):
        app.oldX = None
        app.oldY = None
        
        layer.addBrushStroke(app, self.getCurrentStroke())

        self.currentStroke = Image.new('RGBA', (app.imageWidth, app.imageHeight),
        (255,255,255,0))
        self.active = False
        