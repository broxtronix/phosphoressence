# Phosphoressence
from parameters import pe
from shapes.vg_sprite import OpenVgSprite

# OpenVG
from OpenVG import VG
from OpenVG import VGU
from OpenVG.constants import *

# Python standard library (and numpy)
from random import random, seed
import math
from numpy import array

# ---------------------------------------------------------------------------
#                               AimlessBitSprite
# ---------------------------------------------------------------------------

class AimlessBitSprite(OpenVgSprite):

    def __init__(self):
        self.last_x = 0.0
        self.last_y = 0.0
        self.x = 0.0
        self.y = 0.0
        self.vr = 0.01
        self.vt = math.pi/4
        self.at = 0
    
    def render(self):
        self.setup_canvas()
        
        p = VG.Path(capabilities=VG_PATH_CAPABILITY_APPEND_TO)
        vx=self.vr*math.cos(self.vt)
        vy=self.vr*math.sin(self.vt)

        # Update position
        self.x+=vx
        self.y+=vy
        p.move_to((self.last_x,self.last_y))
        p.line_to((self.x,self.y))
        p.draw(VG_FILL_PATH);                             # Draw the Fill
        p.draw(VG_STROKE_PATH);

        # Save current position
        self.last_x = self.x
        self.last_y = self.y

        if random()<.01:
            self.at = 0

        if self.x<-(pe.aspect) or self.x>pe.aspect or self.y<-1.0 or self.y>1.0:
            self.x=0
            self.y=0
            
        self.vt += (random()-.5)*.1
        self.vt += self.at
        self.at += (random()-.5)*.1
