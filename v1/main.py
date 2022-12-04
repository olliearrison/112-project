from cmu_112_graphics import *
import windows
import button
import slider
import brush
import layer
from background import *
from coors import *
from colorselector import *
from layerselector import *
from color import *
from drawing import *
from gallerybackground import *

""" 
Questions:
- 

Bugs Found:
- can not be selecting a layer
- 'NoneType' object is not subscriptable app.colorCoor[1] = loc[0]


pillow docs: https://pillow.readthedocs.io/en/stable/reference/Image.html

"""
def appStarted(app):
    app.mode = 'galleryMode'
    adjustImage = getImage("plus", app, scale=2)
    app.addDrawing = button.Button(app, 30, app.width-80, 15, startDrawMode, False, 
    adjustImage, "adjust")
    galleryMode_appStarted(app)

def galleryMode_appStarted(app):
    app.allDrawings = []
    app.title = Image.open("gallery-assets/title.png").convert("RGBA")
    app.title = app.scaleImage(app.title, 1/3)

def startDrawMode(app):
    app.mode = 'drawMode'
    index = len(app.allDrawings)
    newDrawing = Drawing(app, index)
    app.allDrawings.append(newDrawing)
    drawMode_appStarted(app, newDrawing)

def galleryMode_redrawAll(app, canvas):
    drawGalleryBackground(app, canvas)

    for drawing in app.allDrawings:
        drawing.drawThumbnail(app, canvas)

    app.addDrawing.drawButton(app, canvas)
    canvas.create_image(100,30, image=ImageTk.PhotoImage(app.title))

def galleryMode_mousePressed(app, event):
    if app.addDrawing.checkClicked(event.x, event.y, app):
        return True
    for drawing in app.allDrawings:
        if (drawing.checkClicked(event.x, event.y, app)):
            drawMode_appStarted(app, app.allDrawings[drawing.index])
            app.mode = 'drawMode'
            return True

def galleryMode_keyPressed(app, event):
    app.mode = 'drawMode'
    index = len(app.allDrawings)
    newDrawing = Drawing(app, index)
    app.allDrawings.append(newDrawing)
    drawMode_appStarted(app, newDrawing)

def drawMode_appStarted(app, newDrawing):
    app.startTime = None
    app.margin = 5
    app.imageWidth, app.imageHeight = 400, 450

    app.reload = 0

    app.currentDrawing = newDrawing

    app.color = (70, 10, 90)
    app.eraser = (255,255,255)
    app.currentColor = app.color

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

    airbrushImage = Image.open("airbrush.png").convert("RGBA")
    app.airbrush = brush.Brush(airbrushImage, app.currentColor, 10, 255, 80, 
                None, None, False, (10, 80))

    pencilImage = Image.open("pencil.png").convert("RGBA")
    app.pencil = brush.Brush(pencilImage, app.currentColor, 10, 255, 80, 
                None, None, False, (3,10), jitter = True)

    # holds the most recent x and y position on the canvas
    app.oldX = None
    app.oldY = None

    # defines the user mode: pen, blend, eraser, layer, colorselect, etc
    app.userMode = "pencil"

    # creates the buttons
    app.mainButtons = createButtons(app)

    app.barMoving = False
    app.barCurrent = app.height/2 -70 - 50 + 35


    app.sizeSlider = slider.Slider(app, 10, 55, 5, 20, app.height/2 - 100, response, 
                    False, app.height/2 - 70)

    app.opacitySlider = slider.Slider(app, 10, 50, 5, 20,app.height/2 + 55, response, 
                    True, 285)

    initSize = 40
    initOpacity = 200

    app.opacitySlider.setAmount(initOpacity)
    app.sizeSlider.setAmount(initSize)

    app.airbrush.opacity = initOpacity
    app.pencil.opacity = initOpacity
    app.airbrush.createResultingBrush(app, app.currentColor, initSize)
    app.pencil.createResultingBrush(app, app.currentColor, initSize/4)

    app.mainSliders = []
    app.mainSliders.extend([app.opacitySlider, app.sizeSlider])

    createLayers(app)
    loadColorSelect(app)
    loadLayerSelect(app)

    app.layerSelectedI = 0


