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
        glMaterialfv(GL_FRONT, GL_SPECULAR, colors.LIGHT_SPECULAR)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, colors.LIGHT_DIFFUSE)
        glMaterialfv(GL_FRONT, GL_SHININESS, 50)
        # glLightfv(GL_LIGHT0, GL_POSITION, (self.x*0.01, self.y*0.01, self.z+2, .2))

        
class Cube(Obj3d):
    def __init__(self, color, rotation, position, dimension):
        super().__init__(color, rotation, position)
        self.w, self.h, self.d = dimension # Largura, Altura Profundidade

    def draw(self):
        w, h, d = self.w, self.h, self.d
        glScalef(2*w, 2*h, 2*d)
        glutSolidCube(1)

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

        self.limit_top = self.border_top.abs_y - self.border_top.h
        self.limit_bottom = self.border_bottom.abs_y + self.border_bottom.h
        self.limit_right = self.border_right.abs_x - self.border_right.w
        self.limit_left = self.border_left.abs_x + self.border_left.w
        self.limit_depth = z - dz_leg - leg_d
    
    def render(self):
        for obj in self.objects:
            obj.render()

class Scene(Obj3d):
    def __init__(self, rotation, position):
        super().__init__([0]*4, rotation, position)
        x, y, z = position
        
        r = 0.2
        self.table =   Table(colors.TABLE,  (0, 0, 0), (x,y, z), (2.5, 1.5, 0.5))
        self.ball =    Ball(colors.BALL,    (0, 0, 0), (x,y, z+self.table.d+r), radius = r, slices = 20, stacks = 20)

        w_p, d_p = 0.1, 0.1
        self.player1 = Cube(colors.PLAYER1, (0, 0, 0), (self.table.limit_left+w_p,  y, z+self.table.d+d_p), (w_p, 0.4, d_p))
        self.player2 = Cube(colors.PLAYER2, (0, 0, 0), (self.table.limit_right-w_p, y, z+self.table.d+d_p), (w_p, 0.4, d_p))

        w_g, d_g = 15, 0.1
        self.ground =     Cube(colors.GROUND, (0, 0, 0), (x, y, z-abs(self.table.limit_depth)-d_g), (w_g, w_g, d_g))
        d_w = w_g/2
        self.wall_back =  Cube(colors.WALL,   (0, 0, 0), (    x, y-w_g, z-abs(self.table.limit_depth)+d_w), (w_g, d_g, d_w))
        self.wall_front = Cube(colors.WALL,   (0, 0, 0), (    x, y+w_g, z-abs(self.table.limit_depth)+d_w), (w_g, d_g, d_w))
        self.wall_left =  Cube(colors.WALL,   (0, 0, 0), (x-w_g,     y, z-abs(self.table.limit_depth)+d_w), (d_g, w_g, d_w))
        self.wall_right = Cube(colors.WALL,   (0, 0, 0), (x+w_g,     y, z-abs(self.table.limit_depth)+d_w), (d_g, w_g, d_w))


        self.objects = [self.table, self.ball, self.player1, self.player2, self.ground, self.wall_back, self.wall_front, self.wall_left, self.wall_right]

        

    def draw(self):
        # self.angleX += 0.01
        for obj in self.objects:
            obj.render()
    
    def ballHittedTopBorder(self) -> bool:
        return self.ball.abs_y + self.ball.radius >= self.table.limit_top
    def ballHittedBottomBorder(self) -> bool:
        return self.ball.abs_y - self.ball.radius <= self.table.limit_bottom
    def ballHittedLeftBorder(self) -> bool:
        return self.ball.abs_x - self.ball.radius <= self.table.limit_left
    def ballHittedRightBorder(self) -> bool:
        return self.ball.abs_x + self.ball.radius >= self.table.limit_right

    def playerTwoHitBall(self)->bool:
        return self.ball.abs_x + self.ball.radius >= self.player2.abs_x - self.player2.w
    def playerOneHitBall(self)->bool:
        return self.ball.abs_x - self.ball.radius <= self.player1.abs_x + self.player1.w

    def isPlayer1BellowTopBorder(self, speed:float) -> bool:
        return self.player1.abs_y + self.player1.h + speed < self.table.limit_top
    def isPlayer1AboveBottomBorder(self, speed:float) -> bool:
        return self.table.limit_bottom < self.player1.abs_y - self.player1.h - speed
    def isPlayer2BellowTopBorder(self, speed:float) -> bool:
        return self.player2.abs_y + self.player2.h + speed < self.table.limit_top
    def isPlayer2AboveBottomBorder(self, speed:float) -> bool:
        return self.table.limit_bottom < self.player2.abs_y - self.player2.h - speed
    
    def isPlayer1BellowBall(self, speed:float) -> bool:
        return self.player1.abs_y + speed  < self.ball.abs_y - self.ball.radius
    def isPlayer2BellowBall(self, speed:float) -> bool:
        return self.player2.abs_y + speed  < self.ball.abs_y - self.ball.radius