from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

player_x, player_y, player_rot = 0.0, 0.0, 0.0
life, tscore, missed = 5, 0, 0
khela_cholche = True
fpview = False

#cam view
cam_height = 800.0
cam_angle = -math.pi / 2  
cam_radius = 850.0

# for Cheat Mode 
is_cheat = False
automatic = False
cheat_rot = 0.0 

wallcolour = []
for i in range(4):
    wallcolour.append((random.random(), random.random(), random.random()))

grid = 600
bullets = []   # [x, y, rotation]
enemies = []   # [x, y]

def create_enemy():       #create enemy
    side = random.randint(0, 3)

    if side == 0: 
        return [random.uniform(-550, 550), 550]   #top
    if side == 1: 
        return [random.uniform(-550, 550), -550]  #bottom
    if side == 2: 
        return [550, random.uniform(-550, 550)]   #right
    if side == 3: 
        return [-550, random.uniform(-550, 550)]  #left

for i in range(5):   #each time 5 enemies lagbe
    enemies.append(create_enemy())

def draw_text(x, y, text):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text: 
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix() 
    glMatrixMode(GL_MODELVIEW)

def shape_ako():
    # Checkerboard Floor
    onebox = 100
    for i in range(-grid, grid, onebox):
        for j in range(-grid, grid, onebox):
            if (i + j) // onebox % 2 == 0:
                glColor3f(0.8, 0.7, 1.0) #purple color for even
            else:
                glColor3f(1.0, 1.0, 1.0) #white color for odd

            glBegin(GL_QUADS)
            glVertex3f(i, j, 0) 
            glVertex3f(i + onebox, j, 0)
            glVertex3f(i + onebox, j + onebox, 0)
            glVertex3f(i, j + onebox, 0)
            glEnd()

    # Wall
    wall_h = 60
    dour = [[(-600,-600), (600,-600)], [(600,-600), (600,600)], [(600,600), (-600,600)], [(-600,600), (-600,-600)]]
    for i in range(4):
        r, g, b = wallcolour[i]
        glColor3f(r, g, b)
        
        glBegin(GL_QUADS)
        glVertex3f(dour[i][0][0], dour[i][0][1], 0)
        glVertex3f(dour[i][1][0], dour[i][1][1], 0)
        glVertex3f(dour[i][1][0], dour[i][1][1], wall_h)
        glVertex3f(dour[i][0][0], dour[i][0][1], wall_h)
        glEnd()

    #Player
    glPushMatrix()
    glTranslatef(player_x, player_y, 0)
    glRotatef(player_rot, 0, 0, 1)
    if not khela_cholche: 
        glRotatef(90, 1, 0, 0)  #tip over for death

    q = gluNewQuadric()

    # Leg
    glColor3f(0, 0, 1) #blue
    for side in [-10, 10]:
        glPushMatrix()
        glTranslatef(side, 0, 0)  #-10 hole left , 10 hole right ; 2 legs on 2 sides
        gluCylinder(q, 3, 6, 35, 16, 16) #(quadric, baseRadius, topRadius, height, slices, stacks)
        glPopMatrix()

    # body
    glColor3f(0.8, 0.7, 0.5)  #tan colour
    glPushMatrix() 
    glTranslatef(0, 0, 45)    # 45 ghor away from camera view
    glScalef(1.8, 0.8, 1.5)  #to make the cube look rectangle
    glutSolidCube(20) 
    glPopMatrix()

    # hands
    for pos in [-15, 15]:
        glPushMatrix()
        glTranslatef(pos, 8, 50)  #-15 left , 15 right , 8 up , 50 away from camera view
        gluCylinder(q, 3, 3, 20, 10, 10) 
        glPopMatrix()

    # Head
    glColor3f(0, 0, 0)  #black
    glPushMatrix()
    glTranslatef(0, 0, 75)
    gluSphere(q, 12, 16, 16) #(radius,slices , stack)
    glPopMatrix()

    # Gun 
    glColor3f(0.4, 0.4, 0.4)  #dark gray
    glPushMatrix()
    glTranslatef(0, 10, 50) # 10 upward , 50 far away from camera view
    if is_cheat: 
        glRotatef(cheat_rot, 0, 0, 1) # rotate along z axis
    gluCylinder(q, 4, 3, 40, 10, 10)
    glPopMatrix()

    glPopMatrix()

    #enemies
    for e in enemies:
        glPushMatrix()
        glTranslatef(e[0], e[1], 15)
        store = 1.0 + 0.2 * math.sin(glutGet(GLUT_ELAPSED_TIME)/200.0)  #200 slows down the oscilation , sin wave oscillate between -1 , 1 which multiplied by .2 , then i is added to make it positive
        glScalef(store, store, store)  #scale in all direction ; will become big and small
        glColor3f(1, 0, 0)
        gluSphere(q, 20, 12, 12) #red body
        glTranslatef(0, 0, 20)
        glColor3f(0, 0, 0)
        gluSphere(q, 10, 10, 10) #black head
        glPopMatrix()

    # Bullet
    glColor3f(0, 0, 0)
    for b in bullets:
        glPushMatrix()
        glTranslatef(b[0], b[1], 50) 
        glutSolidCube(6)
        glPopMatrix()


