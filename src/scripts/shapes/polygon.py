# Phosphoressence
from color import ColorGenerator
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
#                               PolygonSprite
# ---------------------------------------------------------------------------
        
class PolygonSprite(OpenVgSprite):

    def render(self):
        self.setup_canvas()

        # Drow a polygon with n sides
        p = VG.Path()
        num_sides = 3
        scale_factor = 0.5 * pe.vg_scale
        sub_angle = 2*math.pi/num_sides
        p.move_to((scale_factor,0.0))
        for i in range(1, num_sides):
            p.line_to((scale_factor*math.cos(i * sub_angle),
                       scale_factor*math.sin(i * sub_angle)))
        p.close()

        # Drow the final shape
        p.draw(VG_FILL_PATH);                             # Draw the Fill
        p.draw(VG_STROKE_PATH);                           # Draw the stroke

