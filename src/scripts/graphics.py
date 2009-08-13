import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *

from parameters import pe
from shapes.bezier import *

class PeGraphics(object):

    def __init__(self):
        self.sprites = []
        self.HORIZ_MESH_SIZE = 48
        self.VERT_MESH_SIZE = 48

        print "initialize using aspect " + str(pe.aspect)
        aspect = 1.0
        framebuffer_radius = math.sqrt(1.0 + math.pow(aspect,2));
        screen_w = 2.0*framebuffer_radius;  
        screen_h = 2.0*framebuffer_radius;

        self._feedback_texcoords = zeros([self.HORIZ_MESH_SIZE+1, self.VERT_MESH_SIZE+1, 2])
        self._feedback_screencoords = zeros([self.HORIZ_MESH_SIZE+1, self.VERT_MESH_SIZE+1, 2])
        self._warped_screencoords = zeros([self.HORIZ_MESH_SIZE+1, self.VERT_MESH_SIZE+1, 2])

        for  i in range(self.HORIZ_MESH_SIZE + 1):
            for j in range(self.VERT_MESH_SIZE + 1):
                self._feedback_texcoords[i,j,0] = i * 1.0 / self.HORIZ_MESH_SIZE;
                self._feedback_texcoords[i,j,1] = j * 1.0 / self.VERT_MESH_SIZE;
                self._feedback_screencoords[i,j,0] = -framebuffer_radius + (i * screen_w) / self.HORIZ_MESH_SIZE;
                self._feedback_screencoords[i,j,1] = -framebuffer_radius + (j * screen_h) / self.VERT_MESH_SIZE;
        
    def register(self, sprite):
        self.sprites.append(sprite)
    
    def render(self):
        for sprite in self.sprites:
            sprite.render()

    def render_feedback(self):
        aspect = 1.0
        framebuffer_radius = math.sqrt(1.0 + math.pow(aspect,2));

        # Compute warp-related parameters
        warp_time = pe.time * pe.warp_speed
        warp_scale_inv = 1.0 / pe.warp_scale
        f = [ 11.68 + 4.0 * math.cos(warp_time*1.413 + 10),
              8.77 + 3.0 * math.cos(warp_time*1.113 + 7),
              10.54 + 3.0 * math.cos(warp_time*1.233 + 3),
              11.49 + 4.0 * math.cos(warp_time*0.933 + 5) ]

        # Iterate through the coordinates in the mesh, applying a
        # coordinate by coordinate mesh distortion.  THIS IS WHERE THE
        # MAGIC HAPPENS, FOLKS
        for i in range(self.HORIZ_MESH_SIZE + 1):
            for j in range(self.VERT_MESH_SIZE + 1):
                u = self._feedback_screencoords[i,j,0]
                v = self._feedback_screencoords[i,j,1]

                # ---
                # Do per-vertex here
                # ---

                zoom_coefficient = math.pow(pe.zoom,
                                            math.pow(pe.zoomexp, 
                                                     math.sqrt(u * u + v * v) * 2.0 * 
                                                     framebuffer_radius -
                                                     framebuffer_radius))

                u = u * zoom_coefficient
                v = v * zoom_coefficient

                # Apply the scaling effect
                u = (u - pe.cx)/pe.sx + pe.cx;
                v = (v - pe.cy)/pe.sy + pe.cy;

                # Apply the Milkdrop warp effect (most of these constants were
                # taken from the milkdrop source code)
                u += pe.warp * 0.0035 * math.sin(warp_time * 0.333 + warp_scale_inv*(self._feedback_screencoords[i,j,0] * f[0] - self._feedback_screencoords[i,j,1] * f[3]))
                v += pe.warp * 0.0035 * math.cos(warp_time * 0.375 - warp_scale_inv*(self._feedback_screencoords[i,j,0] * f[2] + self._feedback_screencoords[i,j,1] * f[1]))
                u += pe.warp * 0.0035 * math.cos(warp_time * 0.753 - warp_scale_inv*(self._feedback_screencoords[i,j,0] * f[1] - self._feedback_screencoords[i,j,1] * f[2]))
                v += pe.warp * 0.0035 * math.sin(warp_time * 0.825 + warp_scale_inv*(self._feedback_screencoords[i,j,0] * f[0] + self._feedback_screencoords[i,j,1] * f[3]))

                # Apply the rotation effect
                u2 = u - pe.cx;
                v2 = v - pe.cy;
                cos_rot = math.cos(pe.rot);
                sin_rot = math.sin(pe.rot);
                u = u2*cos_rot - v2*sin_rot + pe.cx;
                v = u2*sin_rot + v2*cos_rot + pe.cy;

                # Apply the translation effect
                u -= pe.dx;
                v -= pe.dy;

                self._warped_screencoords[i,j,0] = u;
                self._warped_screencoords[i,j,1] = v;

        # Now we draw the warped feedback image
        glDisable(GL_BLEND)
        glColor4f(1.0,1.0,1.0,1.0);
        glBegin(GL_QUADS);
        for i in range(self.HORIZ_MESH_SIZE):
            for j in range(self.VERT_MESH_SIZE):
                glTexCoord2f( self._feedback_texcoords[i,j,0], self._feedback_texcoords[i,j,1] )
                glVertex2f(   self._warped_screencoords[i,j,0] , self._warped_screencoords[i,j,1] )
                glTexCoord2f( self._feedback_texcoords[i,j+1,0], self._feedback_texcoords[i,j+1,1] )
                glVertex2f(   self._warped_screencoords[i,j+1,0], self._warped_screencoords[i,j+1,1] )
                glTexCoord2f( self._feedback_texcoords[i+1,j+1,0],  self._feedback_texcoords[i+1,j+1,1] )
                glVertex2f(   self._warped_screencoords[i+1,j+1,0], self._warped_screencoords[i+1,j+1,1] )
                glTexCoord2f(  self._feedback_texcoords[i+1,j,0],  self._feedback_texcoords[i+1,j,1] )
                glVertex2f(   self._warped_screencoords[i+1,j,0], self._warped_screencoords[i+1,j,1] )
        glEnd();


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
#                            [-0.25, 0.25, 0.25, -0.25]]) * pe.mid
                            [-0.25, 0.25, 0.25, -0.25]]) * pe.square_scale
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
#pe_graphics.register(BezierSprite())
