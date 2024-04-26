"""
Tic-Tac-Toe Game for Two Players

MIT license
Copyright (c) 2024 ddotplus@github
"""


def init_game(board_size=3, users_hist=None):
    """ Initialize tic-tac-toe game
    Input:
        board_size: int, grid size n of a play board nxn
        users_hist: list, users' position history, eg.
            [[usr1_pos1, usr1_pos2, usr1_pos3], [usr2_pos1, usr2_pos2]]
            if there is, otherwise use the default.
    Output:
        users_hist: list, initialized or checked history
        win_lines: list of sets, on-a-line positions for winning conditions
    """
    board_pos_label = list(range(1, 1 + board_size ** 2))
    if users_hist is None:
        users_hist = [[], []]
    else:
        ## check consistence
        if len(users_hist[0]) != len(set(users_hist[0])) \
           or len(users_hist[1]) != len(set(users_hist[1])):
            raise ValueError("init_game(): <users_hist> position duplicates")
        if len(set(sum(users_hist, [])) - set(board_pos_label)) > 0:
            raise ValueError("init_game(): <users_hist> out of position range")
        if len(users_hist[0]) < len(users_hist[1]) or \
           len(users_hist[0]) > len(users_hist[1]) + 1:
            raise ValueError("init_game(): <users_hist> wrong lengths")
    ## lines on play board for winning
    win_lines = []
    tmp = list(range(board_size))
    for i in range(board_size):
        win_lines.append({1 + x + i * board_size for x in tmp})
        win_lines.append({1 + x * board_size + i for x in tmp})
    win_lines.append({1 + x * board_size + x for x in tmp})
    win_lines.append({(1+x) * board_size - x for x in tmp})
    return users_hist, win_lines


