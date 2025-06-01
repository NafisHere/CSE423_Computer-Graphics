#22101653
#Abujor Dishary Shabbib
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math
import random
import time


#window er jonne
window_width = 1000
window_height = 800
grid_length = 600
fov_y = 120

# Player er jonne
player_pos = [0, 0, 0]
player_angle = 0
player_speed = 10
player_turn_speed = 8
player_life = 5
player_score = 0

#Enemy 
enemy_list = []
enemy_pulse = 1.0
enemy_pulse_time = 0
enemy_speed = 0.025
enemy_count = 5

# for guns
gun_speed = 0.5
gun_bullets = []
gun_missed_bullets = 0
gun_max_misses = 10
gun_bullet_speed = 6

# Camera-er jonne
camera_pos = [0, 600, 600]
camera_angle = 0
camera_radius = 600
camera_height = 600

# view Modes
mode_first_person = False
mode_cheat = False
mode_over = False

#cheat mode er jonne
cheat_last_bullet_time = 0
cheat_wait_time = 0.09
mode_follow_view = False
fixed_look_angle = 0
fixed_look_enabled = False

def drawGrid():
    glBegin(GL_QUADS)
   
    for i in range(-grid_length, grid_length + 1, 100):
        for j in range(-grid_length, grid_length + 1, 100):
            if (i + j) % 200 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)            
           
            glVertex3f(i, j, 0)             # Bottom left
            glVertex3f(i + 100, j, 0)          # Bottom right
            glVertex3f(i + 100, j + 100, 0)      # Top right
            glVertex3f(i, j + 100, 0)           # Top left

    # =========Boundary walls======================
   
    # Left Wall
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-grid_length, -grid_length, 0)        # Bottom left
    glVertex3f(-grid_length, grid_length+100, 0)        # Top left
    glVertex3f(-grid_length, grid_length+100, 100)     # Top right
    glVertex3f(-grid_length, -grid_length, 100)         # Bottom right
   
    # Right Wall
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(grid_length+100, -grid_length, 0)        # Bottom left
    glVertex3f(grid_length+100, grid_length+100, 0)      # Top left
    glVertex3f(grid_length+100, grid_length+100, 100)   # Top right
    glVertex3f(grid_length+100, -grid_length, 100)         # Bottom right
   
    # Bottom Wall
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(-grid_length, grid_length+100, 0)       # Bottom left
    glVertex3f(grid_length+100, grid_length+100, 0)      # Top left
    glVertex3f(grid_length+100, grid_length+100, 100) # Top right
    glVertex3f(-grid_length, grid_length+100, 100)      # Bottom right
   
    # Top Wall
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-grid_length, -grid_length, 0)           # Bottom left
    glVertex3f(grid_length+100, -grid_length, 0)        # Top left
    glVertex3f(grid_length+100, -grid_length, 100)     # Top right
    glVertex3f(-grid_length, -grid_length, 100)         # Bottom right
   
    glEnd()

def setupCamera():
    global camera_pos, camera_angle, camera_radius, camera_height, fov_y
    global mode_first_person, mode_cheat, mode_follow_view
    global fixed_look_angle, fixed_look_enabled
   
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov_y, float(window_width) / float(window_height), 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if mode_first_person:
        if mode_cheat and mode_follow_view:
            
            
            
            angle_rad = math.radians(-fixed_look_angle if fixed_look_enabled else -player_angle)
            eye_x = player_pos[0] - 10 * math.sin(angle_rad)  
            eye_y = player_pos[1] - 10 * math.cos(angle_rad)  
            eye_z = player_pos[2] + 165 # 165 units above the ground
            
        
            center_x = player_pos[0] - 150 * math.sin(angle_rad)  
            center_y = player_pos[1] - 150 * math.cos(angle_rad)
            center_z = player_pos[2] + 80  
            
            gluLookAt(eye_x, eye_y, eye_z,
                    center_x, center_y, center_z,
                    0, 0, 1)
        else:
            
            eye_x = player_pos[0]
            eye_y = player_pos[1]
            eye_z = player_pos[2] + gun_point[2] + 60
           
            angle_rad = math.radians(-player_angle)
            center_x = eye_x - math.sin(angle_rad) * 100
            center_y = eye_y - math.cos(angle_rad) * 100
            center_z = eye_z
           
            gluLookAt(eye_x, eye_y, eye_z,
                      center_x, center_y, center_z,
                      0, 0, 1)
    else:
        # Third
        angle_rad = math.radians(camera_angle)
       
        x = camera_radius * math.sin(angle_rad)
        y = camera_radius * math.cos(angle_rad)
        z = camera_height
       
        gluLookAt(x, y, z,
                 0, 0, 0,  # Look at the center of the grid (0,0,0)
                 0, 0, 1)
