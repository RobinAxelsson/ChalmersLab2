from graphics import update
from math import sin,cos,radians,copysign
import random
import enum


class Projectile:
    """
        Constructor parameters:
        angle and velocity: the initial angle and velocity of the projectile 
            angle 0 means straight east (positive x-direction) and 90 straight up
    """
    def __init__(self, angle, velocity, wind, xPos, yPos, xLower, xUpper):
        self.yPos = yPos
        self.xPos = xPos
        self.xLower = xLower
        self.xUpper = xUpper
        theta = radians(angle)
        self.xvel = velocity*cos(theta)
        self.yvel = velocity*sin(theta)
        self.wind = wind

    """ 
        Advance time by a given number of seconds
        (typically, time is less than a second, 
         for large values the projectile may move erratically)
    """
    def update(self, time):
        # Compute new velocity based on acceleration from gravity/wind
        yvel1 = self.yvel - 9.8*time
        xvel1 = self.xvel + self.wind*time
        
        # Move based on the average velocity in the time period 
        self.xPos = self.xPos + time * (self.xvel + xvel1) / 2.0
        self.yPos = self.yPos + time * (self.yvel + yvel1) / 2.0
        
        # make sure yPos >= 0
        self.yPos = max(self.yPos, 0)
        
        # Make sure xLower <= xPos <= mUpper   
        self.xPos = max(self.xPos, self.xLower)
        self.xPos = min(self.xPos, self.xUpper)
        
        # Update velocities
        self.yvel = yvel1
        self.xvel = xvel1
        
    """ A projectile is moving as long as it has not hit the ground or moved outside the xLower and xUpper limits """
    def isMoving(self):
        return 0 < self.getY() and self.xLower < self.getX() < self.xUpper

    def getX(self):
        return self.xPos

    """ The current y-position (height) of the projectile". Should never be below 0. """
    def getY(self):
        return self.yPos

class Color(enum.Enum):
    blue = 0
    red = 1

class Const:
    LEFT_END = -110
    RIGHT_END = 110
    P0_POS = -90
    P1_POS = 90
    WIND_MIN = -10
    WIND_MAX = 10
    STARTING_COLOR = Color.blue
    DEFAULT_ANGLE = 45
    DEFAULT_VELOCITY = 40

class Game:
    def __init__(self, cannonSize, ballRadi):
        self.wind = Game.__newWind()
        self.ballSize = ballRadi # radius cannonballs
        self.cannonSize = cannonSize # height (square)
        self.players = [Player(Color.blue, Const.P0_POS, self), Player(Color.red, Const.P1_POS, self)]
        self.currentIndex = 0 if Const.STARTING_COLOR == Color.blue else 1

    def getScore(self, color):
        player = self.players[0] if color == Color.blue else self.players[1]
        return player.getScore()
    def __newWind():
        return random.randint(Const.WIND_MIN, Const.WIND_MAX)
    def getPlayers(self):
        return self.players
    def getCurrentPlayer(self):
        return self.players[self.currentIndex]
    def getOtherPlayer(self):
        otherIndex = 1 if self.currentIndex == 0 else 0
        return self.players[otherIndex]
    def getCurrentPlayerNumber(self):
        return self.currentIndex
    def getCannonSize(self):
        return self.cannonSize
    def getBallSize(self):
        return self.ballSize
    def setCurrentWind(self, wind):
        self.wind = wind
    def getCurrentWind(self):
        return self.wind
    def nextPlayer(self):
        self.currentIndex = 1 if self.currentIndex == 0 else 0
    def newRound(self):
        self.wind = Game.__newWind()
        return self.wind
    def distanceFromTarget(self, xCannonBall, xTargetCannon):
        absDistX = abs(xCannonBall - xTargetCannon)
        trueDistX = absDistX - (self.ballSize + self.cannonSize/2.0)
        if trueDistX <= 0:
            return 0
        missToTheLeft = (xCannonBall - xTargetCannon) < 0
        distX = trueDistX*-1.0 if missToTheLeft else trueDistX
        return distX

class Player:
    def __init__(self, color: Color, positionX:int, game: Game):
        self.game: Game = game
        self.color = color
        self.score = 0
        self.x = positionX
        self.projectile: Projectile = None
        self.aim = (Const.DEFAULT_ANGLE, Const.DEFAULT_VELOCITY)
        self.firingDirection = 1 if self.color == Color.blue else -1
        
   #HINT: It should probably take the Game that creates it as parameter and some additional properties that differ between players (like firing-direction, position and color)
    
    """ Create and return a projectile starting at the centre of this players cannon. Replaces any previous projectile for this player. """
    def fire(self, angle, velocity):
        angle = angle if self.firingDirection > 0 else 180-angle
        self.aim = (angle, velocity)
        proj = Projectile(angle, velocity, self.game.getCurrentWind(), self.x, self.game.getCannonSize()/2.0, Const.LEFT_END, Const.RIGHT_END)
        self.projectile = proj
        return proj

    def getProjectile(self):
        return self.projectile

    """ Gives the x-distance from this players cannon to a projectile. If the cannon and the projectile touch (assuming the projectile is on the ground and factoring in both cannon and projectile size) this method should return 0"""
    def projectileDistance(self, proj: Projectile):
        # absolute difference between center of cannonball and center of enemy cannon
        absDistX = abs(proj.getX() - self.getX())
        trueDistX = absDistX - (self.game.ballSize + self.game.cannonSize/2.0)
        if trueDistX <= 0:
            return 0
        missToTheLeft = (proj.getX() - self.getX()) < 0
        distX = trueDistX*-1.0 if missToTheLeft else trueDistX
        return distX

    def getScore(self):
        return self.score
    def increaseScore(self):
        self.score += 1
    def getColor(self):
        return self.color
    """ The x-position of the centre of this players cannon """
    def getX(self):
        return self.x
    """ The angle and velocity of the last projectile this player fired, initially (45, 40) """
    def getAim(self):
        return self.aim


