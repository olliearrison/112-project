from cmu_112_graphics import *
from windows import *
from background import *
from controller import *

"""
to do:
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
    bgColor = (255, 255, 255)
    app.currentBrush = (255, 255, 255, 110)

    app.image1 = Image.new('RGBA', (app.imageWidth, app.imageHeight), bgColor)
    for x in range(app.image1.width):
        for y in range(app.image1.height):
            app.image1.putpixel((x,y),bgColor)

    app.oldX = None
    app.oldY = None
    app.image1 = app.scaleImage(app.image1, 1)
    app.mainButtons = []

    #app.mainBrush = [[1,1,1][1,1,1],[1,1,1]]

    #app.newButton = Button(50, 5, 5)

def response():
    print("hi")
    
def mousePressed(app, event):
    (x, y) = event.x, event.y

    checkButtons(app, x, y)
    if (insideImage(app,x,y) != None):
        imageX, imageY = insideImage(app,x,y)
        drawPixels(app,imageX,imageY)

def keyPressed(app, event):
    print("sup")
    if event.key == "Up":
        adjustBrushOpacity(app, -10)
    elif event.key == "Down":
        adjustBrushOpacity(app, 10)

def adjustBrushOpacity(app, amount):
    checkValue = app.currentBrush[3] + amount
    if checkValue >= 0 and checkValue <= 255:
        app.currentBrush = (app.currentBrush[0],
        app.currentBrush[1],app.currentBrush[2],checkValue)

def mouseReleased(app, event):
    app.oldX = None
    app.oldY = None

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

def checkButtons(x, y, app):
    print("hiiii")
    #for buttons in app.mainButtons:
    #    print("hi")

def insideImage(app,x,y):
    marginX = (app.width - app.imageWidth)//2
    marginY = (app.height - app.imageHeight)//2
    imageX = x - marginX
    imageY = y - marginY
    return (imageX,imageY)

def drawLine(app, x1, y1, x2, y2):
    draw = ImageDraw.Draw(app.image1)
    draw.line((x1, y1, x2, y2), width=7, fill= app.currentBrush)

def drawPixels(app,x,y):
    for row in range(-2,3):
        for col in range(-2,3):
            drawPixel(app, x+row, y+col)

def drawPixel(app, x, y):
    color = app.currentBrush
    xWorks = (x < app.imageWidth) and (x > 0)
    yWorks = (y < app.imageHeight) and (y > 0)
    if xWorks and yWorks:
        r,g,b,a = app.image1.getpixel((x,y))
        color = newPixelColor((r,g,b,a), app.currentBrush)
        app.image1.putpixel((x,y),color)

def newPixelColor(init, new):
    #app.currentBrush[0]
    #app.currentBrush[1]
    #app.currentBrush[2]
    #app.currentBrush[3]
    return (new)

#def keyPressed(app, event):
#    drawLine(app, 50, 50, 70, 70)

def redrawAll(app, canvas):
    drawBackground(app, canvas)

    centerX = app.width//2
    centerY = app.height//2
    canvas.create_image(centerX, centerY, image=ImageTk.PhotoImage(app.image1))
    
    drawWindows(app, canvas)

runApp(width=800, height=550)