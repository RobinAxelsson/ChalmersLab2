#------------------------------------------------------
#This module contains all graphics-classes for the cannon game.
#The two primary classes have these responsibilities:
#  * GameGraphics is responsible for the main window
#  * Each PlayerGraphics is responsible for the graphics of a 
#    single player (score, cannon, projectile)
#In addition there are two UI-classes that have no 
#counterparts in the model:
#  * Button
#  * InputDialog
#------------------------------------------------------

# This is the only place where graphics should be imported!
from gamemodel import Const as GameConst, Game, Color as GameColor
from graphics import Circle, GraphWin, Text, Point, Entry, Rectangle

class Win:
    WIDTH = 640
    HEIGHT = 480
    X1 = GameConst.LEFT_END
    Y1 = -10
    X2 = GameConst.RIGHT_END
    Y2 = 155
    BLUE_X = GameConst.P0_POS
    RED_X = GameConst.P1_POS

class Color:
    Sky = 'lightblue'
    Ground = 'green'
    Red = 'red'
    Blue = 'blue'
    Text = 'yellow'

class text:
    Title = 'Cannon Game'
    Score = 'Score: '

class GameGraphics():
    def __init__(self, cannonSize, ballSize):
        win = GraphWin(text.Title, Win.WIDTH, Win.HEIGHT, autoflush=False)
        win.setCoords(Win.X1, Win.Y1, Win.X2, Win.Y2)
        draw = DrawGraphics(win)
        draw.Sky(Color.Sky)
        draw.Ground(Color.Ground)
        draw.Cannon(Color.Blue, Win.BLUE_X, cannonSize)
        draw.Cannon(Color.Red, Win.RED_X, cannonSize)
        self.blueScore:Text = draw.text(Win.BLUE_X, text.Score)
        self.redScore: Text = draw.text(Win.RED_X, text.Score)
        self.blueBall: Circle = draw.cannonBall(Color.Blue, ballSize, Win.BLUE_X, cannonSize)
        self.redBall: Circle = draw.cannonBall(Color.Red, ballSize, Win.RED_X, cannonSize)

    def UpdateCannonBall(self, color, getX, getY):
        ball = self.blueBall if color == GameColor.blue else self.redBall
        xy = self.__convertPos(ball, getX(), getY())
        ball.move(xy[0], xy[1])
    
    def __convertPos(self, ball: Circle, newX, newY):
        point = ball.getCenter()
        pX = point.getX()
        pY = point.getY()
        dX = newX - pX
        dY = newY - pY
        return (dX, dY)

class DrawGraphics():
    def __init__(self, window: GraphWin):
      self.window = window
    def Ground(self, color):
        sky = Rectangle(Point(Win.X1, Win.Y1), Point(Win.X2, 0))
        sky.setFill(color)
        sky.draw(self.window)
    def Sky(self, color):
        ground = Rectangle(Point(Win.X1, 0), Point(Win.X2, Win.Y2))
        ground.setFill(color)
        ground.draw(self.window)
    def Cannon(self, color, x, cannonSize):
        point1 = Point(x-cannonSize/2, 0)
        point2 = Point(x+cannonSize/2, cannonSize)
        cannon = Rectangle(point1, point2)
        cannon.setFill(color)
        cannon.draw(self.window)
    def cannonBall(self, color, radi, x, cannonSize):
        ball = Circle(Point(x, cannonSize/2), radi)
        ball.setFill(color)
        ball.draw(self.window)
        return ball

""" A somewhat specific input dialog class (adapted from the book) """
class InputDialog:
    """ Creates an input dialog with initial values for angle and velocity and displaying wind """
    def __init__ (self, getCurrentWind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        self.angleText = Text(Point(1,1), 'Angle').draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(GameConst.DEFAULT_ANGLE))
        self.getCurrentWind = getCurrentWind
        
        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(GameConst.DEFAULT_VELOCITY))
        
        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(getCurrentWind()))
        
        self.fire = Button(win, Point(1,4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()

    """ Waits for the player to enter values and click a button """
    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    """ Gets the values entered into this window, typically called after interact """
    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a,v

    """ Closes the input window """
    def close(self):
        self.win.close()



""" A general button class (from the book) """
class Button:

    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, Point(30,25), 20, 10, 'Quit') """ 

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        "RETURNS true if button active and p is inside"
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        "RETURNS the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0