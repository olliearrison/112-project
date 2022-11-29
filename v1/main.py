from cmu_112_graphics import *
import time
import windows
import button
import slider
import brush
import layer
from background import *
from coors import *
from colorselector import *
from layerselector import *
import math
from color import *

"""
To Do:
get local way of saving
get crop working better
make window/color select work the same way with mode
create gallery using modes
get x, y value from image
work on adding color history
set window to constant size
make zoom work again
get black slider working
triadic color scheme
get adjusted color for color selector text

Questions:
- making app responsive
- reverse color select: search through all pixel values
- create a small dictionary - if not there yet

- check for other x,y inputs????
- how to avoid circular inputs for layerblock, layerselect, and layer
- how to handle scroll/too many layers: indicies

circular buffers
try some kind of division for colors
appStopped
time entire duration, take difference and add it 


pillow docs: https://pillow.readthedocs.io/en/stable/reference/Image.html

- test out layer mask (maybe create a test subclass to handle new brush
ideas)
- cache images

def composite(image1, image2, mask):

    Create composite image by blending images using a transparency mask.

    :param image1: The first image.
    :param image2: The second image.  Must have the same mode and
       size as the first image.
    :param mask: A mask image.  This image can have mode
       "1", "L", or "RGBA", and must have the same size as the
       other two images.

- eraser functionality
- make everything on the app scale when the window size is changed 
(use similar strategy as for robot)
- make pixel distance reletive to size of brush (smaller brushes don't look 
good @ 10 pixels)
- create layer class
- make layer naming consistant
- add rotation (pillow)
- non square/word based buttons (for gallery and on option pages)
- create window to create and delete layers

must be after MVP:
- undo, redo
- numpy
- compile into c python
- transparent blur windows (brushes, erasers, layers, colors)
- threading: multi threading
- pygame maybe

"""
def redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, text='This demos a ModalApp!',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 200, text='This is a modal splash screen!',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 250, text='Press any key for the game!',
                       font=font, fill='black')

def keyPressed(app, event):
    app.mode = 'drawMode'
    drawMode_appStarted(app)

def drawMode_appStarted(app):
    app.startTime = None
    app.margin = 5
    app.imageWidth, app.imageHeight = 400, 450

    app.reload = 0

    app.color = (70, 10, 90)
    app.eraser = (255,255,255)
    app.currentColor = app.color
    app.colorWindow = False
    app.layerWindow = False

    app.brushSize = 7
    app.scaleFactor = 1
    app.rotation = 0
    app.toBeDrawn = set()
    app.timerDelay = 50
    app.drag = False

    # define primary image in RGBA (includes opacity 0-255)
    background = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
    (255,255,255,255))
    app.backgroundLayer = layer.Layer(background, 1, "normal", 1, True, None, None)
    app.scaleBackgroundLayer = app.backgroundLayer.zoomReturnLayer(app)

    brushImage = Image.open("airbrush.png").convert("RGBA")
    app.airbrush = brush.Brush(brushImage, app.currentColor, app.height/2 - 70, 255, 80, 
                None, None, False)

    # holds the most recent x and y position on the canvas
    app.oldX = None
    app.oldY = None

    # defines the user mode: pen, blend, eraser, layer, colorselect, etc
    app.userMode = "pen"

    # creates the buttons
    app.mainButtons = createButtons(app)

    app.barMoving = False
    app.barCurrent = app.height/2 -70 - 50 + 35


    app.sizeSlider = slider.Slider(app, 10, 55, 5, 20, app.height/2 - 100, response, 
                    False, app.height/2 - 70)

    app.opacitySlider = slider.Slider(app, 10, 50, 5, 20,app.height/2 + 55, response, 
                    True, 285)

    initSize = 60
    initOpacity = 200
    app.opacitySlider.setAmount(initOpacity)
    app.sizeSlider.setAmount(initSize)
    app.airbrush.opacity = initOpacity
    app.airbrush.createResultingBrush(app, app.currentColor, initSize)

    app.mainSliders = []
    app.mainSliders.extend([app.opacitySlider, app.sizeSlider])

    createLayers(app)
    loadColorSelect(app)
    loadLayerSelect(app)

    app.layerSelectedI = 0

    app.testing = False
    if app.testing:
        background = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
        (255,200,255,255))
        app.backgroundLayer = layer.Layer(background, 1, "normal", 1, True, None, None)
        app.scaleBackgroundLayer = app.backgroundLayer.zoomReturnLayer(app)


        app.testBrush = brush.Testing(brushImage, app.currentColor, app.height/2 - 70, 255, 80, 
                None, None, False)
        app.testBrush.opacity = initOpacity
        app.testBrush.createResultingBrush(app, app.currentColor, initSize)

