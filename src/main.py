from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import objects, colors

# x, y, z de referencia
x, y, z = 0., 0., 0.


# scene = objects.Scene((0, 90, 0), (x, y, z)) # Angulo bom pra vizualização geral
scene = objects.Scene((0, 0, 0), (x, y, z)) # Angulo bom pra editar cordenadas


def clearScreen():
    glClearColor(*colors.BACKGROUND)
    
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_LIGHTING) # Habilita luz
    glEnable(GL_LIGHT0) # Habilita luz 0
    glEnable(GL_NORMALIZE) # Normaliza vetor normal
    glEnable(GL_COLOR_MATERIAL) # Habilita material
    glEnable(GL_BLEND) # Habilitando transparência da cor RGBA
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # Define a função de transparência


    glMatrixMode(GL_PROJECTION)

    gluPerspective(45., 1., 0.1, 500.)

    glMatrixMode(GL_MODELVIEW)


dx = .0015
dy = .0010
players_speed = .001
p1hitted = True # dx positive -> ball is going to p2 -> p2 will defend

def renderScene():
    global dy, dx, p1hitted
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLightfv(GL_LIGHT0, GL_POSITION, (scene.wall_back.w, scene.wall_back.w, scene.wall_back.h, .7))
    # glLightfv(GL_LIGHT0, GL_POSITION, (scene.ball.x, scene.ball.y, scene.wall_back.h, .2))

    gluLookAt( # Mudando a posição da camera de acordo com a posição da bola
        # 3, 6, 8, # Camera afasta 8 unid. para frente e 5 unid. para cima da origem # Angulo bom pra vizualização geral
        0, 0, 10, # Angulo bom pra editar cordenadas
        scene.ball.x, scene.ball.y, scene.ball.z,  # Camera olha para a bola
        0, 1, 0   # Camera olha para cima
    )

    # BALL MOVEMENT
    if scene.ballHittedTopBorder() or scene.ballHittedBottomBorder():
        dy = -dy
    if scene.ballHittedLeftBorder() or scene.ballHittedRightBorder():
        dx = -dx

    # BALL MOVEMENT ON PLAYER HIT
    if scene.playerTwoHitBall() or scene.playerOneHitBall():
        dx = -dx
        # Invert: One atacked and the other will defend
        p1hitted = not p1hitted
    
    # PLAYER MOVEMENT
    if p1hitted:
        step = players_speed if scene.isPlayer2BellowBall(players_speed) else -players_speed
        if scene.isPlayer2BellowTopBorder(players_speed) and step > 0:
            scene.player2.y += step
        if scene.isPlayer2AboveBottomBorder(players_speed) and step < 0:
            scene.player2.y += step
    else:
        step = players_speed if scene.isPlayer1BellowBall(players_speed) else -players_speed
        if scene.isPlayer1BellowTopBorder(players_speed) and step > 0:
            scene.player1.y += step
        if scene.isPlayer1AboveBottomBorder(players_speed) and step < 0:
            scene.player1.y += step

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