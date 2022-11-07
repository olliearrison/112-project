from cmu_112_graphics import *
import windows
from background import *
from coors import *
from brushClass import *
import math

"""
pillow docs: https://pillow.readthedocs.io/en/stable/reference/Image.html

to do:
- eraser functionality
- color picker functionality
- update color
- make everything on the app scale when the window size is changed 
(use similar strategy as for robot)
- fix zoom

to do later:
- create brush class
- create layer class
- make layer naming consistant
- add rotation (pillow)
- non square/word based buttons (for gallery and on option pages)
- create window to create and delete layers
- create window to select colors

must be after MVP:
- undo, redo
- numpy
- compile into c python
- transparent blur windows (brushes, erasers, layers, colors)
- threading: multi threading
- pygame maybe

plan to fix opacity:
when brush is first clicked, start a new image that is multiplied by the
opacity. after the brush is picked up, flatten this image into the layer
"""

def appStarted(app):
    app.margin = 5
    app.imageWidth, app.imageHeight = 400, 450
    bgColor = (255, 255, 255)

    app.currentColor = (70, 10, 90)

    app.brushSize = 7
    app.scaleFactor = 1
    app.rotation = 0
    app.toBeDrawn = set()
    app.timerDelay = 50
    app.drag = False

    # define primary image in RGBA (includes opacity 0-255)
    app.background1 = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
    (255,255,255,255))
    app.background2 = app.scaleImage(app.background1, app.scaleFactor)

    app.image1 = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
    (255,255,255,0))
    # scales image
    app.image2 = app.scaleImage(app.image1, app.scaleFactor)

    brushImage = Image.open("brush.png").convert("RGBA")
    app.airbrush = Brush(brushImage, (70, 10, 90), app.height/2 - 70, 255, 1, 
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


    app.sizeSlider = windows.Slider(app, 10, 55, 5, 20,app.height/2 - 100, response, 
                    False, app.height/2 - 70)

    app.opacitySlider = windows.Slider(app, 10, 50, 5, 20,app.height/2 + 55, response, 
                    True, 285)

    app.opacitySlider.setAmount(255)
    app.sizeSlider.setAmount(app.height/2 - 70)

    app.mainSliders = []
    app.mainSliders.extend([app.opacitySlider, app.sizeSlider])


def timerFired(app):
    for coor in app.toBeDrawn:
        app.airbrush.addDot(coor[0],coor[1])
        #app.airbrush.brushClick(coor[0],coor[1], app.image2, app)
    app.toBeDrawn = set()
    app.image2 = app.scaleImage(app.image1, app.scaleFactor)

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
    print(windows.Button)
    tool = windows.Button(app, 10, 2*rowWidth, 15, saveImage, False, toolImage, "tool")

    # opens full layer adjustments
    wandImage = getImage("wand", app)
    wand = windows.Button(app, 10, 3*rowWidth, 15, response, False, 
    wandImage, "wand")

    # allows user to select parts of the layer they are on
    selectImage = getImage("select", app)
    select = windows.Button(app, 10, 4*rowWidth, 15, response, False, 
    selectImage, "select")

    # allows the user to adjust the selection
    adjustImage = getImage("adjust", app)
    adjust = windows.Button(app, 10, 5*rowWidth, 15, response, False, 
    adjustImage, "adjust")

    # either switches to the selected pen or opens a window to choose a pen
    penImage = getImage("pen", app)
    pen = windows.Button(app, 10, 15*rowWidth, 15, penMode, True, 
    penImage, "pen")

    # either switches to the selected blender or opens a window to choose a
    # blender
    blendImage = getImage("blend", app)
    blend = windows.Button(app, 10, 16*rowWidth, 15, response, False, 
    blendImage, "blend")

    # either switches to the selected eraser or opens a window to choose 
    # a eraser
    eraserImage = getImage("eraser", app)
    eraser = windows.Button(app, 10, 17*rowWidth, 15, eraserMode, False, 
    eraserImage, "eraser")

    # opens layers
    layersImage = getImage("layers", app)
    layers = windows.Button(app, 10, 18*rowWidth, 15, response, False, 
    layersImage, "layers")

    # allows the user to select a color from the canvas
    selectorImage = getImage("selector", app)
    selector = windows.Button(app, 10, 15, app.height//2 - 25, colorSelectMode, False, 
    selectorImage, "selector")

    # allows the user to go forward if they just went backward
    forwardImage = getImage("forward", app)
    forward = windows.Button(app, 10, 15, 10 + 7*app.height//9 - rowWidth//2, response, False, 
    forwardImage, "forward")

    # allows the user to go backwards
    backwardImage = getImage("backward", app)
    backward = windows.Button(app, 10, 15, 20 + int(7*app.height//9 - rowWidth*1.25), 
    response, False, 
    backwardImage, "backward")

    # adds each of the buttons and returns them
    result.extend([tool, wand, select, adjust, pen, blend, eraser, layers,
                selector, forward, backward])
    return result

# saves an image with a white background and with a transparent background
# why image2?
def saveImage(app):
    flatImage = Image.alpha_composite(app.background1, app.image2)
    app.image2.save("result/clearImage.png","PNG")
    flatImage.save("result/flatImage.png","PNG")
    print("Image saved inside of result folder")

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

# filler response function
def response(app):
    print("response has been called")

# when the mouse has been pressed
def mousePressed(app, event):
    app.drag = False
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
                #app.currentBrush = (r,g,b,a)
                app.currentColor = (r,g,b)
                app.opacitySlider.setAmount(a)
                changeMode(app, "pen")
                #app.selector.isActive = False
            else:
                imageX, imageY = coors[0], coors[1]
                # draw pixels based on that
                app.airbrush.brushClick(imageX ,imageY, app.image1, app)

# navigate options with keys
def keyPressed(app, event):
    if event.key == "w":
        print("zoom in")
        print(app.scaleFactor)
        # adjust the scale factor
        app.scaleFactor = round(app.scaleFactor + .1, 1)
        # scale the results image (but not the actual image)
        app.image2 = app.scaleImage(app.image1, app.scaleFactor)
        # scale the results background (but not the actual image)
        app.background2 = app.scaleImage(app.background1, app.scaleFactor)
    elif event.key == "s":
        print("zoom out")
        print(app.scaleFactor)
        # adjust the scale factor
        app.scaleFactor = round(app.scaleFactor - .1, 1)
        # scale the results image (but not the actual image)
        app.image2 = app.scaleImage(app.image1, app.scaleFactor)
        # scale the results background (but not the actual image)
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

def changeToWhite(app, input, newR = 255,newG = 255,newB = 255):
    altered = input.convert("RGBA")
    app.brush = Image.open("brush.png").convert("RGBA")
    r,g,b,a = app.brush.split()
    r = r.point(lambda i: (i+1) * newR)
    g = g.point(lambda i: (i + 1) * newG)
    b = b.point(lambda i: (i+1) * newB)
    altered = Image.merge('RGBA', (r, g, b, a))
    return altered.convert("png")

# when the mouse is released
def mouseReleased(app, event):
    # reset the x and y mouse values
    app.airbrush.afterBrushStroke(app, app.image1)

# when the mouse is dragged
def mouseDragged(app, event):
    app.drag = True
    (x, y) = event.x, event.y

    # check if the opacity or slide slider has been clicked
    if (app.opacitySlider.checkClicked(x, y, app)):
        app.airbrush.opacity = app.opacitySlider.dragSlider(app, event)
    elif (app.sizeSlider.checkClicked(x, y, app)):
        app.airbrush.size = app.sizeSlider.dragSlider(app,event)

    else:
        # find the value inside the image1
        imageX, imageY = insideImage(app,x,y)
        app.airbrush.duringBrushStroke(app, imageX, imageY)

# calculate the hex from RGBA with a white background
def rgbaString(r, g, b, a=255):
    a = a/255
    R,G,B = (255,255,255)
    # three lines adjusted from StackOverflow
    r2 = int(r * a + (1.0 - a) * R)
    g2 = int(g * a + (1.0 - a) * G)
    b2 = int(b * a + (1.0 - a) * B)
    return f'#{r2:02x}{g2:02x}{b2:02x}'

def redrawAll(app, canvas):
    # draw the background
    drawBackground(app, canvas)

    # display the white background
    centerX = app.width//2
    centerY = app.height//2
    
    canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(app.background2))

    # display the user image
    canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(app.image2))
    if (app.airbrush.active):
        currentStroke = app.airbrush.getCurrentStroke()
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


runApp(width=800, height=550)