"""
Creative assignment for BIO345
Alex Kazaiev
"""
import curses
import random
import time

TITLE_MESSAGE = "BIO345 Activity 1.2 - DEEP HISTORY"
LOADING_MESSAGE = "Loading Earth History Simulation"

TYPE_SPEED = 0.05
PAUSE_BEFORE_MATRIX = 2
MATRIX_DURATION = 5
MATRIX_SPEED = 0.05
MOVE_LOADING_DELAY = 2

MATRIX_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*"

def show_centered_message(stdscr, message, color_pair, delay=0.05):
    sh, sw = stdscr.getmaxyx()
    x = max((sw - len(message)) // 2, 0)
    y = sh // 2

    for i in range(len(message)):
        if 0 <= x + i < sw:
            try:
                stdscr.addstr(y, x + i, message[i], curses.color_pair(color_pair))
            except curses.error:
                pass
        stdscr.refresh()
        time.sleep(delay)

def show_top_message(stdscr, message, color_pair):
    sh, sw = stdscr.getmaxyx()
    x = max((sw - len(message)) // 2, 0)
    y = 1  # near top
    try:
        stdscr.addstr(y, x, message, curses.color_pair(color_pair))
    except curses.error:
        pass
    stdscr.refresh()

def draw_matrix(stdscr):
    sh, sw = stdscr.getmaxyx()
    columns = sw
    drops = [random.randint(0, sh - 1) for _ in range(columns)]

    start_time = time.time()
    while time.time() - start_time < MATRIX_DURATION:
        stdscr.clear()
        for i in range(columns):
            char = random.choice(MATRIX_CHARS)
            x = i
            y = drops[i]

            if 0 <= y < sh and 0 <= x < sw:
                try:
                    stdscr.addstr(y, x, char, curses.color_pair(1))
                except curses.error:
                    pass

            drops[i] = (drops[i] + 1) % sh

        stdscr.refresh()
        time.sleep(MATRIX_SPEED)

def main():
    curses.wrapper(init)

def init(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Matrix
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Title
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Loading

    curses.curs_set(0)
    stdscr.clear()

    # Step 1: Show Title
    show_centered_message(stdscr, TITLE_MESSAGE, color_pair=2, delay=TYPE_SPEED)
    time.sleep(PAUSE_BEFORE_MATRIX)

    # Step 2: Matrix effect
    draw_matrix(stdscr)

    # Step 3: Show loading centered
    stdscr.clear()
    show_centered_message(stdscr, LOADING_MESSAGE, color_pair=3, delay=0.05)

    # Step 4: Move it to the top after short delay
    time.sleep(MOVE_LOADING_DELAY)
    stdscr.clear()
    show_top_message(stdscr, LOADING_MESSAGE, color_pair=3)
    time.sleep(2)

if __name__ == "__main__":
    main()