def display(board_size, position_list):
    """ Box-drawing of tic-tac-toe play board
    Input:
        board_size: int, grid size n of a play board nxn, with n < 32,
              i.e. <= sqrt(999), as each text box only for 3 digits
        position_list: list, a list of position numbers within [1, n**2], or
              position history of two users
    Output:
        boxdraw: list, recorded in a list of line strings
    """
    if board_size >= 32:
        raise ValueError("display(): <board_size> >= 32, as 32**2 > 999.")
    if isinstance(position_list[0], list):
        tmp = sum(list(position_list), [])
    else:
        tmp = list(position_list)
    if len(tmp) > 0 and (min(tmp) < 1 or max(tmp) > board_size ** 2):
        raise ValueError("display(): <position_list> out of range: [1,n**2]")
    if isinstance(position_list[0], list):
        ## case of player-1/2 position history
        show_list = [str(i) for i in list(range(1, 1 + board_size ** 2))]
        for y in position_list[0]:
            show_list[y-1] = 'X'
        for y in position_list[1]:
            show_list[y-1] = 'O'
    else:
        ## case of single position list
        if len(position_list) == board_size**2:  ## ready to show
            show_list = position_list
        else:                                ## fill incomplete list
            show_list = [' '] * board_size ** 2
            for y in position_list:
                show_list[y-1] = str(y)
    boxdraw = ["┌───" + "┬───" * (board_size - 1) + "┐"]
    for i in range(board_size):
        row = [f'{s: ^3}' for s in show_list[i*board_size:(i+1)*board_size]]
        for j in range(board_size, -1, -1):
            row.insert(j, '│')
        boxdraw.append(''.join(row))
        boxdraw.append("├───" + "┼───" * (board_size - 1) + "┤")
    boxdraw[-1] = "└───" + "┴───" * (board_size - 1) + "┘"
    hspace = max([1, 8-board_size//4-board_size//6])
    for line in boxdraw:
        print(' ' * hspace + line.replace('X', '\033[31mX\033[0;0m')
              .replace('O', '\033[34mO\033[0;0m'))  # with font colors
    return boxdraw


def update_winlines(win_lines, users_hist):
    """ remove useless sets in <win_lines>,
        to reduce unnecessary searching space of winning conditions
    """
    for i in range(len(win_lines)-1, -1, -1):
        if len(win_lines[i].intersection(set(users_hist[0]))) > 0 and \
           len(win_lines[i].intersection(set(users_hist[1]))) > 0:
            win_lines.pop(i)
    return win_lines


def check_win_status(win_lines, users_hist):
    """ Check if any player wins
    Input:
        win_lines: list of sets, collection of winning conditions
        users_hist: list, users' position history
    Output:
        win: int, status of win status
             0: game continues
             1: game stops, player-1 wins
             2: game stops, player-2 wins
             -1: game stops, no one wins
    """
    win = 0
    for w in win_lines:
        if len(w - set(users_hist[0])) == 0:
            win = 1
            print('Player1 (X) won the game, congratulations!')
        if len(w - set(users_hist[1])) == 0:
            win = 2
            print('Player2 (O) won the game, congratulations!')
    win_lines = update_winlines(win_lines, users_hist)
    if len(win_lines) == 0:
        win = -1
        print('No one can win the game any more!\nThe game is over.')
    return win


def hist_input(board_size):
    """ Get an input of users' previous game history if user wants
    Input:
        board_size: int, grid size n of a play board nxn
    Output:
        users_hist: list, checked input from user
    """
    users_hist = None
    inp = input('Do you want continue an unfinished game? (y/n) [n]: ')
    if inp.lower() == 'y' or inp.lower() == 'yes':
        print("   %% 'n' - just pass, start a new game")
        print('  > please input history of two users in list form below:')
        print('    [[usr1_pos1, usr1_pos2, ...], [usr2_pos1, ...]]')
        inp = input('    ')
        chk_input = True
        while chk_input:
            if inp.lower() == 'n':
                print('Start a new game now ...')
                break
            try:
                ## exec() cannot modify local var directly, work around
                ldict = {}
                exec('a = ' + inp, globals(), ldict)
                users_hist = ldict['a']
            except SyntaxError:
                print('  > not valid expression, try again:')
                inp = input('    ')
                continue
            if not isinstance(users_hist, list):
                print('  > not a list, try again:')
                inp = input('    ')
            elif len(users_hist) != 2 or \
                    not isinstance(users_hist[0], list) or \
                    not isinstance(users_hist[1], list):
                print('  > not a list of two lists, try again:')
                inp = input('    ')
            elif len(set(sum(users_hist[0:2], []))
                     - set(range(1, board_size ** 2 + 1))) > 0:
                print(f'  > not int or out of [1,{board_size ** 2}], '
                      + 'try again:')
                inp = input('    ')
            elif len(sum(users_hist, [])) > len(set(sum(users_hist, []))):
                print(f'  > duplicate position numbers, try again')
                inp = input('    ')
            elif len(users_hist[0]) != len(users_hist[1]) \
                    and len(users_hist) != 1+len(users_hist[1]):
                print(f'  > improper lengths from two users, try again')
                inp = input('    ')
            else:
                chk_input = False
    return users_hist


def get_input(board_size, users_hist, available_pos):
    """ Get an input of a proper position chosen by user
    Input:
        board_size: int, grid size n of a play board nxn
        users_hist: list, users' position history
        available_pos: list, available positions on play board
    Output:
        inp: user chosen position
    """
    print("   %% 'a' - print available positions")
    print("   %% 'd' - draw game board")
    print("   %% 'u' - print users' history")
    print("   %% 'q' - quit")
    inp = input(f'  > please input position [1-{board_size ** 2}]: ')
    while not inp.isdigit() or (int(inp) not in available_pos):
        if inp == 'a':
            print(f'  available positions:')
            print(f'    {available_pos}')
            inp = input('  > input your position choice: ')
        elif inp == 'd':
            display(board_size, users_hist)
            inp = input(f'  > input position [1-{board_size ** 2}]: ')
        elif inp == 'u':
            print("  players' history:")
            print(f'    {users_hist}')
            inp = input('  > input your position choice: ')
        elif inp == 'q':
            print("Users' history (in case to continue later):")
            print(f'    {users_hist}')
            print('Quit game now.')
            exit(0)
        else:
            inp = input(f'  > invalid, try again [1-{board_size ** 2}]: ')
    return int(inp)


def main_2players():
    """ Two-players version (i.e. Player1 vs Player2)
    """
    print('****************************************')
    print('****  Tic-Tac-Toe game (2 players)  ****')
    print('****************************************')

    ## initialize a game
    board_size_n = 3                   ## by default
    p = input('Please input grid size of the play board [3]: ')
    while len(p) > 0 and (not p.isdigit() or int(p) < 3):
        p = input('  > not an integer or too small (<3). try again [3]: ')
    if len(p) > 0:
        board_size_n = int(p)
    users_history = hist_input(board_size_n)
    users_record, win_line = init_game(board_size_n, users_history)

    display(board_size_n, users_record)
    available_pos_label = list(set(range(1, board_size_n ** 2 + 1))
                               - set(users_record[0])
                               - set(users_record[1]))
    win_status = 0
    while win_status == 0:
        if len(users_record[0]) == len(users_record[1]):
            print('Player1 (X):')
            p = get_input(board_size_n, users_record, available_pos_label)
            users_record[0].append(p)
        elif len(users_record[0]) == 1 + len(users_record[1]):
            print('Player2 (O):')
            p = get_input(board_size_n, users_record, available_pos_label)
            users_record[1].append(p)
        else:
            raise ValueError('main(): <users_record> lengths go wrong :()')
        available_pos_label.remove(p)
        display(board_size_n, users_record)
        win_status = check_win_status(win_line, users_record)
    display(board_size_n, users_record)
    print('')


if __name__ == '__main__':
    main_2players()
