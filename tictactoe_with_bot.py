"""
Tic-Tac-Toe Game with Bot

MIT license
Copyright (c) 2024 ddotplus@github
"""

from tictactoe_2players import *
from time import sleep
import random


def find_win_pos_best(user_hist, available_pos, win_lines, N=1):
    """ find N positions for user/bot to satisfy winning lines
    Input:
        user_hist: list, position history for a given user
        available_pos: list, available positions on play board
        win_lines: list of sets, collection of winning conditions
        N: int, num of positions to fill before satisfy a winning line
    Output:
        win_pos_best: list, most frequent winning positions
    """
    win_pos = []
    if len(user_hist) == 0:    ## don't do anything for totally new game
        return win_pos
    else:
        for wl in win_lines:
            missing_pos = list(wl - set(user_hist))
            missing_not_available = set(missing_pos)-set(available_pos)
            if (len(missing_pos) == N) and (len(missing_not_available) == 0):
                win_pos = win_pos + missing_pos
    if len(win_pos) == 0:
        return win_pos
    elif len(set(win_pos)) == 1:
        return list(set(win_pos))
    ## 2+ distinct positions in win_pos, find best one(s)
    win_pos_dict = {k: win_pos.count(k) for k in set(win_pos)}
    count_max = max(win_pos_dict.values())
    win_pos_best = [k for k in win_pos_dict if win_pos_dict[k] == count_max]
    return win_pos_best


def get_input_from_bot(users_hist, available_pos, win_lines,
                       board_size, bot_level):
    """ Get a proper position from bot
        (thinking only (N-1)-Steps ahead at most)
    Input:
        user_hist: list, position history for a given user
        available_pos: list, available positions on play board
        win_lines: list of sets, collection of winning conditions
        board_size: int, grid size n of a play board nxn
        bot_level: float, smart level of bot
    Output:
        pos_chosen: int, position chosen for the bot
    """
    ## set users_hist_ordered[0] always bot
    if len(users_hist[0]) > len(users_hist[1]):   ## i.e. bot_role = 2
        users_hist_ordered = users_hist[::-1]
    else:
        users_hist_ordered = users_hist
    ## find most frequent win_pos for Bot/User, then Bot chooses one if exists
    bot_prob = bot_level ** 1.5 + 1e-6      ## twist for better user experience
    for i in range(1, board_size):
        if random.random() < bot_prob:
            win_pos_i = find_win_pos_best(users_hist_ordered[0], available_pos,
                                          win_lines, i)
            if len(win_pos_i) > 0:
                return random.choice(win_pos_i)
        if random.random() < bot_prob:
            win_pos_i = find_win_pos_best(users_hist_ordered[1], available_pos,
                                          win_lines, i)
            if len(win_pos_i) > 0:
                return random.choice(win_pos_i)
    ## find nothing, then pick up any available position
    pos_chosen = random.choice(available_pos)
    return pos_chosen


def bot_vs_bot_stats(board_size, bot1_level, bot2_level, n_games=10000):
    """ Statistics of bot against bot games for user experience improvement
    Input:
        board_size: int, grid size n of a play board nxn
        bot1_level: float, smart level for bot-1, range: [0,1]
        bot2_level: float, smart level for bot-2, range: [0,1]
        n_games: int, number of games to test for statistics
    Output:
        bot1_win_rate: float, percentage of bot-1 wins
        bot2_win_rate: float, percentage of bot-2 wins
        draw_rate: float, percentage of no one wins
    """
    if board_size < 3:
        raise ValueError('bot_vs_bot_stats(): input <board_size> less than 3!')
    if bot1_level < 0 or bot1_level > 1:
        raise ValueError('bot_vs_bot_stats(): input <bot1_level> not in [0,1]')
    if bot2_level < 0 or bot2_level > 1:
        raise ValueError('bot_vs_bot_stats(): input <bot2_level> not in [0,1]')

    bot1_win_rate = 0
    bot2_win_rate = 0
    draw_rate = 0
    for i in range(int(n_games)):
        users_record, win_line = init_game(board_size)
        available_pos_label = list(range(1, board_size**2+1))
        win_status = 0
        while win_status == 0:
            if len(users_record[0]) == len(users_record[1]):
                p = get_input_from_bot(users_record, available_pos_label,
                                       win_line, board_size, bot1_level)
                users_record[0].append(p)
            else:
                p = get_input_from_bot(users_record, available_pos_label,
                                       win_line, board_size, bot2_level)
                users_record[1].append(p)
            win_status = check_win_status(win_line, users_record)
        if win_status == 1:
            bot1_win_rate += 1
        elif win_status == 2:
            bot2_win_rate += 1
        else:
            draw_rate += 1
    bot1_win_rate = round(bot1_win_rate/n_games, 3)
    bot2_win_rate = round(bot2_win_rate/n_games, 3)
    draw_rate = round(draw_rate/n_games, 3)
    return bot1_win_rate, bot2_win_rate, draw_rate


