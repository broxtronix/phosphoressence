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

WIDTH, HEIGHT = 2048, 2048
NUM_SEGMENTS = 6
DUTY_CYCLE = .9
OUTER_RADIUS = .9/2
INNER_RADIUS = .2/2
LINE_WIDTH = .04


class WheelSprite(object):

    def __init__(self):
        VG.create_context((2048,2048))

        self.x = 0
        self.y = -.99
        self.vr = 10
        self.vt = math.pi/2
        self.at = 0

    def wheel(self, num_segments, duty_cycle, outer_radius, inner_radius, line_width,
              color_bias, saturation, value):
        VG.set(VG_STROKE_LINE_WIDTH, .05)
        for i in range(0, num_segments):
            inner = 2*pi/num_segments*(i + .5)
            inner_x = inner_radius*cos(inner)
            inner_y = inner_radius*sin(inner)

            p = VG.Path()

            r_start = 360.0/num_segments*i
            r_dist = 360.0/num_segments*duty_cycle
            p.move_to((inner_x, inner_y))
            VGU.arc(p, (0,0), (outer_radius*2, outer_radius*2),
                    r_start, r_dist,
                    0xF100)
            p.line_to((inner_x, inner_y))
            # XXX doesn't join to arc start quite correctly
            p.line_to((outer_radius*cos(r_start/360.0*2*pi),
                       outer_radius*sin(r_start/360.0*2*pi)))
            
            (r,g,b) = hsv_to_rgb(float(i)/num_segments + color_bias*2*pi,
                                 saturation, value)
            paint = VG.ColorPaint((0,0,0, 1.0))
            VG.set_paint(paint, VG_STROKE_PATH)
            paint = VG.ColorPaint((r, g, b, 1.0))
            VG.set_paint(paint, VG_FILL_PATH)
            p.draw(VG_FILL_PATH)
            p.draw(VG_STROKE_PATH)

    def render_back(self):
        smack = 1/2048.0
        glScale(smack,smack,1.0)

#        VG.set(VG_STROKE_JOIN_STYLE, VG_JOIN_ROUND)

        VG.set(VG_MATRIX_MODE, VG_MATRIX_PATH_USER_TO_SURFACE)
        VG.load_identity()
        VG.scale(1.0/smack, 1.0/smack)

        p = VG.Path()
        p.move_to((0,0))
        VG.set(VG_STROKE_LINE_WIDTH, .01)



#       VGU.rect(p, (0,0), (pe.q1,pe.q2))
#       VGU.rect(p, (0,0), (x,y))
#       VGU.arc(p, (0,0), (pe.q1,pe.q2),
#               0, 2*pi,
#               0xF100)
#        VGU.arc(p, (0,0), (.5,.5), 0, 90, 0xF100)
#        r = pe.q1
#        p.move_to((0,r))
#        p.arc_to((r,0), r, r, 0, False, False)

#        paint = VG.ColorPaint((0.0, 1.0, 1.0, 1.0))
#        VG.set_paint(paint, VG_STROKE_PATH)

#        p.draw(VG_STROKE_PATH);


#        self.wheel(NUM_SEGMENTS, DUTY_CYCLE, OUTER_RADIUS, INNER_RADIUS, LINE_WIDTH,
#                   0, 1, 1)


        RADIUS = .2 * (sin(pe.time)+1.0)/2.0*3.0
        COUNT = 10
        SIZE = .2
        BIAS = pe.time/COUNT * 2*pi
        for i in range(0, COUNT):
            saved = VG.get_matrix()
            angle = 2*pi*(float(i)/COUNT) + BIAS
            VG.translate(RADIUS*cos(angle),
                         RADIUS*sin(angle))
            VG.scale(SIZE,SIZE)
            VG.rotate(pe.time*2*pi*10.0+float(i)/COUNT*2*pi*2.0)
            self.wheel(5, DUTY_CYCLE, OUTER_RADIUS, INNER_RADIUS, LINE_WIDTH,
                       float(COUNT), 1, 1)
            VG.load_matrix(saved)

        return

        GRID_X = 5
        GRID_Y = 5
        idx = 0
        seed(int(pe.time))
        step = pe.time-int(pe.time)
        phase = sin(step*pi)
        for j in range(0,GRID_Y):
            for i in range(0,GRID_X):
                saved = VG.get_matrix()
                VG.translate((i + .5) / GRID_X * 2 - 1, (j + .5) / GRID_Y * 2 - 1)
                VG.scale(2.0/GRID_X,2.0/GRID_Y)
#                if random() < .1:
#                    VG.scale(1.0+phase,1.0+phase)
                VG.scale(pe.bass+1.0,pe.treb+1.0)
                VG.rotate(float(i)/GRID_X*360.0*pe.time)


                # awesome
#                VG.translate(sin(pe.time+i/GRID_Y),0)

                    


                segments = min(j+1, GRID_Y-j)
                flag = True if ((j+2) % (i+2)) and ((i+2) % (j+2)) else False

                self.wheel(segments, DUTY_CYCLE, OUTER_RADIUS, INNER_RADIUS, LINE_WIDTH,
                      float(i)/GRID_X, sin(float(i)/GRID_X*pi)+sin(pe.time)*2*pi, 1)
                VG.load_matrix(saved)
