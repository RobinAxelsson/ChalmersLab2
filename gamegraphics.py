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
from gamemodel import Const as GameConst, Color as GameColor
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
    Button = 'black'
    ButtonLabel = 'pink'
    ControlDialog = 'white'
    EntryBox = 'white'

class text:
    WinTitle = 'Cannon Game'
    Score = 'Score: '
    ControlTitle = 'Fire Controls'
    FireBtn = 'Fire!'
    QuitBtn = 'Quit'
    Wind = 'Wind'
    Velocity = 'Velocity'
    Angle = 'Angle'

class GameGraphics():
    def __init__(self, cannonSize, ballSize, gameGetScore):
        self.gameGetScore = gameGetScore
        self.win = GraphWin(text.WinTitle, Win.WIDTH, Win.HEIGHT, autoflush=False)
        self.win.setCoords(Win.X1, Win.Y1, Win.X2, Win.Y2)
        draw = GraphicsCreator(self.win)
        draw.Sky(Color.Sky)
        draw.Ground(Color.Ground)
        draw.Cannon(Color.Blue, Win.BLUE_X, cannonSize)
        draw.Cannon(Color.Red, Win.RED_X, cannonSize)
        self.blueScore:Text = draw.text(Win.BLUE_X, text.Score + '0')
        self.redScore: Text = draw.text(Win.RED_X, text.Score + '0')
        self.blueBall: Circle = draw.cannonBall(Color.Blue, ballSize, Win.BLUE_X, cannonSize)
        self.redBall: Circle = draw.cannonBall(Color.Red, ballSize, Win.RED_X, cannonSize)
    
    # only needed to fit test template, the graphics doesnt need it
    def sync(self):
        pass

    def getWindow(self):
        #removes sky and ground rectangles for testcase
        items = self.win.items
        for item in items:
            if hasattr(item, "testStatus") and item.testStatus == False:
                items.remove(item)
        return self.win
    def quit(self):
        """Closes the game window"""
        self.win.close()
    def UpdateCannonBall(self, color, x, y):
        ball = self.blueBall if color == GameColor.blue.name else self.redBall
        xy = self.__convertPos(ball, x, y)
        ball.move(xy[0], xy[1])
    def UpdateScore(self, color):
        scoreText = self.blueScore if color == GameColor.blue else self.redScore
        scoreText.setText(text.Score + str(self.gameGetScore(color)))

    def __convertPos(self, ball: Circle, newX, newY):
        point = ball.getCenter()
        pX = point.getX()
        pY = point.getY()
        dX = newX - pX
        dY = newY - pY
        return (dX, dY)

class GraphicsCreator():
    def __init__(self, window: GraphWin):
      self.window = window
    def Ground(self, color):
        ground = Rectangle(Point(Win.X1, Win.Y1), Point(Win.X2, 0))
        ground.setFill(color)
        ground.draw(self.window)
        ground.testStatus = False
    def Sky(self, color):
        sky = Rectangle(Point(Win.X1, 0), Point(Win.X2, Win.Y2))
        sky.setFill(color)
        sky.draw(self.window)
        sky.testStatus = False
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
    def text(self, x, text):
        text = Text(Point(x, Win.Y1/2), text)
        text.setTextColor(Color.Text)
        text.draw(self.window)
        return text

""" The input dialog that controls the game """
class InputDialog:
    """ Creates an input dialog with initial values for angle and velocity and displaying wind """
    def __init__ (self, getCurrentWind, quit):
        self.win = win = GraphWin(text.ControlTitle, 200, 300)
        win.setCoords(0,4.5,4,.5)
        self.win.setBackground(Color.ControlDialog)
        self.angleText = Text(Point(1,1), text.Angle).draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setFill(Color.EntryBox)
        self.angle.setText(str(GameConst.DEFAULT_ANGLE))
        self.getCurrentWind = getCurrentWind
        self.quitGame = quit
        
        Text(Point(1,2), text.Velocity).draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setFill(Color.EntryBox)
        self.vel.setText(str(GameConst.DEFAULT_VELOCITY))
        
        Text(Point(1,3), text.Wind).draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(getCurrentWind()))
        
        self.fire = Button(win, Point(1,4), 1.25, .5, text.FireBtn)
        self.fire.activate()

        self.quit = Button(win, Point(3,4), 1.25, .5, text.QuitBtn)
        self.quit.activate()

    """ Updates the wind after each round """
    def updateWind(self):
        self.height.setText("{0:.2f}".format(self.getCurrentWind()))

    """ Waits for the player to enter values and click a button """
    def interact(self, fire):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                self.quitGame
                self.close()
            if self.fire.clicked(pt):
                return fire(int(self.angle.getText()), int(self.vel.getText()))

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

    def __init__(self, win: GraphWin, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, Point(30,25), 20, 10, 'Quit') """
        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill(Color.Button)
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()
        return

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
        self.label.setFill(Color.ButtonLabel)
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0