def cheatModeAimRotate():
    global player_pos, player_angle, gun_bullets, mode_over, cheat_last_bullet_time, cheat_wait_time
   
    if not enemy_list:
        return
   
    enemy_angles = getEnemyAngles()

    rotation_speed = player_turn_speed
    player_angle = (player_angle + rotation_speed / 5) % 360
   
    current_time = time.time()
    
    if current_time - cheat_last_bullet_time > 0.3: 
        # Check all enemies for potential shots
        for angle in enemy_angles:
            angle_diff = abs((player_angle - angle + 540) % 360 - 180)
            
           
            if angle_diff < 15:
                fireBullet()
                cheat_last_bullet_time = current_time
                break


def drawPlayer():
    global gun_point
       
    glPushMatrix()
   
    # Player Position
    glTranslatef(*player_pos)
    glRotatef(player_angle, 0, 0, 1)  # Rotate around z-axis
   
    if mode_over:
        glRotatef(-90, 1, 0, 0)
   
    # Left Leg
    glTranslatef(15, 0, 0)      # At (15, 0, 0)
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(gluNewQuadric(), 5, 10, 50, 10, 10) # quadric, base radius, top radius, height, slices, stacks
   
    # Right Leg
    glTranslatef(-30, 0, 0)     # At (-15, 0, 0)
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(gluNewQuadric(), 5, 10, 50, 10, 10) # quadric, base radius, top radius, height, slices, stacks
   
    # Body
    glTranslatef(15, 0, 50+20)# At (0, 0, 70)
    glColor3f(85/255, 108/255, 47/255)
    glutSolidCube(40)
   
    # Head
    glTranslatef(0, 0, 40)    # At (0, 0, 110)
    glColor3f(0.0, 0.0, 0.0)
    gluSphere(gluNewQuadric(), 20, 10, 10) # radius, slices, stacks
   
    # Left Arm
    glTranslatef(20, -60, -30) # At (20, -60, 80)
    glRotatef(-90, 1, 0, 0)      
    glColor3f(254/255, 223/255, 188/255)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 10, 10) # quadric, base radius, top radius, height, slices, stacks
   
    # Right Arm
    glRotatef(90, 1, 0, 0)  # Reset rotation
    glTranslatef(-40, 0, 0)    # At (-20, -60, 80)
    glRotatef(-90, 1, 0, 0)    
    glColor3f(254/255, 223/255, 188/255)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 10, 10) # quadric, base radius, top radius, height, slices, stacks
   
    # Gun
    glRotatef(90, 1, 0, 0)      # Reset rotation
    glTranslatef(20, -40, 0)    # At (0, -100, 80)
    glRotatef(-90, 1, 0, 0)    
    glColor3f(192/255, 192/255, 192/255)
    gluCylinder(gluNewQuadric(), 1, 10, 80, 10, 10) # quadric, base radius, top radius, height, slices, stacks
   
    glPopMatrix()
   
    gun_point = (85, 0, 80)

def drawEnemy(x, y, z):

    glPushMatrix()
   
    #the current position for the body
    glTranslatef(x, y, z + 35)
    
    # Draw the body apply pulse to radius
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), 35 * enemy_pulse, 10, 10)  # quadric, radius, slices, stacks

    glTranslatef(0, 0, 40)
 
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 15 * enemy_pulse, 10, 10)  # quadric, radius, slices, stacks
    
    glPopMatrix()
   
