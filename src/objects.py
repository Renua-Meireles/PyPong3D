import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import colors

class Obj3d(object):
    def __init__(self, color, rotation, position):
        self.color = color
        self.angleX, self.angleY, self.angleZ = rotation
        self.x, self.y, self.z = position
        self.transformation_matrix = np.eye(4,4)  # Salva a matriz de transformação para encontrar as cordenadas absolutas
        self.abs_x, self.abs_y, self.abs_z, _w = np.matmul(self.transformation_matrix, np.array([*position]+[1]))

    def render(self):
        glPushMatrix() # Permitir que as transformações ocorram apenas neste objeto
        glColor4f(*self.color)
        glTranslatef(0,0,0) # Vai para o centro do eixo
        glRotatef(self.angleX, 0, 1, 0) # Rotaciona em torno do eixo X
        glRotatef(self.angleY, -1, 0, 0) # Rotaciona em torno do eixo Y
        glRotatef(self.angleZ, 0, 0, 1) # Rotaciona em torno do eixo Z
        glTranslatef(self.x, self.y, self.z)  # A partir do centro, desloca-se para o destino
        self.set_light_configs() # Ajuste de luz antes de desenhar o objeto
        self.draw()
        glGetFloatv(GL_MODELVIEW_MATRIX, self.transformation_matrix) # Salva a matriz de transformação para encontrar as cordenadas absolutas
        self.abs_x, self.abs_y, self.abs_z, _w = np.matmul(self.transformation_matrix, np.array([self.x, self.y, self.z, 1]))
        glPopMatrix()
    
    def set_light_configs(self):
        pass

    def draw(self):
        raise NotImplementedError("Subclasses must override draw()")


class Ball(Obj3d):
    def __init__(self, color, rotation, position, radius, slices, stacks):
        super().__init__(color, rotation, position)
        self.radius = radius
        self.slices = slices
        self.stacks = stacks
    
    def draw(self):
        glutSolidSphere(self.radius, self.slices, self.stacks)
    
    def set_light_configs(self):
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0.8, 0.8, 0.8, 1))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        glMaterialfv(GL_FRONT, GL_SHININESS, 80)
        glLightfv(GL_LIGHT0, GL_POSITION, (self.abs_x, self.abs_y, self.abs_z, 1))

        
class Cube(Obj3d):
    def __init__(self, color, rotation, position, dimension):
        super().__init__(color, rotation, position)
        self.w, self.h, self.d = dimension # Largura, Altura Profundidade
    
    def set_light_configs(self):
        glMaterialfv(GL_FRONT, GL_SPECULAR, colors.LIGHT_SPECULAR)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        glMaterialfv(GL_FRONT, GL_SHININESS, 50)

    def draw(self):
        w, h, d = self.w, self.h, self.d
        glBegin(GL_QUADS)
        glVertex3f( w, h, d)
        glVertex3f(-w, h, d)
        glVertex3f(-w, -h, d)
        glVertex3f( w, -h, d)

        glVertex3f( w, h, -d)
        glVertex3f(-w, h, -d)
        glVertex3f(-w, -h, -d)
        glVertex3f( w, -h, -d)

        glVertex3f( w, h, d)
        glVertex3f( w, h, -d)
        glVertex3f( w, -h, -d)
        glVertex3f( w, -h, d)

        glVertex3f(-w, h, d)
        glVertex3f(-w, h, -d)
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, -h, d)

        glVertex3f( w, h, d)
        glVertex3f( w, h, -d)
        glVertex3f(-w, h, -d)
        glVertex3f(-w, h, d)

        glVertex3f( w, -h, d)
        glVertex3f( w, -h, -d)
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, -h, d)
        glEnd()


