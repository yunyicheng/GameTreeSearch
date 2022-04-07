# AI-GTS
This is a course project from CSC384: Intro to AI at University of Toronto. In this project, I implemented an AI agent to play Othello.

## Introduction

Acknowledgements: This project is based on one used in Columbia University’s Artificial Intelligence Course (COMS W4701). Special thanks to Daniel Bauer, who originally developed the starter code.

Othello is a 2-player board game that is played with distinct pieces that are typically black on one side and white on the other side, each side belonging to one player. Our version of the game is played on a chess board of any size, but the typical game is played on an 8x8 board. Players (black and white) take turns placing their pieces on the board.

Placement is dictated by the rules of the game, and can result in the flipping of coloured pieces from white to black or black to white. The rules of the game are explained in detail at https://en.wikipedia.org/wiki/Reversi.

- Objective: The player’s goal is to have a majority of their coloured pieces showing at the end of the game.

- Game Ending: Our version of the game differs from the standard rules described on Wikipedia in one minor point: The game ends as soon as one of the players has no legal moves left.

- Rules: The game begins with four pieces placed in a square in the middle of the grid, two white pieces and two black pieces (Figure 1, at left). Black makes the first move.

At each player’s turn, the player may place a piece of their own colour on an unoccupied square if it “brackets” one or more opponent pieces in a straight line along at least one axis (vertical, horizontal, or diagnonal). For example, from the initial state black can achieve this bracketing by placing a black piece in any of the positions indicated by grey pieces in Figure 1 (in the middle). Each of these potential placements would create a Black-White-Black sequence, thus “bracketing” the White piece. Once the piece is placed, all opponent pieces that are bracketed, along any axis, are flipped to become the same colour as the current player’s. Returning to our example, if black places a piece in Position 6-d in the middle panel of Figure 1, the white piece in position 5-d will become bracketed and consequently will be flipped to black, resulting in the board depicted in the right panel of Figure 1.
<img width="1128" alt="Screen Shot 2022-04-06 at 11 41 07 PM" src="https://user-images.githubusercontent.com/55462866/162115731-31244902-889f-45f6-b614-590d94e32dbc.png">
Now it’s white’s turn to play. All of white’s possibilities at this time are shown as grey pieces in Figure 2 (at left). If white places a piece on 4-c it will cause the black piece in 4-d to be bracketed resulting in the 4-d piece being flipped to white as shown in Figure 2 (at right). To summarize, a legal move for a player is one that results in at least one of its opponents pieces being flipped. Our version of the game ends when one player no longer has any legal moves available.
<img width="746" alt="Screen Shot 2022-04-06 at 11 40 54 PM" src="https://user-images.githubusercontent.com/55462866/162115741-5a96c3b6-cb1f-4b32-9a5d-bb46bedbe81a.png">

## Files
The starter code contains 5 files:

1. `othello_gui.py`, which contains a simple graphical user interface (GUI) for Othello.

2. `othello_game.py`, which contains the game ”manager”. This stores the current game state and communicates with different player AIs.

3. `othello_shared.py`, which contains functions for computing legal moves, captured disks, and successor game states. These are shared between the game manager, the GUI and the AI players.

4. `randy_ai.py`, which specifies an ”AI” player (named Randy) that randomly selects a legal move.

5. `agent.py`, The file of the game agent I implemented.

## Game State Representation
Each game state contains two pieces of information: The current player and the current disks on the board. Throughout our implementation, Player 1 (dark) is represented using the integer 1, and Player 2 (light) is represented using the integer 2.
The board is represented as a tuple of tuples. The inner tuple represents each row of the board. Each entry in the rows is either an empty square (integer 0), a dark disk (integer 1) or a light disk (integer 2). For example, an 8x8 initial state looks like this:

<img width="404" alt="Screen Shot 2022-04-06 at 11 52 38 PM" src="https://user-images.githubusercontent.com/55462866/162116823-cc342792-8bb5-4bfc-bb96-1af0e53baa4a.png">

## Running the Code
You can run the Othello GUI by typing `$python3 othello gui.py -d board size -a agent.py`, where the parameter board size is an integer that determines the dimension of the board upon which you will play and agent.py is the game agent you would like to play against. If you type `$python3 othello gui.py -d board size -a randy ai.py`, you will play against an agent that selects moves randomly, and that is named Randy. Playing a game should bring up a game window. If you play against a game agent, you and the agent will take turns. We recommend that you play against Randy to develop a better understanding of how the game works and what strategies can give you an advantage.

The GUI can take also take two AI programs as command line parameters. When two AIs are specified at the command line you can watch them play against each other. To see Randy play against itself, type `$python3 othello gui.py -d board size -a randy ai.py -b randy ai.py`. You may want to try playing the agents you create against those that are made by your friends.

The GUI is rather minimalistic, so you need to close the window and then restart to play a new game.

## Time Constraints

Your AI player will be expected to make a move within 10 seconds. If no move has been selected, the AI loses the game. This time constraint does not apply for human players.

You may change the time constraint by editing line 32 in othello game.py: TIMEOUT = 10

However, we will run your AI with a timeout of 10 seconds during grading.

## Tasks
### Minimax
You will want to test your Minimax implementations on boards that are only 4x4 in size. This restriction makes the game somewhat trivial: it is easy even for human players to think ahead to the end of the game. When both players play optimally, the player who goes second always wins. However, the default Minimax algorithm, without a depth limit, takes too long even on a 6x6 board.

