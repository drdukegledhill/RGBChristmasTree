# RGBChristmasTree

Simple helper scripts for the RGB Xmas Tree project (ThePiHut's `rgbxmastree`).

Files included
- `tree.py` – from ThePiHut/rgbxmastree (controls the LED tree). Keep this file in the same folder.
- `set_all_white.py` – small script that sets all LEDs to white at 50% brightness and keeps them on until you press Ctrl+C.

Quick start (macOS / Linux / Raspberry Pi)

1. Make sure `tree.py` is in the same directory as this repository. If you don't have it, download it from ThePiHut:

   ```bash
   wget https://bit.ly/2Lr9CT3 -O tree.py
   ```

2. (Optional) create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. If you are running on Raspberry Pi Lite, you may need `gpiozero`:

   ```bash
   sudo apt update
   sudo apt install python3-gpiozero
   ```

   On desktop Linux or macOS the `tree.py` file runs without extra packages for simulation/LED printing.

4. Run the script to set all LEDs to white at 50% brightness:

   ```bash
   python3 set_all_white.py
   ```

   Press `Ctrl+C` to exit; the script will attempt to turn the tree off when interrupted.

Notes
- Brightness is expressed as a floating value between `0` and `1`. `set_all_white.py` explicitly sets `tree.brightness = 0.5`.
- This repository intentionally contains a minimal wrapper script. Replace `tree.py` with the hardware version on a Raspberry Pi to control real LEDs.

License
- This repo contains small helper scripts; the `tree.py` code is from ThePiHut/rgbxmastree and is subject to its original license.
