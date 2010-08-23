import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
from parameters import pe

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
            if (pe.orientation == 1):
                vertices = array([[-1/pe.aspect, 1/pe.aspect, 1/pe.aspect, -1/pe.aspect],
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