Write the function `compute_utility(board, color)` that computes the utility of a final game board state (in the format described above). The utility should be calculated as the number of disks of the player’s color minus the number of disks of the opponent. Hint: The function `get_score(board)` returns a tuple (number of dark disks, number of light disks).

Then, implement the method `select_move_minimax(board, color)`. For the time being, you can ignore the limit and caching parameters that the function will also accept; we will return to these later. Your function should select the action that leads to the state with the highest minimax value. The ’board’ parameter is the current board (in the format described above) and the ’color’ parameter is the color of the AI player. We use an integer 1 for dark and 2 for light. The return value should be a (column, row) tuple, representing the move. Implement minimax recursively by writing two functions `minimax_max_node(board, color)` and `minimax_min_node(board, color)`. Again, just ignore the limit and caching parameters for now.

Once you are done you can run your MINIMAX algorithm via the command line using the flag `-m`. If you issue the command ”`$python3 othello gui.py -d 4 -a agent.py -m`” you will play against your agent on a 4x4 board using the MINIMAX algorithm. The command ”`$python3 othello gui.py -d 4 -a agent.py`” will have you play against the same agent using the ALPHA-BETA algorithm. You can also play your agent against Randy with the command ”`$python3 othello gui.py -d 4 -a agent.py -b randy ai.py`”

### Alpha-Beta Pruning
The simple minimax approach becomes infeasible for boards larger than 4x4. To ameliorate this we will write the the function `select_move_alphabeta(board, color)` to compute the best move using alphabeta pruning. The parameters and return values will be the same as for minimax. Once again, you can again ignore the limit, caching and ordering parameters that the function will also accept for the time being; we will return to these later. Much like minimax, your alpha-beta implementation should recursively call two helper functions: `alphabeta_min_node(board, color, alpha, beta)` and `alphabeta_max_node(board,color, alpha, beta)`.

Playing with pruning should speed up decisions for the AI, but it may not be enough to be able to play on boards larger than 4x4. Use the command ”`$python3 othello gui.py -d 4 -a agent.py`” to play against your agent using the ALPHA-BETA algorithm on a 4x4 board.

### Depth Limit
Next we’ll work on speeding up our agents. One way to do this is by setting a depth limit. Your starter code is structured to do this by using the `-l` flag at the command line. For example, if you type `$python3 othello gui.py -d 6 -a agent.py -m -l 5`, the game manager will call your agent’s MINIMAX routine with a depth limit of 5. If you type `$python3 othello gui.py -d 6 -a agent.py -l 5`, the game manager will call your agent’s ALPHA-BETA routine with a depth limit of 5.

Alpha beta will recursively send the ’limit’ parameter to both alphabeta min node and alphabeta max node. Minimax is similar and will recursively sends the ’limit’ parameter to minimax min node and minimax max node. In order to enforce the depth limit in your code, you will want to decrease the limit parameter at each recursion. When you arrive at your depth limit (i.e. when the ’limit’ parameter is zero), use a heuristic function to define the value any non-terminal state. You can call the compute utility function as your heuristic to estimate non-terminal state quality.

### Caching States
We can try to speed up the AI even more by caching states we’ve seen before. To do this, we will want to alter your program so that it responds to the `-c` flag at the command line. To implement state caching you will need to create a dictionary in your AI player (this can just be stored in a global variable on the top level of the file) that maps board states to their minimax value. Modify your minimax and alpha-beta pruning functions to store states in that dictionary after their minimax value is known. Then check the dictionary, at the beginning of each function. If a state is already in the dictionary and do not explore it again.

The starter code is structured so that if you type `$python3 othello gui.py -d 6 -a agent.py -m -c`, the game manager will call your agent’s MINIMAX routines with the ’caching’ flag on. If instead you remove the `-m` and type `$python3 othello gui.py -d 6 -a agent.py -c`, the game manager will call your agent’s ALPHA-BETA routines with the ’caching’ flag on.

### Node Ordering Heuristic
Alpha-beta pruning works better if nodes that lead to a better utility are explored first. To do this, in the Alpha-beta pruning functions, we will want to order successor states according to the following heuristic: the nodes for which the number of the AI player’s disks minus the number of the opponent’s disks is highest should be explored first. Note that this is the same as the utility function, and it is okay to call the utility function to compute this value. This should provide another small speed-up.

Alter your program so that it executes node ordering when the `-o` flag is placed on the command line. The starter code is already structured so that if you type `$python3 othello gui.py -d 6 -a agent.py -o`, the game manager will call your agent’s ALPHA-BETA routines with an ’ordering’ parameter that is equal to 1.

Taken together, the steps above should give you an AI player that is challenging to play against. To play against your agent on an 8x8 board when it is using state caching, alpha-beta pruning and node ordering, type `$python3 othello gui.py -d 8 -a agent.py -c -o`.

### Your Own Heuristic
The prior steps should give you a good AI player, but we have only scratched the surface. There are many possible improvements that would create an even better AI. To improve your AI, create your own game heuristic. You can use this in place of compute utility in your alpha-beta routines.
Some Ideas for Heuristic Functions for Othello Game

1. Consider board locations where pieces are stable, i.e. where they cannot be flipped anymore.

2. Consider the number of moves you and your opponent can make given the current board configuration.

3. Use a different strategy in the opening, mid-game, and end-game.

You can also do your own research to find a wide range of other good heuristics (for example, here is a good start: http://www.radagast.se/othello/Help/strategy.html).
