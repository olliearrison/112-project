def drawGalleryBackground(app, canvas):
    # create a grey background
    canvas.create_rectangle(0,0,app.width, app.height, fill = '#252525')
    drawTopWindow(app, canvas)

# draw the top
def drawTopWindow(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height//10,
    fill = '#181818', outline = '#181818')