#!/usr/bin/env python3
"""
set_all_white.py

Simple script to set all LEDs on the RGB Xmas Tree to white at 50% brightness.

Place this file in the same folder as the `tree.py` file from the
ThePiHut/rgbxmastree project (see https://github.com/ThePiHut/rgbxmastree).

Run with:

    python3 set_all_white.py

Press Ctrl+C to exit; the script will attempt to turn the tree off on exit.
"""

from tree import RGBXmasTree
import time


def main():
    tree = RGBXmasTree()

    # Ensure brightness is 50% (0-1 range). README says default is 0.5,
    # but we set it explicitly here.
    tree.brightness = 0.5

    # Set color to white (RGB values 0-1)
    tree.color = (1, 1, 1)

    try:
        # Keep the program running so the lights stay on until the user
        # interrupts with Ctrl+C.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Try to switch the tree off if possible; otherwise set colour to black.
        try:
            tree.off()
        except Exception:
            try:
                tree.color = (0, 0, 0)
            except Exception:
                pass


if __name__ == "__main__":
    main()
