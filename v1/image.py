"""

overall flow:

user opens app
retreives any images: from filesystem
displays them: getThumbnail
user can create a new image: create a new instance of drawing retreiving
values from the filesystem and passes it into the drawMode_appStarted
or open a new one: passes default values into drawMode_appStarted

"""



class Drawing:

    def __init__(self, thumbnail):
        self.thumbnail = thumbnail
        print("hi")

    #
    def setThumbnail(self):
        # self.save from function in main
        # scale to correct size
        return 42
    
    #
    def getThumbnail(self):
        return self.thumbnail

    #
    def getDrawing(self):
        return 42

    #
    def drawThumbnail(self, app, canvas):
        return 42

    #
    def checkClicked(self, x, y):
        return 42

    #
    def setDrawing(self):
        return 42