def main_play_with_bot():
    """ Play-with-Bot version
    """
    print('********************************************')
    print('****  Tic-Tac-Toe game (play with bot)  ****')
    print('********************************************')

    ## smart level of the bot
    bot_level = 0.5                ## by default
    print('How smart the bot you want to play with? [0.0-1.0]')
    print('   0.0: random beginner; 1.0: full-power bot')
    p = input('  > please input smart level [0.5]:')
    while len(p) > 0 and (not isinstance(p, (float, int))
                          or (p < 0 or p > 1)):
        p = input('  > not a float number in [0,1]. try again [0.5]: ')
    if len(p) > 0:
        bot_level = float(p)

    ## who plays first
    bot_role = 2                   ## user first, by default
    p = input('Do you want to play first? (y/n) [y]: ')
    if len(p) > 0 and not (p.lower() == 'y' or p.lower() == 'yes'):
        bot_role = 1

    ## initialize a game
    board_size_n = 3               ## by default
    p = input('Please input grid size of the play board [3]: ')
    while len(p) > 0 and (not p.isdigit() or int(p) < 3):
        p = input('  > not a number or too small (<3). try again [3]: ')
    if len(p) > 0:
        board_size_n = int(p)
    users_history = hist_input(board_size_n)
#    users_history = [[2, 7], [5, 4]]    ## test example
    users_record, win_line = init_game(board_size_n, users_history)

    try_again = 1
    while try_again > 0:
        if try_again > 1:
            users_record, win_line = init_game(board_size_n)

        display(board_size_n, users_record)
        available_pos_label = list(set(range(1, board_size_n**2+1))
                                   - set(users_record[0])
                                   - set(users_record[1]))
        win_status = 0
        while win_status == 0:
            bot_turn = 0
            if len(users_record[0]) == len(users_record[1]):
                if bot_role == 1:
                    sleep(0.5)
                    p = get_input_from_bot(users_record, available_pos_label,
                                           win_line, board_size_n, bot_level)
                    print('Player1-Bot (X): ' + str(p))
                    bot_turn = 1
                else:
                    print('Player1-User (X):')
                    p = get_input(board_size_n, users_record,
                                  available_pos_label)
                users_record[0].append(p)
            elif len(users_record[0]) == 1 + len(users_record[1]):
                if bot_role == 1:
                    print('Player2-User (O):')
                    p = get_input(board_size_n, users_record,
                                  available_pos_label)
                else:
                    sleep(0.5)
                    p = get_input_from_bot(users_record, available_pos_label,
                                           win_line, board_size_n, bot_level)
                    print('Player2-Bot (O): ' + str(p))
                    bot_turn = 1
                users_record[1].append(p)
            else:
                raise ValueError('main(): <users_record> lengths go wrong :(')
            available_pos_label.remove(p)
            if bot_turn == 1:
                display(board_size_n, users_record)
            win_status = check_win_status(win_line, users_record)
        display(board_size_n, users_record)
        print('-----------------------------------------')
        p = input('Do you want to play again (a new game)? (y/n) [y]: ')
        if p.lower() == 'n' or p.lower() == 'no':
            try_again = 0
        else:
            try_again += 1


def main_bot_vs_bot():
    """ test example to check win rates
    """
    import io
    import sys
    text_trap = io.StringIO()
    sys.stdout = text_trap

    board_size_n = 4
    bot1_level = 0.4
    bot2_level = 0.4
    b1r, b2r, dr = bot_vs_bot_stats(board_size_n, bot1_level, bot2_level)

    sys.stdout = sys.__stdout__
    print('win rates of bot1 vs bot2 on {}x{} grid:'.format(
         board_size_n, board_size_n))
    print('bot1 ({}): {:.3f}'.format(bot1_level, b1r))
    print('bot2 ({}): {:.3f}'.format(bot2_level, b2r))
    print('draw: {:.3f}'.format(dr))


def main_bot_vs_bot_tables():
    """ test example to get tables of win rates for bots at different levels
    """
    import io
    import sys

    board_size_n = 3
    levels = [i/10 for i in range(11)]
    table_bot1_win = ['## table of bot-1 win rate on {}x{} grid'.format(
                 board_size_n, board_size_n)]
    table_bot2_win = ['## table of bot-2 win rate on {}x{} grid'.format(
                 board_size_n, board_size_n)]
    table_draw = ['## table of draw rate on {}x{} grid'.format(
                 board_size_n, board_size_n)]
    column_names = '# bot1_level, ' + ', '.join(['bot2_'+str(i) for i in levels])
    table_bot1_win.append(column_names)
    table_bot2_win.append(column_names)
    table_draw.append(column_names)

    text_trap = io.StringIO()
    sys.stdout = text_trap
    for l1 in levels:
        w1r = [str(l1)]
        w2r = [str(l1)]
        wdr = [str(l1)]
        for l2 in levels:
            b1r, b2r, dr = bot_vs_bot_stats(board_size_n, l1, l2)
            w1r.append('{:.3f}'.format(b1r))
            w2r.append('{:.3f}'.format(b2r))
            wdr.append('{:.3f}'.format(dr))
        table_bot1_win.append(', '.join(w1r))
        table_bot2_win.append(', '.join(w2r))
        table_draw.append(', '.join(wdr))

    sys.stdout = sys.__stdout__
    print('## win rates for games among bots of different smart levels')
    print('')
    for s in table_bot1_win:
        print(s)
    print('')
    for s in table_bot2_win:
        print(s)
    print('')
    for s in table_draw:
        print(s)


if __name__ == '__main__':
    main_play_with_bot()        ## for user to play games with bots
#    main_bot_vs_bot()           ## calc win rates given smart levels of bots
#    main_bot_vs_bot_tables()    ## tables of win rates at sampled smart levels

