#CSE423 Lab
#Abujor Dishary Shabbib
#22101653 #Section 01
#Assignment 02 Diamond catching game

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


is_timer_running = False

# Coordinates for plate
plate_x1 = 210
plate_x2 = 350
plate_y1 = 20
plate_y2 = 0
score = 0

diamond_x = random.randint(0, 750)
diamond_y = 600
diamond_speed = 7


is_game_over = False
is_game_paused = False
diamond_color = [random.random(), random.random(), random.random()]


# def set_pixel(x, y):
#     glBegin(GL_POINTS)
#     glVertex2f(x, y)
#     glEnd()
#     glFlush()

def set_pixel(x, y):
    glBegin(GL_POINTS)
    # Draw a 3x3 block of points to simulate thickness
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            glVertex2f(x + dx, y + dy)
    glEnd()
    glFlush()


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx >= 0:
        if dy >= 0:
            return 0 if abs(dx) > abs(dy) else 1
        else:
            return 7 if abs(dx) > abs(dy) else 6
    else:
        if dy >= 0:
            return 3 if abs(dx) > abs(dy) else 2
        else:
            return 4 if abs(dx) > abs(dy) else 5
        
def convert_to_original_zone(x, y, original_zone):
    if original_zone == 0:
        return x, y
    elif original_zone == 1:
        return y, x
    elif original_zone == 2:
        return -y, x
    elif original_zone == 3:
        return -x, y
    elif original_zone == 4:
        return -x, -y
    elif original_zone == 5:
        return -y, -x
    elif original_zone == 6:
        return y, -x
    elif original_zone == 7:
        return x, -y


def convert_to_zone_zero(x, y, original_zone):
    if original_zone == 0:
        return x, y
    elif original_zone == 1:
        return y, x
    elif original_zone == 2:
        return y, -x
    elif original_zone == 3:
        return -x, y
    elif original_zone == 4:
        return -x, -y
    elif original_zone == 5:
        return -y, -x
    elif original_zone == 6:
        return -y, x
    elif original_zone == 7:
        return x, -y