def keyboard_function(key, x, y):
    global player_x, player_y, player_rot, khela_cholche, tscore, life, missed, is_cheat, automatic
    if key == b'r': 
        player_x, player_y, tscore, life, missed, khela_cholche = 0, 0, 0, 5, 0, True
        is_cheat = False
        print("--- Game Restarted ---")
    if not khela_cholche: 
        return
    
    if key == b'c': 
        is_cheat = not is_cheat
    if key == b'v' and is_cheat: 
        automatic= not automatic

    kona = math.radians(player_rot + 90)  # player should start along y axis instead of x axis
    step = 25 
    if key == b'w': 
        player_x += step * math.cos(kona); 
        player_y += step * math.sin(kona)  #forward,for rad sin cos is used
    if key == b's': 
        player_x -= step * math.cos(kona); 
        player_y -= step * math.sin(kona)  #backward
    if key == b'a': 
        player_rot += 10   #left
    if key == b'd': 
        player_rot -= 10   #right

def mouse_function(button, state, x, y):
    global fpview, bullets
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and khela_cholche:
        bullets.append([player_x, player_y, player_rot])
        print("Player Bullet Fired!")
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fpview = not fpview

def special_function(key, x, y):
    global cam_height, cam_angle
    
    if key == GLUT_KEY_UP:
        cam_height += 20
    if key == GLUT_KEY_DOWN:
        cam_height -= 20
        if cam_height < 100: 
            cam_height = 100 

    if key == GLUT_KEY_LEFT:
        cam_angle -= 0.1
    if key == GLUT_KEY_RIGHT:
        cam_angle += 0.1

def main_logic():
    global life, tscore, missed, khela_cholche, cheat_rot
    if not khela_cholche: 
        return

    if is_cheat:
        cheat_rot = (cheat_rot + 5) % 360   #increases 5 times and 360 keeps it betn 0-360
        for e in enemies:
            aos = math.degrees(math.atan2(e[1]-player_y, e[0]-player_x)) - 90 #finding the angle betn 2 points
            if abs((player_rot + cheat_rot)%360 - aos %360) < 15:  #15 degree r moddhe hole shoot korbo , and ensuring the angle is betn 0-360
                if random.random() < 0.1:  #without this it will cross 10 shoots
                    bullets.append([player_x, player_y, player_rot + cheat_rot])
                    print("Player Bullet Fired!")

    for b in bullets[:]:
        length = math.radians(b[2] + 90)  #b[2] indicates angle 
        b[0] += 25 * math.cos(length); b[1] += 25 * math.sin(length)  #x and y coordinates
        if abs(b[0]) > 600 or abs(b[1]) > 600:
            bullets.remove(b); missed += 1  #if missed then removed
            print(f"Bullet missed: {missed}")
        else:
            for e in enemies:
                if math.sqrt((b[0]-e[0])**2 + (b[1]-e[1])**2) < 35: #straight dist betn bullet and enemy
                    tscore += 1; print(f"Enemy Hit! Score: {tscore}")
                    enemies.remove(e); enemies.append(create_enemy()); bullets.remove(b); break

    for e in enemies:
        dist = math.sqrt((player_x-e[0])**2 + (player_y-e[1])**2) #dist betn player and enemy
        e[0] += (player_x-e[0])/dist * 0.2  #moving enemies towards players
        e[1] += (player_y-e[1])/dist * 0.2
        if dist < 45:   #enemies collied with player
            life -= 1; print(f"Player hit! Remaining Player Life: {life}")
            enemies.remove(e); enemies.append(create_enemy())

    if life <= 0 or missed >= 10: 
        khela_cholche = False
        print("GAME OVER")

def camerasetup():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65, 1.25, 1, 2500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if fpview:
        radstore = math.radians(player_rot + 90)  #for keeping in shoulder
               
        shoulder_x = 15 * math.cos(radstore - math.pi/2)   #for shoulder view
        shoulder_y = 15 * math.sin(radstore - math.pi/2)
               
        eye_x = player_x + shoulder_x - 20 * math.cos(radstore)   #behind and to the side
        eye_y = player_y + shoulder_y - 20 * math.sin(radstore)
        eye_z = 85 
               
        target_x = eye_x + 100 * math.cos(radstore)
        target_y = eye_y + 100 * math.sin(radstore)
        target_z = 75 
        
        gluLookAt(eye_x, eye_y, eye_z, target_x, target_y, target_z, 0, 0, 1)  #first person view
    else: 
        eye_x = cam_radius * math.cos(cam_angle)
        eye_y = cam_radius * math.sin(cam_angle)
        
        gluLookAt(eye_x, eye_y, cam_height, 0, 0, 0, 0, 0, 1)

def screen_dekhao():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camerasetup()
    main_logic()
    shape_ako()

    if khela_cholche:
        draw_text(10, 760, f"Player Life Remaining: {life}")
        draw_text(10, 735, f"Game Score: {tscore}")
        draw_text(10, 710, f"Player Bullet Missed: {missed}")
    else:
        draw_text(10, 760, f"Game is Over. Your Score is {tscore}.")
        draw_text(10, 735, "Press 'R' to RESTART the Game.")
    
    glutSwapBuffers()

def idle():
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutCreateWindow(b"Assignment3")
    
    glutDisplayFunc(screen_dekhao)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard_function) 
    glutMouseFunc(mouse_function)
    glutSpecialFunc(special_function)
    glutMainLoop()

if __name__ == "__main__":
    main()

