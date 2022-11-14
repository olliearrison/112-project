from cmu_112_graphics import *
from coors import *

def loadColorSelect(app):
    app.colorImage = Image.open("color.png").convert("RGBA")
    app.colorImageAdjust = Image.open("color.png").convert("RGBA")
    app.blackValue = 0

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

    fillColor = '#181818'

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

    # sets each point on the brush to the correct value
    r = r.point(lambda i: min(max(i + app.blackValue,0),255))
    g = g.point(lambda i: min(max(i + app.blackValue,0),255))
    b = b.point(lambda i: min(max(i + app.blackValue,0),255))

    # merges the values to create a final brush stamp
    app.colorImageAdjust = Image.merge('RGBA', (r, g, b, a))

def drawColorSelectBackground(app, canvas):
    x1 = app.width//10*7
    y1 = app.height//15 * 1.5
    x2 = app.width//100*98
    y2 = app.height//5*3

    centerX = (x1 + x2)//2
    centerY = (y1 + y2)//2

    drawRoundedBoxBackground(app, canvas,app.width//10*1.3,app.height//5*2.5,centerX,centerY)

    canvas.create_image(centerX, centerY, 
    image=ImageTk.PhotoImage(app.colorImageAdjust))