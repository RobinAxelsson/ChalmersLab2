from gamemodel import Game, HelpText, Projectile, Const as GameConst
from gamegraphics import GameGraphics, InputDialog, ValidateInput
import graphics
import sys

def graphicPlay(cannonSize, ballRadi):
    game = Game(cannonSize,ballRadi)
    ggame = GameGraphics(game)
    controls = InputDialog(game.getCurrentWind) # control is handed the quit function
    winner = None
    while True:
        player = game.getCurrentPlayer()
        cannonBall: Projectile = controls.interact(player.fire) # the fire function is given to the control dialog
        
        while cannonBall.isMoving():
            cannonBall.update(1/50)
            ggame.updateCannonBall(player.getColor(), cannonBall.getX(), cannonBall.getY())
            graphics.update(50)
        #if the player hits enemy cannon and wins round the loop will end
        if game.distanceFromTarget(cannonBall.getX(), game.getOtherPlayer().getX()) == 0:
            player.increaseScore()
            ggame.UpdateScore(player.getColor())
            if player.getScore() == GameConst.WINNER_SCORE: #First to max score
                winner = player
                break
            game.newRound()
            controls.updateWind()
        game.nextPlayer() #if no hit the round loop continues and next player attacks

    print("Winner: " + winner.getColor() + ", congratulations!") # End of Game
    reply = input('Play again? Y/n: ')
    if reply == 'Y' or reply == 'y':
        controls.close()
        ggame.close()
        graphicPlay(cannonSize, ballRadi)
    else:
        print('GG')
        quit()

if '__main__' == __name__:

    if len(sys.argv) == 1:
        graphicPlay(GameConst.DEFAULT_CANNON_SIZE, GameConst.DEFAULT_BALL_RADIUS)
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg == '--help':
            HelpText.display()
        else:
            print("Invalid argument input.")
            print(HelpText.tryHelp)
    elif len(sys.argv) == 3:
            cannonSize = ValidateInput.cannonSize(sys.argv[1])
            cannonBallSize = ValidateInput.ballSize(sys.argv[2])
            if cannonSize != None and cannonBallSize != None:
                graphicPlay(cannonSize, cannonBallSize)
            else:
                print(HelpText.tryHelp)