def drawBullet(x, y, z):
    glPushMatrix()
   
    glTranslatef(x, y, z) # Gun Point
    glRotatef(-90, 1, 0, 0)    
    glColor3f(1, 0, 0)
    glutSolidCube(15)
   
    glPopMatrix()


def fireBullet():
    global gun_bullets, gun_bullet_speed, player_pos, player_angle, gun_point
   
    if mode_first_person:
        x = player_pos[0]
        y = player_pos[1]
        z = player_pos[2] + gun_point[2]
        bullet = [x, y, z, player_angle]
    else:
        angle_rad = math.radians(player_angle - 90)
        offset_x = gun_point[0] * math.cos(angle_rad) - gun_point[1] * math.sin(angle_rad)
        offset_y = gun_point[0] * math.sin(angle_rad) + gun_point[1] * math.cos(angle_rad)
        x = player_pos[0] + offset_x
        y = player_pos[1] + offset_y
        z = player_pos[2] + gun_point[2]
        bullet = [x, y, z, player_angle]
       
    gun_bullets.append(bullet)
   
def moveBullets():
    global gun_bullets, gun_missed_bullets, enemy_list, gun_bullet_speed, gun_max_misses, mode_over
   
    to_remove = []
   
    for bullet in gun_bullets:
        angle_rad = math.radians(bullet[3] - 90)
       
        bullet[0] += gun_bullet_speed * math.cos(angle_rad)
        bullet[1] += gun_bullet_speed * math.sin(angle_rad)
       
        if (bullet[0] > grid_length + 100
        or bullet[0] < -grid_length
        or bullet[1] > grid_length + 100
        or bullet[1] < -grid_length):
            to_remove.append(bullet)
            gun_missed_bullets += 1
            print(f"Bullet missed: {gun_missed_bullets}")
   
    for bullet in to_remove:
        gun_bullets.remove(bullet)


    if gun_missed_bullets >= gun_max_misses:
        mode_over = True
   
       
def spawnEnemies(num_enemies=enemy_count):
    global enemy_list, enemy_count
    for i in range(num_enemies):
        x = random.uniform(-grid_length + 100, grid_length - 100)
        y = random.uniform(-grid_length + 100, grid_length - 100)
        z = 0
        while abs(x) < 200:
            x = random.uniform(-grid_length + 100, grid_length - 100)
        while abs(y) < 200:
            y = random.uniform(-grid_length + 100, grid_length - 100)
        enemy_list.append([x, y, z])
   


def moveEnemies():
    global enemy_list, enemy_speed, mode_over, player_life
   
    for enemy in enemy_list:
        dx = player_pos[0] - enemy[0]
        dy = player_pos[1] - enemy[1]
        distance = (dx**2 + dy**2) ** 0.5
       
        # Losing a Life
        if distance < 50:
            player_life -= 1
            print(f"Remaining Player Life: {player_life}")
           
            if player_life <= 0:
                mode_over = True
                enemy_list.clear()
                gun_bullets.clear()
                break
           
            enemy_list.remove(enemy)
            spawnEnemies(1)
       
        else:
            angle = math.atan2(dy, dx)
            enemy[0] += enemy_speed * math.cos(angle)
            enemy[1] += enemy_speed * math.sin(angle)

def hitEnemy(bullets, enemies):
    global player_score, gun_bullets, enemy_list
   
    for bullet in bullets:
        bullet_x = bullet[0]
        bullet_y = bullet[1]
       
        for enemy in enemies:
            enemy_x = enemy[0]
            enemy_y = enemy[1]
           
            dx = bullet_x - enemy_x
            dy = bullet_y - enemy_y
            distance = (dx**2 + dy**2) ** 0.5
           
            if distance < 60:
                player_score += 1
                bullets.remove(bullet)
                enemies.remove(enemy)
                spawnEnemies(1)
                break
           
def pulseEnemy():
    
    global enemy_pulse_time, enemy_pulse
   
    enemy_pulse_time += 0.015 
    enemy_pulse = 1.0 + 0.2 * math.sin(enemy_pulse_time) 
 
