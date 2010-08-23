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
#                               BezierSprite
# ---------------------------------------------------------------------------

class BezierSprite(OpenVgSprite):

    def render(self):
        self.setup_canvas()
        
        speed = 0.3
        start_point = [ math.cos(2*math.pi*0.42*speed*pe.time),  
                        math.cos(2*math.pi*0.17*speed*pe.time),  
                        0]
        control_point1 = [ math.cos(2*math.pi*.38*speed*pe.time),  
                           math.cos(2*math.pi*.29*speed*pe.time),  
                           0]        
        control_point2 = [ math.cos(2*math.pi*.12*speed*pe.time),  
                           math.cos(2*math.pi*.40*speed*pe.time),  
                           0]
        control_point3 = [ math.cos(2*math.pi*.24*speed*pe.time),  
                           math.cos(2*math.pi*.13*speed*pe.time),
                           0]

        p = VG.Path()
        p.move_to(start_point)
        p.cubic_to(control_point1, control_point2, control_point3)

        # Drow the final shape
        p.draw(VG_FILL_PATH);                             # Draw the Fill
        p.draw(VG_STROKE_PATH);                           # Draw the stroke

