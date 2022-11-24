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
        self.layerBlockImageActive = Image.open("layer-assets/layerblock-active.png").convert("RGBA")
        self.layerBlockImageScaledActive = None
        self.visibilityButton = None

    def checkClicked(self, x, y, app):
        blockWidth, blockHeight = self.layerBlockImageScaled.size
        maxWidth = blockWidth
        maxHeight = 33
        centerX, centerY = self.getCoors(app)

        x1 = centerX - maxWidth//2
        x2 = centerX + maxWidth//2
        y1 = centerY - maxHeight//2
        y2 = centerY + maxHeight//2

        if (x >= x1 and x <= x2) and (y >= y1 and y <= y2):
            self.selected = not(self.selected)
            self.resetAllElse(app)

            return True
        return False

    def resetAllElse(self, app):
        if (self.selected == True):
            for layerBlock in app.allLayerBlocks:
                if self != layerBlock:
                    layerBlock.selected = False

    def getCoors(self, app):
        centerX = app.width//7*5.9
        centerY = app.height//4.8 + self.index * 40
        return (centerX, centerY)


    def init(self, app):
        buttonImage = Image.open("layer-assets/visible.png").convert("RGBA")
        buttonImage = app.scaleImage(buttonImage, 1/20)
        buttonImageActive = Image.open("layer-assets/visible-active.png").convert("RGBA")
        buttonImageActive = app.scaleImage(buttonImageActive, 1/20)
        tup = (buttonImage,buttonImageActive)

        centerX, centerY = self.getCoors(app)
        self.visibilityButton = Button(app, 10, centerX*1.12, centerY-4, self.response, False,tup, "tool")
        
    def response(self, app):
        self.visible = not(self.visible)
        return True

    def scaleCropLayer(self,app):
        self.layerBlockImageScaled = app.scaleImage(self.layerBlockImage, .57)
        self.layerBlockImageScaledActive = app.scaleImage(self.layerBlockImageActive, .57)

        blockWidth, blockHeight = self.layerBlockImageScaled.size
        maxWidth = blockWidth / 5.8
        maxHeight = (blockHeight+5) / 1.8

        image = self.getImage(app)
        scaleFactor = min(maxWidth/blockWidth,maxHeight/blockHeight)
        image = app.scaleImage(image, scaleFactor)
        image = image.crop((0,0,maxWidth, maxHeight))
        
        return image, maxWidth*2.14

    def updateImage(self, image, app):
        self.layer.image = image.image
        #self.scaleCropLayer(app)

    def getImage(self, app):
        return self.layer.image

    def drawLayerBlock(self, app, canvas):
        centerX, centerY = self.getCoors(app)

        image, xOffset = self.scaleCropLayer(app)
        canvas.create_image(centerX - xOffset, centerY+2, image= ImageTk.PhotoImage(image))
        if self.selected:
            canvas.create_image(centerX, centerY, image= ImageTk.PhotoImage(self.layerBlockImageScaledActive))
        else:
            canvas.create_image(centerX, centerY, image= ImageTk.PhotoImage(self.layerBlockImageScaled))
        if (self.visibilityButton != None):
            self.visibilityButton.drawButton(app, canvas)
        