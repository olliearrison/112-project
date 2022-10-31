from cmu_112_graphics import *

def appStarted(app):
    app.moving = False
    app.current = app.height/2

    width = 10
    height = 60
    app.bound1 = app.height/2 - height + width
    app.bound2 = app.height/2 + height - width

def mousePressed(app, event):
    app.moving = True
    app.current = event.y

def mouseDragged(app, event):
    if app.moving:
        if (event.y < app.bound1):
            app.current = app.bound1
        elif (event.y > app.bound2):
            app.current = app.bound2
        else:
            app.current = event.y

def redrawAll(app, canvas):
    width = 10
    height = 60
    canvas.create_rectangle(app.width/2 - width, app.height/2 - height,
                            app.width/2 + width, app.height/2 + height,
                            fill = "grey")
    canvas.create_rectangle(app.width/2 - width, app.current - width,
                            app.width/2 + width, app.current + width,
                            fill = "black")
    canvas.create_text(app.width/2, 20,
                       text='Move dot with mouse presses',
                       fill='black')
                       

runApp(width=400, height=400)