def createLayers(app):
    app.allLayers = []
    app.allScaleLayers = []

    for i in range(3):
        # new layer
        paintImage = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
        (255,255,255,0))
        paintLayer = layer.Layer(paintImage, 1, "normal", 1, False, None, None)
        scalePaintLayer = paintLayer.zoomReturnLayer(app)

        app.allLayers.append(paintLayer)
        app.allScaleLayers.append(scalePaintLayer)

def drawMode_timerFired(app):
    for coor in app.toBeDrawn:
        if app.testing:
            app.testBrush.addDot(coor[0], coor[1])
        else:
            app.airbrush.addDot(coor[0],coor[1])
    app.toBeDrawn = set()
    app.scalePaintLayer = app.allLayers[app.layerSelectedI].zoomReturnLayer(app)

# retreives the buttons, scales them, and returns them in a tuple
def getImage(name, app):
    imageTitle = "buttons/" + name + ".png"
    imageTitleActive = "buttons/" + name + "-active" + ".png"

    image = app.loadImage(imageTitle)
    image = app.scaleImage(image, 1/10)

    imageActive = app.loadImage(imageTitleActive)
    imageActive = app.scaleImage(imageActive, 1/10)
    return (image, imageActive)

# creates each of the main screen buttons
def createButtons(app):
    result = []
    cols = 20
    rowWidth = app.width//cols

    # opens tools
    toolImage = getImage("tool", app)
    tool = button.Button(app, 10, 2*rowWidth, 15, saveImage, False, toolImage, "tool")

    # opens full layer adjustments
    wandImage = getImage("wand", app)
    wand = button.Button(app, 10, 3*rowWidth, 15, response, False, 
    wandImage, "wand")

    # allows user to select parts of the layer they are on
    selectImage = getImage("select", app)
    select = button.Button(app, 10, 4*rowWidth, 15, response, False, 
    selectImage, "select")

    # allows the user to adjust the selection
    adjustImage = getImage("adjust", app)
    adjust = button.Button(app, 10, 5*rowWidth, 15, response, False, 
    adjustImage, "adjust")

    # either switches to the selected pen or opens a window to choose a pen
    penImage = getImage("pen", app)
    pen = button.Button(app, 10, 15*rowWidth, 15, penMode, True, 
    penImage, "pen")

    # either switches to the selected blender or opens a window to choose a
    # blender
    blendImage = getImage("blend", app)
    blend = button.Button(app, 10, 16*rowWidth, 15, response, False, 
    blendImage, "blend")

    # either switches to the selected eraser or opens a window to choose 
    # a eraser
    eraserImage = getImage("eraser", app)
    eraser = button.Button(app, 10, 17*rowWidth, 15, eraserMode, False, 
    eraserImage, "eraser")

    # opens layers
    layersImage = getImage("layers", app)
    layers = button.Button(app, 10, 18*rowWidth, 15, toggleLayerWindow, False, 
    layersImage, "layers")

    colorImage = getImage("blank", app)
    color = button.Button(app, 10, 19*rowWidth, 15, toggleColorWindow, False, 
    colorImage, "color")

    # allows the user to select a color from the canvas
    selectorImage = getImage("selector", app)
    selector = button.Button(app, 10, 15, app.height//2 - 25, colorSelectMode, False, 
    selectorImage, "selector")

    # allows the user to go forward if they just went backward
    forwardImage = getImage("forward", app)
    forward = button.Button(app, 10, 15, 10 + 7*app.height//9 - rowWidth//2, response, False, 
    forwardImage, "forward")

    # allows the user to go backwards
    backwardImage = getImage("backward", app)
    backward = button.Button(app, 10, 15, 20 + int(7*app.height//9 - rowWidth*1.25), 
    response, False, 
    backwardImage, "backward")

    # adds each of the buttons and returns them
    result.extend([tool, wand, select, adjust, pen, blend, eraser, layers, color,
                selector, forward, backward])
    return result

def toggleColorWindow(app):
    app.colorWindow = not(app.colorWindow)
    if app.colorWindow:
        app.layerWindow = False

def toggleLayerWindow(app):
    app.layerWindow = not(app.layerWindow)
    if app.layerWindow:
        for layerI in range(len(app.allLayers)):
            app.allLayerBlocks[layerI].updateImage(app.allLayers[layerI], app)
        app.colorWindow = False


# saves an image with a white background
def saveImage(app):
    flatImage = None
    for layer in app.allLayers:
        if flatImage == None:
            flatImage = Image.alpha_composite(app.backgroundLayer.image, layer.image)
        else:
            flatImage = Image.alpha_composite(flatImage, layer.image)
    flatImage.save("result/flatImage.png","PNG")

# draws each of the main buttons
def drawButtons(app, canvas):
    for button in app.mainButtons:
        button.drawButton(app, canvas)

# changes the user mode
# if one button is selected, it will turn all other buttons off
def changeMode(app, mode):
    app.userMode = mode
    for button in app.mainButtons:
        if button.mode == mode:
            button.resetAllElse(app)
            return True
    # if none are found (never should happen), 
    print("no button found")
    return False

# checks whether any of the buttons or sliders have have been clicked
def checkButtons(app, x, y):
    for button in app.mainButtons:
        # once a button has been clicked, stop looking
        if button.checkClicked(x,y, app):
            button.resetAllElse(app)
            return True
    for slider in app.mainSliders:
        if not(slider.checkClicked(x,y,app)):
            slider.isActive = False
        else:
            return True
    return False

def checkLayerBlocks(app, x, y):
    for layerBlockI in range(len(app.allLayerBlocks)):
        if not(app.allLayerBlocks[layerBlockI].visibilityButton != None and 
        app.allLayerBlocks[layerBlockI].visibilityButton.checkClicked(x,y,app)):
            if app.allLayerBlocks[layerBlockI].checkClicked(x,y,app):
                app.allLayerBlocks[layerBlockI].resetAllElse(app)
                app.layerSelectedI = layerBlockI
                return True

# filler response function
def response(app):
    print("response has been called")

# navigate options with keys
def drawMode_keyPressed(app, event):
    if event.key == "w":
        # adjust the scale factor
        app.scaleFactor = round(app.scaleFactor + .1, 1)
        # scale the results image (but not the actual image)
        #app.scalePaintLayer = app.paintLayer.zoomReturnLayer(app)
        # scale the results background (but not the actual image)
        app.scaleBackgroundLayer = app.backgroundLayer.zoomReturnLayer(app)
    elif event.key == "s":
        # adjust the scale factor
        app.scaleFactor = round(app.scaleFactor - .1, 1)
        # scale the results image (but not the actual image)
        #app.scalePaintLayer = app.paintLayer.zoomReturnLayer(app)
        # scale the results background (but not the actual image)
        app.scaleBackgroundLayer = app.backgroundLayer.zoomReturnLayer(app)
    elif event.key == "a":
        adjustBlack(app, 10)
        #getValues(app)
    elif event.key == "d":
        adjustBlack(app, -10)

# select a color
def colorSelectMode(app):
    app.userMode = "colorselect"
    print("color select")

# change to penMode
def penMode(app):
    app.userMode = "pen"
    app.currentColor = app.color
    if app.testing:
        app.testBrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
        print("pen mode")
    else:
        app.airbrush.createResultingBrush(app, app.currentColor, app.airbrush.size)

# change to eraserMode
def eraserMode(app):
    app.userMode = "eraser"
    app.currentColor = app.eraser
    if app.testing:
        app.testBrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
    else:
        app.airbrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
    print("eraser mode")

def changeToWhite(app, input, newR = 255,newG = 255,newB = 255):
    altered = input.convert("RGBA")
    app.brush = Image.open("airbrush.png").convert("RGBA")
    r,g,b,a = app.brush.split()
    r = r.point(lambda i: (i+1) * newR)
    g = g.point(lambda i: (i + 1) * newG)
    b = b.point(lambda i: (i+1) * newB)
    altered = Image.merge('RGBA', (r, g, b, a))
    return altered.convert("png")

def drawMode_mousePressed(app, event):
    if app.layerWindow:
        checkLayerBlocks(app, event.x, event.y)
    if (app.colorWindow and inCircle(app, event.x, event.y)[0] != None):
        getColor(app, event)
        
        if app.testing:
            app.testBrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
        else:
            app.airbrush.createResultingBrush(app, app.currentColor, app.airbrush.size)

# when the mouse is released
def drawMode_mouseReleased(app, event):
    
    # reset the x and y mouse values
    index = 0
    if (app.drag):
        if app.testing:
            app.testBrush.afterBrushStroke(app, app.allLayers[app.layerSelectedI])
        else:
            app.airbrush.afterBrushStroke(app, app.allLayers[app.layerSelectedI])
        app.drag = False
    else:
        app.drag = False
        (x, y) = event.x, event.y

        # check the buttons, and if they haven't been pressed
        if not(checkButtons(app, x, y)):
            # get the coordinates within the image
            coors = insideImage(app,x,y)
            # if the coordinates are in the image
            if (coors != None):
                if (app.userMode == "colorselect"):

                    
                    r,g,b,a = app.allLayers[app.layerSelectedI].image.getpixel((coors[0], coors[1]))
                    app.currentColor = (r,g,b)
                    app.opacitySlider.setAmount(a)
                    app.airbrush.opacity = a
                    app.airbrush.color = app.currentColor
                    changeMode(app, "pen")
                    if app.testing:
                        app.testBrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
                    else:
                        app.airbrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
                else:
                
                    if app.testing:

                        imageX, imageY = coors[0], coors[1]
                        # draw pixels based on that
                        app.testBrush.brushClick(imageX ,imageY, app.allLayers[app.layerSelectedI], app)
                    else:
                        imageX, imageY = coors[0], coors[1]
                        # draw pixels based on that
                        app.airbrush.brushClick(imageX ,imageY, app.allLayers[app.layerSelectedI], app)

# when the mouse is dragged
def drawMode_mouseDragged(app, event):
    (x, y) = event.x, event.y

    app.colorWindow = False
    app.layerWindow = False

    # check if the opacity or slide slider has been clicked
    if (app.opacitySlider.checkClicked(x, y, app)):
        if app.testing:
            app.testBrush.opacity = app.opacitySlider.dragSlider(app, event)
        else:
            app.airbrush.opacity = app.opacitySlider.dragSlider(app, event)
    elif (app.sizeSlider.checkClicked(x, y, app)):
        if app.testing:
            app.testBrush.size = app.sizeSlider.dragSlider(app,event)
            app.testBrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
        else:
            app.airbrush.size = app.sizeSlider.dragSlider(app,event)
            app.airbrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
    else:
        # find the value inside the 
        imageX, imageY = insideImage(app,x,y)
        if (coorsWork(app, imageX, imageY)):
            app.drag = True
            if app.testing:
                app.testBrush.duringBrushStroke(app, imageX, imageY)
            else:
                app.airbrush.duringBrushStroke(app, imageX, imageY)

def drawMode_redrawAll(app, canvas):
    # draw the background
    drawBackground(app, canvas)

    # display the white background
    centerX = app.width//2
    centerY = app.height//2
    
    canvas.create_image(centerX, centerY, image=app.backgroundLayer.zoomReturnLayer(app))

    
    # display the user image
    for layerI in range(len(app.allLayers)-1, -1,-1):
        if app.allLayerBlocks[layerI].visible:
            canvas.create_image(centerX, centerY, image= app.allLayers[layerI].zoomReturnLayer(app))
            if layerI == app.layerSelectedI:
                if (app.airbrush.active or (app.testing and app.testBrush.active)):
                    if app.testing:
                        currentStroke = app.testBrush.getCurrentStroke()
                        currentStroke = app.scaleImage(currentStroke, app.scaleFactor)
                        canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(currentStroke))
                    else:
                        currentStroke = app.airbrush.getCurrentStroke()
                        currentStroke = app.scaleImage(currentStroke, app.scaleFactor)
                        canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(currentStroke))


    # draw the windows
    windows.drawWindows(app, canvas)

    # draw the buttons
    drawButtons(app, canvas)

    # create the current brush color display
    rowWidth = app.width//20
    x = 19*rowWidth
    y = 18
    radius = 10
    r,g,b = app.currentColor
    color = rgbaString(r, g, b)
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
    fill = color, outline = color)

    # draw the sliders
    app.opacitySlider.drawSlider(app, canvas)
    app.sizeSlider.drawSlider(app, canvas)
    
    if app.colorWindow:
        drawColorSelectBackground(app, canvas)
    if app.layerWindow:
        drawLayerSelectBackground(app, canvas)

# remember to remove mvcCheck
runApp(width=800, height=550)