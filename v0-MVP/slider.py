class Slider:
    # the amount variable should be changed to represent 0-255
    def __init__(self, app, sizeX, sizeY, slideSize, x, y, response, isActive, 
    amount):
        self.app = app
        self.sizeX = sizeX # 10
        self.sizeY = sizeY # 60
        self.slideSize = slideSize
        self.x = x # 20
        self.y = y # app.height/2 - 90
        self.response = response
        self.isActive = isActive
        self.amount = amount

    # num is 0-255
    def setAmount(self, num):
        bound1 = self.y - self.sizeY + self.slideSize
        bound2 = self.y + self.sizeY - self.slideSize
        den = bound2 - bound1
        adjust = num/255
        self.amount = bound2 - (den*adjust)
        
    # get the percent location from the slider
    def getPercent(self):
        bound1 = self.y - self.sizeY + self.slideSize
        bound2 = self.y + self.sizeY - self.slideSize
        den = bound2 - bound1
        num = den - (self.amount - bound1)
        return num/den

    # draw the slider
    def drawSlider(self, app, canvas):

        # draw the larger piece
        canvas.create_rectangle(self.x - self.sizeX, self.y - self.sizeY,
                            self.x + self.sizeX, self.y + self.sizeY,
                            fill = "#252525", outline = "#252525")
        
        # draw the small, movable piece
        canvas.create_rectangle(self.x - self.sizeX, self.amount - self.slideSize,
                            self.x + self.sizeX, self.amount + self.slideSize,
                            fill = "#868686", outline = "#868686")

    # move the slider
    def dragSlider(self, app, event):

        # calculate the bound
        bound1 = self.y - self.sizeY + self.slideSize
        bound2 = self.y + self.sizeY - self.slideSize

        # if it is active, move the amount to the right place
        if self.isActive:
            if (event.y < bound1):
                self.amount = bound1
            elif (event.y > bound2):
                self.amount = bound2
            else:
                self.amount = event.y
        
        # return the most recent value
        lastValue = int(self.getPercent() * 255)
        return lastValue

    # check whether the slider has been clicked
    def checkClicked(self, x, y, app):
        x1 = self.x
        x2 = self.x + self.sizeX
        y1 = self.y - self.sizeY + self.slideSize
        y2 = self.y + self.sizeY - self.slideSize

        if (x >= x1 and x <= x2) and (y >= y1 and y <= y2):
            self.isActive = True
            return True
        return False

        
    
