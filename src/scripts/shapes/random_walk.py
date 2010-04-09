import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from parameters import pe

from numpy import *

class RandomWalkSprite(object):

    def reseed_decay(self):
        if (pe.q7 > 0): # a value of 1.0 seems good
            self.decay_counter = random.geometric(pe.q7)
        else:
            self.decay_counter = random.geometric(0.1)

    def randomize_direction(self):
        std_dev = pe.q8  # a value of 0.2 is pretty good
        if (std_dev <= 0): std_dev = 1
        angle = random.normal(0, std_dev);
        rotation = array([[math.cos(angle), -math.sin(angle)],
                          [math.sin(angle), math.cos(angle)]]);
        # note the right multiply here...
        new_direction = dot(self.direction, rotation)
        self.direction = new_direction
        
    def __init__(self):
        self.loc = array([0, 0])
        self.direction = array([1, 0])
        self.reseed_decay()
        
    def render(self):
        if (pe.square_a != 0.0):
            speed = 0.01
            self.loc = self.loc + self.direction * speed
            
            # Check to see if we bounce off walls
            if (self.loc[0] < -pe.aspect or self.loc[0] > pe.aspect or 
                self.loc[1] < -1 or self.loc[1] > 1):
                self.loc = array([0,0])
                
            # Change direction randomly
            if (self.decay_counter <= 0):
                self.reseed_decay()
                self.randomize_direction();
            self.decay_counter -= 1

            # Drow the shape.
            glLoadIdentity()
            glEnable(GL_BLEND);
            glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

            color = array([pe.square_r, pe.square_g, pe.square_b])
            norm_color = color
            if (pe.wave_brighten):
                norm_color = color / sqrt(dot(color,color.conj()))
            glColor4f(norm_color[0], norm_color[1], norm_color[2], math.pow(pe.treb,2)*50)

            # Draw the dots at the vertices
            glPointSize(5.0)
            glColor4f(1-norm_color[0], 1-norm_color[1], 1-norm_color[2], 1.0)
            glBegin(GL_POINTS)
            glVertex2f(self.loc[0], self.loc[1])
            glEnd()

