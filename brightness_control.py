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

import sys
import time
import select
import tty
import termios

from tree import RGBXmasTree


def get_key(timeout=None):
    """Read a single keypress from stdin. Returns the character or None on timeout."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        r, _, _ = select.select([sys.stdin], [], [], timeout)
        if r:
            ch = sys.stdin.read(1)
            return ch
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


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
            ch = get_key()
            if ch is None:
                continue

            if ch == 'q':
                print("Quit requested — exiting.")
                break

            if ch.isdigit():
                # Handle potential two-character '10' (pressing '1' then '0')
                if ch == '1':
                    # wait a short moment to see if user types '0'
                    nxt = get_key(timeout=0.25)
                    if nxt == '0':
                        val = 10
                    else:
                        val = 1
                        # if nxt is another key, keep it in variable to process
                        if nxt is not None:
                            # process nxt in next loop iteration by printing it back
                            # (can't push back into stdin easily)
                            pass
                else:
                    val = int(ch)

                # Map 0..10 -> 0.0..1.0
                brightness = max(0.0, min(1.0, val / 10.0))

                if val == 0:
                    # turn off if supported
                    try:
                        tree.off()
                    except Exception:
                        tree.color = (0, 0, 0)
                else:
                    # ensure the tree shows white at the requested brightness
                    tree.brightness = brightness
                    tree.color = (1, 1, 1)

                print(f"Set brightness to {val} -> {brightness:.2f}")

            else:
                # ignore other keys but print for clarity
                print(f"Unhandled key: {repr(ch)}")

    except KeyboardInterrupt:
        print("Interrupted — exiting.")
    finally:
        try:
            tree.off()
        except Exception:
            try:
                tree.color = (0, 0, 0)
            except Exception:
                pass


if __name__ == '__main__':
    main()
