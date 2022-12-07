from cmu_112_graphics import *

class Layer:
    def __init__(self, image, opacity, layerMode, index, active, tkImage, 
    zoomTkImage):
        self.image = image
        self.opacity = opacity
        self.layerMode = layerMode
        self.index = index
        self.active = active
        self.tkImage = tkImage
        self.zoomTkImage = zoomTkImage

    # add a brush stroke to the image, update the layer
    def addBrushStroke(self, app, brushStroke):
        self.image = Image.alpha_composite(self.image, brushStroke)
        self.calculateLayer(app)

    # get the tk image and tk image scaled
    def calculateLayer(self, app):
        # multiply by opacity, adjust based on layerMode
        self.tkImage = ImageTk.PhotoImage(self.image)
        self.zoomTkImage = ImageTk.PhotoImage(app.scaleImage(self.image, app.scaleFactor))

    # return the zoom layer
    def zoomReturnLayer(self, app):
        if self.zoomTkImage == None:
            self.calculateLayer(app)
        return self.zoomTkImage

    # return the origional layer
    def returnLayer(self, app):
        if self.tkImage == None:
            self.calculateLayer(app)
        return self.tkImage
