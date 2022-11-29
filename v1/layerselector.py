from cmu_112_graphics import *
from coors import *
from color import *
from layerblock import *

def loadLayerSelect(app):
    app.layertitle = Image.open("layer-assets/layertitle.png").convert("RGBA")
    app.layertitle = app.scaleImage(app.layertitle, 1/6)

    app.allLayerBlocks = []

    for layerI in range(len(app.allLayers)):
        layerBlock = LayerBlock(app.allLayers[layerI], True, False, layerI)
        layerBlock.init(app)
        app.allLayerBlocks.append(layerBlock)

    app.allLayerBlocks[0].selected = True
    

def response():
    print("hi")

def inCircle(app, x, y):
    x1 = app.width//10*7
    y1 = app.height//15 * 1.5
    x2 = app.width//100*98
    y2 = app.height//5*3

    centerX = (x1 + x2)//2
    centerY = (y1 + y2)//2

    r = 94
    if getDistance(centerX, centerY, x, y) <= r:
        adjustedX = x - centerX + r
        adjustedY = y - centerY + r
        app.colorCoor[0] = adjustedX - r
        app.colorCoor[1] = adjustedY - r
        return (adjustedX, adjustedY)
    else:
        return (None, None)

def getColor(app, event):
    x = event.x
    y = event.y
    adjustedX, adjustedY = inCircle(app, x, y)
    if (adjustedX != None):
        adjustX = adjustedX
        adjustY = adjustedY

        r,g,b,a = app.colorImageAdjust.getpixel((adjustX, adjustY))
        app.currentColor = (r,g,b)

def adjustBlack(app, amount):
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


def drawLayerSelectBackground(app, canvas):
    x1 = app.width//10*7
    y1 = app.height//15 * 1.5
    x2 = app.width//100*98
    y2 = app.height//5*3

    centerX = (x1 + x2)//2
    centerY = (y1 + y2)//2

    drawRoundedBoxBackground(app, canvas,app.width//10*1.3,app.height//5*2.5,centerX,centerY)
    for layerBlock in app.allLayerBlocks:
        layerBlock.drawLayerBlock(app,canvas)
    canvas.create_image(centerX//10*9.2, centerY//3*1.2, image= ImageTk.PhotoImage(app.layertitle))



