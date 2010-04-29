from parameters import pe
import math, time
from random import random
from numpy import *

import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *

FRAMEBUFER_SIZE = 1600
PIXEL_SCALE_FACTOR = 1.0/400.0

class Mycelium(object):

    def __init__(self):
        random.seed()
        self.hypha = []


    def spawn(self, x, y):
        self.hypha.append( Hyphae(x,y) )


    # pass the list of hypha to each hyphae
    def render(self):
        for h in self.hypha:
            h.render(self.hypha); 

class Hyphae(object):

    # Initialize a hyphae with the specified center location.
    def __init__(self, x, y):
        self.center = array([float(x), float(y)])
        self.tendrils = []
        self.next_id = 0
        self.num_generated_tendrils = 0

        for i in range(1,int(random.uniform(1,30))):
            self.add_tendril(self.center,self.center, random.uniform(1.2, 2.0))

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

        for t in self.tendrils:
            # Remove connected tendrils
            if (t.connected):
                self.tendrils.remove(t)
            else:
                t.render(hypha)

    def add_tendril(self, l, c, r):
        self.tendrils.append( Tendril(self, self.next_id, l, c, r) )
        self.next_id = self.next_id + 1
        self.num_generated_tendrils = self.num_generated_tendrils + 1


# -------------------------------------------------------------------------------
#                               PlantSmarts
# -------------------------------------------------------------------------------

# The PlantSmarts class tracks other Tendrils and Hyphae in a
# performant manner.  It keeps track of the closest of each, and
# searches for the new best match occasionally.  The more occasional
# the search, the better!
class PlantSmarts(object):

    def __init__(self, parent, center, loc):
        self.parent = parent
        self.closest_hyphae = None
        self.closest_tendril = None
        self.tcenter = center
        self.loc = loc

    def center(self):
        return self.tcenter

    # Update the nearest hyphae
    def update_closest_hyphae(self, hypha):
        # Check to see if we are the only hyphae.  If so, we return
        # None.
        if (len(hypha) == 1):
            self.closest_hyphae = None
        else:
            self.closest_hyphae = None
            closestDist = 10000;
            for h in hypha:
                d = linalg.norm(self.loc - h.center)
                if ((d < closestDist) and (h != self.parent)):
                    closestDist = d
                    self.closest_hyphae = h
    
        return self.closest_hyphae

    def update_closest_tendril(self, hypha):

        # Check to see if we are the only hyphae.  If so, we return
        # None.
        if (len(hypha) == 1):
            self.closest_tendril = None
        else:
            self.closest_tendril = None
            closestDist = 10000
            for h in hypha:
                for t in h.tendrils:
                    distl = linalg.norm(self.loc - t.loc)
                    if ((distl < closestDist) and (t != self) and
                        (t.parent != self.parent) and (t.connected == False)):
                        closestDist = distl
                        self.closest_tendril = t
        return self.closest_tendril

# -------------------------------------------------------------------------------
#                               Tendril
# -------------------------------------------------------------------------------

class Tendril(PlantSmarts):

    def __init__(self, parent, tendril_id, loc, center, r):
        PlantSmarts.__init__(self, parent, center.copy(), loc.copy())

        self.tendril_id = tendril_id
        self.vel = array([random.uniform(-0.5,0.5), random.uniform(-0.5,0.5)])
        self.acc = array([0.0, 0.0])
        self.radius = r
        self.maxspeed = 1.0
        self.connected = False
        self.separateFactor = 1

    def render(self, hypha):
        #        print "Rendering " + str(self.tendril_id) + "   " + str(self.loc) + " " + str(self.tcenter)

        # Periodically update the closest hyphae and tendril.  The
        # less often you do this, the faster the simulation runs!
        if (random.randint(1,200) == 1):
            self.update_closest_tendril(hypha)
            self.update_closest_hyphae(hypha)

        if (not self.connected):
            self.fungal(hypha)
            self.branch(hypha)
            self.update()

        # Draw the shape.
        glLoadIdentity()
        glEnable(GL_BLEND);
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glPointSize(self.radius)

        # Draw shadow
        glColor4f(0.0, 0.0, 0.0, 0.5)
        glBegin(GL_POINTS)
        glVertex2f((self.loc[0]+self.radius/2)*PIXEL_SCALE_FACTOR, (self.loc[1]-self.radius/2)*PIXEL_SCALE_FACTOR)
        glEnd()

        # Draw the dots at the vertices
        if (self.connected):
            glColor4f(1.0, 0.0, 0.0, 1.0)
        else:
            glColor4f(1.0, 1.0, 1.0, 1.0)
        glBegin(GL_POINTS)
        glVertex2f(self.loc[0]*PIXEL_SCALE_FACTOR, self.loc[1]*PIXEL_SCALE_FACTOR)
        glEnd()


    def fungal(self, hypha):
        disp = self.disperse()       # grow away from own center
        wand = self.wander()         # adds randomness
        atrc = self.attract(hypha)   # grow towards closest hyphae center, check if connected
        stic = self.stick(hypha)     # connect to other tendril tips, check if connected
#        sep = self.separate(hypha)   # ??

        # Weight these forces
        disp *= 0.1
        wand *= 0.15
        atrc *= 0.05
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
        k = linalg.norm(self.loc - self.tcenter)
        r = random.uniform(0,(100/(k+0.5)))
        if ((r <= 0.2) and (self.parent.num_generated_tendrils < 50)):
            self.parent.add_tendril( self.loc, self.tcenter, 1.0)

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

        d = array([0.0,0.0])
        
        # Check to see if we are the only hyphae.  If so, we return
        # zero acceleration (i.e. no attraction)
        if (self.closest_hyphae != None):
            d = self.closest_hyphae.center - self.loc
            dist = linalg.norm(d)

            # Check to see if we connected to another hyphae center
            if (dist < 5) and (dist > 0):
                self.connected = True

            # Normalize
            if (linalg.norm(d) != 0.0): # avoid NaN
                d /= linalg.norm(d)
                
        return d

    def stick(self, hypha):
        d = array([0.0, 0.0])
        
        # Make sure there is a closest tendril we are tracking
        if (self.closest_tendril != None):

            distl = linalg.norm(self.loc - self.closest_tendril.loc)
            if (distl < 3 and distl > 0):   # Check for connection
                self.connected = True

            if (distl < 31):
                self.separateFactor = 0

            if (distl < 50):                 # If the other tendril is close, zoom towards it.
                d = self.closest_tendril.loc - self.loc
                if (linalg.norm(d) != 0.0):  # avoid NaN
                    d /= linalg.norm(d)      # normalize

        return d

    def separate(self, hypha):
        sum = array([0.0,0.0])
        desiredseparation = 0
        for h in hypha:
            if (h == self.parent):
                desiredseparation = random.uniform(1,40) * self.separateFactor

            for t in h.tendrils:
                d = linalg.norm(self.loc - t.loc)

                # If the distance is greater than 0 and less than an
                # arbitrary amount (0 when you are yourself)
                if ((d > 0) and (d < desiredseparation)):
                    diff = self.loc - t.loc
                    if (linalg.norm(diff) != 0.0):  # avoid NaN
                        diff /= linalg.norm(diff)   # normalize

                    # Weight by distance
                    sum += diff
        return sum
