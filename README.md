
# Arduino serial interface
Doesn't appear to be a way to choose which row of players yet.
There is a certain time delay for each time we try to send a command to the Arduino so we need to avoid sending the same command over and over again (i.e. repeatedly sending the command to kick could cause the players to just quiver as they go backwards.
 - horizontal : make players horizontal
 - clockwise : clockwise full revolution
 - anticlockwise : anticlockwise revolution
 - stand : go back to being vertical after being horozontal
 - kick : kick
 - moveTo : horozontally move from (0 - 110), 0 being leftmost point on board, 110 being rightmost.


# Player Controller

Each player only has access to their third of the board, there is no overlap between areas that each player can reach. At 0 player 1 would be at the leftmost edge of their third, at 110 player 1 would be at the right most edge of their third.

The Player Controller will work out which third the ball is expected to be in, then which player can reach this ball, then (given this player) how to move the motor to reach the ball.

If the ball is behind the set of players I suggest making them go horozontal so that the don't interupt the forward movement of the ball.

We need some kind of way of storing the information:
- the orientation of the players (horizontal or vertical)
- if the players are currently in the process of kicking

# Ball Path Finder
I suggest that we make a common interface for the different classes which predict ball trajectories. This will make it easy to swap them and test out which one works best, without having to change the surrounding code. 

