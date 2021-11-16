#!/bin/env python

import curses
from curses import wrapper
import time
import random
import os

current_text = "texts/classic.txt"
wpm = 0

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Carter's Typing Test!")
    stdscr.addstr("\nPress enter to begin!")
    stdscr.addstr("\nMore options:")
    stdscr.addstr("\n\tt: change theme")
    stdscr.addstr("\n\tm: change mode")
    stdscr.addstr("\n\ta: add to current text")
    stdscr.addstr("\n\ts: score report(currently unsupported)")
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

def change_mode(stdscr):
    global current_text
    stdscr.clear()
    stdscr.addstr(f"Current text file is: {current_text}")
    stdscr.addstr("\nWhich text file would you like to use?")
    i = 0
    for file in os.listdir("./texts"):
        stdscr.addstr(f"\n{i}: {file}")
        i += 1
    stdscr.refresh()
    key = stdscr.getkey()

    j = 0
    for file in os.listdir("./texts"):
        stdscr.addstr(f"\n{j}")
        if int(key) == j:
            current_text = "texts/" + file
            break
        j += 1

def add_text(stdscr):
    global current_text
    stdscr.clear()
    stdscr.addstr(f"The current text file is: {current_text}")
    stdscr.addstr("\nPlease input a new line, or press esc to cancel.\nOnce you are done press esc.")
    stdscr.refresh()
    new_line = []
    while True:
        key = stdscr.getkey()
        stdscr.clear()
        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(new_line) > 0:
                new_line.pop()
        else:
            new_line.append(key)
        stdscr.addstr("".join(new_line))
        stdscr.refresh()
    if len(new_line) > 0:
        stdscr.clear()
        stdscr.addstr("Your new line is:")
        stdscr.addstr("\n" + "".join(new_line).strip())
        stdscr.addstr("\nPress esc to cancel, enter to save.")
        stdscr.refresh()
        key = stdscr.getkey()
        if ord(key) == 27:
            pass
        else:
            new_line = "".join(new_line).strip()
            with open(current_text, "a") as f:
                f.writelines("\n" + new_line)

def score_report(stdscr):
    stdscr.clear()
    scores = []
    sum_of_scores = 0
    high_score = 0
    low_score = 1000
    with open("scores.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            scores.append(line)
            sum_of_scores += int(line)
            if int(line) > high_score:
                high_score = int(line)
            if int(line) < low_score:
                low_score = int(line)
    stdscr.addstr(f"\nAverage WPM: {sum_of_scores/len(scores)}")
    stdscr.addstr(f"\nHigh Score: {high_score}")
    stdscr.addstr(f"\nLow Score: {low_score}")
    stdscr.getkey()

def add_score(score):
    with open("scores.txt", "a") as f:
        f.writelines("\n" + str(score))
    lines = []
    with open("scores.txt", "r") as f:
        lines = f.readlines()
    with open("scores.txt", "w") as f:
        for number, line in enumerate(lines):
            if line != "\n":
                f.write(line)

def load_text():
    global current_text
    with open(current_text, "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    global wpm
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

        try:
            if ord(key) == 27: #If user hits escape key
                break
        except:
            print()

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    global current_text
    global wpm

    while True:
        start_screen(stdscr)
        key = stdscr.getkey()

        doTest = False
        if key == "t":
            change_theme(stdscr)
        elif key == "m":
            change_mode(stdscr)
        elif key == "a":
            add_text(stdscr)
        elif key == "s":
            score_report(stdscr)
        elif ord(key) == 27:
            break
        else:
            doTest = True

        while doTest:
            wpm_test(stdscr)
            add_score(wpm)
            stdscr.addstr(2, 0, "You completed the text! Press enter to do another test...")
            key = stdscr.getkey()

            if ord(key) == 27:
                doTest = False

wrapper(main)
