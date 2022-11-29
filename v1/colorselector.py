from cmu_112_graphics import *
from coors import *
from color import *

def loadColorSelect(app):
    app.colorImage = Image.open("color.png").convert("RGBA")
    app.colorImageAdjust = Image.open("color.png").convert("RGBA")
    app.blackValue = 200
    app.colorCoor = [0,0]

    #app.colorSlider = ThinSlider(app, app.width//10*7+20, app.height//2 + 30, .75, 
    #print("hi"), True, 0)


def inCircle(app, x, y):
    x1 = app.width//10*7
    y1 = app.height//15 * 1.5
    x2 = app.width//100*98
    y2 = app.height//5*3

    centerX = (x1 + x2)//2
    centerY = (y1 + y2)//2 #+ app.height//15 * 1.5

    r = 94
    if getDistance(centerX, centerY, x, y) <= r:
        print("inside")
        adjustedX = x - centerX + r
        adjustedY = y - centerY + r
        app.colorCoor[0] = adjustedX - r
        app.colorCoor[1] = adjustedY - r
        print(app.colorCoor)
        return (adjustedX, adjustedY)
    else:
        return (None, None)

def getColor(app, event):
    x = event.x
    y = event.y
    adjustedX, adjustedY = inCircle(app, x, y)
    if (adjustedX != None):
        print(adjustedX, adjustedY)
        adjustX = adjustedX
        adjustY = adjustedY

        r,g,b,a = app.colorImageAdjust.getpixel((adjustX, adjustY))
        app.currentColor = (r,g,b)
        print(app.currentColor)

def adjustBlack(app, amount):
    print(amount)
    app.blackValue += amount
    updateImage(app)

# code taken from what I wrote during Hack112
def drawRoundedBoxBackground(app, canvas,xSize,ySize,xCenter, yCenter):
    r = min(app.height, app.width)/80

    w, h = xCenter, yCenter
    xDif = xSize
    yDif = ySize//2

    fillColor = '#232323'

    # rounded outline
    canvas.create_oval(w-r -xDif, h-r-yDif,
    w+r-xDif, h+r-yDif, fill = fillColor, outline = fillColor)
    canvas.create_oval(w-r-xDif, h-r+yDif,
    w+r-xDif, h+r+yDif, fill = fillColor, outline = fillColor)
    canvas.create_oval(w-r+xDif, h-r-yDif,
    w+r+xDif, h+r-yDif, fill = fillColor, outline = fillColor)
    canvas.create_oval(w-r+xDif, h-r+yDif,
    w+r+xDif, h+r+yDif, fill = fillColor, outline = fillColor)

    # grey fill
    canvas.create_rectangle(w-xDif-r,h-yDif,
    w+xDif+r,h+yDif, fill= fillColor, outline = fillColor)
    canvas.create_rectangle(w-xDif,h-yDif-r,
    w+xDif,h+yDif+r, fill= fillColor, outline = fillColor)

    # verticle outlines
    canvas.create_line(w-xDif-r,h-yDif,
    w-xDif-r,h+yDif, fill = fillColor)
    canvas.create_line(w+xDif+r,h-yDif,
    w+xDif+r,h+yDif, fill = fillColor)

    # horizontal outlines
    canvas.create_line(w-xDif,h-yDif-r,
    w+xDif,h-yDif-r, fill = fillColor)
    canvas.create_line(w-xDif,h+yDif+r,
    w+xDif,h+yDif+r, fill = fillColor)

def updateImage(app):
    r,g,b,a = app.colorImage.split()

    const = (app.blackValue)/255
    
    # sets each point on the brush to the correct value
    r = r.point(lambda i: min(max(i * const,0),255))
    g = g.point(lambda i: min(max(i * const,0),255))
    b = b.point(lambda i: min(max(i * const,0),255))

    # merges the values to create a final brush stamp
    app.colorImageAdjust = Image.merge('RGBA', (r, g, b, a))

def drawColorSelectBackground(app, canvas):
    x1 = app.width//10*7
    y1 = app.height//15 * 1.5
    x2 = app.width//100*98
    y2 = app.height//5*3

    centerX = (x1 + x2)//2
    centerY = (y1 + y2)//2
    r = 5

    drawRoundedBoxBackground(app, canvas,app.width//10*1.3,app.height//5*2.5,centerX,centerY)

    canvas.create_image(centerX, centerY, 
    image=ImageTk.PhotoImage(app.colorImageAdjust))
    ccenterX = centerX + app.colorCoor[0]
    ccenterY = centerY + app.colorCoor[1]
    canvas.create_oval(ccenterX-r,ccenterY-r,ccenterX+r,ccenterY+r, outline = "white")

    #app.colorSlider.drawSlider(app, canvas)

class ThinSlider:
    # the amount variable should be changed to represent 0-255
    def __init__(self, app, xPosition, yPosition, slideSize, response, isActive, 
    amount):
        self.app = app
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.slideSize = slideSize
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

    # draw the slider
    def drawSlider(self, app, canvas):
        r = 8
        # draw the larger piece
        for i in range(255):
            color = rgbaString(i, i, i)
            xValue = self.xPosition + i*self.slideSize
            canvas.create_line(xValue, self.yPosition, 
                                xValue + self.slideSize, self.yPosition,
                                fill = color, width = 5)
        xValue = self.xPosition + self.slideSize * self.amount
        color = rgbaString(self.amount, self.amount, self.amount)
        canvas.create_oval(xValue - r, self.yPosition - r, 
                            xValue + r, self.yPosition + r, fill = color, 
                            outline = color)

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