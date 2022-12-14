from cmu_112_graphics import *
from coors import *
from color import *
from layerblock import *
import button
from layer import *

# add layer and create an associated layer block
def addLayer(app):
    if len(app.allLayers) <= 4:
        paintImage = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
                (255,255,255,0))
        paintLayer = Layer(paintImage, 1, "normal", 1, False, None, None)
        scalePaintLayer = paintLayer.zoomReturnLayer(app)

        app.allLayers.append(paintLayer)
        app.allScaleLayers.append(scalePaintLayer)

        layerBlock = LayerBlock(app.allLayers[len(app.allLayers)-1], True, False, len(app.allLayers)-1)
        layerBlock.init(app)
        app.allLayerBlocks.append(layerBlock)

# update layer select
def loadLayerSelect(app):
    image = app.loadImage("layer-assets/plus.png")
    image = app.scaleImage(image, 1/9)
    tup = (image,image)
    app.addLayer = button.Button(app, 10, app.width-60, 70, addLayer, False, 
    tup, "adjust")

    app.layertitle = Image.open("layer-assets/layertitle.png").convert("RGBA")
    app.layertitle = app.scaleImage(app.layertitle, 1/6)
    app.allLayerBlocks = []

    if len(app.currentDrawing.layerBlocks) == 0:

        for layerI in range(len(app.allLayers)):
            layerBlock = LayerBlock(app.allLayers[layerI], True, False, layerI)
            layerBlock.init(app)
            app.allLayerBlocks.append(layerBlock)
    else:
        app.allLayerBlocks = app.currentDrawing.layerBlocks

    app.allLayerBlocks[0].selected = True
    
def response():
    print("")

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

# draw background and layer blocks
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
    app.addLayer.drawButton(app, canvas)


