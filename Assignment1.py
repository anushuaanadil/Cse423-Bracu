#Task-1

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


janala_breadth, janala_height = 500, 500

bristi_goti = 5
bristi_horizon = 0.0  
bristi_directY = -1.0 # direction of y
bristir_fota = []

day_night = [0.0, 0.0, 0.0] 

def draw_recttri(x1, y1, x2, y2, r, g, b):
    
   glColor3f(r, g, b)
   glBegin(GL_TRIANGLES)
   glVertex2f(x1, y1); glVertex2f(x2, y1); glVertex2f(x2, y2)
   glVertex2f(x1, y1); glVertex2f(x2, y2); glVertex2f(x1, y2)
   glEnd()

def fixing_update_animate(): 
    
   global bristi_horizon, bristi_directY 
   for fota in bristir_fota :
      fota[0] += bristi_horizon * bristi_goti  #horizontal
      fota[1] += bristi_directY  * bristi_goti #vertical
        
      if fota[1] < 0 or fota[0] < -300 or fota[0] > janala_breadth+ 300:  #reseting position for out of boundaries
        fota[0] = random.uniform(-300, janala_breadth + 300)
        fota[1] = random.uniform(janala_height, janala_height + 300)
    
    
   glutPostRedisplay()  #redraw the screen with new position

def display_screen():
    
   glClearColor(day_night[0], day_night[1], day_night[2], 1.0)
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glLoadIdentity()
   screen_updates()

   #maati
   draw_recttri(0, 0, 500, 300, 0.56, 0.44, 0.20)

   #gaach
   for i in range(0, 500, 40):
        glBegin(GL_TRIANGLES)
        glColor3f(0.0, 0.9, 0.0)  
        glVertex2d(i, 225); glVertex2d(i + 20, 285); glVertex2d(i + 40, 225)
        glEnd()

   #bashabari
   draw_recttri(100, 100, 400, 250, 1.0, 1.0, 1.0)

   #chaad
   glColor3f(0.40, 0.0, 0.6)
   glBegin(GL_TRIANGLES)
   glVertex2d(250, 350); glVertex2d(50, 250); glVertex2d(450, 250)
   glEnd()

   #dorja
   draw_recttri(200, 100, 300, 200, 0.25, 0.66, 1.0)

   #janala
   draw_recttri(125, 150, 175, 200, 0.25, 0.66, 1.0)
   draw_recttri(325, 150, 375, 200, 0.25, 0.66, 1.0)

   #janalar grill
   glColor3f(0, 0, 0)
   glBegin(GL_LINES)
   glVertex2f(125, 175); glVertex2f(175, 175); glVertex2f(150, 200); glVertex2f(150, 150)
   glVertex2f(325, 175); glVertex2f(375, 175); glVertex2f(350, 200); glVertex2f(350, 150)
   glEnd()

   #dorjar handel
   glPointSize(7)
   glBegin(GL_POINTS)
   glColor3f(0, 0, 0)
   glVertex2f(290, 150)
   glEnd()

   draw_bristi()
   glutSwapBuffers()

def create_bristi():
   
  for i in range(200):
    x = random.uniform(-300, janala_breadth + 300)
    y = random.uniform(0, janala_height + 300)
       
    color = random.choice([(1.0, 1.0, 1.0), (0.0, 0.0, 0.5)])
    bristir_fota .append([x, y, color])

def draw_bristi():
   glLineWidth(2)
   for fota in bristir_fota :
      x, y, color = fota
      glColor3f(color[0], color[1], color[2])
      glBegin(GL_LINES)
      
      glVertex2f(x, y)
      glVertex2f(x + bristi_horizon * 20, y + bristi_directY  * 20)
      glEnd()

def keyboard_keys(key, x, y):
   global day_night
   if key == b'w':
       day_night = [min(1.0, p + 0.1) for p in day_night]
   elif key == b's':
       day_night = [max(0.0, p - 0.1) for p in day_night]
   glutPostRedisplay()

