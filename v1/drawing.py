from cmu_112_graphics import *

"""
when image is left, returns thumbnail
"""

class Drawing:
    def __init__(self, app, index):
        self.app = app
        self.thumbnail = None
        self.layerBlocks = []
        self.layers = []
        self.index = index

    def getThumbnail(self):
        if self.thumbnail == None:
            self.thumbnail = Image.new('RGBA', (400, 450), (255,255,255,255))
        return self.thumbnail

    def setThumbnail(self, image, app):
        self.thumbnail = app.scaleImage(image, 1/5)

    def getLayerBlocks(self):
        return self.layerBlocks

    def setLayerBlocks(self, layerBlocks):
        self.layerBlocks = layerBlocks

    def getLayers(self):
        return self.layers

    def setLayers(self, layer):
        self.layers = layer

    def getXY(self, app):
        rows = 5
        cols = 5
        height = app.height//rows
        width = app.width//cols
        yAdjust = (self.index // rows) * height
        xAdjust = (self.index % rows) * width
        return xAdjust, yAdjust

    def drawThumbnail(self, app, canvas):
        x, y = self.getXY(app)
        canvas.create_image(app.width//10 + x , app.height//5 + y, 
        image=ImageTk.PhotoImage(self.getThumbnail()))

    def response(self, app):
        print("")

    def checkClicked(self, x, y, app):
        xLoc, yLoc = self.getXY(app)
        xLoc += app.width//10
        yLoc += app.height//5
        size = 400//5
        x1 = xLoc - size
        x2 = xLoc + size
        y1 = yLoc - size
        y2 = yLoc + size

        # if it has
        if (x >= x1 and x <= x2) and (y >= y1 and y <= y2):
            # do the response and set itself to active
            self.response(self.app)
            self.isActive = True
            return True
        return False
    
