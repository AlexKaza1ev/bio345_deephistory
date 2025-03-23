import curses
import time

# Configuration
TOTAL_YEARS = 4_540_000_000  # Earth's age in years
INITIAL_YEARS_PER_SECOND = 100000  # Initial speed
BAR_CHAR = "█"

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
    (0,             "Today")
]

def year_to_col(year, total_years, width):
    return int((1 - year / total_years) * width)

def draw_legend(stdscr, h, w, speed):
    legend_text = f"Speed: {speed:,} years/sec  (+ / - to adjust)"
    try:
        stdscr.addstr(h - 2, 2, legend_text, curses.color_pair(2))
    except curses.error:
        pass

def draw_progress_bar(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()

    h, w = stdscr.getmaxyx()
    bar_y = h // 3  # move to top third
    log_start_y = h // 2  # middle third start
    log_height = h // 3 - 2
    log_window = []

    total_width = w - 2  # leave margins
    current_year = TOTAL_YEARS
    years_per_second = INITIAL_YEARS_PER_SECOND
    shown_labels = set()
    drawn_cols = set()

    label_colors = [3, 4, 5, 6, 7, 8]
    label_color_map = {}

    while current_year >= 0:
        draw_legend(stdscr, h, w, years_per_second)

        # Display current year above the progress bar
        try:
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
            if year >= current_year and label not in shown_labels:
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
                        log_window.append(f"[{int(year):,} yrs ago]: {label}")
                        if len(log_window) > log_height:
                            log_window.pop(0)
                    except curses.error:
                        pass

        # Draw event log in middle third
        for idx, msg in enumerate(log_window):
            try:
                stdscr.addstr(log_start_y + idx, 4, f"- {msg}", curses.color_pair(2))
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

    # Ensure "Present" is always logged and shown
    year, label = 0, "Today"
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
    time.sleep(10)

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
    draw_progress_bar(stdscr)

def main():
    curses.wrapper(run)

if __name__ == "__main__":
    main()
