from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


janala_width, janala_height = 400, 600 
nouka_x = -60 
hera_x = random.randint(-150, 150)
hera_y = 250
totalscore = 0
goti = 0.2  
thamo = False
lifeover = False
cheating = False
hera_color = [random.random(), random.random(), random.random()]


def zone_khujo(x1, y1, x2, y2):
   x_point = x2 - x1
   y_point = y2 - y1

   if abs(x_point) >= abs(y_point):
      if x_point >= 0 and y_point >= 0: 
        return 0
      elif x_point < 0 and y_point >= 0: 
        return 3
      elif x_point < 0 and y_point < 0: 
        return 4
      elif x_point >=0 and y_point < 0 :
        return 7
   else:
      if x_point >= 0 and y_point >= 0: 
        return 1
      elif x_point < 0 and y_point >= 0: 
        return 2
      elif x_point < 0 and y_point < 0: 
        return 5
      elif x_point >= 0 and y_point < 0:
        return 6

def zero_te_jabo(khetro, x, y):
   if khetro == 0: 
      return x, y
   elif khetro == 1: 
      return y, x
   elif khetro == 2: 
      return y, -x
   elif khetro == 3: 
      return -x, y
   elif khetro == 4: 
      return -x, -y
   elif khetro == 5: 
      return -y, -x
   elif khetro == 6: 
      return -y, x
   elif khetro == 7: 
      return x, -y

def zero_theke_jabo(khetro, x, y):
    if khetro == 0: 
        return x, y
    elif khetro == 1: 
        return y, x
    elif khetro == 2: 
        return -y, x
    elif khetro == 3: 
        return -x, y
    elif khetro == 4: 
        return -x, -y
    elif khetro == 5: 
        return -y, -x
    elif khetro == 6: 
        return y, -x
    elif khetro == 7: 
        return x, -y

def line_ako(x1, y1, x2, y2, color):
   
    if x1 > x2:   #line left to right jachhe
        x1, y1, x2, y2 = x2, y2, x1, y1
        
    store = zone_khujo(x1, y1, x2, y2)
    x1_c, y1_c = zero_te_jabo(store, x1, y1)  #converting to 0
    x2_c, y2_c = zero_te_jabo(store, x2, y2)

    dx = x2_c - x1_c
    dy = y2_c - y1_c
    dinit= 2*dy - dx
    deast = 2*dy
    dnortheast =  2*(dy - dx)

    store_x, store_y = x1_c, y1_c
    glColor3f(*color)
    glBegin(GL_POINTS)

    while store_x <= x2_c:
        ori_x, ori_y = zero_theke_jabo(store, store_x, store_y)  #converting back again
        glVertex2f(ori_x, ori_y)

        if dinit > 0:
            dinit += dnortheast
            store_y += 1
        else:
            dinit += deast
        store_x += 1

    glEnd()

def draw_nouka():
    
    if lifeover:
      rong = [1,0,0]  #red colour if player dead
    else:
      rong = [1,0.7,0.8] #or else pink colour
    
    line_ako(nouka_x, -270, nouka_x + 120, -270, rong)
    line_ako(nouka_x + 10, -290, nouka_x + 110, -290, rong)
    line_ako(nouka_x, -270, nouka_x + 10, -290, rong)
    line_ako(nouka_x + 120, -270, nouka_x + 110, -290, rong)

def draw_hera():
    line_ako(hera_x, hera_y + 15, hera_x + 10, hera_y, hera_color)
    line_ako(hera_x + 10, hera_y, hera_x, hera_y - 15, hera_color)
    line_ako(hera_x, hera_y - 15, hera_x - 10, hera_y, hera_color)
    line_ako(hera_x - 10, hera_y, hera_x, hera_y + 15, hera_color)

def draw_up_portion():
    blue = [0,1,1]
    line_ako(-180, 270, -150, 270, blue) #restart arrow
    line_ako(-180, 270, -165, 285, blue)
    line_ako(-180, 270, -165, 255, blue)
    
    red = [1,0,0]
    line_ako(160, 285, 190, 255, red) #exit cross
    line_ako(160, 255, 190, 285, red)
    
    yellow =  [1,0.7,0]
    if thamo: 
        line_ako(-10, 285, -10, 255, yellow) #play
        line_ako(-10, 285, 15, 270, yellow)
        line_ako(-10, 255, 15, 270, yellow)
    else: 
        line_ako(-5, 285, -5, 255, yellow) #pause
        line_ako(10, 285, 10, 255, yellow)
   

def check_boundary(target):
    if target < -200:  #left edge limit -200
        target = -200
    elif target > 80:  #right edge (nouka=120) + 80 = 200
        target = 80
    return target

def animation():
  global hera_y, hera_x, lifeover, totalscore, goti, hera_color, nouka_x
  if not thamo and not lifeover:
    hera_y -= goti    #falling effect of diamond
                
    if cheating:
        target_x = hera_x - 60   #boat kottuk move korbe diamond er shathe align er jonno
        target_x = check_boundary(target_x)
           
        if abs(nouka_x - target_x) > 8:
            if nouka_x < target_x: 
                nouka_x += 1.5   #right move
            else: 
                nouka_x -= 1.5   #left move

    if hera_y < -250:    #bottom of the screen
        if nouka_x <= hera_x <= nouka_x + 120:  #range er moddhe
            totalscore += 1

            print(f"Score: {totalscore}")

            hera_x = random.randint(-150, 150)  #reset again
            hera_y = 250
            goti += 0.01 
            hera_color = [random.random(), random.random(), random.random()]
        else:
            lifeover = True
            print(f"Game Over! Congratulations!!!! Total Score: {totalscore}")

  glutPostRedisplay()

def mouse_things(button, state, x, y):
    global thamo, lifeover, totalscore, goti, hera_y, nouka_x

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mx = x - (janala_width / 2)
        my = (janala_height / 2) - y

        if -190 < mx < -140 and 250 < my < 290:
            totalscore, goti, lifeover, thamo = 0, 0.2, False, False
            hera_y, nouka_x = 250, -60
            print("Restarting...")
        elif -30 < mx < 30 and 250 < my < 290: 
            thamo = not thamo
        elif 150 < mx < 200 and 250 < my < 290:
            print(f"Goodbye!! Total Score: {totalscore}")
            
            glutLeaveMainLoop()

def leftright_keys(key, x, y):
   global nouka_x

   if not thamo and not lifeover:

      if key == GLUT_KEY_LEFT:
        nouka_x = max(-200, nouka_x - 25)
      elif key == GLUT_KEY_RIGHT:
        nouka_x = min(80, nouka_x + 25)

def cheat_key(key, x, y):
    global cheating
    if key == b'c': 
       cheating = not cheating

       if cheating:
         cheat_mode = "ON"
       else:
         cheat_mode = "OFF"

       print(f"Cheat Mode: {cheat_mode}")

def show():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_up_portion()
    draw_hera() 
    draw_nouka()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(janala_width, janala_height)
glutCreateWindow(b"23301477||Assignment-2: Diamond Catcher")
glClearColor(0, 0, 0, 1)
glOrtho(-200, 200, -300, 300, -1, 1)
glutDisplayFunc(show)
glutMouseFunc(mouse_things) 
glutKeyboardFunc(cheat_key) 
glutSpecialFunc(leftright_keys)
glutIdleFunc(animation)
glutMainLoop() 