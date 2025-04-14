# By Simeon Beckford-Tongs BSc MSc Copyright © 2024. All rights reserved. By Simeon Beckford-Tongs BSc MSc Copyright © 2023. All rights reserved.
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from vpython import *
import random

def create_particle(radius, color, cube_size):
    half_size = cube_size / 2
    return sphere(
        radius=radius,
        color=color,
        pos=vector(random.uniform(-half_size, half_size), random.uniform(-half_size, half_size), random.uniform(-half_size, half_size)),
        velocity=vector(random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2))
    )

def check_collision(p1, p2):
    distance = mag(p1.pos - p2.pos)
    return distance < p1.radius + p2.radius

def create_walls(cube_size):
    wall_thickness = 0.1
    wall_opacity = 0.3  # Semi-transparent walls
    half_size = cube_size / 2

    # Create walls (excluding one wall for viewing)
    box(pos=vector(0, 0, -half_size), size=vector(cube_size, cube_size, wall_thickness), color=color.white, opacity=wall_opacity)  # Back
    box(pos=vector(-half_size, 0, 0), size=vector(wall_thickness, cube_size, cube_size), color=color.white, opacity=wall_opacity)  # Left
    box(pos=vector(half_size, 0, 0), size=vector(wall_thickness, cube_size, cube_size), color=color.white, opacity=wall_opacity)  # Right
    box(pos=vector(0, -half_size, 0), size=vector(cube_size, wall_thickness, cube_size), color=color.white, opacity=wall_opacity)  # Bottom
    box(pos=vector(0, half_size, 0), size=vector(cube_size, wall_thickness, cube_size), color=color.white, opacity=wall_opacity)  # Top

def create_explosion(position):
    explosion = sphere(pos=position, radius=0.5, color=color.yellow, opacity=0.6, make_trail=True)
    explosion.trail_radius = 0.1
    explosion.lifetime = 0.1
    return explosion

def run_simulation(num_red_particles, num_blue_particles, collision_elimination_chance, cube_size):
    # Initialize scene
    scene = canvas(title='3D Particle Simulation', width=600, height=400)
    scene.camera.pos = vector(0, 0, -cube_size)  # Slightly zoomed out

    # Create walls
    create_walls(cube_size)

    # Add instructions
    instructions = """
    Instructions:
    - Rotate: Drag with right mouse button or Ctrl+drag.
    - Zoom: Use the mouse wheel or drag with both mouse buttons or Alt/Option + drag.
    - Pan: Shift + drag.
    """
    label(pos=vector(0, -cube_size/2 - 2, 0), text=instructions, height=12, box=False, line=False)

    # Create particles
    red_particles = [create_particle(0.2, color.red, cube_size) for _ in range(num_red_particles)]
    blue_particles = [create_particle(0.1, color.blue, cube_size) for _ in range(num_blue_particles)]
    particles = red_particles + blue_particles

    # Simulation loop
    while True:
        rate(60) # Controls the speed of the simulation

        particles_to_remove = set()
        explosions = []

        for i, particle in enumerate(particles):
            # Update position
            particle.pos += particle.velocity

            # Boundary collision
            for coord in ['x', 'y', 'z']:
                if abs(getattr(particle.pos, coord)) > cube_size / 2 - particle.radius:
                    setattr(particle.velocity, coord, -getattr(particle.velocity, coord))

            # Particle collision detection and response
            for other in particles[i+1:]:
                if check_collision(particle, other):
                    if random.random() < collision_elimination_chance:
                        particle.visible = False
                        other.visible = False
                        particles_to_remove.add(particle)
                        particles_to_remove.add(other)
                        explosions.append(create_explosion((particle.pos + other.pos) / 2))

        # Remove collided particles from the list
        for p in particles_to_remove:
            if p in red_particles:
                red_particles.remove(p)
            elif p in blue_particles:
                blue_particles.remove(p)
        particles = [p for p in particles if p not in particles_to_remove]

        # Update and display particle counts
        print(f"Red particles: {len(red_particles)}, Blue particles: {len(blue_particles)}")

        # Manage explosions
        for explosion in explosions:
            explosion.lifetime -= 1/60
            if explosion.lifetime <= 0:
                explosion.visible = False

# GUI to get user input
def get_user_input():
    def on_submit():
        global num_red_particles, num_blue_particles, collision_elimination_chance
        num_red_particles = int(red_particles_entry.get())
        num_blue_particles = int(blue_particles_entry.get())
        collision_elimination_chance = elimination_chance_slider.get() / 100
        root.destroy()

    root = tk.Tk()
    root.title("Particle Simulation Settings")

    tk.Label(root, text="Enter number of red particles:").grid(row=0, column=0)
    red_particles_entry = tk.Entry(root)
    red_particles_entry.grid(row=0, column=1)

    tk.Label(root, text="Enter number of blue particles:").grid(row=1, column=0)
    blue_particles_entry = tk.Entry(root)
    blue_particles_entry.grid(row=1, column=1)

    tk.Label(root, text="Collision elimination chance:").grid(row=2, column=0)
    elimination_chance_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
    elimination_chance_slider.grid(row=2, column=1)

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=3, columnspan=2)

    root.mainloop()

# Get user input via GUI
get_user_input()

# Define default cube size
cube_size = 20

# Run simulation if inputs are valid
if num_red_particles is not None and num_blue_particles is not None and collision_elimination_chance is not None:
    run_simulation(num_red_particles, num_blue_particles, collision_elimination_chance, cube_size)
else:
    print("Simulation aborted due to invalid input.")
