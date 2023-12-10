def draw_sun(rotation_angle):
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for the sun

    glPushMatrix()  # Save the current matrix
    glRotatef(rotation_angle, 0.0, 5.0, 5.0)  # Rotate around the Z-axis

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

    glPopMatrix() 