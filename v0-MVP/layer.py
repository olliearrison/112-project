from cmu_112_graphics import *

class Layer:
    def __init__(self, image, opacity, layerMode, index, active, tkImage):
        self.image = image
        self.opacity = opacity
        self.layerMode = layerMode
        self.index = index
        self.active = active
        self.tkImage = tkImage

    def addBrushStroke(self, app, brushStroke):
        print("working on it")

    def calculateLayer(self, app):
        # multiply by opacity, adjust based on layerMode
        self.tkImage = ImageTk.PhotoImage(app.image)

    def returnLayer(self, app):
        if self.tkImage == None:
            self.calculateImage(app)
        return self.tkImage
