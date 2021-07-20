# Imports everything from both model and graphics
from gamemodel import Game, Projectile
from gamegraphics import GameGraphics, InputDialog
import graphics

# Here is a nice little method you get for free
# It fires a shot for the current player and animates it until it stops
# def graphicFire(game, graphics, angle, vel):
#     player = game.getCurrentPlayer()
#     # create a shot and track until it hits ground or leaves window
#     proj = player.fire(angle, vel)
#     while proj.isMoving():
#         proj.update(1/50)
#         graphics.sync() # This deals with all graphics-related issues
#         update(50) # Waits for a short amount of time before the next iteration
#     return proj

CannonSize = 10
BallRadi = 3

def graphicPlay():
    game = Game(CannonSize,BallRadi)
    ggame = GameGraphics(CannonSize, BallRadi, game.getScore)
    controls = InputDialog(game.getCurrentWind, ggame.quit)
    while True:
        for i in range(2):
            player = game.getCurrentPlayer()
            cannonBall: Projectile = controls.interact(player.fire)
            while cannonBall.isMoving():
                cannonBall.update(1/50)
                ggame.UpdateCannonBall(player.getColor(), cannonBall.getX(), cannonBall.getY())
                graphics.update(50)
            if game.distanceFromTarget(cannonBall.getX(), game.getOtherPlayer().getX()) == 0:
                player.increaseScore()
                ggame.UpdateScore(player.getColor())
            if player.getScore() >= 10:
                break
            game.nextPlayer()
        game.newRound()
        controls.updateWind()

# Run the game with graphical interface
graphicPlay()