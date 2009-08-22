import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from numpy import *
from random import random


from parameters import pe

class PolyBouncerSprite(object):
    def __init__(self, num_vertices = 4, speed = 0.01):

        self.speed = speed
        self.points = ones( (2, num_vertices) )
        self.directions = ones( (2, num_vertices) )
        for i in range(num_vertices):
            self.points[0,i] = random() * 2.0 - 1.0
            self.points[1,i] = random() * 2.0 - 1.0
            self.directions[0,i] = round(random()) * 2.0 - 1.0
            self.directions[1,i] = round(random()) * 2.0 - 1.0
    
    def render(self):
        num_points = self.points.shape[1]

        for i in range(num_points):
            self.points[0,i] += self.speed * self.directions[0,i]
            self.points[1,i] += self.speed * self.directions[1,i]
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
        glColor4f(norm_color[0], norm_color[1], norm_color[2], math.pow(pe.treb,2)*10)

        # Draw the lines that connect the dots
        glBegin(GL_LINES)
        for i in range(num_points-1):
            glVertex2f(self.points[0,i], self.points[1,i]);
            glVertex2f(self.points[0,i+1], self.points[1,i+1]);
        glVertex2f(self.points[0,num_points-1], self.points[1,num_points-1]);
        glVertex2f(self.points[0,0], self.points[1,0]);
        glEnd()

        # Draw the dots at the vertices
        glPointSize(5.0)
        glColor4f(1-norm_color[0], 1-norm_color[1], 1-norm_color[2], 1.0)
        glBegin(GL_POINTS)
        for i in range(num_points):
            glVertex2f(self.points[0,i], self.points[1,i]);
        glEnd()

