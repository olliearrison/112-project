def drawBackground(app, canvas):
    # create a grey background
    canvas.create_rectangle(0,0,app.width, app.height, fill = '#252525')
    drawGrid(app, canvas)

# fill the canvas with 10*10 cubes
def drawGrid(app, canvas):
    cubeSize = 10
    for i in range(app.width//cubeSize):
        canvas.create_line(i*cubeSize,0,i*cubeSize,app.height, 
        fill = '#2F2F2F', width = .1)

    for i in range(app.height//cubeSize):
        canvas.create_line(0,i*cubeSize,app.width,i*cubeSize, 
        fill = '#2F2F2F', width = .1)