from cmu_112_graphics import *
from layer import *
from button import *
 

class LayerBlock:
    def __init__(self, layer, visible, selected, index):
        self.layer = layer
        self.visible = visible
        self.selected = selected
        self.index = index
        self.layerBlockImage = Image.open("layer-assets/layerblock.png").convert("RGBA")
        self.layerBlockImageScaled = None
        self.visibilityButton = None

    def getCoors(self, app):
        centerX = app.width//7*5.9
        centerY = app.height//4.8 + self.index * 35
        return (centerX, centerY)

    def response(self):
        self.visible = not(self.visible)

    def init(self, app):
        buttonImage = Image.open("layer-assets/normal.png").convert("RGBA")
        buttonImage = app.scaleImage(buttonImage, 1/20)
        tup = (buttonImage,buttonImage)

        centerX, centerY = self.getCoors(app)
        self.visibilityButton = Button(app, 10, centerX, centerY, self.response, False,tup, "tool")
        
    def scaleCropLayer(self,app):
        self.layerBlockImageScaled = app.scaleImage(self.layerBlockImage, .57)

        blockWidth, blockHeight = self.layerBlockImageScaled.size
        maxWidth = blockWidth / 5.8
        maxHeight = (blockHeight+5) / 1.8

        image = self.getImage(app)
        scaleFactor = min(blockWidth/maxWidth,blockHeight/maxHeight)
        image = app.scaleImage(image, scaleFactor)
        image = image.crop((0,0,maxWidth, maxHeight))
        
        return image, maxWidth*2.14

    def getImage(self, app):
        return self.layer.image

    def drawLayerBlock(self, app, canvas):
        centerX, centerY = self.getCoors(app)

        image, xOffset = self.scaleCropLayer(app)
        canvas.create_image(centerX - xOffset, centerY+2, image= ImageTk.PhotoImage(image))
        canvas.create_image(centerX, centerY, image= ImageTk.PhotoImage(self.layerBlockImageScaled))
        if (self.visibilityButton != None):
            self.visibilityButton.drawButton(app, canvas)
        