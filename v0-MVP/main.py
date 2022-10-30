from cmu_112_graphics import *
from windows import *
from background import *
from controller import *

"""
Questions:
- doesn't load nearly fast enough - line opacity, wait until MVP
- working with multiple files, cmd save

to do:

MULTIPLE LAYERS BEFORE OPACITY ADDITION WORKS

- prescale images to save loading time
- add zoom
- break code more effectivly into groups
- creating a button class

to do later:
- add rotation to the inside image
- numpy

"""

def appStarted(app):
    app.margin = 5
    app.imageWidth, app.imageHeight = 400, 450
    #clearBgColor = (255, 255, 255, 0)
    bgColor = (255, 255, 255)
    app.currentBrush = (255, 255, 255, 110)
    app.scaleFactor = 1
    app.rotation = 0

    app.image1 = Image.new('RGBA', (app.imageWidth, app.imageHeight), 
    bgColor)
    app.image1 = app.scaleImage(app.image1, app.scaleFactor)

    app.oldX = None
    app.oldY = None

    app.mainButtons = createButtons(app)

def getImage(name, app):
    imageTitle = "buttons/" + name + ".png"
    imageTitleActive = "buttons/" + name + "-active" + ".png"

    image = app.loadImage(imageTitle)
    image = app.scaleImage(image, 1/250)

    imageActive = app.loadImage(imageTitleActive)
    imageActive = app.scaleImage(imageActive, 1/250)
    return (image, imageActive)

def createButtons(app):
    result = []

    # first row (24)
    rows = 20
    rowWidth = app.width//rows

    # (size, x, y, response, isActive, image1, image2)


    #gallery = Button(app, 40, 1*rowWidth, 10, brushOpacityUp, "gallery", False)
    #gallery.getImage(app)
    #result.append(gallery)

    toolImage = getImage("tool", app)
    tool = Button(app, 10, 2*rowWidth, 15, brushOpacityUp, False, 
    toolImage)

    wandImage = getImage("adjust", app)
    wand = Button(app, 10, 3*rowWidth, 15, brushOpacityUp, False, 
    wandImage)

    selectImage = getImage("select", app)
    select = Button(app, 10, 4*rowWidth, 15, brushOpacityUp, False, 
    selectImage)

    adjustImage = getImage("adjust", app)
    adjust = Button(app, 10, 5*rowWidth, 15, brushOpacityUp, False, 
    adjustImage)

    penImage = getImage("pen", app)
    pen = Button(app, 10, 15*rowWidth, 15, brushOpacityUp, False, 
    penImage)

    blendImage = getImage("blend", app)
    blend = Button(app, 10, 16*rowWidth, 15, brushOpacityUp, False, 
    blendImage)

    eraserImage = getImage("eraser", app)
    eraser = Button(app, 10, 17*rowWidth, 15, brushOpacityUp, False, 
    eraserImage)

    layersImage = getImage("layers", app)
    layers = Button(app, 10, 18*rowWidth, 15, brushOpacityUp, False, 
    layersImage)

    selectorImage = getImage("selector", app)
    selector = Button(app, 10, 15, app.height//2, brushOpacityUp, False, 
    selectorImage)

    result.extend([tool, wand, select, adjust, pen, blend, eraser, layers,
                selector])

    return result

    """wand = Button(app, 10, 3*rowWidth, 15, brushOpacityUp, "adjust", False)
    wand.getImage(app)
    result.append(wand)

    select = Button(app, 10, 4*rowWidth, 15, brushOpacityUp, "select", False)
    select.getImage(app)
    result.append(select)

    adjust = Button(app, 10, 5*rowWidth, 15, brushOpacityUp, "adjust", False)
    adjust.getImage(app)
    result.append(adjust)
"""
    return result

def drawButtons(app, canvas):
    for button in app.mainButtons:
        button.drawButton(app, canvas)

def checkButtons(app, x, y):
    for button in app.mainButtons:
        button.checkClicked(x,y, app)
        #button.getImage(app)

    """
    rotate and zoom

    current strategy:
    - display image for mouse to click over
    - calculate margin
    - subtract the margin from the x and y value
    - apply the change and display

    - 
    """


def response():
    print("response has been called")
    
def mousePressed(app, event):
    (x, y) = event.x, event.y

    checkButtons(app, x, y)
    if (insideImage(app,x,y) != None):
        imageX, imageY = insideImage(app,x,y)
        print(imageX,imageY)
        drawPixels(app,imageX,imageY)

def keyPressed(app, event):
    if event.key == "Up":
        adjustBrushOpacity(app, -10)
    elif event.key == "Down":
        adjustBrushOpacity(app, 10)

def brushOpacityUp(app):
    adjustBrushOpacity(app, 10)

def brushOpacityDown(app):
    adjustBrushOpacity(app, -10)

def adjustBrushOpacity(app, amount):
    checkValue = app.currentBrush[3] + amount
    if checkValue >= 0 and checkValue <= 255:
        app.currentBrush = (app.currentBrush[0],
        app.currentBrush[1],app.currentBrush[2],checkValue)

def mouseReleased(app, event):
    app.oldX = None
    app.oldY = None

def insideImage(app,x,y):
    marginX = (app.width - app.imageWidth)//2
    marginY = (app.height - app.imageHeight)//2
    imageX = int((x - marginX)*app.scaleFactor)
    imageY = int((y - marginY)*app.scaleFactor)
    return (imageX,imageY)

def drawLine(app, x1, y1, x2, y2):
    draw = ImageDraw.Draw(app.image1)
    xWorks = (x2 < app.imageWidth) and (x2 > 0)
    yWorks = (y2 < app.imageHeight) and (y2 > 0)
    if xWorks and yWorks:
        r,g,b,a = app.image1.getpixel((x2,y2))
        color = newPixelColor(app, (r,g,b,a), app.currentBrush)
        draw.line((x1, y1, x2, y2), width=7, fill= color)

def drawPixels(app,x,y):
    for row in range(-2,3):
        for col in range(-2,3):
            drawPixel(app, x+row, y+col)

def drawPixel(app, x, y):
    color = app.currentBrush
    xWorks = (x < app.imageWidth) and (x > 0)
    yWorks = (y < app.imageHeight) and (y > 0)
    if xWorks and yWorks:
        app.image1.putpixel((x,y),app.currentBrush)

def newPixelColor(app, init, new):
    r = app.currentBrush[0]
    g = app.currentBrush[1]
    b = app.currentBrush[2]
    a = app.currentBrush[3]
    return (r,g,b,a)

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

def redrawAll(app, canvas):
    drawBackground(app, canvas)

    centerX = app.width//2
    centerY = app.height//2
    canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(app.image1))
    
    drawWindows(app, canvas)
    drawButtons(app, canvas)
    #canvas.create_image(20, app.height//2, image=ImageTk.PhotoImage(app.image13))

runApp(width=800, height=550)