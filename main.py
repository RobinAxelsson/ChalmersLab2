# Imports everything from both model and graphics
from gamemodel import Game
from gamegraphics import GameGraphics, InputDialog


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
    ggame = GameGraphics(CannonSize, BallRadi)
    controls = InputDialog()
    controls.interact()

# Run the game with graphical interface
graphicPlay()
wait = input("Press Enter to terminate.")