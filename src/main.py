from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import objects, colors

# x, y, z de referencia
x, y, z = 0., 0., 0.

table =   objects.Table(colors.TABLE,  (0, 0, 0), (x,           y, z), (2.5, 1.5, 0.5))
ball =    objects.Ball(colors.BALL,    (0, 0, 0), (x,           y, z+1), radius = .1, slices = 20, stacks = 20)
player1 = objects.Cube(colors.PLAYER1, (0, 0, 0), (x-table.w/2, y, z+1), (0.1, 0.4, 0.1))
player2 = objects.Cube(colors.PLAYER2, (0, 0, 0), (x+table.w/2, y, z+1), (0.1, 0.4, 0.1))

# scene = objects.Scene((0, 90, 0), table, ball, player1, player2) # Angulo bom pra vizualização geral
scene = objects.Scene((0, 0, 0), table, ball, player1, player2) # Angulo bom pra editar cordenadas


def clearScreen():
    glClearColor(*colors.BACKGROUND)
    
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)

    glMatrixMode(GL_PROJECTION)

    gluPerspective(45., 1., 0.1, 500.)
    # gluLookAt( # Posição inicial fixada
    #     # 0, 5, 8, # Camera afasta 8 unid. para frente e 5 unid. para cima da origem # Angulo bom pra vizualização geral
    #     0, 0, 8, # Angulo bom pra editar cordenadas
    #     0, 0, 0,  # Camera olha para a origem
    #     0, 1, 0   # Camera olha para cima
    # )

    glMatrixMode(GL_MODELVIEW)


dx = .0005
dy = .0002

def renderScene():
    global dy, dx
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    gluLookAt( # Mudando a posição da camera de acordo com a posição da bola
        # 0, 5, 8, # Camera afasta 8 unid. para frente e 5 unid. para cima da origem # Angulo bom pra vizualização geral
        0, 0, 8, # Angulo bom pra editar cordenadas
        scene.ball.x, scene.ball.y, scene.ball.z,  # Camera olha para a origem
        0, 1, 0   # Camera olha para cima
    )

    if scene.ballHittedTopBorder() or scene.ballHittedBottomBorder():
        dy = -dy
    if scene.ballHittedLeftBorder() or scene.ballHittedRightBorder():
        dx = -dx

    scene.ball.x += dx
    scene.ball.y += dy

    scene.render()

    glutSwapBuffers()
    glutPostRedisplay()



glutInit()

glutInitDisplayMode(GLUT_RGB)
glutInitWindowSize(700, 700)
glutInitWindowPosition(0, 0)
glutCreateWindow("Point")
glutDisplayFunc(renderScene)
glutIdleFunc(renderScene)

clearScreen()

glutMainLoop()