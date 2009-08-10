import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *

from parameters import pe


class PeGraphics(object):

    def __init__(self):
        self.sprites = []
        
    def register(self, sprite):
        self.sprites.append(sprite)
    
    def render(self):
        for sprite in self.sprites:
            sprite.render()

class SquareSprite(object):
    def render(self):

        if (pe.square_a != 0.0):

            glLoadIdentity()
            glEnable(GL_BLEND);
            glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glEnable(GL_LINE_SMOOTH)

            # Compute rotation
            theta = pe.time * pe.square_frequency * 2.0 * math.pi;
            rot = array([[cos(theta), sin(theta)],
                         [-sin(theta), cos(theta)]])

            # Create & rotate the square
            square = array([[-0.25, -0.25, 0.25, 0.25],
                            [-0.25, 0.25, 0.25, -0.25]]) * pe.mid
                            #[-0.25, 0.25, 0.25, -0.25]]) * pe.square_scale
            vertices = dot(rot, square)
        
            # Set up drawing parameters
            glLineWidth(pe.square_thick)
            glPointSize(pe.square_thick/2.0)

            color = array([pe.square_r, pe.square_g, pe.square_b])
            norm_color = color
            if (pe.wave_brighten):
                norm_color = color / sqrt(dot(color,color.conj()))
            glColor4(norm_color[0], norm_color[1], norm_color[2], pe.square_a)

            if pe.wave_move:
                glTranslate(( 0.60*math.sin(2.121*pe.time*0.1) +
                              0.40*math.sin(1.621*pe.time*0.1) ),
                            ( 0.60*math.sin(1.742*pe.time*0.1) +
                              0.40*math.sin(2.322*pe.time*0.1) ),
                            0.0)
            else:
                glTranslate(pe.wave_x * 2.0 - 1.0,
                            pe.wave_y * 2.0 - 1.0,
                            0.0)


            # Draw the square
            glBegin(GL_LINES)
            glVertex( vertices[:,0] )
            glVertex( vertices[:,1] )
            glVertex( vertices[:,1] )
            glVertex( vertices[:,2] )
            glVertex( vertices[:,2] )
            glVertex( vertices[:,3] )
            glVertex( vertices[:,3] )
            glVertex( vertices[:,0] )
            glEnd()    

            glBegin(GL_POINTS)
            glVertex( vertices[:,0] )
            glVertex( vertices[:,1] )
            glVertex( vertices[:,2] )
            glVertex( vertices[:,3] )
            glEnd();

class BorderSprite(object):
    def render(self):

        if (pe.ib_a):
            glLoadIdentity()
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_BLEND);
            glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

            glLineWidth(pe.ib_size)
            glPointSize(pe.ib_size/2.0)

            vertices = array([[-pe.aspect, pe.aspect, pe.aspect, -pe.aspect],
                              [1.0, 1.0, -1.0, -1.0]])

            glColor4f(pe.ib_r, pe.ib_g, pe.ib_b, pe.ib_a)

            # Draw the border
            glBegin(GL_LINES)
            glVertex( vertices[:,0] )
            glVertex( vertices[:,1] )
            glVertex( vertices[:,1] )
            glVertex( vertices[:,2] )
            glVertex( vertices[:,2] )
            glVertex( vertices[:,3] )
            glVertex( vertices[:,3] )
            glVertex( vertices[:,0] )
            glEnd()

            glBegin(GL_POINTS)
            glVertex( vertices[:,0] )
            glVertex( vertices[:,1] )
            glVertex( vertices[:,2] )
            glVertex( vertices[:,3] )
            glEnd();

            glDisable( GL_BLEND );

# Instantiate the graphics object
pe_graphics = PeGraphics()
pe_graphics.register(SquareSprite())
pe_graphics.register(BorderSprite())
