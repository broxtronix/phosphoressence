import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from numpy import *
from random import random

from parameters import pe

class VuSpiralSprite(object):
    def __init__(self, num_sprites = 4):

        self.points = ones( (2, num_sprites) )
        self.directions = ones( (2, num_sprites) )
        self.speeds = ones( (1, num_sprites) )
        self.angle = ones( (1, num_sprites) )
        for i in range(num_sprites):
            self.points[0,i] = random() * 2.0 - 1.0
            self.points[1,i] = random() * 2.0 - 1.0
            self.directions[0,i] = round(random()) * 2.0 - 1.0
            self.directions[1,i] = round(random()) * 2.0 - 1.0
            self.speeds[0, i] = random()/100+0.001
            self.angle[0, i] = random()*3.14
    
    def render(self):
        num_sprites = self.points.shape[1]

        for i in range(num_sprites):
            self.points[0,i] += self.speeds[0,i] * self.directions[0,i]
            self.points[1,i] += self.speeds[0,i] * self.directions[1,i]
            if self.points[0,i] > pe.aspect or self.points[0,i] < -pe.aspect:
                self.directions[0,i] *= -1
            if self.points[1,i] > 1.0 or self.points[1,i] < -1.0:
                self.directions[1,i] *= -1
 
        glLoadIdentity()
        glEnable(GL_BLEND);
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glEnable(GL_LINE_SMOOTH)
        glLineWidth(pe.square_thick)

        color = array([pe.square_r, pe.square_g, pe.square_b])
        norm_color = color
        if (pe.wave_brighten):
            norm_color = color / sqrt(dot(color,color.conj()))
        glColor4f(norm_color[0], norm_color[1], norm_color[2], 1.0)

        r = 0#math.cos(pe.time)
        size = 0.5#math.pow(pe.bass,2)+math.pow(pe.mid,2)+math.pow(pe.treb,2)
        vertices = array([[ -.5,
                            sin(r) * (self.points[1,i]) ],
                          [ 0.5,
                            cos(r) * (self.points[1,i]) ]])
#array([[ cos(r) * (self.points[0,i]-size),
#                            sin(r) * (self.points[1,i]) ],
#                          [ -sin(r) * (self.points[0,i]+size),
#                            cos(r) * (self.points[1,i]) ]])


        # Draw the lines that connect the dots
        glBegin(GL_LINES)
        for i in range(num_sprites):
            glVertex2f(vertices[0,0], vertices[1,0]);
            glVertex2f(vertices[0,1], vertices[1,1]);
        glEnd()

        # Draw the dots at the vertices
        glPointSize(3.0)
        glColor4f(1-norm_color[0], 1-norm_color[1], 1-norm_color[2], 1.0)
        glBegin(GL_POINTS)
        for i in range(num_sprites):
            glVertex2f(vertices[0,0], vertices[1,0]);
            glVertex2f(vertices[0,1], vertices[1,1]);
        glEnd()