def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = convert_to_zone_zero(x1, y1, zone)
    x2, y2 = convert_to_zone_zero(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incr_E = 2 * dy
    incr_NE = 2 * (dy - dx)
    x, y = x1, y1
    while x < x2:
        if d <= 0:
            d += incr_E
            x += 1
        else:
            d += incr_NE
            x += 1
            y += 1
        New_x, New_y = convert_to_original_zone(x, y, zone)
        set_pixel(New_x, New_y)
 # Draw diamond
def draw_diamond():
    # glLineWidth(10)
    draw_line(diamond_x, diamond_y, diamond_x + 10, diamond_y + 15)
    draw_line(diamond_x + 10, diamond_y - 15, diamond_x, diamond_y)
    draw_line(diamond_x + 20, diamond_y, diamond_x + 10, diamond_y + 15)
    draw_line(diamond_x + 10, diamond_y - 15, diamond_x + 20, diamond_y)


 # Draw plate
def draw_plate():
    # glLineWidth()
    # Upper line
    draw_line(plate_x1, plate_y1, plate_x2, plate_y1)
    # Lower line
    draw_line(plate_x1 + 20, plate_y2, plate_x2 - 20, plate_y2)
    # Connect
    draw_line(plate_x1 + 20, plate_y2, plate_x1, plate_y1)
    draw_line(plate_x2 - 20, plate_y2, plate_x2, plate_y1)





def display():
    global is_game_over, diamond_color
    glClear(GL_COLOR_BUFFER_BIT)
    # glLineWidth(10)


    if not is_game_over:

        glColor3f(*diamond_color)
        draw_diamond()

        glColor3f(1.0, 1.0, 1.0)
        draw_plate()

        # Restart button
        glColor3f(0.0, 0.6, 0.6)
        draw_line(50, 550, 100, 550)
        draw_line(50, 550, 70, 570)
        draw_line(70, 530, 50, 550)

        # Terminate button
        glLineWidth(100)
        glColor3f(1.0, 0.0, 0.0)
        draw_line(700, 530, 750, 570)
        draw_line(750, 530, 700, 570)

        # Catch Diamond #collision
        if (diamond_x +20 >= plate_x1 and diamond_x  <= plate_x2 and diamond_y -20 <= plate_y1 ):

            global score, diamond_speed

            score += 1
            print("Score:", score)
            reset_diamond()
            diamond_speed += 1.2
            diamond_color = (random.random(), random.random(), random.random())
            # diamond_color = [random.uniform(0.6, 1.0) for _ in range(3)]


        # Diamond miss the plate
        if diamond_y + 16 < plate_y2:
            is_game_over = True
            print(f"Game Over! Final Score: {score}")
            glColor3f(1.0, 0.0, 0.0)
            draw_plate()
            glutIdleFunc(None)

        glColor3f(1.0, 0.8, 0.0)
        if not is_game_paused:
            # Pause button
            draw_line(400, 530, 400, 580)
            draw_line(420, 530, 420, 580)
        elif is_game_paused:
            # Play button
            # draw_line(400, 530, 400, 580)
            # draw_line(400, 530, 430, 550)
            # draw_line(430, 550, 400, 580)
            # Play button (when game is paused)
            draw_line(400, 530, 400, 580)  # Left vertical line
            draw_line(400, 530, 450, 555)       # Diagonal to top (centered)
            draw_line(450, 555, 400, 580)    # Diagonal to bottom

    else:
        glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()

def pause():
    global is_game_paused
    is_game_paused = not is_game_paused
    # if is_game_paused:
    #     print("Game Paused") #checking if its pausing or not
    # else:
    #     print("Game Resumed")
    #     glutTimerFunc(0, update_game, 0)

    if not is_game_paused:  # If unpausing
        glutTimerFunc(0, update_game, 0)

def update_game(value):
    global diamond_y, is_timer_running

    if not is_game_over and not is_game_paused:
        diamond_y -= diamond_speed
        glutPostRedisplay()
        glutTimerFunc(16, update_game, 0)
    else:
        is_timer_running = False #Stop the timer loop when game is over or paused


def reset_diamond():
    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(20, 760)# Ensure diamond stays inside 800px screen
    diamond_y = 600

def restart_game():
    glColor3f(0.0, 0.7, 0.7)
    global is_game_over, score, diamond_speed ,is_game_paused, diamond_color, is_timer_running
    # glutTimerFunc(-1, None, 0)
    is_game_over = False
    is_game_paused = False
    score = 0
    diamond_speed = 4
    # print(f"Speed after restart: {diamond_speed}")
    diamond_color = [random.random(), random.random(), random.random()]
    reset_diamond()
    
    if not is_timer_running:
        is_timer_running = True
        glutTimerFunc(0, update_game, 0)

    print("Starting Over")
# def reset_diamond():
#     global diamond_x, diamond_y, diamond_color
#     diamond_x = random.randint(0, 750)
#     diamond_y = 600

def reset_diamond():
    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(20, 740)  # Ensure diamond (40px wide) stays inside 800px screen
    diamond_y = 600

def special_key(key, x, y):
    global plate_x1, plate_x2, is_game_paused

    if not is_game_over and not is_game_paused:
        if key == GLUT_KEY_LEFT:
            change = -15
        elif key == GLUT_KEY_RIGHT:
            change = 15
        else:
            return

        dx = plate_x2 - plate_x1
        plate_x1 += change
        plate_x2 = plate_x1 + dx

        # Plate Boundary check
        if plate_x1 < 0:
            plate_x1 = 0
            plate_x2 = dx
        if plate_x2 > 800:
            plate_x2 = 800
            plate_x1 = 800 - dx

        glutPostRedisplay()

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Pause button
        if 400 <= x <= 510 and 35 <= y <= 85:
            pause()
        # Restart button
        elif 30 <= x <= 110 and 25 <= y <= 75:
            restart_game()
        # Terminate button
        if 660 <= x <= 760 and 20 <= y <= 80:
            global score
            print(f"Good Bye! Score: {score}")
        
            
            glutLeaveMainLoop()
            


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0, 800, 0, 600)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
# glPointSize(3)  # Add this in your init() to thicken points (if using points)

glutInitWindowSize(800, 600)
glutCreateWindow(b"423_Assignment_2 Catch the diamonds")
glutDisplayFunc(display)
glutSpecialFunc(special_key)
glutMouseFunc(mouse)
init()
glutTimerFunc(0, update_game, 0)
glutMainLoop()