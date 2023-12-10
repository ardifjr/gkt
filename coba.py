import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import cos, sin, pi

# Inisialisasi Pygame di bagian awal
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set orthographic projection
glOrtho(-1, 1, -1, 1, -1, 1)

snow_positions = [
    {"x": -0.7, "y": 0.9, "scale": 0.25},
    {"x": 0.2, "y": 0.8, "scale": 0.3},
    {"x": 0.8, "y": 0.7, "scale": 0.28},
    {"x": -0.5, "y": 0.6, "scale": 0.23},
    {"x": 0.4, "y": 0.5, "scale": 0.26},
    {"x": 1.0, "y": 0.4, "scale": 0.29}
]

def draw_snowflake(position):
    x, y, scale = position["x"], position["y"], position["scale"]
    glColor3f(1.0, 1.0, 1.0)  # Warna putih untuk salju
    glPointSize(5.0)  # Ubah ukuran titik salju menjadi lebih besar
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_grass():
    glColor3f(0.0, 0.8, 0.0)  # Warna hijau untuk rumput
    glBegin(GL_QUADS)
    glVertex2f(-1, -0.6)  # Ubah posisi bawah rumput
    glVertex2f(1, -0.6)
    glVertex2f(1, -1)
    glVertex2f(-1, -1)
    glEnd()

def draw_sun(rotation_angle):
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for the sun

    glPushMatrix()  # Save the current matrix
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)  # Rotate around the Z-axis

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(-0.85, 0.85)  # Center coordinates of the sun
    num_segments = 50  # Reduce the number of segments
    radius = 0.1

    for i in range(num_segments + 1):
        theta = 2.0 * pi * i / num_segments
        x = -0.85 + radius * cos(theta)
        y = 0.85 + radius * sin(theta)
        glVertex2f(x, y)

    glEnd()

    glColor3f(1.0, 1.0, 0.0)  # Yellow color for sun rays
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

    glPopMatrix()  # Restore the previous matrix

def draw_road():
    glColor3f(0.4, 0.4, 0.4)  # Warna abu-abu untuk jalan
    glBegin(GL_QUADS)
    glVertex2f(-1, -0.6)  # Koordinat bawah jalan
    glVertex2f(1, -0.6)
    glVertex2f(1, -0.2)  # Koordinat atas jalan (memperlebar jalan ke atas)
    glVertex2f(-1, -0.2)
    glEnd()

    # Gambar garis putih di tengah jalan (dipotong-potong)
    glColor3f(1.0, 1.0, 1.0)  # Warna putih untuk garis jalan
    glLineWidth(6.0)  # Ubah ketebalan garis

    num_segments = 40  # Jumlah potongan garis putih
    segment_length = 2.0 / num_segments  # Panjang tiap potongan garis
    glBegin(GL_LINES)
    for i in range(num_segments + 1):  # Ubah +1 agar mencakup titik akhir
        if i % 2 == 0:  # Gambar garis putih hanya pada iterasi genap
            glVertex2f(-1 + i * segment_length, -0.4)  # Koordinat awal garis
            glVertex2f(-1 + (i + 1) * segment_length, -0.4)  # Koordinat akhir garis
    glEnd()
    
def draw_cloud(position):
    x, y, scale = position["x"], position["y"], position["scale"]
    glColor3f(1.0, 1.0, 1.0)  # Warna putih untuk awan
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)  # Titik tengah awan
    num_segments = 100  # Jumlah segmen untuk awan

    for i in range(num_segments):
        angle = 2.0 * pi * i / num_segments
        cloud_radius = 0.1 * scale  # Ukuran awan
        cloud_x = x + cloud_radius * cos(angle)  # Pergerakan awan ke kanan
        cloud_y = y + 0.05 * scale * sin(angle)
        glVertex2f(cloud_x, cloud_y)

    glEnd()

