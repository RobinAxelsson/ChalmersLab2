from gamemodel import Game, HelpText, Projectile, Const as GameConst
from gamegraphics import GameGraphics, InputDialog
import graphics
import sys

def graphicPlay(cannonSize, ballRadi):
    game = Game(cannonSize,ballRadi)
    ggame = GameGraphics(cannonSize, ballRadi, game.getScore)
    controls = InputDialog(game.getCurrentWind, ggame.quit) # control is handed the quit function
    hasWinner = False   
    while hasWinner == False:

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
                if player.getScore() == 10: #First to ten wins the game
                    hasWinner == True
                ggame.UpdateScore(player.getColor())
                game.nextPlayer()
                game.newRound()
                controls.updateWind()
                break 
            game.nextPlayer() #if no hit the round loop continues and next player attacks

    winner = game.players[0] if game.players[0].getScore == 10 else game.players[1]
    controls.quitGame()
    print("Winner: " + winner.getColor() + ", congratulations!") # End of Game
    reply = input('Play again? Y/n: ')
    if reply == 'Y' or 'y':
        graphicPlay(cannonSize, ballRadi)
    else:
        print('GG')

if '__main__' == __name__:
    if len(sys.argv) == 1:
        graphicPlay(GameConst.DEFAULT_CANNON_SIZE, GameConst.DEFAULT_BALL_RADIUS)
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg == '--help':
            HelpText.display()
        else:
            print("Arg2 (cannonSize) and arg3 (cannonballRadius) is needed.")
            print(HelpText.tryHelp)
    elif len(sys.argv) == 3:
            try:
                cannonSize = int(sys.argv[1])
                cannonBallSize = int(sys.argv[2])
                graphicPlay(cannonSize, cannonBallSize)
            except ValueError:
                print("Arg2(cannonSize) and arg3 (cannonballRadius) must be integers.")
                print(HelpText.tryHelp)
            else:
                print(HelpText.tryHelp)