import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
from parameters import pe

class PeGraphics(object):
    def render():
        square_scale = 0.2;
        vertices = [(),(),(),()];
        vertices[0] = (-0.25 * square_scale, -0.25 * square_scale)
        vertices[1] = (-0.25 * square_scale, 0.25 * square_scale)
        vertices[2] = (0.25 * square_scale,  0.25 * square_scale)
        vertices[3] = (0.25 * square_scale, -0.25 * square_scale)


        # PyOpenGl Test
        glBegin(GL_LINES)
        glColor(1.0,0.0,0.0,1.0)
        glVertex( vertices[0] )
        glVertex( vertices[1] )
        glVertex( vertices[1] )
        glVertex( vertices[2] )
        glVertex( vertices[2] )
        glVertex( vertices[3] )
        glVertex( vertices[3] )
        glVertex( vertices[0] )
        glEnd()    
