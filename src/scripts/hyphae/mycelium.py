from parameters import pe
import math, time
from random import random
from numpy import *

import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenVG import VG
from OpenVG import VGU
from OpenVG.constants import *

FRAMEBUFER_SIZE = 1600
PIXEL_SCALE_FACTOR = 1.0/300.0

class Mycelium(object):

    def __init__(self):
        VG.create_context((FRAMEBUFER_SIZE,FRAMEBUFER_SIZE))
        self.hypha = []


    def spawn(self, x, y):
        self.hypha.append( Hyphae(x,y) )


    # pass the list of hypha to each hyphae
    def render(self):
        # Set up rendering context.  Messy, but necessary for now.
        smack = 1.0/FRAMEBUFER_SIZE
        glLoadIdentity()
        glScale(smack,smack,1.0)
        VG.set(VG_MATRIX_MODE, VG_MATRIX_PATH_USER_TO_SURFACE)
        VG.load_identity()
        VG.scale(1.0/smack, 1.0/smack)

        for h in self.hypha:
            h.render(self.hypha); 

class Hyphae(object):

    # Initialize a hyphae with the specified center location.
    def __init__(self, x, y):
        self.center = array([float(x), float(y)])
        self.tendrils = []
        self.next_id = 0

        for i in range(1,random.uniform(1,30)):
            self.add_tendril(self.center,self.center,2,1.0)

    # We pass in the complete list of hypha so that hyphae children
    # can access those center loctaions.
    def render(self, hypha):
        
        # Draw the shape.
        glLoadIdentity()
        glEnable(GL_BLEND);
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glColor4f(0.0, 0.8, 0.2, 1.0)

        # Draw the dots at the vertices
        glPointSize(10.0)
        glBegin(GL_POINTS)
        glVertex2f(self.center[0]*PIXEL_SCALE_FACTOR, self.center[1]*PIXEL_SCALE_FACTOR)
        glEnd()

        # # Create the path (a simple circle for now...)
        # p = VG.Path()
        # VGU.ellipse(p, (self.center[0]*PIXEL_SCALE_FACTOR,
        #                 self.center[1]*PIXEL_SCALE_FACTOR),
        #             (10.0*PIXEL_SCALE_FACTOR, 10.0*PIXEL_SCALE_FACTOR))

        # # Set up the drawing and painting parameters
        # VG.set(VG_STROKE_LINE_WIDTH, pe.vg_stroke_thickness)
        # paint = VG.ColorPaint((pe.vg_stroke_r, pe.vg_stroke_g, 
        #                        pe.vg_stroke_b, pe.vg_stroke_a))
        # VG.set_paint(paint, VG_STROKE_PATH)
        
        # paint = VG.ColorPaint((1.0, 0.0, 0.0, 1.0))
        # VG.set_paint(paint, VG_FILL_PATH)
        
        # p.draw(VG_FILL_PATH)
        # #        p.draw(VG_STROKE_PATH)

        for t in self.tendrils:
            t.render(hypha)

    def add_tendril(self, l, c, r, s):
        self.tendrils.append( Tendril(self, self.next_id, l, c, r, s ) )
        self.next_id = self.next_id + 1

class Tendril(object):

    def __init__(self, parent, tendril_id, loc, center, r, s):
        self.parent = parent
        self.tendril_id = tendril_id
        self.loc = loc.copy()
        self.tcenter = center.copy()
        self.vel = array([random.uniform(-0.5,0.5), random.uniform(-0.5,0.5)])
        self.acc = array([0.0, 0.0])
        self.radius = r
        self.speed = s
        self.maxspeed = 1.0
        self.connected = False
        self.seperateFactor = 2

    def render(self, hypha):
