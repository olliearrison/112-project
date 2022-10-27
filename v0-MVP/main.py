from cmu_112_graphics import *

def appStarted(app):
    app.margin = 5

    app.timerDelay = 150
    app.imageWidth, app.imageHeight = app.width//2, app.height//2
    bgColor = (0, 255, 255) # cyan
    fgColor = (0, 0, 0)
    app.image1 = Image.new('RGB', (app.imageWidth, app.imageHeight), bgColor)

    for x in range(app.image1.width):
        for y in range(app.image1.height):
            app.image1.putpixel((x,y),bgColor)

    app.oldX = None
    app.oldY = None
    app.image1 = app.scaleImage(app.image1, 1)

def insideImage(app,x,y):
    marginX = (app.width - app.imageWidth)//2
    imageX = x - marginX
    imageY = y - marginX
    return (imageX,imageY)

def drawLine(app, x1, y1, x2, y2):
    draw = ImageDraw.Draw(app.image1)
    draw.line((x1, y1, x2, y2), width=7, fill=(0, 0, 0))

def drawPixels(app,x,y):
    for row in range(-2,3):
        for col in range(-2,3):
            drawPixel(app, x+row, y+col)

def drawPixel(app, x, y):
    color = (0,0,0)
    xWorks = (x < app.imageWidth) and (x > 0)
    yWorks = (y < app.imageHeight) and (y > 0)
    if xWorks and yWorks:
        app.image1.putpixel((x,y),color)

def keyPressed(app, event):
    drawLine(app, 50, 50, 70, 70)

def mousePressed(app, event):
    (x, y) = event.x, event.y
    if (insideImage(app,x,y) != None):
        imageX, imageY = insideImage(app,x,y)
        drawPixels(app,imageX,imageY)

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

def redrawAll(app, canvas):
    canvas.create_image(300, 300, image=ImageTk.PhotoImage(app.image1))

runApp(width=600, height=600)