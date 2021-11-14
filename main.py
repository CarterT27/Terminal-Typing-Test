import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Carter's Typing Test!")
    stdscr.addstr("\nPress enter to begin!")
    stdscr.addstr("\nMore options:")
    stdscr.addstr("\n\tt: change theme")
    stdscr.addstr("\n\tm: change mode(currently unsupported)")
    stdscr.addstr("\n\te: add to current text(currently unsupported)")
    stdscr.refresh()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def change_theme(stdscr):
    stdscr.clear()
    stdscr.addstr("Light (L) or Dark (D) mode?")
    key = stdscr.getkey()
    background_color = curses.COLOR_WHITE
    default_text_color = curses.COLOR_BLACK
    if key in ("L", "l"):
        background_color = curses.COLOR_WHITE
        default_text_color = curses.COLOR_BLACK
    elif key in ("D", "d"):
        background_color = curses.COLOR_BLACK
        default_text_color = curses.COLOR_WHITE

    stdscr.clear()
    stdscr.addstr("Pick color of correct text")
    stdscr.addstr("\n\tb: blue")
    stdscr.addstr("\n\tc: cyan")
    stdscr.addstr("\n\tg: green")
    stdscr.addstr("\n\tm: magenta")
    stdscr.addstr("\n\ty: yellow")
    key = stdscr.getkey()
    correct_text_color = curses.COLOR_GREEN
    if key in ("b", "B"):
        correct_text_color = curses.COLOR_BLUE
    elif key in ("c", "C"):
        correct_text_color = curses.COLOR_CYAN
    elif key in ("g", "G"):
        correct_text_color = curses.COLOR_GREEN
    elif key in ("m", "M"):
        correct_text_color = curses.COLOR_MAGENTA
    elif key in ("y", "Y"):
        correct_text_color = curses.COLOR_YELLOW

    curses.init_pair(1, correct_text_color, background_color)
    curses.init_pair(2, curses.COLOR_RED, background_color)

def load_text():
    with open("classic_texts.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if current_text == []:
            start_time = time.time()

        if ord(key) == 27: #If user hits escape key
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    start_screen(stdscr)
    key = stdscr.getkey()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    if key == "t":
        change_theme(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)