def getClosestEnemy():
    enemy_distances = []
   
    for enemy in enemy_list:
        dx = player_pos[0] - enemy[0]
        dy = player_pos[1] - enemy[1]
        distance = (dx**2 + dy**2) ** 0.5
        enemy_distances.append(distance)
   
    closest_enemy_distance = min(enemy_distances)
    closest_enemy_index = enemy_distances.index(closest_enemy_distance)
    closest_enemy = enemy_list[closest_enemy_index]
   
    return closest_enemy


def getEnemyAngles():
    enemy_angles = [] 
   
    for enemy in enemy_list:
        dx = player_pos[0] - enemy[0]
        dy = player_pos[1] - enemy[1]
       
        angle = math.degrees(math.atan2(dy, dx)) - 90
        angle = (angle + 360) % 360
       
        enemy_angles.append(angle)
    return enemy_angles


def cheatModeAimRotate():
    global player_pos, player_angle, gun_bullets, mode_over, cheat_last_bullet_time, cheat_wait_time
   
    if not enemy_list:
        return
   
    enemy_angles = getEnemyAngles()
   
    player_angle = (player_angle + player_turn_speed / 10) % 360
   
    for angle in enemy_angles:
        angle_diff = abs((player_angle - angle + 540) % 360 - 180)
        if angle_diff < 2:  # Within 5 degrees threshold
            current_time = time.time()
            if current_time - cheat_last_bullet_time > cheat_wait_time:
                fireBullet()
                cheat_last_bullet_time = current_time
            break


def cheatModeAimClosest():
    global player_pos, player_angle, gun_bullets, mode_over, cheat_last_bullet_time, cheat_wait_time
   
    if not enemy_list:
        return
   
    closest_enemy = getClosestEnemy()
   
    dx = closest_enemy[0] - player_pos[0]
    dy = closest_enemy[1] - player_pos[1]
   
    enemy_angle = math.degrees(math.atan2(dy, dx)) + 90
    enemy_angle = (enemy_angle + 360) % 360
    current_angle = player_angle % 360
   
    angle_diff = (enemy_angle - current_angle + 540) % 360 - 180
   
    if abs(angle_diff) > player_turn_speed:
        if angle_diff > 0:
            player_angle += player_turn_speed / 10
        else:
            player_angle -= player_turn_speed / 10
    else:
        player_angle = enemy_angle


        # Fire if cooldown is over
        current_time = time.time()
        if current_time - cheat_last_bullet_time > cheat_wait_time:
            fireBullet()
            cheat_last_bullet_time = current_time
       
def mouseListener(button, state, x, y):
    global mode_over, mode_first_person, player_turn_speed
   
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not mode_over:
            fireBullet()
            print("Player Bullet Fired!")
   
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if not mode_over:
            # Toggle first-person view
            mode_first_person = not mode_first_person
            if mode_first_person:
                player_turn_speed = 2.5
            else:
                player_turn_speed = 5