def keyboard_updown(key, x, y):
   global bristi_horizon
   if key == GLUT_KEY_LEFT:
      bristi_horizon -= 0.1   # Move left
   elif key == GLUT_KEY_RIGHT:
      bristi_horizon += 0.1   #Move right
   glutPostRedisplay()

def screen_updates():
   glViewport(0, 0, 500, 500)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0.0, 500.0, 0.0, 500.0, 0.0, 1.0)
   glMatrixMode(GL_MODELVIEW)

def main():
   glutInit()
   
   glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
   glutInitWindowSize(janala_breadth, janala_height)
   glutInitWindowPosition(100, 100)
   glutCreateWindow(b"Task-1")
   
   create_bristi()
   
   glutDisplayFunc(display_screen)
   glutIdleFunc(fixing_update_animate)  
   glutKeyboardFunc(keyboard_keys)
   glutSpecialFunc(keyboard_updown)

   glutMainLoop()

if __name__ == "__main__":
    main()


#Task-2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


janala_breadth, janala_height = 500, 500
storage = []     #[x er value , y er value , dx horizontal speed, dy vertical speed, r, g, b]
goti = 1.0
atkano = False    #blackout active or not
shesh_click = 0 


def coordinate_bodol(x, y):
   a = x - (janala_breadth / 2)
   b = (janala_height / 2) - y
   return a*2, b*2

def keyboard_keys(key, x, y):   
  global atkano
  if key == b' ':  
    atkano = not atkano
  glutPostRedisplay()

def keyboard_updown(key, x, y):
  global goti
  if atkano: 
    return   #not process as blackout e ache
    
  if key == GLUT_KEY_UP:
    goti += 0.2 
  elif key == GLUT_KEY_DOWN:
    goti = max(0.1, goti - 0.2)

  glutPostRedisplay()

def mouse_moves(button, state, x, y):
  global storage, shesh_click
  if atkano: 
    return  #not process as blackout e ache
   
  if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
    shesh_click = time.time()    #latest click
    print("Blackout started!yayy!!! It works !!")
   
  elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
    prothom, shesh = coordinate_bodol(x, y)
    dx = random.choice([-1.5, 1.5])  #horizontal speed
    dy = random.choice([-1.5, 1.5])  #verical speed
    r, g, b = random.random(), random.random(), random.random()
    storage.append([prothom, shesh, dx, dy, r, g, b])


def fixing_update_animate():
  if not atkano:
    for p in storage:
            
      p[0] += p[2] * goti   #update x
      p[1] += p[3] * goti   #update y
                       
      if p[0] >= 500 or p[0] <= -500:
        p[2] *= -1       #reverse horizontal direction i.e x
      if p[1] >= 500 or p[1] <= -500:
        p[3] *= -1       #reverse vertical direction i.e y
                   
  glutPostRedisplay()    #display update


def display_screen():
    
   ondhokar = (time.time() - shesh_click) < 1.0

   glClearColor(0.0, 0.0, 0.0, 1.0) #bg is black , 1 means full opaque
   glClear(GL_COLOR_BUFFER_BIT)  #Clear color 
   glLoadIdentity()
    
    
   glViewport(0, 0, janala_breadth, janala_height)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(-500, 500, -500, 500, -1, 1) 
   glMatrixMode(GL_MODELVIEW)

    
   if not ondhokar:
     glPointSize(10)
     for p in storage:
        glBegin(GL_POINTS)
        glColor3f(p[4], p[5], p[6]) # Setting color 
        glVertex2f(p[0], p[1])      # Setting position
        glEnd()

   glutSwapBuffers()


def main():
  glutInit()
  glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
  glutInitWindowSize(janala_breadth, janala_height)
  glutInitWindowPosition(100, 100)
  glutCreateWindow(b"Task 2")
    
  glutDisplayFunc(display_screen)
  glutIdleFunc(fixing_update_animate)
  glutKeyboardFunc(keyboard_keys)
  glutSpecialFunc(keyboard_updown)
  glutMouseFunc(mouse_moves)
    
  glutMainLoop()

if __name__ == "__main__":
  main()