def createLayers(app):
    app.allLayers = []
    app.allScaleLayers = []


    if len(app.currentDrawing.layers) == 0:
        for i in range(3):
            # new layer
            paintImage = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
            (255,255,255,0))
            paintLayer = layer.Layer(paintImage, 1, "normal", 1, False, None, None)
            scalePaintLayer = paintLayer.zoomReturnLayer(app)

            app.allLayers.append(paintLayer)
            app.allScaleLayers.append(scalePaintLayer)
    else:
        app.allLayers = app.currentDrawing.layers
        for layerItem in app.allLayers:
            scalePaintLayer = layerItem.zoomReturnLayer(app)
            app.allScaleLayers.append(scalePaintLayer)

def drawMode_timerFired(app):
    for coor in app.toBeDrawn:
        if app.userMode == "airbrush":
            app.airbrush.addDot(coor[0],coor[1])
        elif app.userMode == "pencil":
            app.pencil.addDot(coor[0],coor[1])
    app.toBeDrawn = set()
    app.scalePaintLayer = app.allLayers[app.layerSelectedI].zoomReturnLayer(app)

# retreives the buttons, scales them, and returns them in a tuple
def getImage(name, app, scale=1):
    imageTitle = "button-assets/" + name + ".png"
    imageTitleActive = "button-assets/" + name + "-active" + ".png"

    image = app.loadImage(imageTitle)
    image = app.scaleImage(image, 1/10*scale)

    imageActive = app.loadImage(imageTitleActive)
    imageActive = app.scaleImage(imageActive, 1/10*scale)
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
    wand = button.Button(app, 10, 3*rowWidth, 15, gallery, False, 
    wandImage, "wand")

    # allows user to select parts of the layer they are on
    selectImage = getImage("select", app)
    select = button.Button(app, 10, 4*rowWidth, 15, response, False, 
    selectImage, "select")

    # allows the user to adjust the selection
    adjustImage = getImage("adjust", app)
    adjust = button.Button(app, 10, 5*rowWidth, 15, getPixelValueXY, False, 
    adjustImage, "adjust")

    # either switches to the selected pen or opens a window to choose a pen
    penImage = getImage("pen", app)
    pen = button.Button(app, 10, 15*rowWidth, 15, pencilMode, True, 
    penImage, "pencil")

    # either switches to the selected blender or opens a window to choose a
    # blender
    blendImage = getImage("blend", app)
    blend = button.Button(app, 10, 16*rowWidth, 15, airbrushMode, False, 
    blendImage, "airbrush")

    # either switches to the selected eraser or opens a window to choose 
    # a eraser
    eraserImage = getImage("eraser", app)
    eraser = button.Button(app, 10, 17*rowWidth, 15, eraserMode, False, 
    eraserImage, "eraser")

    # opens layers
    layersImage = getImage("layers", app)
    layers = button.Button(app, 10, 18*rowWidth, 15, layersMode, False, 
    layersImage, "layers")

    colorImage = getImage("blank", app)
    color = button.Button(app, 10, 19*rowWidth, 15, colorsMode, False, 
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

"""ef toggleColorWindow(app):
    app.colorWindow = not(app.colorWindow)
    if app.colorWindow:
        app.layerWindow = False

# shouldn't be called
# PROBABLY REMOVE
def toggleLayerWindow(app):
    app.layerWindow = not(app.layerWindow)
    if app.layerWindow:
        for layerI in range(len(app.allLayers)):
            app.allLayerBlocks[layerI].updateImage(app.allLayers[layerI], app)
        app.colorWindow = False
"""

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

# checks whether any of the buttons or sliders have have been clicked
def checkButtons(app, x, y):
    for button in app.mainButtons:
        # once a button has been clicked, stop looking
        if button.checkClicked(x,y, app):
            #changeMode(app, button.mode)
            #button.resetAllElse(app)
            return True
    for slider in app.mainSliders:
        if not(slider.checkClicked(x,y,app)):
            slider.isActive = False
        else:
            return True
    return False

def checkLayerBlocks(app, x, y):
    app.addLayer.checkClicked(x,y,app)
    for layerBlockI in range(len(app.allLayerBlocks)):
        if app.allLayerBlocks[layerBlockI].layerBlockImageScaled != None:
            if not(app.allLayerBlocks[layerBlockI].visibilityButton != None and
            app.allLayerBlocks[layerBlockI].visibilityButton.checkClicked(x,y,app)):
                if app.allLayerBlocks[layerBlockI].checkClicked(x,y,app):
                    app.allLayerBlocks[layerBlockI].resetAllElse(app)
                    app.layerSelectedI = layerBlockI
                    return True

# filler response function
def response(app):
    print("response has been called")

def gallery(app):
    flatImage = None
    for layer in app.allLayers:
        if flatImage == None:
            flatImage = Image.alpha_composite(app.backgroundLayer.image, layer.image)
        else:
            flatImage = Image.alpha_composite(flatImage, layer.image)

    app.currentDrawing.setThumbnail(flatImage, app)
    app.currentDrawing.setLayerBlocks(app.allLayerBlocks)
    app.currentDrawing.setLayers(app.allLayers)
    app.mode = 'galleryMode'

# navigate options with keys
def drawMode_keyPressed(app, event):
    if event.key == "BackSpace":
        if len(app.allLayers) > 1:
            app.allLayers.pop(app.layerSelectedI)
            app.allLayerBlocks.pop(app.layerSelectedI)
            app.layerSelectedI = max(0, app.layerSelectedI-1)
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

# changes the user mode
# if one button is selected, it will turn all other buttons off
def changeMode(app, mode):
    app.userMode = mode
    for button in app.mainButtons:
        if button.mode == mode:
            button.isActive = True
            print(button.mode, button.isActive)
        else:
            button.isActive = False

# select a color
def colorSelectMode(app):
    changeMode(app, "selector")

def colorsMode(app):
    if app.userMode == "colors":
        print("same mode, change to pencil")
        pencilMode(app)
    else:
        changeMode(app, "colors")

def layersMode(app):
    if app.userMode == "layers":
        print("same mode, change to pencil")
        pencilMode(app)
    else:
        changeMode(app, "layers")
        for layerI in range(len(app.allLayers)):
            app.allLayerBlocks[layerI].updateImage(app.allLayers[layerI], app)

# change to penMode
def pencilMode(app):
    changeMode(app, "pencil")
    #app.currentColor = app.color

    app.opacitySlider.setAmount(app.pencil.opacity)
    app.sizeSlider.setAmount(app.pencil.size)
    app.pencil.createResultingBrush(app, app.currentColor, app.pencil.size)

# change to penMode
def airbrushMode(app):
    changeMode(app, "airbrush")
    #app.currentColor = app.color
    app.opacitySlider.setAmount(app.airbrush.opacity)
    app.sizeSlider.setAmount(app.airbrush.size)
    app.airbrush.createResultingBrush(app, app.currentColor, app.airbrush.size)

# change to eraserMode
def eraserMode(app):
    changeMode(app, "eraser")
    app.currentColor = app.eraser

    if app.userMode == "airbrush":
        app.airbrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
    elif app.userMode == "pencil":
        app.pencil.createResultingBrush(app, app.currentColor, app.pencil.size)

    print("eraser mode")


def drawMode_mousePressed(app, event):
    if app.userMode == "layers":
        checkLayerBlocks(app, event.x, event.y)
    if (app.userMode == "colors" and inCircle(app, event.x, event.y)[0] != None):
        getColor(app, event)
        
        if app.userMode == "airbrush":
            app.airbrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
        elif app.userMode == "pencil":
            app.pencil.createResultingBrush(app, app.currentColor, app.pencil.size)

# when the mouse is released
def drawMode_mouseReleased(app, event):
    
    # reset the x and y mouse values
    index = 0
    if (app.drag):
        if app.userMode == "airbrush":
            app.airbrush.afterBrushStroke(app, app.allLayers[app.layerSelectedI])
        elif app.userMode == "pencil":
            app.pencil.afterBrushStroke(app, app.allLayers[app.layerSelectedI])
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
                if (app.userMode == "selector"):

                    r,g,b,a = app.allLayers[app.layerSelectedI].image.getpixel((coors[0], coors[1]))
                    app.currentColor = (r,g,b)
                    app.opacitySlider.setAmount(a)
                    app.airbrush.opacity = a
                    app.airbrush.color = app.currentColor

                    app.pencil.opacity = a
                    app.pencil.color = app.currentColor

                    if a == 0:
                        app.colorCoor[0] = 0
                        app.colorCoor[1] = 0
                    else:
                        loc = getPixelValueXY(app)
                        app.colorCoor[1] = loc[0]
                        app.colorCoor[0] = loc[1]
                        app.blackValue = loc[2]
                        updateImage(app)

                    changeMode(app, "pencil")
                    
                    if app.userMode == "airbrush":
                        app.airbrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
                    elif app.userMode == "pencil":
                        app.pencil.createResultingBrush(app, app.currentColor, app.pencil.size)
                else:
                    imageX, imageY = coors[0], coors[1]
                    if app.userMode == "airbrush":
                        app.airbrush.brushClick(imageX ,imageY, app.allLayers[app.layerSelectedI], app)
                    elif app.userMode == "pencil":
                        app.pencil.brushClick(imageX ,imageY, app.allLayers[app.layerSelectedI], app)
                    
# when the mouse is dragged
def drawMode_mouseDragged(app, event):
    if app.userMode == "selector":
        pencilMode(app)

    (x, y) = event.x, event.y

    # check if the opacity or slide slider has been clicked
    if (app.opacitySlider.checkClicked(x, y, app)):
        if app.userMode == "airbrush":
            app.airbrush.opacity = app.opacitySlider.dragSlider(app, event)
        elif app.userMode == "pencil":
            app.pencil.opacity = app.opacitySlider.dragSlider(app, event)
    elif (app.sizeSlider.checkClicked(x, y, app)):
        if app.userMode == "airbrush":
            app.airbrush.size = app.sizeSlider.dragSlider(app,event)
            app.airbrush.createResultingBrush(app, app.currentColor, app.airbrush.size)
        elif app.userMode == "pencil":
            app.pencil.size = app.sizeSlider.dragSlider(app,event)
            app.pencil.createResultingBrush(app, app.currentColor, app.pencil.size)
    else:
        # find the value inside the 
        imageX, imageY = insideImage(app,x,y)
        if (coorsWork(app, imageX, imageY)):
            app.drag = True
            if app.userMode == "airbrush":
                app.airbrush.duringBrushStroke(app, imageX, imageY)
            elif app.userMode == "pencil":
                app.pencil.duringBrushStroke(app, imageX, imageY)
            

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
                if app.userMode == "airbrush":
                    if app.airbrush.active:
                        currentStroke = app.airbrush.getCurrentStroke()
                        currentStroke = app.scaleImage(currentStroke, app.scaleFactor)
                        canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(currentStroke))
                elif app.userMode == "pencil":
                    if app.pencil.active:
                        currentStroke = app.pencil.getCurrentStroke()
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
    
    if app.userMode == "colors":
        drawColorSelectBackground(app, canvas)
    if app.userMode == "layers":
        drawLayerSelectBackground(app, canvas)

# remember to remove mvcCheck
runApp(width=800, height=550)