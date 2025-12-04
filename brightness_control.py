#!/usr/bin/env python3
"""
brightness_control.py

Listen for numeric keypresses 0-10 and set the RGB Xmas Tree brightness.

Usage:
  - Press digits `0`..`9` to set brightness to that value / 10.
  - Press `10` by pressing `1` then `0` quickly (within 0.25s).
  - Press `q` to quit.

This script expects to be in the same folder as `tree.py` from
ThePiHut/rgbxmastree.
"""


import curses
from tree import RGBXmasTree


def main():
    tree = RGBXmasTree()

    # Start with white colour so brightness changes affect visible output
    tree.color = (1, 1, 1)

    print("Brightness control — press 0..10 to set brightness (0=off).")
    print("Press 'q' to quit.")

    current = getattr(tree, "brightness", 0.5)
    print(f"Current brightness: {current:.2f}")


    try:
        while True:
            inp = input("Enter brightness (0-10), or 'q' to quit: ").strip()
            if inp.lower() == 'q':
                print("Quit requested — exiting.")
                break
            if inp.isdigit():
                val = int(inp)
                if not (0 <= val <= 10):
                    print("Please enter a value between 0 and 10.")
                    continue
                brightness = val / 10.0
                if val == 0:
                    try:

                        def curses_main(stdscr):
                            tree = RGBXmasTree()
                            tree.color = (1, 1, 1)
                            current = getattr(tree, "brightness", 0.5)
                            stdscr.nodelay(True)
                            stdscr.clear()
                            stdscr.addstr(0, 0, "Brightness control — press 0-9 or 1 then 0 for 10 (0=off). Press 'q' to quit.")
                            stdscr.addstr(1, 0, f"Current brightness: {current:.2f}")
                            stdscr.refresh()
                            last_key = None
                            while True:
                                try:
                                    key = stdscr.getch()
                                    if key == -1:
                                        continue
                                    if key in (ord('q'), ord('Q')):
                                        stdscr.addstr(2, 0, "Quit requested — exiting.   ")
                                        stdscr.refresh()
                                        break
                                    if key in range(ord('0'), ord('9')+1):
                                        val = key - ord('0')
                                        # If previous key was '1' and now '0', treat as '10'
                                        if last_key == ord('1') and key == ord('0'):
                                            val = 10
                                        last_key = key
                                        brightness = val / 10.0
                                        if val == 0:
                                            try:
                                                tree.off()
                                            except Exception:
                                                tree.color = (0, 0, 0)
                                        else:
                                            tree.brightness = brightness
                                            tree.color = (1, 1, 1)
                                        stdscr.addstr(1, 0, f"Current brightness: {brightness:.2f}   ")
                                        stdscr.addstr(2, 0, f"Set brightness to {val} -> {brightness:.2f}   ")
                                        stdscr.refresh()
                                    else:
                                        last_key = key
                                except KeyboardInterrupt:
                                    stdscr.addstr(2, 0, "Interrupted — exiting.   ")
                                    stdscr.refresh()
                                    break
                            try:
                                tree.off()
                            except Exception:
                                try:
                                    tree.color = (0, 0, 0)
                                except Exception:
                                    pass

                        curses.wrapper(curses_main)
