from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import objects, colors

# x, y, z de referencia
x, y, z = 0., 0., 0.

table =   objects.Table(colors.TABLE,  (0, 0, 0), (x,y, z), (2.5, 1.5, 0.5))
ball =    objects.Ball(colors.BALL,    (0, 0, 0), (x,y, z+table.d+.2), radius = .2, slices = 20, stacks = 20)

scene = objects.Scene((0, 90, 0), (x, y, z), table, ball) # Angulo bom pra vizualização geral
# scene = objects.Scene((0, 0, 0), (x, y, z), table, ball) # Angulo bom pra editar cordenadas


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
    glEnable(GL_BLEND) # Habilitando transparência da cor RGBA
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);


    glMatrixMode(GL_PROJECTION)

    gluPerspective(45., 1., 0.1, 500.)

    glMatrixMode(GL_MODELVIEW)


dx = .0008
dy = .0004

def renderScene():
    global dy, dx
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    gluLookAt( # Mudando a posição da camera de acordo com a posição da bola
        0, 5, 8, # Camera afasta 8 unid. para frente e 5 unid. para cima da origem # Angulo bom pra vizualização geral
        # 0, 0, 8, # Angulo bom pra editar cordenadas
        scene.ball.x, scene.ball.y, scene.ball.z,  # Camera olha para a origem
        0, 1, 0   # Camera olha para cima
    )

    if scene.ballHittedTopBorder() or scene.ballHittedBottomBorder():
        dy = -dy
    if scene.ballHittedLeftBorder() or scene.ballHittedRightBorder():
        dx = -dx
    if scene.playerTwoHitBall() or scene.playerOneHitBall():
        dx = -dx
    # Jogadores recebem a mesma coordenada da bola em y
    scene.player1.y = scene.ball.abs_y
    scene.player2.y = scene.ball.abs_y

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