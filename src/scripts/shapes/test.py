#import OpenGL
#OpenGL.ERROR_CHECKING = False
#from OpenGL.GL import *
#from OpenGL.GLU import *
#import math

from OpenVG import VG
from OpenVG import VGU
from OpenVG.constants import *
from random import random
import math

from parameters import pe

class TestSprite(object):

    def __init__(self):
        VG.create_context((2048,2048))

        self.x = 0
        self.y = -.99
        self.vr = 10
        self.vt = math.pi/2
        self.at = 0
        

    
    def render(self):

        VG.set(VG_STROKE_LINE_WIDTH, 4.0)
                
        fill_paint = VG.ColorPaint((0.0, 1.0, 1.0, 1.0))
        stroke_paint = VG.ColorPaint((  0.65 + 0.350*( 0.60*math.sin(0.742*pe.time) + 
                                                       0.40*math.sin(1.021*pe.time) ),
                                        0.65 + 0.350*( 0.60*math.sin(0.703*pe.time) + 
                                                       0.40*math.sin(0.969*pe.time) ),
                                        0.65 + 0.350*( 0.60*math.sin(1.090*pe.time) + 
                                                       0.40*math.sin(0.963*pe.time) ),
                                        1.0))
        VG.set_paint(fill_paint, VG_FILL_PATH)
        VG.set_paint(stroke_paint, VG_STROKE_PATH)

        p = VG.Path(capabilities=VG_PATH_CAPABILITY_APPEND_TO)

        vx=self.vr*math.cos(self.vt)
        vy=self.vr*math.sin(self.vt)

        p.move_to((self.x,self.y))
        self.x+=vx
        self.y+=vy
        p.line_to((self.x,self.y))

        VG.set(VG_MATRIX_MODE, VG_MATRIX_PATH_USER_TO_SURFACE)
        VG.load_identity()
        VG.scale(0.001, 0.001)
        p.draw(VG_STROKE_PATH);

        if random()<.01:
            self.at = 0

        if self.x<-1000 or self.x>1000 or self.y<-1000 or self.y>1000:
            self.x=0
            self.y=0

        self.vt += (random()-.5)*.1
        self.vt += self.at
        self.at += (random()-.5)*.1

