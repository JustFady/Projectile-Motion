# Projectile Motion Simulator

A 3D projectile motion simulation built with VPython. Launch a ball under different planetary gravities (Earth, Mars, Venus, Jupiter) and observe the effects of wind resistance in real time.

## GlowScript

You can also view and run the simulation directly in your browser via GlowScript:
[ProjectileMotion on GlowScript](https://www.glowscript.org/#/user/byte4589/folder/MyPrograms/program/ProjectileMotion/edit)

## Features

- **Multiple Environments** — Switch between Earth, Mars, Venus, and Jupiter gravity.
- **Interactive Sliders** — Adjust launch velocity, launch angle, and wind resistance before each run.
- **Live Stats HUD** — See velocity, distance to target, and impact force right in the browser.
- **Velocity Graph** — Real-time plot of ball speed over time.
- **Trajectory Comparison** — A second ball (blue dots) shows the ideal path without wind.

## How to Run

1. **Clone the repo**
   ```
   git clone https://github.com/JustFady/Projectile-Motion.git
   cd Projectile-Motion
   ```

2. **Create a virtual environment and install dependencies**
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install vpython "setuptools<70"
   ```

3. **Run the simulation**
   ```
   python3 ProjectileMotion.py
   ```
   A browser tab will open automatically with the simulation.

## Usage

1. Pick a planet from the dropdown menu.
2. Adjust the sliders (velocity, angle, wind resistance) to your liking.
3. Click **Reset** to apply the new slider values.
4. Click **Run** to launch the ball and watch it fly.

## Author

Fady Youssef
