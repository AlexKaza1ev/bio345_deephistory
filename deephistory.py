"""
Creative assignment for BIO345
Alex Kazaiev
"""
import curses
import time

# Configuration
TOTAL_YEARS = 4_540_000_000  # Earth's age in years
INITIAL_YEARS_PER_SECOND = 100000  # Initial speed
BAR_CHAR = "█"
TITLE = "BIO345 Activity 1.2 - DEEP HISTORY"
AUTHOR = "Alex Kazaiev"
LOADING_TEXT = "Earth History Simulation"

# Timeline events (in years ago)
TIMELINE_EVENTS = [
    (4_540_000_000, "Formation of Earth"),
    (3_500_000_000, "Start of Life"),
    (2_500_000_000, "Oxygenation of Atmosphere"),
    (2_000_000_000, "Origin of Eukaryotes"),
    (1_000_000_000, "Multicellularity"),
    (500_000_000,   "Origin of Vertebrates"),
    (450_000_000,   "Origin of Plants"),
    (400_000_000,   "Origin of Land Animals"),
    (252_000_000,   "Mass Extinction"),
    (230_000_000,   "Origin of Dinosaurs"),
    (200_000_000,   "Origin of Mammals"),
    (66_000_000,    "Dinosaur Extinction"),
    (300_000,       "Homo s."),
    (0,             "Present")
]

def year_to_col(year, total_years, width):
    return int((1 - year / total_years) * width)

def draw_legend(stdscr, h, w, speed):
    legend_text = f"Speed: {speed:,} years/sec  (+ / - to adjust)"
    try:
        stdscr.addstr(h - 2, 2, legend_text, curses.color_pair(2))
    except curses.error:
        pass

def draw_title_screen(stdscr):
    h, w = stdscr.getmaxyx()
    title_y = h // 2 - 1
    author_y = title_y + 2
    title_x = (w - len(TITLE)) // 2
    author_x = (w - len(AUTHOR)) // 2
    stdscr.clear()
    for i in range(len(TITLE)):
        try:
            stdscr.addstr(title_y, title_x + i, TITLE[i], curses.color_pair(2))
        except curses.error:
            pass
        stdscr.refresh()
        time.sleep(0.05)

    for i in range(len(AUTHOR)):
        try:
            stdscr.addstr(author_y, author_x + i, AUTHOR[i], curses.color_pair(2))
        except curses.error:
            pass
        stdscr.refresh()
        time.sleep(0.05)
        time.sleep(0.05)
    time.sleep(1)

