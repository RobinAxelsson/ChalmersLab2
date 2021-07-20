# Imports everything from both model and graphics
from gamemodel import Game, Projectile
from gamegraphics import GameGraphics, InputDialog
import graphics

CannonSize = 10
BallRadi = 3

def graphicPlay():
    game = Game(CannonSize,BallRadi)
    ggame = GameGraphics(CannonSize, BallRadi, game.getScore)
    controls = InputDialog(game.getCurrentWind, ggame.quit) # control is handed the quit function
    hasWinner = False
    while hasWinner == False:
        #round starts here
        for i in range(2):
            player = game.getCurrentPlayer()
            cannonBall: Projectile = controls.interact(player.fire) # the fire function is given to the control object
            while cannonBall.isMoving():
                cannonBall.update(1/50)
                ggame.UpdateCannonBall(player.getColor(), cannonBall.getX(), cannonBall.getY())
                graphics.update(50)
            #if the player hits enemy cannon
            if game.distanceFromTarget(cannonBall.getX(), game.getOtherPlayer().getX()) == 0:
                player.increaseScore()
                ggame.UpdateScore(player.getColor())
            #first to ten
            if player.getScore() == 10:
                hasWinner == True
            game.nextPlayer()
        game.newRound()
        controls.updateWind()
    winner = game.players[0] if game.players[0].getScore == 10 else game.players[1]
    print("Winner: " + winner.getColor() + ", congratulations!")

if '__main__' == __name__:
    graphicPlay()