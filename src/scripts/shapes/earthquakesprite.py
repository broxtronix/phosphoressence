import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from OpenVG import VG
from OpenVG import VGU
from OpenVG.constants import *
from random import random, seed
from math import pi, cos, sin
import math
from colorsys import hsv_to_rgb


from parameters import pe

class EarthquakeSprite(object):

    def __init__(self):
        VG.create_context((2048,2048))

        self.offsets = []
        self.displacements = []
        self.values = []
        
        self.fill()

    def fill(self):
        while len(self.offsets) > 0 and self.offsets[0]< -1.5:
            self.offsets = self.offsets[1:]
            self.displacements = self.displacements[1:]
            self.values = self.values[1:]

        here = -1.5
        if len(self.offsets) > 0:
            here = self.offsets[-1] + random()*.2*3
            
        while 1:
            self.offsets.append(here)
            self.displacements.append(random()*.3)
            self.values.append(random())
            if here > 1.5:
                break
            here += random()*.2*3

    def update(self):
        for idx in range(0,len(self.offsets)):
            self.offsets[idx] += (random()-.5)*2*.01 - .1
            self.displacements[idx] += (random()-.5)*2*.1
        self.fill()

    def render_bg(self):
        return
        self.update()
        
        smack = 1/2048.0
        glScale(smack,smack,1.0)
 
        VG.set(VG_MATRIX_MODE, VG_MATRIX_PATH_USER_TO_SURFACE)
        VG.load_identity()
        VG.scale(1.0/smack, 1.0/smack)


        idx = 0
        while 1:
            here = self.offsets[idx]
            width = self.offsets[idx+1]-here
            disp = self.displacements[idx]
            v = self.values[idx]
            idx += 1
            if here > 1.0:
               break
            
            p = VG.Path()

            p.move_to((-5,here+width/2))
            p.line_to((5,here+width/2 + disp))

            VG.set(VG_STROKE_LINE_WIDTH, width)
            paint = VG.ColorPaint((0.0, 0.0, 0.0, 1.0))
            VG.set_paint(paint, VG_STROKE_PATH)
            p.draw(VG_STROKE_PATH)

            VG.set(VG_STROKE_LINE_WIDTH, width*.85)
            paint = VG.ColorPaint((v, v, v, 1.0))
            VG.set_paint(paint, VG_STROKE_PATH)
            p.draw(VG_STROKE_PATH)

            

    def render_bg_old(self):
        smack = 1/2048.0
        glScale(smack,smack,1.0)
 
        VG.set(VG_MATRIX_MODE, VG_MATRIX_PATH_USER_TO_SURFACE)
        VG.load_identity()
        VG.scale(1.0/smack, 1.0/smack)

        here = -1
        idx = 0
        while here < 1:
            width = random()*.2*3
            p = VG.Path()

            p.move_to((-5,here+width/2))
            p.line_to((5,here+width/2 + random()*.1))
            v = random()

            VG.set(VG_STROKE_LINE_WIDTH, width)
            paint = VG.ColorPaint((0.0, 0.0, 0.0, 1.0))
            VG.set_paint(paint, VG_STROKE_PATH)
            p.draw(VG_STROKE_PATH)

            VG.set(VG_STROKE_LINE_WIDTH, width*.85)
            paint = VG.ColorPaint((v, v, v, 1.0))
            VG.set_paint(paint, VG_STROKE_PATH)
            p.draw(VG_STROKE_PATH)

            here += width
