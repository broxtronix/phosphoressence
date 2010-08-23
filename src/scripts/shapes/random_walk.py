import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from parameters import pe
from numpy import *


# Each Hyphae is a single strand of randomness, with a mind of its
# own.  It may split from time to two hyphae.
class Hyphae(object):

    def __init__(self, loc, level):
        self.loc = loc
        self.level = level
        self.direction = array([1, 0])
        self.children = []
        self.stroke_width = 5

        self.decay_counter = 0
        self.split_counter = 0
        self.reseed_decay()

    def reseed_decay(self):
        self.decay_counter -= 1
        self.split_counter -= 1

        if (self.decay_counter < 0):
            if (pe.q7 > 1.0): # a value of 1.0 seems good
                self.decay_counter = random.geometric(pe.q7)
            else:
                self.decay_counter = random.geometric(0.1)

        if (self.split_counter < 0):
            if (pe.q6 > 200): # a value of 200.0 seems good
                self.split_counter = random.poisson(pe.q6)
            else:
                self.split_counter = random.poisson(200.0)


    # This function creates a new child!
    def split(self):
        if (self.split_counter == 0 and self.level < 5):  # Max of 5 levels.
            self.children.append( RandomWalkSprite(self.loc, self.stroke_width*3.0/4.0, self.level+1 ) )

    def randomize_direction(self):
        std_dev = 0.2  # a value of 0.2 is pretty good
        if (std_dev <= 0): std_dev = 1
        angle = random.normal(0, std_dev);
        rotation = array([[math.cos(angle), -math.sin(angle)],
                          [math.sin(angle), math.cos(angle)]]);
        # note the right multiply here...
        new_direction = dot(self.direction, rotation)
        self.direction = new_direction
                
    def draw(self):

        # Update location
        speed = 0.005
        self.loc = self.loc + self.direction * speed
            
        # Check to see if we bounce off walls
        if (self.loc[0] < -pe.aspect or self.loc[0] > pe.aspect or 
            self.loc[1] < -1 or self.loc[1] > 1):
            self.loc = array([0,0])

        # Update random counters
        self.reseed_decay()
                
        # Change direction randomly
        if (self.decay_counter <= 0):
            self.randomize_direction();

        # Split occasionally
        self.split()
        
        # Draw the shape.
        glLoadIdentity()
        glEnable(GL_BLEND);
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        color = array([pe.square_r, pe.square_g, pe.square_b])
        norm_color = color
        if (pe.wave_brighten):
            norm_color = color / sqrt(dot(color,color.conj()))
        glColor4f(norm_color[0], norm_color[1], norm_color[2], math.pow(pe.treb,2)*50)

        # Draw the dots at the vertices
        glPointSize(self.stroke_width)
        glColor4f(1-norm_color[0], 1-norm_color[1], 1-norm_color[2], 1.0)
        glBegin(GL_POINTS)
        glVertex2f(self.loc[0], self.loc[1])
        glEnd()

        # Draw children (recursively)
        for hyphae in self.children:
            hyphae.draw()
        

class RandomWalkSprite(object):

    def __init__(self):
        self.root_node = Hyphae(array([0, 0]), 5)

    # Draw RandomWalkSprite (recursively)
    def render(self):
        self.root_node.draw()

