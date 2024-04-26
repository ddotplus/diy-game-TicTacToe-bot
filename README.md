## Tic-Tac-Toe game in Python (with Bot)

This was originally a Python exercise to write a Tic-Tac-Toe game for two 
players on `3x3` grid. It has been now extended to:
- a general game on `NxN` grid, and also
- a **bot** added for single-player case.

The **bot** is not super smart, but may bring some real fun to the game in spare 
time. If interesting enough, the bot may be upgraded in the future, using 
machine learning models together with bot-vs-bot training data.

### Game in terminal
```
********************************************
****  Tic-Tac-Toe game (play with bot)  ****
********************************************
How smart the bot you want to play with? [0.0-1.0]
   0.0: random beginner; 1.0: full-power bot
  > please input smart level [0.5]:
Do you want to play first? (y/n) [y]: 
Please input grid size of the play board [3]: 4
Do you want continue an unfinished game? (y/n) [n]: 
        ┌───┬───┬───┬───┐
        │ 1 │ 2 │ 3 │ 4 │
        ├───┼───┼───┼───┤
        │ 5 │ 6 │ 7 │ 8 │
        ├───┼───┼───┼───┤
        │ 9 │10 │11 │12 │
        ├───┼───┼───┼───┤
        │13 │14 │15 │16 │
        └───┴───┴───┴───┘
Player1-User (X):
   %% 'a' - print available positions
   %% 'd' - draw game board
   %% 'u' - print users' history
   %% 'q' - quit
  > please input position [1-16]: 2
Player2-Bot (O): 6
        ┌───┬───┬───┬───┐
        │ 1 │ X │ 3 │ 4 │
        ├───┼───┼───┼───┤
        │ 5 │ O │ 7 │ 8 │
        ├───┼───┼───┼───┤
        │ 9 │10 │11 │12 │
        ├───┼───┼───┼───┤
        │13 │14 │15 │16 │
        └───┴───┴───┴───┘
Player1-User (X):
   %% 'a' - print available positions
   %% 'd' - draw game board
   %% 'u' - print users' history
   %% 'q' - quit
  > please input position [1-16]: 
```


### How to run
In Unix / Linux terminal:
- For case of two players:
  `$ python3 tictactoe_2players.py`
- For case of single player against bot:
  `$ python3 tictactoe_with_bot.py`

The game was tested under `Python 3.8.10`.

### MIT License

Copyright (c) 2024 ddotplus@github
