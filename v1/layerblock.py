from cmu_112_graphics import *

def appStarted(app):
    print("started")


def redrawAll(app, canvas):
    canvas.create_rectangle(10,20,40,50, fill = "black")

class LayerBlock:
    def __init__(self, image, visible, selected, index):
        self.image = image
        self.visible = visible
        self.selected = selected
        self.index = index

    def drawLayerBlock(self, app, canvas):
        print("draw")

runApp(width=800, height=550, mvcCheck = False)