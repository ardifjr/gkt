import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import cos, sin, pi
import time

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
snow_positions = [
    {"x": -0.7, "y": 0.9, "scale": 0.25},
    {"x": 0.2, "y": 0.8, "scale": 0.3},
    {"x": 0.8, "y": 0.7, "scale": 0.28},
    {"x": -0.5, "y": 0.6, "scale": 0.23},
    {"x": 0.4, "y": 0.5, "scale": 0.26},
    {"x": 1.0, "y": 0.4, "scale": 0.29}
]
car_position = {"x": -1.2, "y": -0.55, "scale": 2.0}
car_speed = 0.015
original_cloud_positions = [
    {"x": -0.5, "y": 0.8, "original_scale": 0.3},
    {"x": 0.0, "y": 0.9, "original_scale": 0.9},
    {"x": 0.7, "y": 0.7, "original_scale": 0.9},
    {"x": -0.8, "y": 0.6, "original_scale": 1.0},
    {"x": 0.4, "y": 0.5, "original_scale": 0.7},
    {"x": 1.1, "y": 0.5, "original_scale": 1.2}
]

def draw_snowflake(position):
    x, y, scale = position["x"], position["y"], position["scale"]
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_sun(rotation_angle):
    glColor3f(1.0, 1.0, 0.0)
    glPushMatrix()
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(-0.85, 0.85)
    num_segments = 50
    radius = 0.1
    for i in range(num_segments + 1):
        theta = 2.0 * pi * i / num_segments
        x = -0.85 + radius * cos(theta)
        y = 0.85 + radius * sin(theta)
        glVertex2f(x, y)
    glEnd()
    glColor3f(1.0, 1.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    for i in range(num_segments):
        theta = 2.0 * pi * i / num_segments
        x1 = -0.85 + (radius - 0.02) * cos(theta)
        y1 = 0.85 + (radius - 0.02) * sin(theta)
        x2 = -0.85 + (radius + 0.02) * cos(theta)
        y2 = 0.85 + (radius + 0.02) * sin(theta)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
    glEnd()
    glPopMatrix()

def draw_road():
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_QUADS)
    glVertex2f(-1, -0.6)
    glVertex2f(1, -0.6)
    glVertex2f(1, -0.2)
    glVertex2f(-1, -0.2)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(6.0)
    num_segments = 40
    segment_length = 2.0 / num_segments
    glBegin(GL_LINES)
    for i in range(num_segments + 1):
        if i % 2 == 0:
            glVertex2f(-1 + i * segment_length, -0.4)
            glVertex2f(-1 + (i + 1) * segment_length, -0.4)
    glEnd()

def draw_cloud(position):
    x, y, scale = position["x"], position["y"], position["scale"]
    glColor3f(1.0, 1.0, 1.0)
    num_circles = 8
    circle_radius = 0.08
    for i in range(num_circles):
        circle_x = x + (i * 0.1 * scale)
        circle_y = y
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(circle_x, circle_y)
        num_segments = 50
        for j in range(num_segments + 1):
            angle = 2 * pi * j / num_segments
            x_circle = circle_x + circle_radius * cos(angle) * scale
            y_circle = circle_y + circle_radius * sin(angle) * scale
            glVertex2f(x_circle, y_circle)
        glEnd()

def draw_car(position):
    x, y, scale = position["x"], position["y"], position["scale"]
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(x - 0.40 * scale, y + 0.15 * scale)
    glVertex2f(x + 0.35 * scale, y + 0.15 * scale)
    glVertex2f(x + 0.40 * scale, y + 0.1 * scale)
    glVertex2f(x - 0.35 * scale, y + 0.1 * scale)
    glEnd()
    glColor3f(0.0, 0.0, 0.0)
    num_segments = 50
    for wheel_position in [(x - 0.3 * scale, y + 0.1 * scale), (x + 0.3 * scale, y + 0.1 * scale)]:
        radius = 0.037 * scale
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(wheel_position[0], wheel_position[1])
        for i in range(num_segments + 1):
            theta = 2.0 * pi * i / num_segments
            x_wheel = wheel_position[0] + radius * cos(theta)
            y_wheel = wheel_position[1] + radius * sin(theta)
            glVertex2f(x_wheel, y_wheel)
        glEnd()
    glColor3f(0.7, 0.9, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(x - 0.3 * scale, y + 0.15 * scale)
    glVertex2f(x + 0.3 * scale, y + 0.15 * scale)
    glVertex2f(x + 0.2 * scale, y + 0.3 * scale)
    glVertex2f(x - 0.2 * scale, y + 0.3 * scale)
    glEnd()
    glColor3f(0.0, 0.0, 0.4)
    glBegin(GL_QUADS)
    glVertex2f(x + 0.05 * scale, y + 0.15 * scale)
    glVertex2f(x + 0.1 * scale, y + 0.15 * scale)
    glVertex2f(x + 0.1 * scale, y + 0.3 * scale)
    glVertex2f(x + 0.05 * scale, y + 0.3 * scale)
    glEnd()

def draw_grass_with_snow():
    glColor3f(0.0, 0.8, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(-1, -0.6)
    glVertex2f(1, -0.6)
    glVertex2f(1, -1)
    glVertex2f(-1, -1)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    for snow_position in snow_positions:
        x, y, scale = snow_position["x"], snow_position["y"], snow_position["scale"]
        glBegin(GL_TRIANGLES)
        glVertex2f(x - 0.05 * scale, y - 0.6 * scale)
        glVertex2f(x + 0.05 * scale, y - 0.6 * scale)
        glVertex2f(x, y - 0.5 * scale)
        glEnd()

def draw_car_shadow(position):
    x, y, scale = position["x"], position["y"], position["scale"]
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(x - 0.40 * scale, -0.5)
    glVertex2f(x + 0.35 * scale, -0.5)
    glVertex2f(x + 0.40 * scale, -0.38)
    glVertex2f(x - 0.35 * scale, -0.38)
    glEnd()

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(1.0, 0.498, 0.314)
    glBegin(GL_QUADS)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, 1)
    glVertex2f(-1, 1)
    glEnd()
    draw_sun(rotation_angle)
    draw_road()
    draw_grass_with_snow()
    draw_car_shadow(car_position)
    draw_car(car_position)
    car_position["x"] += car_speed
    if car_position["x"] > 1.2:
        car_position["x"] = -1.2
    for snow_position in snow_positions:
        draw_snowflake(snow_position)
    current_time = time.time()
    scaling_factor = (1 + sin(current_time)) * 0.2 + 0.8
    for cloud_position in original_cloud_positions:
        cloud_position["scale"] = scaling_factor * cloud_position["original_scale"]
    for cloud_position in original_cloud_positions:
        draw_cloud(cloud_position)
    pygame.display.flip()

cloud_positions = original_cloud_positions.copy()
rotation_angle = 0.0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    draw()
    rotation_angle += -0.1
    pygame.time.wait(10)