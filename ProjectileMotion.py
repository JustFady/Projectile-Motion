# Author: Fady Youssef
# Date: 12/09/22
# Description:
# A Web VPython simulation modeling projectile motion of a ball under different gravities 
# (Earth, Mars, Venus, Jupiter). Users can start, pause, reset the simulation, and switch 
# between environments. The program tracks the ball's position, velocity, and impact force 
# upon landing, illustrating the effects of gravitational and wind resistance forces.

from vpython import *

# Setup the canvas and environment parameters
scene = canvas(center=vector(1, 1, 0), background=color.black)
ground = box(pos=vec(0, -0.02, 0), size=vec(30, 0.02, 0.4), color=color.green)
running = False
environments = {"Earth": 9.81, "Mars": 3.72, "Venus": 8.87, "Jupiter": 24.5}
current_env = "Earth"
g = environments[current_env]

# Change environment gravity based on the selected option
def change_environment(env):
    global g, current_env
    current_env = env.selected
    g = environments[current_env]
    print(f"Environment changed to {current_env} with gravity {g} m/s^2")

menu(choices=["Earth", "Mars", "Venus", "Jupiter"], bind=change_environment)

# Toggle simulation state between running and paused
def Run(b):
    global running, dt
    running = not running
    b.text = "Pause" if running else "Run"
    dt = remember_dt if running else 0

# Reset simulation to its initial state
def Reset():
    global t, running, dt
    t = 0
    ball.pos = vec(x0, y0, 0)
    ball.v = vConstant * vec(cos(theta), sin(theta), 0)
    ball.mo = ball.mass * ball.v
    ball.clear_trail()  # Clear the trail of the ball
    ball_2.pos = vec(x0, y0, 0)
    ball_2.clear_trail()  # Clear the trail of the second ball
    b_speed.delete()  # Clear the graph data
    running = False
    run_button.text = "Run"
    if 'hud_impact' in globals():
        hud_impact.text = 'Impact Force: -- N\n'
    print("Simulation reset.")

# Buttons for control
run_button = button(text="Run", bind=Run)
button(text="Reset", bind=Reset)

# Parameters for initial setup
wind_resistance = 0.01
vConstant = 6.1
x0, y0 = -1.4, 0.0001
theta = 50 * pi / 180
t = 0
dt = 0.004
remember_dt = dt

# Create objects: ball, secondary ball for trajectory visualization, and target hole
ball = sphere(pos=vec(x0, y0, 0), mass=5, v=vConstant * vec(cos(theta), sin(theta), 0),
              radius=0.02, color=color.red, make_trail=True)
ball_2 = sphere(pos=vec(x0, y0, 0), radius=0.07, color=color.blue, make_trail=True, trail_type="points")
hole = box(pos=vec(1.5, -0.06, 0), size=vec(0.5, 0.5, 0), color=color.white)
ball.mo = ball.mass * ball.v
speed_graph = graph(title='Motion through time', xtitle='Time (s)', ytitle='Velocity (m/s)')
b_speed = gcurve(graph=speed_graph, color=color.red)

# HUD for live stats
scene.append_to_caption('\n\n--- Simulation Stats ---\n')
hud_velocity = wtext(text='Velocity: 0 m/s\n')
hud_distance = wtext(text='Distance from target: 0 m\n')
hud_impact = wtext(text='Impact Force: -- N\n')

# Main simulation loop
while True:
    rate(500)
    if running and ball.pos.y >= 0:
        # Calculate forces: gravity and wind resistance
        FEnet = vector(0, ball.mass * -g, 0)
        Fwind = -wind_resistance * ball.v.mag2 * norm(ball.v)
        Fnet = FEnet + Fwind

        # Update ball's momentum and position
        ball.mo += Fnet * dt
        ball.v = ball.mo / ball.mass
        ball.pos += ball.v * dt
        ball_2.pos = vec(x0 + vConstant * cos(theta) * t, 
                         y0 + vConstant * sin(theta) * t - g / 2 * t ** 2, 0)

        # Plotting ball speed over time
        b_speed.plot(pos=(t, mag(ball.v)))
        t += dt

        # Display current state information
        d = hole.pos.x - ball.pos.x
        hud_velocity.text = f"Velocity: {mag(ball.v):.2f} m/s\n"
        hud_distance.text = f"Distance from target: {d:.2f} m\n"

    # Check if the ball has hit the ground and stop the simulation
    if ball.pos.y < 0 and running:
        impact_force = mag(Fnet)
        hud_impact.text = f"Impact force on {current_env}: {impact_force:.2f} Newtons\n"
        running = False
        run_button.text = "Run"
