
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import colors

class Obj3d(object):
    def __init__(self, color, rotation, position):
        self.color = color
        self.angleX, self.angleY, self.angleZ = rotation
        self.x, self.y, self.z = position

    def render(self):
        glPushMatrix() # Permitir que as transformações ocorram apenas neste objeto
        glColor3f(*self.color)
        glTranslatef(0,0,0) # Vai para o centro do eixo
        glRotatef(self.angleX, 0, 1, 0) # Rotaciona em torno do eixo X
        glRotatef(self.angleY, -1, 0, 0) # Rotaciona em torno do eixo Y
        glRotatef(self.angleZ, 0, 0, 1) # Rotaciona em torno do eixo Z
        glTranslatef(self.x, self.y, self.z)  # A partir do centro, desloca-se para o destino
        self.draw()
        glPopMatrix()
    
    def draw(self):
        raise NotImplementedError("Subclasses must override draw()")


class Ball(Obj3d):
    def __init__(self, color, rotation, position, radius, slices, stacks):
        super().__init__(color, rotation, position)
        self.radius = radius
        self.slices = slices
        self.stacks = stacks
    
    def draw(self):
        glLightfv(GL_LIGHT0, GL_POSITION, (self.x, self.y, self.z, 1))
        glutSolidSphere(self.radius, self.slices, self.stacks)

        
class Cube(Obj3d):
    def __init__(self, color, rotation, position, dimension):
        super().__init__(color, rotation, position)
        self.w, self.h, self.d = dimension
    
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

        # ARRUMAR ESSAS POSIÇÕES
        border_w, border_h, border_d = 0.2, 0.2, 0.2
        dx_border, dy_border, dz_border = border_w/2+w, border_h/2+h, border_d/2+d
        self.border_top =    Cube(colors.TABLE_BORDER, rotation, (x, y+dy_border, z+dz_border), (w, border_h, border_d))
        self.border_left =   Cube(colors.TABLE_BORDER, rotation, (x-dx_border, y, z+dz_border), (border_w, h, border_d))
        self.border_right =  Cube(colors.TABLE_BORDER, rotation, (x+dx_border, y, z+dz_border), (border_w, h, border_d))
        self.border_bottom = Cube(colors.TABLE_BORDER, rotation, (x, y-dy_border, z+dz_border), (w, border_h, border_d))

        leg_w, leg_h, leg_d = 0.3, 0.3, 2
        dx_leg, dy_leg, dz_leg = w+leg_w/2, h+leg_h/2, d+leg_d/2
        leg_top_left =     Cube(colors.TABLE_LEG, rotation, (x-dx_leg, y+dy_leg, z-dz_leg), (leg_w, leg_h, leg_d))
        leg_top_right =    Cube(colors.TABLE_LEG, rotation, (x+dx_leg, y+dy_leg, z-dz_leg), (leg_w, leg_h, leg_d))
        leg_bottom_left =  Cube(colors.TABLE_LEG, rotation, (x-dx_leg, y-dy_leg, z-dz_leg), (leg_w, leg_h, leg_d))
        leg_bottom_right = Cube(colors.TABLE_LEG, rotation, (x+dx_leg, y-dy_leg, z-dz_leg), (leg_w, leg_h, leg_d))

        self.legs = [leg_bottom_left, leg_bottom_right, leg_top_left, leg_top_right]
        self.borders = [self.border_top, self.border_bottom, self.border_right, self.border_left]

        self.objects = self.legs + self.borders + [self.table]
    
    def render(self):
        for obj in self.objects:
            obj.render()


class Scene(Obj3d):
    def __init__(self, rotation, table:Table, ball:Ball, player1:Cube, player2:Cube):
        super().__init__([0]*3, rotation, [0]*3)

        self.table = table
        self.ball = ball
        self.player1 = player1
        self.player2 = player2

        self.objects = [self.table, self.ball, self.player1, self.player2]
    
    def draw(self):
        # self.angleX += 0.01
        # self.angleY += 0.01
        # self.angleZ += 0.01
        for obj in self.objects:
            obj.render()