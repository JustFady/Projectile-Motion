#author: fady youssef
#date: 12/09/22
#desc: 3d sim showing how a ball flies in different gravity 
#(earth, mars, venus, jupiter). play with speed, angle, 
# n wind to see what happens.

from vpython import *

#setting up the screen n stuff
scene = canvas(center=vector(1, 1, 0), background=color.black)
ground = box(pos=vec(0, -0.02, 0), size=vec(30, 0.02, 0.4), color=color.green)
running = False
environments = {"Earth": 9.81, "Mars": 3.72, "Venus": 8.87, "Jupiter": 24.5}
current_env = "Earth"
g = environments[current_env]

#  swaps gravity when u pick a planet
def change_environment(env):
    global g, current_env
    current_env = env.selected
    g = environments[current_env]
    print(f"Environment changed to {current_env} with gravity {g} m/s^2")

menu(choices=["Earth", "Mars", "Venus", "Jupiter"], bind=change_environment)

#  play/pause toggle
def Run(b):
    global running, dt
    running = not running
    b.text = "Pause" if running else "Run"
    dt = remember_dt if running else 0

#put everything back to the start
def Reset():
    global t, running, dt, vConstant, theta, wind_resistance
    t = 0
    #  read current slider values
    vConstant = velocity_slider.value
    theta = angle_slider.value * pi / 180
    wind_resistance = wind_slider.value
    ball.pos = vec(x0, y0, 0)
    ball.v = vConstant * vec(cos(theta), sin(theta), 0)
    ball.mo = ball.mass * ball.v
    ball.clear_trail()  # wipe the red path
    ball_2.pos = vec(x0, y0, 0)
    ball_2.clear_trail() #  wipe the blue path
    b_speed.delete() #clear the graph
    running = False
    run_button.text = "Run"
    if 'hud_impact' in globals():
        hud_impact.text = 'Impact Force: -- N\n'
    print("Simulation reset.")

# making the main buttons
run_button = button(text="Run", bind=Run)
button(text="Reset", bind=Reset)

#basic starting values
wind_resistance = 0.01
vConstant = 6.1
x0, y0 = -1.4, 0.0001
theta = 50 * pi / 180
t = 0
dt = 0.004
remember_dt = dt

#  making the balls n target hole
ball = sphere(pos=vec(x0, y0, 0), mass=5, v=vConstant * vec(cos(theta), sin(theta), 0),
              radius=0.02, color=color.red, make_trail=True)
ball_2 = sphere(pos=vec(x0, y0, 0), radius=0.07, color=color.blue, make_trail=True, trail_type="points")
hole = box(pos=vec(1.5, -0.06, 0), size=vec(0.5, 0.5, 0), color=color.white)
ball.mo = ball.mass * ball.v
speed_graph = graph(title='Motion through time', xtitle='Time (s)', ytitle='Velocity (m/s)')
b_speed = gcurve(graph=speed_graph, color=color.red)

#live stats display
scene.append_to_caption('\n\n--- Simulation Stats ---\n')
hud_velocity = wtext(text='Velocity: 0 m/s\n')
hud_distance = wtext(text='Distance from target: 0 m\n')
hud_impact = wtext(text='Impact Force: -- N\n')

# --- sliders ---
#  slider functions to update values
def set_velocity(s):
    velocity_label.text = f'  Launch Velocity: {s.value:.1f} m/s\n'

def set_angle(s):
    angle_label.text = f'  Launch Angle: {s.value:.0f}°\n'

def set_wind(s):
    wind_label.text = f'  Wind Resistance: {s.value:.3f}\n'

scene.append_to_caption('\n--- Launch Parameters (adjust then hit Reset) ---\n')
velocity_slider = slider(min=1, max=15, value=vConstant, step=0.1, bind=set_velocity)
velocity_label = wtext(text=f'  Launch Velocity: {vConstant:.1f} m/s\n')

angle_slider = slider(min=5, max=85, value=50, step=1, bind=set_angle)
angle_label = wtext(text=f'  Launch Angle: 50°\n')

wind_slider = slider(min=0, max=0.1, value=wind_resistance, step=0.001, bind=set_wind)
wind_label = wtext(text=f'  Wind Resistance: {wind_resistance:.3f}\n')

#  main loop where the magic happens
while True:
    rate(500)
    if running and ball.pos.y >= 0:
        #  gravity n wind stuff
        FEnet = vector(0, ball.mass * -g, 0)
        Fwind = -wind_resistance * ball.v.mag2 * norm(ball.v)
        Fnet = FEnet + Fwind

        #moving the ball based on forces
        ball.mo += Fnet * dt
        ball.v = ball.mo / ball.mass
        ball.pos += ball.v * dt
        ball_2.pos = vec(x0 + vConstant * cos(theta) * t, 
                         y0 + vConstant * sin(theta) * t - g / 2 * t ** 2, 0)

        #  keep the speed graph updated
        b_speed.plot(pos=(t, mag(ball.v)))
        t += dt

        #update live stats on screen
        d = hole.pos.x - ball.pos.x
        hud_velocity.text = f"Velocity: {mag(ball.v):.2f} m/s\n"
        hud_distance.text = f"Distance from target: {d:.2f} m\n"

    #  stop if it hits the ground
    if ball.pos.y < 0 and running:
        impact_force = mag(Fnet)
        hud_impact.text = f"Impact force on {current_env}: {impact_force:.2f} Newtons\n"
        running = False
        run_button.text = "Run"
