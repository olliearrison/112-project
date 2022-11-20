import math

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

# returns the distance between
def getDistance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)