#        print "Rendering " + str(self.tendril_id) + "   " + str(self.loc) + " " + str(self.tcenter)
        if (not self.connected):
            self.fungal(hypha)
            self.branch(hypha)
            self.update()

        # Draw the shape.
        glLoadIdentity()
        glEnable(GL_BLEND);
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glColor4f(1.0, 1.0, 1.0, 1.0)

        # Draw the dots at the vertices
        glPointSize(self.radius)
        glBegin(GL_POINTS)
        glVertex2f(self.loc[0]*PIXEL_SCALE_FACTOR, self.loc[1]*PIXEL_SCALE_FACTOR)
        glEnd()

    def fungal(self, hypha):
        disp = self.disperse()       # grow away from own center
        wand = self.wander()         # adds randomness
        atrc = self.attract(hypha)   # grow towards closest hyphae center, check if connected
        stic = self.stick(hypha)     # connect to other tendril tips, check if connected
#        sep = separateFactor(hypha)  # ??

        # Weight these forces
        disp *= 0.2
        wand *= 0.2
        atrc *= 0.1
        stic *= 1.0
#        sep *= 0.5

        # Add force vectors to acceleration
        self.acc += disp
        self.acc += wand
        self.acc += atrc
        self.acc += stic
#        self.acc += sep   # weight differently at dif proximity?

    def update(self):
        self.vel += self.acc

        # Limit to maxspeed
        if (linalg.norm(self.vel) > self.maxspeed):
            self.vel /= linalg.norm(self.vel) * self.maxspeed

        self.loc += self.vel

        # Reset acceleration to 0 on each cycle
        self.acc = array([0.0,0.0])

    def branch(self, hypha):
        for h in hypha:
            if (linalg.norm(h.center - self.tcenter) == 0):
                r = random.uniform(0,20)
                if ((r <= 0.2) and (len(h.tendrils) < 5)):
                    h.add_tendril( self.loc, self.tcenter, 1.0, 0.9 )

    def disperse(self):
        d = array([0.0,0.0])
        cdist = linalg.norm(self.loc - self.tcenter)
        if (cdist < 40):
            d = self.loc - self.tcenter
            if (linalg.norm(d) != 0.0):  # avoid NaN
                d /= linalg.norm(d)      # normalize
        return d

    def wander(self):
        w = array([random.uniform(-0.1,0.1), random.uniform(-0.1,0.1)])
        if (linalg.norm(w) != 0.0):  # avoid NaN
            w /= linalg.norm(w) # normalize
        return w

    def attract(self, hypha):
        closest = array([0.0,0.0])
        closestDist = 10000;
        for h in hypha:
            d = linalg.norm(self.loc - h.center)

            if ((d < closestDist) and (linalg.norm(h.center - self.tcenter) != 0)):
                closestDist = d
                closest = h.center
                if (d < 1) and (d > 0):
                    connected = True

        d = closest - self.loc
        if (linalg.norm(d) != 0.0):  # avoid NaN
            d /= linalg.norm(d)  # normalize
        return d

    def stick(self, hypha):
        closest = array([0.0,0.0])
        d = array([0.0, 0.0])
        closestDist = 10000;
        for h in hypha:
            for t in h.tendrils:
                distl = linalg.norm(self.loc - t.loc)
                if ((distl < closestDist) and (linalg.norm(self.tcenter - t.tcenter) != 0)):
                    closestDist = distl
                    closest = t.loc
                    if (distl < 1 and distl > 0):
                        connected = True
#                    if (distl < 31):
#                        separateFactor = 0
        if (linalg.norm(self.loc - closest) < 50):
            d = closest - self.loc
            if (linalg.norm(d) != 0.0):  # avoid NaN
                d /= linalg.norm(d)  # normalize
        return d

    def separate(self, hypha):
        sum = array([0.0,0.0])
        desiredseparation = 0
        for h in hypha:
            if ( linalg.norm(h.center - self.tcenter) == 0):
                desiredseparation = random.uniform(1,40)

            for t in h.tendrils:
                d = linalg.norm(self.loc - t.loc)

                # If the distance is greater than 0 and less than an
                # arbitrary amount (0 when you are yourself)
                if ((d > 0) and (d < desiredseparation)):
                    diff = self.loc - otherTendril.loc
                    diff /= linalg.norm(diff)

                    # Weight by distance
                    sum += diff
        return sum
