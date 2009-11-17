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

class VectorBrush(object):

    def __init__(self):
        VG.create_context((2048,2048))

    def render(self):
        smack = 1/2048.0
        glScale(smack,smack,1.0)

        VG.set(VG_MATRIX_MODE, VG_MATRIX_PATH_USER_TO_SURFACE)
        VG.load_identity()
        VG.scale(1.0/smack, 1.0/smack)

        # Create the path (a simple circle for now...)
        p = VG.Path()
        r = 0.1
        VGU.ellipse(p, (pe.vg_x,pe.vg_y), (r,r))

        # Set up the drawing and painting parameters
        pe.vg_stroke_r = 0.5 + 0.35 * math.sin(7/10.0*pe.time)
        pe.vg_stroke_g = 0.5 + 0.35 * math.sin(11/10.0*pe.time)
        pe.vg_stroke_g = 0.5 + 0.35 * math.sin(13/10.0*pe.time)
        pe.vg_stroke_a = 1.0;

        pe.vg_fill_r = 1.0 - pe.vg_stroke_r
        pe.vg_fill_g = 1.0 - pe.vg_stroke_g
        pe.vg_fill_g = 1.0 - pe.vg_stroke_b

        VG.set(VG_STROKE_LINE_WIDTH, pe.vg_stroke_thickness)
        paint = VG.ColorPaint((pe.vg_stroke_r, pe.vg_stroke_g, 
                               pe.vg_stroke_b, pe.vg_stroke_a))
        VG.set_paint(paint, VG_STROKE_PATH)
        
        paint = VG.ColorPaint((pe.vg_fill_r, pe.vg_fill_g, 
                               pe.vg_fill_b, pe.vg_fill_a))
        VG.set_paint(paint, VG_FILL_PATH)
        
        p.draw(VG_FILL_PATH)
        p.draw(VG_STROKE_PATH)
