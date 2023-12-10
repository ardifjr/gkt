def draw_car(position):
    global wheel_rotation
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
    
    # Draw wheels with rotation
    glRotatef(wheel_rotation, 0, 0, 1)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(37.0)
    glBegin(GL_POINTS)
    glVertex2f(-0.3 * scale, 0.1 * scale)
    glVertex2f(0.3 * scale, 0.1 * scale)
    glEnd()

    glPopMatrix()