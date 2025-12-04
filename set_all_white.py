#!/usr/bin/env python3
"""
set_all_white.py

Sets all LEDs on the RGB Xmas Tree to white and provides realtime
brightness control (0-10) using keypresses.

Place this file in the same folder as the `tree.py` file from the
ThePiHut/rgbxmastree project (see https://github.com/ThePiHut/rgbxmastree).

Run with:

    python3 set_all_white.py

Controls:
 - Press `0` to turn the tree off (brightness 0.0)
 - Press digits `1`..`9` to set brightness spread evenly from 0.1 up to 1.0
     (so `1` -> 0.1 and `9` -> 1.0). Press `1` then `0` quickly to set `10`
     (also mapped to 1.0).
 - Press `q` to quit

This uses the `curses` module for realtime key handling. On systems
without `curses` available, it will fall back to a simple keep-alive loop
that keeps the lights on at 50% brightness.
"""

import time

from tree import RGBXmasTree


def main():
    # Try to import curses for realtime key handling; fall back if unavailable.
    try:
        import curses
    except Exception:
        # Fallback: simple behavior identical to previous script
        tree = RGBXmasTree()
        tree.brightness = 0.5
        tree.color = (1, 1, 1)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            try:
                tree.off()
            except Exception:
                try:
                    tree.color = (0, 0, 0)
                except Exception:
                    pass
        return

    def curses_main(stdscr):
        tree = RGBXmasTree()
        # Default to 50%
        tree.brightness = 0.5
        tree.color = (1, 1, 1)

        stdscr.nodelay(True)
        stdscr.clear()
        stdscr.addstr(0, 0, "All-white mode: press 0-9 (or 1 then 0 for 10) to change brightness; 'q' to quit.")
        stdscr.addstr(1, 0, f"Current brightness: {tree.brightness:.2f}")
        stdscr.refresh()

        last_key = None
        try:
            while True:
                key = stdscr.getch()
                if key == -1:
                    continue

                # quit
                if key in (ord('q'), ord('Q')):
                    stdscr.addstr(3, 0, "Quit requested — exiting.    ")
                    stdscr.refresh()
                    break

                # digit keys
                if ord('0') <= key <= ord('9'):
                    val = key - ord('0')
                    # handle quick '10' entry: previous '1' then '0'
                    if last_key == ord('1') and key == ord('0'):
                        val = 10
                    last_key = key

                    # apply brightness
                    if val == 0:
                        try:
                            tree.off()
                        except Exception:
                            tree.color = (0, 0, 0)
                    else:
                        # Map 1..9 -> 0.1..1.0 evenly. 10 -> 1.0
                        if val == 10:
                            brightness = 1.0
                        else:
                            # spread 1..9 inclusive across [0.1, 1.0]
                            brightness = 0.1 + (val - 1) * (0.9 / 8)
                        tree.brightness = brightness
                        tree.color = (1, 1, 1)

                    stdscr.addstr(1, 0, f"Current brightness: {tree.brightness:.2f}   ")
                    stdscr.addstr(2, 0, f"Set brightness to {val} -> {tree.brightness:.2f}   ")
                    stdscr.refresh()
                else:
                    last_key = key

        except KeyboardInterrupt:
            # handle Ctrl+C cleanly
            pass

        # attempt to turn off the tree on exit
        try:
            tree.off()
        except Exception:
            try:
                tree.color = (0, 0, 0)
            except Exception:
                pass

    # start curses UI
    curses.wrapper(curses_main)


if __name__ == "__main__":
    main()