class Table(Cube):
    def __init__(self, color, rotation, position, dimension):
        super().__init__(color, rotation, position, dimension)
        self.table = Cube(color, rotation, position, dimension)

        x, y, z = position
        w, h, d = dimension

        border_w, border_h, border_d = 0.2, 0.2, 0.2
        dx_border, dy_border, dz_border = border_w/2+w, border_h/2+h, border_d/2+d
        self.border_top =    Cube(colors.TABLE_BORDER, rotation, (x, y+dy_border, z+dz_border), (w, border_h, border_d))
        self.border_left =   Cube(colors.TABLE_BORDER, rotation, (x-dx_border, y, z+dz_border), (border_w, h, border_d))
        self.border_right =  Cube(colors.TABLE_BORDER, rotation, (x+dx_border, y, z+dz_border), (border_w, h, border_d))
        self.border_bottom = Cube(colors.TABLE_BORDER, rotation, (x, y-dy_border, z+dz_border), (w, border_h, border_d))

        leg_w, leg_h, leg_d = 0.3, 0.3, 2
        dx_leg, dy_leg, dz_leg = w+leg_w/2, h+leg_h/2, d+leg_d/2
        self.leg_top_left =     Cube(colors.TABLE_LEG, rotation, (x-dx_leg, y+dy_leg, z-dz_leg), (leg_w, leg_h, leg_d))
        self.leg_top_right =    Cube(colors.TABLE_LEG, rotation, (x+dx_leg, y+dy_leg, z-dz_leg), (leg_w, leg_h, leg_d))
        self.leg_bottom_left =  Cube(colors.TABLE_LEG, rotation, (x-dx_leg, y-dy_leg, z-dz_leg), (leg_w, leg_h, leg_d))
        self.leg_bottom_right = Cube(colors.TABLE_LEG, rotation, (x+dx_leg, y-dy_leg, z-dz_leg), (leg_w, leg_h, leg_d))

        self.legs = [self.leg_bottom_left, self.leg_bottom_right, self.leg_top_left, self.leg_top_right]
        self.borders = [self.border_top, self.border_bottom, self.border_right, self.border_left]

        self.objects = self.legs + self.borders + [self.table]
    
    def render(self):
        for obj in self.objects:
            obj.render()


class Scene(Obj3d):
    def __init__(self, rotation, position, table:Table, ball:Ball):
        super().__init__([0]*4, rotation, position)
        x, y, z = position

        table.limit_top = table.border_top.abs_y - table.border_top.h - ball.radius
        table.limit_bottom = table.border_bottom.abs_y + table.border_bottom.h + ball.radius
        table.limit_left = table.border_left.abs_x + table.border_left.w + ball.radius
        table.limit_right = table.border_right.abs_x - table.border_right.w - ball.radius
        table.limit_leg = table.leg_bottom_left.z - table.leg_bottom_left.d

        self.table = table
        self.ball = ball
        self.player1 = Cube(colors.PLAYER1, (0, 0, 0), (table.limit_left,  y, z+.6), (0.1, 0.4, 0.1))
        self.player2 = Cube(colors.PLAYER2, (0, 0, 0), (table.limit_right, y, z+.6), (0.1, 0.4, 0.1))

        self.ground = Cube(colors.GROUND,   (0, 0, 0), (x, y, z-abs(table.limit_leg)-0.1), (25, 25, 0.1))

        self.objects = [self.table, self.ball, self.player1, self.player2, self.ground]

    def draw(self):
        self.angleX += 0.01
        # self.angleY += 0.01
        # self.angleZ += 0.01
        for obj in self.objects:
            obj.render()
    
    def ballHittedTopBorder(self) -> bool:
        return self.ball.abs_y >= self.table.limit_top
    def ballHittedBottomBorder(self) -> bool:
        return self.ball.abs_y <= self.table.limit_bottom
    def ballHittedLeftBorder(self) -> bool:
        return self.ball.abs_x <= self.table.limit_left
    def ballHittedRightBorder(self) -> bool:
        return self.ball.abs_x >= self.table.limit_right
    def playerTwoHitBall(self)->bool:
        return self.ball.abs_x >= self.table.limit_right - 0.4
    def playerOneHitBall(self)->bool:
        return self.ball.abs_x <= self.table.limit_left + 0.4