def draw_car(position):
    x, y, scale = position["x"], position["y"], position["scale"]
    glColor3f(0.3, 0.3, 0.3)  # Warna abu-abu gelap untuk mobil

    # Badan mobil
    glBegin(GL_QUADS)
    glVertex2f(x - 0.40 * scale, y + 0.15 * scale)  # Posisi kiri bawah
    glVertex2f(x + 0.35 * scale, y + 0.15 * scale)  # Posisi kanan bawah
    glVertex2f(x + 0.40 * scale, y + 0.1 * scale)  # Posisi kanan atas
    glVertex2f(x - 0.35 * scale, y + 0.1 * scale)  # Posisi kiri atas
    glEnd()

    # Roda mobil
    glColor3f(0.0, 0.0, 0.0)  # Warna hitam untuk roda
    glPointSize(37.0)  # Ukuran titik roda
    glBegin(GL_POINTS)
    glVertex2f(x - 0.3 * scale, y + 0.1 * scale)  # Posisi roda kiri bawah
    glVertex2f(x + 0.3 * scale, y + 0.1 * scale)  # Posisi roda kanan bawah
    glEnd()

    # Jendela
    glColor3f(0.7, 0.9, 1.0)  # Warna biru muda untuk jendela
    glBegin(GL_QUADS)
    glVertex2f(x - 0.3 * scale, y + 0.15 * scale)  # Posisi kiri bawah jendela
    glVertex2f(x + 0.3 * scale, y + 0.15* scale)  # Posisi kanan bawah jendela
    glVertex2f(x + 0.2 * scale, y + 0.3 * scale)  # Posisi kanan atas jendela
    glVertex2f(x - 0.2 * scale, y + 0.3 * scale)  # Posisi kiri atas jendela
    glEnd()

    # Pintu
    glColor3f(0.0, 0.0, 0.4)  # Warna abu-abu gelap untuk pintu
    glBegin(GL_QUADS)
    glVertex2f(x + 0.05 * scale, y + 0.15 * scale)  # Posisi kiri bawah pintu
    glVertex2f(x + 0.1 * scale, y + 0.15 * scale)  # Posisi kanan bawah pintu
    glVertex2f(x + 0.1 * scale, y + 0.3 * scale)  # Posisi kanan atas pintu
    glVertex2f(x + 0.05 * scale, y + 0.3 * scale)  # Posisi kiri atas pintu
    glEnd()
    
    
car_position = {"x": -1.2, "y": -0.55, "scale": 2.0}
car_speed = 0.005

    
def draw_grass_with_snow():
    # Draw the green grass
    glColor3f(0.0, 0.8, 0.0)  # Green color for grass
    glBegin(GL_QUADS)
    glVertex2f(-1, -0.6)  # Bottom position of grass
    glVertex2f(1, -0.6)
    glVertex2f(1, -1)
    glVertex2f(-1, -1)
    glEnd()

    # Draw white snow piles on top of the grass
    glColor3f(1.0, 1.0, 1.0)  # White color for snow
    for snow_position in snow_positions:
        x, y, scale = snow_position["x"], snow_position["y"], snow_position["scale"]
        glBegin(GL_TRIANGLES)
        glVertex2f(x - 0.05 * scale, y - 0.6 * scale)  # Left bottom of snow pile
        glVertex2f(x + 0.05 * scale, y - 0.6 * scale)  # Right bottom of snow pile
        glVertex2f(x, y - 0.5 * scale)  # Top of snow pile
        glEnd()
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Gambar langit
    glColor3f(1.0, 0.498, 0.314)  # Orange-red color for sunset
    glBegin(GL_QUADS)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, 1)
    glVertex2f(-1, 1)
    glEnd()

    draw_sun(rotation_angle)  # Pass the rotation_angle to draw_sun
    # Gambar rumput
    draw_grass()
    
    # Gambar jalan
    draw_road()
    draw_grass_with_snow()
    draw_car(car_position)

    # Update the car's position
    car_position["x"] += car_speed

    # Reset car's position if it goes beyond the right edge of the screen
    if car_position["x"] > 1.2:
        car_position["x"] = -1.2    
    # Gambar salju
    for snow_position in snow_positions:
        draw_snowflake(snow_position)

    # Perbarui posisi salju
    for snow_position in snow_positions:
        snow_position["y"] -= 0.001  # Ubah nilai ini sesuai kecepatan yang Anda inginkan

    # Gambar awan
    cloud_positions = [
        {"x": -0.5, "y": 0.8, "scale": 0.8},
        {"x": 0.0, "y": 0.9, "scale": 1.2},
        {"x": 0.7, "y": 0.7, "scale": 0.9},
        {"x": -0.8, "y": 0.6, "scale": 1.0},
        {"x": 0.4, "y": 0.5, "scale": 0.7},
        {"x": 1.1, "y": 0.5, "scale": 1.2}
    ]
    for cloud_position in cloud_positions:
        draw_cloud(cloud_position)

    pygame.display.flip()
rotation_angle = 0.0  # Initial rotation angle
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    draw()
    rotation_angle += -0.1  # Adjust the rotation speed as needed

    pygame.time.wait(10)
