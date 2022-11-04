from cmu_112_graphics import *
from windows import *
from background import *
from coors import *
import math

"""
pillow docs: https://pillow.readthedocs.io/en/stable/reference/Image.html

to do:
- make everything on the app scale when the window size is changed 
(use similar strategy as for robot)
- new brush size
- new brush opacity
- better code structure
- fix zoom
- add comments to everything

to do later:
- create brush class
- create layer class
- add rotation (pillow)
- non square/word based buttons (for gallery and on option pages)
- comment code
- organize code: no redundancies
- create window to create and delete layers

must be after MVC:
- undo, redo
- numpy
- compile into c python
- transparent blur windows (brushes, erasers, layers, colors)
- threading: multi threading 
- pygame maybe

lock it before
"""

def appStarted(app):
    app.margin = 5
    app.imageWidth, app.imageHeight = 400, 450
    bgColor = (255, 255, 255)
    app.currentBrush = (10, 20, 255, 255)
    app.brushSize = 7
    app.scaleFactor = 1
    app.rotation = 0

    # define primary image in RGBA (includes opacity 0-255)
    app.background1 = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
    (255,255,255,255))
    app.background2 = app.scaleImage(app.background1, app.scaleFactor)

    app.image1 = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
    (255,255,255,0))
    # scales image
    app.image2 = app.scaleImage(app.image1, app.scaleFactor)

    app.originBrush = Image.open("brush.png").convert("RGBA")
    app.originBrush = app.scaleImage(app.originBrush, 1/4)

    app.brush = Image.open("brush.png").convert("RGBA")
    app.brushColored = Image.open("brush.png").convert("RGBA")

    #app.brush = app.scaleImage(app.brush, 1/30)
    app.brushWidth, app.brushHeight = app.brush.size

    #app.brush.paste(app.brushL, app.brush)
    #app.brush = app.brush.convert("RGBA")


    # holds the most recent x and y position on the canvas
    app.oldX = None
    app.oldY = None

    # defines the user mode: pen, blend, eraser, layer, colorselect, etc
    app.userMode = "pen"

    # creates the buttons
    app.mainButtons = createButtons(app)

    app.barMoving = False
    app.barCurrent = app.height/2 -70 - 50 + 35


    app.sizeSlider = Slider(app, 10, 55, 5, 20,app.height/2 - 100, response, 
                    False, app.height/2 - 70)

    app.opacitySlider = Slider(app, 10, 50, 5, 20,app.height/2 + 55, response, 
                    True, 285)

    app.opacitySlider.setAmount(255)
    app.sizeSlider.setAmount(app.height/2 - 70)

    app.mainSliders = []
    app.mainSliders.extend([app.opacitySlider, app.sizeSlider])

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
    tool = Button(app, 10, 2*rowWidth, 15, saveImage, False, 
    toolImage, "tool")

    # opens full layer adjustments
    wandImage = getImage("wand", app)
    wand = Button(app, 10, 3*rowWidth, 15, response, False, 
    wandImage, "wand")

    # allows user to select parts of the layer they are on
    selectImage = getImage("select", app)
    select = Button(app, 10, 4*rowWidth, 15, response, False, 
    selectImage, "select")

    # allows the user to adjust the selection
    adjustImage = getImage("adjust", app)
    adjust = Button(app, 10, 5*rowWidth, 15, response, False, 
    adjustImage, "adjust")

    # either switches to the selected pen or opens a window to choose a pen
    penImage = getImage("pen", app)
    pen = Button(app, 10, 15*rowWidth, 15, penMode, False, 
    penImage, "pen")

    # either switches to the selected blender or opens a window to choose a
    # blender
    blendImage = getImage("blend", app)
    blend = Button(app, 10, 16*rowWidth, 15, response, False, 
    blendImage, "blend")

    # either switches to the selected eraser or opens a window to choose 
    # a eraser
    eraserImage = getImage("eraser", app)
    eraser = Button(app, 10, 17*rowWidth, 15, eraserMode, False, 
    eraserImage, "eraser")

    # opens layers
    layersImage = getImage("layers", app)
    layers = Button(app, 10, 18*rowWidth, 15, response, False, 
    layersImage, "layers")

    # allows the user to select a color from the canvas
    selectorImage = getImage("selector", app)
    selector = Button(app, 10, 15, app.height//2 - 25, colorSelectMode, False, 
    selectorImage, "selector")

    # allows the user to go forward if they just went backward
    forwardImage = getImage("forward", app)
    forward = Button(app, 10, 15, 10 + 7*app.height//9 - rowWidth//2, response, False, 
    forwardImage, "forward")

    # allows the user to go backwards
    backwardImage = getImage("backward", app)
    backward = Button(app, 10, 15, 20 + int(7*app.height//9 - rowWidth*1.25), 
    response, False, 
    backwardImage, "backward")

    # adds each of the buttons and returns them
    result.extend([tool, wand, select, adjust, pen, blend, eraser, layers,
                selector, forward, backward])
    return result

def saveImage(app):
    flatImage = Image.alpha_composite(app.background1, app.image2)
    app.image2.save("result/clearImage.png","PNG")
    flatImage.save("result/flatImage.png","PNG")
    print("Image saved inside of result folder")


def generateBrush(radius):
    return 42

# draws each of the main buttons
def drawButtons(app, canvas):
    for button in app.mainButtons:
        button.drawButton(app, canvas)

def changeMode(app, mode):
    app.userMode = mode
    for button in app.mainButtons:
        if button.mode == mode:
            button.resetAllElse(app)
            return True
    print("no button found")
    return False

# checks whether any of the buttons have been clicked
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

# filler response function
def response():
    print("response has been called")

# when the mouse has been pressed
def mousePressed(app, event):
    (x, y) = event.x, event.y

    # check the buttons, and if they haven't been pressed
    if not(checkButtons(app, x, y)):
        # get the coordinates within the image
        coors = insideImage(app,x,y)
        # if the coordinates are in the image
        if (coors != None):
            #app.image2.paste(app.brush, (x, y), app.brush)
            if (app.userMode == "colorselect"):
                r,g,b,a = app.image1.getpixel((coors[0], coors[1]))
                app.currentBrush = (r,g,b,a)
                app.opacitySlider.setAmount(a)
                changeMode(app, "pen")
                #app.selector.isActive = False
            else:
                imageX, imageY = coors[0], coors[1]
                # draw pixels based on that
                drawPixels(app,imageX,imageY)

# navigate options with keys
def keyPressed(app, event):
    if event.key == "w":
        print("zoom in")
        print(app.scaleFactor)
        app.scaleFactor = round(app.scaleFactor + .1, 1)
        app.image2 = app.scaleImage(app.image1, app.scaleFactor)
        app.background2 = app.scaleImage(app.background1, app.scaleFactor)
    elif event.key == "s":
        print("zoom out")
        print(app.scaleFactor)
        app.scaleFactor = round(app.scaleFactor - .1, 1)
        app.image2 = app.scaleImage(app.image1, app.scaleFactor)
        app.background2 = app.scaleImage(app.background1, app.scaleFactor)
    elif event.key == "a":
        print("rotate counterclockwise")
    elif event.key == "d":
        print("rotate clockwise")

# select a color
def colorSelectMode(app):
    app.userMode = "colorselect"
    print("color select")

# change to penMode
def penMode(app):
    app.userMode = "pen"
    print("pen mode")

# change to eraserMode
def eraserMode(app):
    app.userMode = "eraser"
    print("eraser mode")

def setBrushSize(app, amount):
    final = (amount/20 + 1)/4
    #app.brushSize = final
    app.brush = app.scaleImage(app.originBrush, final)
    app.brushWidth, app.brushHeight = app.brush.size
    print(app.opacitySlider.amount)
    setBrushOpacity(app, app.opacitySlider.getPercent() * 255)

def setBrushColor(app, r,b,g):
    print("hi")

def setBrushOpacity(app, aChange):
    r,g,b,a = app.brush.split()
    newA = aChange/255

    a = a.point(lambda i: i * newA)
    app.brushColored = Image.merge('RGBA', (r, g, b, a))


# when the mouse is released
def mouseReleased(app, event):
    # reset the x and y mouse values
    app.oldX = None
    app.oldY = None

def getMidpoint(x1, y1, x2, y2):
    newCoorX = (x1 + x2)//2
    newCoorY = (y1 + y2)//2
    return newCoorX, newCoorY

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def drawLine(app, x1, y1, x2, y2):
    adjust = app.brushWidth //2
    #app.brushHeight
    app.image2.alpha_composite(app.brushColored, dest = (x2 - adjust, y2 - adjust))

    while (getDistance(x1, y1, x2, y2) > 5):
        x1, y1 = getMidpoint(x1, y1, x2, y2)
        app.image1.alpha_composite(app.brushColored, dest = (x1 - adjust, 
        y1 - adjust))

    #app.image2 = app.scaleImage(app.image1, app.scaleFactor)
    #app.background2 = app.scaleImage(app.background1, app.scaleFactor)

    #newCoorX = (x1 + x2)//2
    #newCoorY = (y1 + y2)//2

    #app.image2.alpha_composite(app.brush, dest = (newCoorX - adjust, 
    #newCoorY - adjust))

    #draw = ImageDraw.Draw(app.image1)
    #if coorsWork(app, x2, y2):
    #    r,g,b,a = app.image1.getpixel((x2,y2))
    #    color = newPixelColor(app, (r,g,b,a), app.currentBrush)
#
   #     draw.line((x1, y1, x2, y2), width=app.brushSize, fill= color)


def drawPixels(app,x,y):
    adjust = app.brushWidth //2
    #app.brushHeight
    app.image2.alpha_composite(app.brushColored, dest = (x - adjust, y - adjust))
    #for row in range(-2,3):
    #    for col in range(-2,3):
    #        drawPixel(app, x+row, y+col)

def drawPixel(app, x, y):
    if coorsWork(app, x, y):
        r,g,b,a = app.image1.getpixel((x,y))
        color = newPixelColor(app, (r,g,b,a), app.currentBrush)
        app.image1.putpixel((x,y),color)
    app.image2 = app.scaleImage(app.image1, app.scaleFactor)
    app.background2 = app.scaleImage(app.background1, app.scaleFactor)

def newPixelColor(app, init, new):
    if app.userMode == "pen":
        r = app.currentBrush[0]
        g = app.currentBrush[1]
        b = app.currentBrush[2]
        a = app.currentBrush[3]
        return (r,g,b,a)
    else:
        return (255,255,255,255)

def mouseDragged(app, event):
    (x, y) = event.x, event.y

    if (app.opacitySlider.checkClicked(x, y, app)):
        setBrushOpacity(app, app.opacitySlider.dragSlider(app, event))
    elif (app.sizeSlider.checkClicked(x, y, app)):
        setBrushSize(app, app.sizeSlider.dragSlider(app,event))
    #app.sizeSlider.dragSlider(app, event)

    imageX, imageY = insideImage(app,x,y)

    if (app.oldX == None) or (app.oldY == None):
        drawPixels(app,imageX,imageY)
    else:
        imageOldX, imageOldY = insideImage(app,app.oldX,app.oldY)
        drawLine(app, imageOldX, imageOldY, imageX, imageY)

    app.oldX = x
    app.oldY = y

def rgbaString(r, g, b, a):
    a = a/255
    R,G,B = (255,255,255)
    # three lines adjusted from StackOverflow
    r2 = int(r * a + (1.0 - a) * R)
    g2 = int(g * a + (1.0 - a) * G)
    b2 = int(b * a + (1.0 - a) * B)
    return f'#{r2:02x}{g2:02x}{b2:02x}'

def redrawAll(app, canvas):
    drawBackground(app, canvas)

    centerX = app.width//2
    centerY = app.height//2
    canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(app.background2))


    canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(app.image2))
    
    drawWindows(app, canvas)
    rowWidth = app.width//20
    x = 19*rowWidth
    y = 18
    radius = 10
    r,g,b,a = app.currentBrush
    color = rgbaString(r, g, b, a)

    drawButtons(app, canvas)

    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
    fill = color, outline = color)
    app.opacitySlider.drawSlider(app, canvas)
    app.sizeSlider.drawSlider(app, canvas)


runApp(width=800, height=550)