def draw_progress_bar(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()

    h, w = stdscr.getmaxyx()
    bar_y = h // 3  # move to top third
    log_start_y = h // 2  # middle third start
    log_height = h // 3 - 2
    log_window = []
    art_x = w // 2 + 10
    art_y = log_start_y

    total_width = w - 2  # leave margins
    current_year = TOTAL_YEARS
    years_per_second = INITIAL_YEARS_PER_SECOND
    shown_labels = set()
    drawn_cols = set()

    label_colors = [3, 4, 5, 6, 7, 8]
    label_color_map = {}
    ascii_art_map = {
        "Formation of Earth": [
            "             _____       ",
            "          .-' .  ':'-.   ",
            "        .''::: .:    '.  ",
            "       /   :::::'      \\",
            "      ;.    ':' `       ;",
            "      |       '..       |",
            "      ; '      ::::.    ;",
            "       \       '::::   / ",
            "        '.      :::  .'  ",
            "          '-.___'_.-'    "
        ],
        "Start of Life": [
            " ~ ~ ~ ~ ~ ~",
            " ~ o o ~ ~ ~",
            " ~ ~ ~ ~ ~ ~"
        ],
        "Oxygenation of Atmosphere": [
          " (O2)  (O2)   (O2) ",
          "(O2) (O2)  (O2)    ",
          " (O2) (O2)  (O2)   ",
          " (O2)    (O2)  (O2)"
        ],
        "Origin of Eukaryotes": [
          " [c]   [c] ",
          "           ",
          "   [c]     "
        ],
        "Multicellularity": [
          " [c][c][c][c][c]  ",
          "[c][c][c][c][c][c]",
          "[c][c][c]         ",
          "[c][c][c]         ",
          "[c][c][c][c][c][c]",
          " [c][c][c][c][c]"
        ],
        "Origin of Vertebrates": [
            "  <>  ",
            "  <>  ",
            "  <>  ",
        ],
        "Origin of Plants": [
            "               .--.",
            "              .'_\\/_'.",
            "              '. /\\ .'",
            "               \"||\"",
            "                 || /\\",
            "               /\\ ||//\\)",
            "             (/\\||/",
            "               ______\\||/_______"
        ],
        "Origin of Land Animals": [
            "  /\\_/\\ ",
            " ( o.o )",
            "  > ^ < "
        ],
        "Mass Extinction": [
            "                       .:'",
            "                   _.::'  ",
            "        .-;;-.   (_.'     ",
            "       / ;;;' \\          ",
            "      |.  `:   |          ",
            "       \\:   `;/          ",
            "        '-..-'            "
        ],
        "Origin of Dinosaurs": [
            "                / _)  ",
            "     _.----._/ /  ",
            "    /         /   ",
            " __/ (  | (  |    ",
            "/__.-'|_|--|_|    "
        ],
        "Origin of Mammals": [
            " (\\__/)  ",
            " ( •.•)   ",
            " / >🍪   "
        ],
        "Dinosaur Extinction": [
            "                       .:'",
            "                   _.::'  ",
            "        .-;;-.   (_.'     ",
            "       / ;;;' \\          ",
            "      |.  `:   |          ",
            "       \\:   `;/          ",
            "        '-..-'            "
        ],
        "Homo s.": [
            "  o   ",
            " /|\\ ",
            " / \\ " 
        ],
        "Present": [
            "  Simulation Complete!  "
        ]
    }
    current_art = ""

    while current_year >= 0:
        draw_legend(stdscr, h, w, years_per_second)

        # Display loading text at the top
        try:
            stdscr.addstr(1, (w - len(LOADING_TEXT)) // 2, LOADING_TEXT, curses.color_pair(2))
        except curses.error:
            pass

        # Clear and update current year line
        try:
            stdscr.move(bar_y - 3, 0)
            stdscr.clrtoeol()
            stdscr.addstr(bar_y - 3, 2, f"Years ago: {int(current_year)}", curses.color_pair(2))
        except curses.error:
            pass

        col = year_to_col(current_year, TOTAL_YEARS, total_width)
        if 0 <= col < total_width and col not in drawn_cols:
            try:
                stdscr.addstr(bar_y, col, BAR_CHAR, curses.color_pair(1))
                drawn_cols.add(col)
            except curses.error:
                pass

        for i, (year, label) in enumerate(TIMELINE_EVENTS):
            if label not in shown_labels and current_year <= year:
                label_col = year_to_col(year, TOTAL_YEARS, total_width)
                if 0 <= label_col < total_width:
                    label_color = label_colors[i % len(label_colors)]
                    label_color_map[label] = label_color
                    try:
                        if i % 2 == 0:
                            stdscr.addstr(bar_y - 1, label_col, "|", curses.color_pair(label_color))
                            stdscr.addstr(bar_y - 2, max(0, label_col - len(label)//2), label, curses.color_pair(label_color))
                        else:
                            stdscr.addstr(bar_y + 1, label_col, "|", curses.color_pair(label_color))
                            stdscr.addstr(bar_y + 2, max(0, label_col - len(label)//2), label, curses.color_pair(label_color))
                        shown_labels.add(label)
                        current_art = ascii_art_map.get(label, "")
                        log_window.append(f"[{int(year):,} yrs ago]: {label}")
                        if len(log_window) > log_height:
                            log_window.pop(0)
                    except curses.error:
                        pass

        for idx, msg in enumerate(log_window):
            try:
                stdscr.addstr(log_start_y + idx, 4, f"- {msg}", curses.color_pair(2))
            except curses.error:
                pass

                # Draw ASCII art to the right of the log
        box_width = 48
        box_height = 20 
        for i in range(box_height):
            try:
                stdscr.move(art_y + i - 1, art_x - 2)
                stdscr.clrtoeol()
            except curses.error:
                pass

        try:
            stdscr.addstr(art_y - 1, art_x - 2, '+' + '-' * (box_width - 2) + '+', curses.color_pair(1))
            art_lines = current_art if isinstance(current_art, list) else []
            vertical_padding = (box_height - 2 - len(art_lines)) // 2
            for i in range(box_height - 2):
                if i < vertical_padding or i >= vertical_padding + len(art_lines):
                    blank = ' ' * (box_width - 2)
                    stdscr.addstr(art_y + i, art_x - 2, f"|{blank}|", curses.color_pair(1))
                else:
                    line = art_lines[i - vertical_padding]
                    padded = line.center(box_width - 2)
                    stdscr.addstr(art_y + i, art_x - 2, f"|{padded}|", curses.color_pair(1))
            stdscr.addstr(art_y + box_height -2, art_x - 2, '+' + '-' * (box_width - 2) + '+', curses.color_pair(1))
        except curses.error:
            pass

        current_year -= years_per_second
        stdscr.refresh()
        time.sleep(0.01)

        try:
            key = stdscr.getch()
            if key == ord('+'):
                years_per_second *= 10
            elif key == ord('-') and years_per_second > 100:
                years_per_second //= 10
        except:
            pass

    year, label = 0, "Present"
    col = year_to_col(year, TOTAL_YEARS, total_width)
    if label not in shown_labels:
        try:
            stdscr.addstr(bar_y, col, BAR_CHAR, curses.color_pair(1))
            stdscr.addstr(bar_y + 1, col, "|", curses.color_pair(2))
            stdscr.addstr(bar_y + 2, max(0, col - len(label)//2), label, curses.color_pair(2))
            log_window.append(f"[{int(year):,} yrs ago]: {label}")
            if len(log_window) > log_height:
                log_window.pop(0)
            for idx, msg in enumerate(log_window):
                stdscr.addstr(log_start_y + idx, 4, f"- {msg}", curses.color_pair(2))
        except curses.error:
            pass

    stdscr.refresh()
    log_window.append("Press any key to continue")
    for idx, msg in enumerate(log_window[-log_height:]):
        try:
            stdscr.addstr(log_start_y + idx, 4, f"- {msg}", curses.color_pair(2))
        except curses.error:
            pass
    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()

def run(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_BLACK)
    draw_title_screen(stdscr)
    draw_progress_bar(stdscr)

def main():
    curses.wrapper(run)

if __name__ == "__main__":
    main()