def drawText(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
   
    gluOrtho2D(0, window_width, 0, window_height)
   
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
   
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def showScreen():
    global mode_over, player_life, player_score, gun_missed_bullets, mode_cheat, mode_follow_view
   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
   
    setupCamera()
    drawGrid()
    drawPlayer()
   
    if not mode_over:
        for enemy in enemy_list:
            drawEnemy(*enemy)
       
        for bullet in gun_bullets:
            drawBullet(bullet[0], bullet[1], bullet[2])

        drawText(10, 770, f"Player Life Remaining: {player_life}")
        drawText(10, 740, f"Game Score: {player_score}")
        drawText(10, 710, f"Player Bullet Missed: {gun_missed_bullets}")
        
        # Display mode status
        if mode_cheat:
            # drawText(10, 680, "Cheat Mode: ON")
            pass
            if mode_first_person and mode_follow_view:
                # drawText(10, 650, "Follow View: ON")
                pass
    else:
        drawText(10, 770, f"Game is Over. Your Score is: {player_score}")
        drawText(10, 740, f'Press "R" to RESTART the Game.')    
   
    glutSwapBuffers()

def idle():
    if not mode_over:
        moveEnemies()
        pulseEnemy()
        moveBullets()
        hitEnemy(gun_bullets, enemy_list)
        
        # Apply cheat mode rotation and firing
        if mode_cheat:
            cheatModeAimRotate()
       
    glutPostRedisplay()

def keyboardListener(key, a, b):
    global player_angle, player_speed, player_turn_speed, player_pos, gun_angle, gun_bullet_speed, gun_bullets, gun_missed_bullets
    global mode_over, player_life, player_score, gun_missed_bullets, player_angle, gun_bullets, enemy_list, mode_cheat, mode_follow_view
    global fixed_look_angle, fixed_look_enabled
   
    x = player_pos[0]
    y = player_pos[1]
    z = player_pos[2]
   
    if not mode_over:
        if key == b'w':
            # Player moves forward
            x -= player_speed * math.sin(math.radians(-player_angle))
            y -= player_speed * math.cos(math.radians(player_angle))
           
            if x < -grid_length:
                x = -grid_length
            if x > grid_length + 100:
                x = grid_length + 100
            if y < -grid_length:
                y = -grid_length
            if y > grid_length + 100:
                y = grid_length + 100
       
        if key == b's':
            # Player moves backward
            x += player_speed * math.sin(math.radians(-player_angle))
            y += player_speed * math.cos(math.radians(player_angle))
           
            if x < -grid_length:
                x = -grid_length
            if x > grid_length + 100:
                x = grid_length + 100
            if y < -grid_length:
                y = -grid_length
            if y > grid_length + 100:
                y = grid_length + 100
       
        if key == b'a':
            # Player rotates left
            player_angle += player_turn_speed
       
        if key == b'd':
            # Player rotates right
            player_angle -= player_turn_speed
       
        if key == b'c':
            # Toggle cheat mode
            mode_cheat = not mode_cheat
            # print(f"Cheat mode: {'ON' if mode_cheat else 'OFF'""}")
            
        if key == b'v':
            # Toggle follow view modeonly works when cheat mode is activate
            if mode_cheat:
                mode_follow_view = not mode_follow_view
                if mode_follow_view:
                
                    fixed_look_angle = player_angle
                    fixed_look_enabled = True
                    # print(f"Camera fixed at angle: {fixed_look_angle}") //debug er jonne
                else:
                    fixed_look_enabled = False
                # print(f"Follow view mode: {'ON' if mode_follow_view else 'OFF'}") //same
            else:
                print("Follow view only works in cheat mode!") 
    if key == b'r':
        # Restart the game
        mode_over = False
        player_pos = [0, 0, 0]
        player_angle = 0
        player_life = 5
        player_score = 0
        gun_missed_bullets = 0
        gun_bullets.clear()
        enemy_list.clear()
        spawnEnemies()
   
    player_pos = [x, y, z]

   
def specialKeyListener(key, a, b):
    global camera_angle, camera_radius, camera_height
    
    # Constants camera
    MIN_HEIGHT = 200  # Minimum height tpp
    MAX_HEIGHT = 800  # Maximum height top down
    HEIGHT_INCREMENT = 5   
    RADIUS_INCREMENT = 4  
    ANGLE_INCREMENT = 2   
    
    if key == GLUT_KEY_UP:

        if camera_height < MAX_HEIGHT:
            camera_height += HEIGHT_INCREMENT
            camera_radius = max(camera_radius - RADIUS_INCREMENT, 100)
    
    if key == GLUT_KEY_DOWN:
        
        if camera_height > MIN_HEIGHT:
            camera_height -= HEIGHT_INCREMENT

            camera_radius = min(camera_radius + RADIUS_INCREMENT, 600)
    
    if key == GLUT_KEY_LEFT:

        camera_angle -= ANGLE_INCREMENT
    
    if key == GLUT_KEY_RIGHT:

        camera_angle += ANGLE_INCREMENT


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy 3D")
    # glEnable(GL_DEPTH_TEST) //use korte bolenai template but dekhte shundor lage use korle :")
    spawnEnemies()
    glutDisplayFunc(showScreen)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutMainLoop()


if __name__ == "__main__":
    main()

