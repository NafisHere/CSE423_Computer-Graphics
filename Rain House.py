# #22101653
# #Abujor Dishary Shabbib Sec 01

# ####################################      TASK  1    #######################################
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math


drops = []
RainDropSpeed = 0.5
drop_angle = 0  
StructureColor = [0.4, 1.0, 1.0]   #white
BackGroundColor = [0, 0, 0]  #black
ColourShiftSpeed = 0.05

# Initialize raindrops random position e top theke
def init_drops():
    global drops
    drops = []
    i = 0;
    while i < 500:

        # 500 extra niyechi shb jaigai to feels more realistic
        x = random.randint(-1000, 1500) #random x cordinate
        y = random.randint(500, 1000)  # upor theke start hocche rains random y co ordinate within range
        drops.append([x, y]) #add co ordinates to the drop list
        i += 1


# for house structure 
def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1) #start
    glVertex2f(x2, y2) #end
    glEnd()

# door lock 
def DrawDots(x, y):
    glPointSize(7)
    glBegin(GL_POINTS)
    glVertex2f(x, y) #point co ordinate
    glEnd()

# house rooftop 
def Create_Roof(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()


# full house building
def RenderHouse(BaseX, BaseY, width, height):

    # Set house color
    glColor3f(StructureColor[0], StructureColor[1], StructureColor[2])
    
    roof_h = 155
    door_w = 85
    door_h = 160
    WinW = 70
    WinH = 50
    
    
    glLineWidth(5)

    # Roof
    Create_Roof(BaseX - 20, BaseY + height, BaseX + width + 20, BaseY + height,  BaseX + width / 2, BaseY + height + roof_h)
                  # left point (slight shift left)                 right point (slight shift right)                           pick point 
    
    # House frame
    draw_line(BaseX, BaseY, BaseX + width, BaseY)  # Bottom
    draw_line(BaseX, BaseY, BaseX, BaseY + height)  # Left
    draw_line(BaseX + width, BaseY, BaseX + width, BaseY + height)  # Right

    # Door
    glLineWidth(2)

    door_x = 125  # assume 
    draw_line(door_x, BaseY, door_x, BaseY + door_h)  # Left
    draw_line(door_x + door_w, BaseY, door_x + door_w, BaseY + door_h)  # Right
    draw_line(door_x, BaseY + door_h, door_x + door_w, BaseY + door_h)  # Top
    DrawDots(190, 150)  # Door lock

    # ---------------------------------------------------------------------------------
    # Window
    glLineWidth(2)
    WinX = BaseX + width * 0.6  # window r starting point ta find out korchi 
    WinY = BaseY + height * 0.4  
    draw_line(WinX, WinY, WinX + WinW, WinY)  # Bottom
    draw_line(WinX, WinY, WinX, WinY + WinH)  # Left
    draw_line(WinX + WinW, WinY, WinX + WinW, WinY + WinH)  # Right
    draw_line(WinX, WinY + WinH, WinX + WinW, WinY + WinH)  # Top

    MidX = WinX + WinW / 2   # horizontal center
    MidY = WinY + WinH / 2  # vertical center
    draw_line(MidX, WinY, MidX, WinY + WinH)     # Drawing a vertical line in the middle of the window
    draw_line(WinX, MidY, WinX + WinW, MidY)     # Drawing a horizontal line in the middle of the window


# how rain moves
def Animate():
    global drops, RainDropSpeed, drop_angle

    angle_rad = math.radians(drop_angle) #radian e niye calculation
    x_delta = math.sin(angle_rad) * RainDropSpeed  #how much raindrop moves in one frame in x axis
    y_delta = math.cos(angle_rad) * RainDropSpeed   #how much raindrop moves in one frame in y axis

    for drop in drops: #drops (x,y)
        drop[0] -= x_delta #left if +ve right if -ve
        drop[1] -= y_delta

        if drop[1] < 200 or check_collision(drop[0], drop[1]): #check if raindrop falls below certain position  or collite with anything?
            if check_collision(drop[0], drop[1]):
                drop[0] = random.randint(-1000, 1500)  # Reset rain position
                drop[1] = random.randint(500, 1000)    # Top of the screen
            else:
                drop[0] = random.randint(-1000, 1500)
                drop[1] = random.randint(500, 1000)

    glutPostRedisplay()


#rain draw korar func
def draw_rain():
    global drop_angle

    angle_rad = math.radians(drop_angle)
    x_delta = 10 * math.sin(angle_rad) #change in x co
    y_delta = 10 * math.cos(angle_rad) #change in y co

    glLineWidth(2) #raindrop width

    glBegin(GL_LINES)
    for x, y in drops:
        glVertex2f(x, y)
        glVertex2f(x - x_delta, y - y_delta)
    glEnd()



def check_collision(x, y):

   
    # Rooftop collision
    if 60 <= x <= 440 and 280 <= y <= 330: 
        return True
    # Wall collision
    if 60 <= x <= 440 and 60 <= y <= 280: 
        return True

    return False


def keyboard_input(key, x, y):
    global BackGroundColor, StructureColor, ColourShiftSpeed

    if key == b'd':  # Lightening to day
        if BackGroundColor[0] < 1.0:
            BackGroundColor[0] += ColourShiftSpeed
        if BackGroundColor[1] < 1.0:
            BackGroundColor[1] += ColourShiftSpeed
        if BackGroundColor[2] < 1.0:
            BackGroundColor[2] += ColourShiftSpeed

    elif key == b'n':  # Getting darker night
        if BackGroundColor[0] > 0.0:
            BackGroundColor[0] -= ColourShiftSpeed
        if BackGroundColor[1] > 0.0:
            BackGroundColor[1] -= ColourShiftSpeed
        if BackGroundColor[2] > 0.0:
            BackGroundColor[2] -= ColourShiftSpeed

    # Update house and rain color based on BackGroundColor change
    if BackGroundColor[0] <= 0.5:
        StructureColor[0] = 0.4
        StructureColor[1] = 1.0
        StructureColor[2] = 1.0
    else:
        StructureColor[0] = 0.0
        StructureColor[1] = 0.0
        StructureColor[2] = 0.0

    glutPostRedisplay()

def SpecialKeyboardInput(key, x, y):
    global drop_angle
    if key == GLUT_KEY_LEFT:
        if drop_angle < 45:  # Limit leftward tilt
            drop_angle += 2 
    elif key == GLUT_KEY_RIGHT:
        if drop_angle > -45:  # Limit rightward tilt
            drop_angle -= 2  

    glutPostRedisplay()

def show_screen():
    global BackGroundColor

    # Set BackGroundColor based on day/night setting
    glClearColor(BackGroundColor[0], BackGroundColor[1], BackGroundColor[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set up 2D viewing region
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Draw house and rain with updated element color
    RenderHouse(BaseX=80, BaseY=80, width=350, height=200)  #starting point 80, 80 of the house
    glColor3f(StructureColor[0], StructureColor[1], StructureColor[2]) 
    draw_rain()

    glutSwapBuffers()
    

# Initialize GLUT and set up window
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Task1:Rain and House")

# Register callbacks
glutDisplayFunc(show_screen)
glutIdleFunc(Animate)
glutKeyboardFunc(keyboard_input)
glutSpecialFunc(SpecialKeyboardInput)

# Initialize raindrops and start main loop
init_drops()
glutMainLoop()

# ####################################      End of TASK  1    #######################################



# ####################################      TASK  2    #######################################


# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random



# def UpdateDots():
#     if frozen == True:
#         return

#     for point in points:
#         point["x"] += point["dx"] * point["speed"] * speed_multiplier #new position of dot x axis
#         point["y"] += point["dy"] * point["speed"] * speed_multiplier #new position of dot y axis

#         #direction reverse  if it clashes with boundary
#         if not (0 <= point["x"] <= height):
#             point["dx"] *= -1
#         if not (0 <= point["y"] <= width):
#             point["dy"] *= -1
#         # for blink
#         if point["blink"]:
#             point["visible"] = not point["visible"]



# def SpecialKeyboardInput(key, x, y):
#     global speed_multiplier
#     MAX_SPEED = 15.0  # Set upper limit for speed
#     MIN_SPEED = 0.1  # Set lower limit for speed
#     if key == GLUT_KEY_UP:
#         if speed_multiplier * 1.2 <= MAX_SPEED:  # Ensure it doesn't exceed max speed
#             speed_multiplier *= 1.2
#             print("Speed Increased:", speed_multiplier)
#         else:
#             print("Max Speed Reached!")

#     elif key == GLUT_KEY_DOWN:
#         if speed_multiplier / 1.2 >= MIN_SPEED:  # Ensure it doesn't go below min speed
#             speed_multiplier /= 1.2
#             print("Speed Decreased:", speed_multiplier)
#         else:
#             print("Min Speed Reached!")

#     glutPostRedisplay()


# def MouseClickInput(button, state, x, y):
#     if state == GLUT_DOWN: #button pressed down?
#         initial_x = x #(x, y) mouse position
#         initial_y = height - y

#         if button == GLUT_RIGHT_BUTTON:
#             dx = random.choice([-1, 1])
#             dy = random.choice([-1, 1]) #random choosed co ordinates -1 or 1
#             r = random.random() #random choosed colours
#             g = random.random()
#             b = random.random()
#             #adding each point details as dictionary
#             points.append({
#                 "x": initial_x, "y": initial_y, "r": r, "g": g, "b": b, "dx": dx, "dy": dy, "speed": 0.5,"blink": False, "visible": True
#             })
            
#         elif button == GLUT_LEFT_BUTTON:
#             for i in points:
#                 i["blink"] = not i["blink"]

#     glutPostRedisplay()

# def iterate():
#     glViewport(0, 0, height, width)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, height, 0.0, width, 0.0, 1.0)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()

# def KeyboardInput(key, x, y):
#     global frozen
#     if key == b' ':
#         frozen = not frozen
#         print("Frozen")

#     glutPostRedisplay()


# def showScreen():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     iterate()
#     glColor3f(1.0, 1.0, 0.0)
#     DrawDots()
#     glutSwapBuffers()

# def DrawDots():
#     glPointSize(5)
#     glBegin(GL_POINTS)
#     for point in points:
#         if point["visible"]:
#             glColor3f(point["r"], point["g"], point["b"])
#             glVertex2f(point["x"], point["y"])
#     glEnd()

# def timer(value):
#     UpdateDots()
#     glutPostRedisplay()
#     glutTimerFunc(8, timer, 0)


# #global variables
# speed_multiplier = 1.0
# width, height = 500, 500
# points = []
# frozen = False


# glutInit()
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(height, width)
# glutInitWindowPosition(0, 0)
# wind = glutCreateWindow(b"Task-2 Amazing Dots Inside the box")
# glutDisplayFunc(showScreen)
# glutMouseFunc(MouseClickInput)
# glutSpecialFunc(SpecialKeyboardInput)

# glutKeyboardFunc(KeyboardInput)
# glutTimerFunc(100, timer, 0)
# glutMainLoop()

####################################      End of TASK  2    #######################################

