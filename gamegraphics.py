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
import gamemodel
from graphics import GraphWin, Text, Point, Entry, Rectangle

class Const:
    WIN_WIDTH = 640
    WIN_HEIGHT = 480
    WIN_X1 = -110
    WIN_Y1 = -10
    WIN_X2 = 110
    WIN_Y2 = 155

class GameGraphics():
    def __init__(self, game: gamemodel.Game) -> None:
        p0 = game.getCurrentPlayer()
        p1 = game.getOtherPlayer()
        self.graphicPlayers = [PlayerGraphics(p0, self), PlayerGraphics(p1, self)]
        win = GraphWin("Cannon game" , Const.WIN_WIDTH, Const.WIN_HEIGHT, autoflush=False)
        win.setCoords(Const.WIN_X1, Const.WIN_Y1, Const.WIN_X2, Const.WIN_Y2)
        self.window = win
        # HINT: The constructor needs to create a window, a couple of graphic components and two 
        #PlayerGraphics-objects that in turn create additional components

    def sync(self):
        for p in self.graphicPlayers:
            p.sync(self)
    def getWindow(self):
        return self.window

# HINT: Don't forget to call draw() on every component you create, otherwise they will not be visible

class PlayerGraphics():
    def __init__(self, player: gamemodel.Player, graphics: GameGraphics):
        self.player = player
        # create two points for the rectangle (cannon)
        p1_x = player.getX()-player.game.cannonSize/2
        p1_y = 0
        p2_x = player.getX()+player.game.cannonSize/2
        p2_y = player.game.cannonSize

        self.cannon = Rectangle(Point(p1_x, p1_y), Point(p2_x, p2_y))

        # HINT: Should draw a cannon and a scoreboard immediately 
        #(the Player object knows its position)
    def sync(self):
        self.cannon.draw(gameGraphics)
        # HINT: Typically doesn't draw a projectile when created, but creates one at some point
        #       when sync() is called.
        # HINT: sync() needs to update the score text and draw/update a circle for the projectile if there is one.


""" A somewhat specific input dialog class (adapted from the book) """
class InputDialog:
    """ Creates an input dialog with initial values for angle and velocity and displaying wind """
    def __init__ (self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))
        
        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))
        
        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))
        
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