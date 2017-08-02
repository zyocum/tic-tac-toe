#!/usr/bin/env python3

"""Run a game of Tic-Tac-Toe with curses"""

import curses
import numpy as np

UP = ord('k'), ord('K'), curses.KEY_UP
DOWN = ord('j'), ord('J'), curses.KEY_DOWN
RIGHT = ord('l'), ord('L'), curses.KEY_RIGHT
LEFT = ord('h'), ord('H'), curses.KEY_LEFT

X = ord('x'), ord('X')
O = ord('o'), ord('O')

CLEAR = ord('c'), ord('C'),
DELETE = ord('~'), ord('\x7f'), curses.KEY_BACKSPACE, curses.KEY_DC
QUIT = ord('q'), ord('Q')

BOARD = (
    '┌─┬─┬─┐\n'
    '│{}│{}│{}│\n'
    '├─┼─┼─┤\n'
    '│{}│{}│{}│\n'
    '├─┼─┼─┤\n'
    '│{}│{}│{}│\n'
    '└─┴─┴─┘\n'
)

def new_game():
    return np.array([[None] * 3] * 3)

def winner(game):
    """Determine if there is a winner and if so return the winning symbol"""
    for player in chr(X[-1]), chr(O[-1]):
        if any((
            # check diagonals
            set(game.diagonal()) == {player},
            set(np.fliplr(game).diagonal()) == {player},
            # check rows
            {player} in map(set, game),
            # check columns
            {player} in map(set, game.T)
        )):
            return player

def cell(y, x):
    """Derive the appropriate game state cell from curses window y, x
    coordinates by correcting for the board offsets
    
    y: y position in the curses window
    x: x position in the curses window
    """
    return y // 2, x // 2

def key(value):
    """Get the firt character from the key binding integer values"""
    key, *_ = value
    return chr(key)

def run(game, debug=False):
    """Start a game in a curses window
    
    game: the current state as a 3x3 numpy array
    """
    if not isinstance(game, np.ndarray) or game.shape != (3, 3):
        raise ValueError('invalid game state (must be a 3x3 numpy.array)')
    # set up curses window
    window = curses.initscr()
    window.keypad(True)
    curses.noecho()
    window.erase()
    try:
        y, x = 1, 1 # start cursor in the upper left cell
        value = None
        # loop until the user quits
        while not value in QUIT:
            board = BOARD.format(*((v or ' ') for v in game.flatten()))
            window.addstr(0, 0, board)
            message = (
                f'{key(LEFT)}:left {key(RIGHT)}:right {key(UP)}:up '
                f'{key(DOWN)}:down '
                f'{key(X)}:"X" {key(O)}:"O" {key(DELETE)}:delete '
                f'{key(CLEAR)}:clear '
                f'{key(QUIT)}:quit'
            )
            window.addstr(9, 0, message)
            value = window.getch(y, x)
            # check for relevant input
            if value in UP:
                y = max(1, y - 2)
            elif value in DOWN:
                y = min(5, y + 2)
            elif value in RIGHT:
                x = min(5, x + 2)
            elif value in LEFT:
                x = max(1, x - 2)
            elif value in X:
                game[cell(y, x)] = chr(X[-1])
            elif value in O:
                game[cell(y, x)] = chr(O[-1])
            elif value in DELETE:
                game[cell(y, x)] = None
            elif value in CLEAR:
                game = new_game()
            else:
                curses.flash()
            player = winner(game)
            # show game status
            if player:
                window.addstr(7, 0, f'{player} wins!')
            elif np.all(game != None): # draw game
                window.addstr(7, 0, "Draw!  ")
            else: # clobber the status
                window.addstr(7, 0, ' ' * 7)
            if debug:
                window.addstr(13, 0, f'value: {value} ')
                window.addstr(14, 0, f'cursor: ({x}, {y})')
                window.addstr(15, 0, f'game:\n{game}')
    finally:
        curses.endwin()

if __name__ == '__main__':
    run(new_game())
