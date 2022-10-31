from cmu_112_graphics import *
from windows import *
from background import *

"""
to do:
- change button color based on whether they are selected
- generate circle shaped brushes based on the size
- create widget for changing opacity/brush size
- color selection
- organize code
- put code into multiple pages without making things break
- create window to figure out layers

to do later:
- add rotation
- undo, redo
- numpy
- transparent blur windows (brushes, erasers, layers, colors)

"""

def appStarted(app):
    app.margin = 5
    app.imageWidth, app.imageHeight = 400, 450
    bgColor = (255, 255, 255)
    app.currentBrush = (10, 20, 255, 110)
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

    # holds the most recent x and y position on the canvas
    app.oldX = None
    app.oldY = None

    # defines the user mode: pen, blend, eraser, layer, colorselect, etc
    app.userMode = "pen"

    # creates the buttons
    app.mainButtons = createButtons(app)

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
    tool = Button(app, 10, 2*rowWidth, 15, brushOpacityUp, False, 
    toolImage, "tool")

    # opens full layer adjustments
    wandImage = getImage("wand", app)
    wand = Button(app, 10, 3*rowWidth, 15, brushOpacityUp, False, 
    wandImage, "wand")

    # allows user to select parts of the layer they are on
    selectImage = getImage("select", app)
    select = Button(app, 10, 4*rowWidth, 15, brushOpacityUp, False, 
    selectImage, "select")

    # allows the user to adjust the selection
    adjustImage = getImage("adjust", app)
    adjust = Button(app, 10, 5*rowWidth, 15, brushOpacityUp, False, 
    adjustImage, "adjust")

    # either switches to the selected pen or opens a window to choose a pen
    penImage = getImage("pen", app)
    pen = Button(app, 10, 15*rowWidth, 15, penMode, False, 
    penImage, "pen")

    # either switches to the selected blender or opens a window to choose a
    # blender
    blendImage = getImage("blend", app)
    blend = Button(app, 10, 16*rowWidth, 15, brushOpacityUp, False, 
    blendImage, "blend")

    # either switches to the selected eraser or opens a window to choose 
    # a eraser
    eraserImage = getImage("eraser", app)
    eraser = Button(app, 10, 17*rowWidth, 15, eraserMode, False, 
    eraserImage, "eraser")

    # opens layers
    layersImage = getImage("layers", app)
    layers = Button(app, 10, 18*rowWidth, 15, brushOpacityUp, False, 
    layersImage, "layers")

    # allows the user to select a color from the canvas
    selectorImage = getImage("selector", app)
    selector = Button(app, 10, 15, app.height//2, colorSelect, False, 
    selectorImage, "selector")

    # allows the user to go forward if they just went backward
    forwardImage = getImage("forward", app)
    forward = Button(app, 10, 15, 7*app.height//9 - rowWidth//2, brushOpacityUp, False, 
    forwardImage, "forward")

    # allows the user to go backwards
    backwardImage = getImage("backward", app)
    backward = Button(app, 10, 15, int(7*app.height//9 - rowWidth*1.25), 
    brushOpacityDown, False, 
    backwardImage, "backward")

    # adds each of the buttons and returns them
    result.extend([tool, wand, select, adjust, pen, blend, eraser, layers,
                selector, forward, backward])
    return result

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
            if (app.userMode == "colorselect"):
                r,g,b,a = app.image1.getpixel((coors[0], coors[1]))
                app.currentBrush = (r,g,b,a)
                changeMode(app, "pen")
                #app.selector.isActive = False
            else:
                imageX, imageY = coors[0], coors[1]
                # draw pixels based on that
                drawPixels(app,imageX,imageY)

# navigate options with keys
def keyPressed(app, event):
    if event.key == "Up":
        adjustBrushOpacity(app, 10)
    elif event.key == "Down":
        adjustBrushOpacity(app, -10)
    elif event.key == "w":
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

# increase the brush opacity
def brushOpacityUp(app):
    adjustBrushOpacity(app, 10)

# decrease the brush opacity
def brushOpacityDown(app):
    adjustBrushOpacity(app, -10)

# select a color
def colorSelect(app):
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

# adjust the opacity
def adjustBrushOpacity(app, amount):
    # set the new value
    checkValue = app.currentBrush[3] + amount
    # if it is allowed, change the value
    if checkValue >= 0 and checkValue <= 255:
        app.currentBrush = (app.currentBrush[0],
        app.currentBrush[1],app.currentBrush[2],checkValue)

# when the mouse is released
def mouseReleased(app, event):
    # reset the x and y mouse values
    app.oldX = None
    app.oldY = None

# adjust the x and y values within the app to correspond the the x and y values
# on the canvas
def insideImage(app,x,y):
    marginX = (app.width - (app.imageWidth*app.scaleFactor))//2
    marginY = (app.height - (app.imageHeight*app.scaleFactor))//2
    imageX = int((x - marginX)//app.scaleFactor)
    imageY = int((y - marginY)//app.scaleFactor)
    return (imageX,imageY)

# check whether the coordinates are within the canvas
def coorsWork(app, x, y):
    xWorks = (x < app.imageWidth) and (x > 0)
    yWorks = (y < app.imageHeight) and (y > 0)
    return xWorks and yWorks

def drawLine(app, x1, y1, x2, y2):
    draw = ImageDraw.Draw(app.image1)
    if coorsWork(app, x2, y2):
        r,g,b,a = app.image1.getpixel((x2,y2))
        color = newPixelColor(app, (r,g,b,a), app.currentBrush)

        draw.line((x1, y1, x2, y2), width=7, fill= color)
    app.image2 = app.scaleImage(app.image1, app.scaleFactor)
    app.background2 = app.scaleImage(app.background1, app.scaleFactor)

def drawPixels(app,x,y):
    for row in range(-2,3):
        for col in range(-2,3):
            drawPixel(app, x+row, y+col)

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
    imageX, imageY = insideImage(app,x,y)

    if (app.oldX == None) or (app.oldY == None):
        drawPixels(app,imageX,imageY)
    else:
        imageOldX, imageOldY = insideImage(app,app.oldX,app.oldY)
        drawLine(app, imageOldX, imageOldY, imageX, imageY)

    app.oldX = x
    app.oldY = y

def rgbString(r, g, b, a):
    a = a/255
    R,G,B = (255,255,255)
    r2 = int(r * a + (1.0 - a) * R)
    g2 = int(g * a + (1.0 - a) * G)
    b2 = int(b * a + (1.0 - a) * B)
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
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
    color = rgbString(r, g, b, a)

    drawButtons(app, canvas)
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
    fill = color, outline = color)

runApp(width=800, height=550)