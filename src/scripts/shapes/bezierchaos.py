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
from random import random

from parameters import pe

class BezierChaos(object):

    def __init__(self):
        VG.create_context((2048,2048))

    def render(self):

        smack = 1/2048.0
        glScale(smack,smack,1.0)

        VG.set(VG_MATRIX_MODE, VG_MATRIX_PATH_USER_TO_SURFACE)
        VG.load_identity()
        VG.scale(1.0/smack, 1.0/smack)

        p = VG.Path()
        p.move_to((-0.5,-0.5))
        VG.set(VG_STROKE_LINE_WIDTH, .01)

        pe.wave_a=0
        pe.square_a=0

        r = pe.mid
        theta = pe.time

        #VGU.round_rect(p, (-0.5,-0.5), (1,1), 1-pe.bass, 1-pe.bass)

        p.quad_to((-r*cos(theta), r*sin(theta)), (0.5, -0.5))
        p.quad_to((-r*cos(theta), r*sin(theta)), (0, 0.5))
        p.quad_to((-r*cos(theta), r*sin(theta)), (-0.5, -0.5))

        paint = VG.ColorPaint((pe.wave_r, pe.wave_g, pe.wave_b, 1.0))
        VG.set_paint(paint, VG_STROKE_PATH)
        
        paint = VG.ColorPaint((1-pe.wave_r, 1-pe.wave_g, 1-pe.wave_b, 1.0))
        VG.set_paint(paint, VG_FILL_PATH)
        
        p.draw(VG_FILL_PATH)
        p.draw(VG_STROKE_PATH)
