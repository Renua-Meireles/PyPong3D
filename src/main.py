from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import objects, colors


# x, y, z de referencia
x, y, z = 0., 0., 0.

table =   objects.Table(colors.TABLE,  (0, 0, 0), (x, y, z-7), (2.5, 1.5, 0.5))
ball =    objects.Ball(colors.BALL,    (0, 0, 0), (x, y, z-5), radius = .1, slices = 20, stacks = 20)
player1 = objects.Cube(colors.PLAYER1, (0, 0, 0), (x-table.w/2, y, z-6), (0.1, 0.4, 0.1))
player2 = objects.Cube(colors.PLAYER2, (0, 0, 0), (x+table.w/2, y, z-6), (0.1, 0.4, 0.1))

scene = objects.Scene(table, ball, player1, player2)


def clearScreen():
    glClearColor(*colors.BACKGROUND)
    
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


dx = .0005
dy = .0002

def drawScene():
    global dy, dx
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    limit_top, limit_bottom = scene.table.border_top.y, scene.table.border_bottom.y
    limit_left, limit_right = scene.table.border_left.x, scene.table.border_right.x
    if scene.ball.y >= limit_top or scene.ball.y <= limit_bottom: # GAMBIARRA!, ERA PRA SER AS COORDENADAS DAS PAREDES DA MESA, POREM A PROJEÇÃO DA MESA MUDA COORDENADA
        dy = -dy
    if scene.ball.x >= limit_right or scene.ball.x <=limit_left:
        dx = -dx

    scene.ball.x += dx
    scene.ball.y += dy

    scene.place()

    glutSwapBuffers()
    glutPostRedisplay()



glutInit()

glutInitDisplayMode(GLUT_RGB)
glutInitWindowSize(700, 700)
glutInitWindowPosition(0, 0)
glutCreateWindow("Point")
glutDisplayFunc(drawScene)
glutIdleFunc(drawScene)

clearScreen()

glutMainLoop()