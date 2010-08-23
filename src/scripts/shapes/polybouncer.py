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
from numpy import array, ones

# ---------------------------------------------------------------------------
#                               PolyBouncerSprite
# ---------------------------------------------------------------------------
class PolyBouncerSprite(OpenVgSprite):

    def __init__(self, num_vertices = 4, speed = 0.01):

        self.speed = speed
        self.points = ones( (2, num_vertices) )
        self.directions = ones( (2, num_vertices) )
        for i in range(num_vertices):
            self.points[0,i] = random() * 2.0 - 1.0
            self.points[1,i] = random() * 2.0 - 1.0
            self.directions[0,i] = round(random()) * 2.0 - 1.0
            self.directions[1,i] = round(random()) * 2.0 - 1.0
    
    def render(self):
        self.setup_canvas()
        num_points = self.points.shape[1]

        for i in range(num_points):
            self.points[0,i] += self.speed * self.directions[0,i]
            self.points[1,i] += self.speed * self.directions[1,i]
            if self.points[0,i] > pe.aspect or self.points[0,i] < -pe.aspect:
                self.directions[0,i] *= -1
            if self.points[1,i] > 1.0 or self.points[1,i] < -1.0:
                self.directions[1,i] *= -1

        # Compute centroid and furthest distance of points.
        for i in range(num_points):
            avg_sum = [0,0]
            avg_sum[0] += self.points[0,i] 
            avg_sum[1] += self.points[1,i]
        centroid = [avg_sum[0]/num_points, avg_sum[1]/num_points]

        # Compute furthest
        fill_radius = 0
        for i in range(num_points):
            if (math.fabs(self.points[0,i]-avg_sum[0]) > fill_radius):
                fill_radius = math.fabs(self.points[0,i]-avg_sum[0]) > fill_radius
            if (math.fabs(self.points[1,i]-avg_sum[1]) > fill_radius):
                fill_radius = math.fabs(self.points[1,i]-avg_sum[1]) > fill_radius


        # Set point to a gradient
        gradient_fill_paint = VG.GradientPaint(((centroid[0],centroid[1]),
                                                (centroid[0],centroid[1]),
                                                fill_radius), False)
        gradient_fill_paint.stops = [(0.0, (pe.vg_fill_r,
                                           pe.vg_fill_g,
                                           pe.vg_fill_b,
                                           1.0)),
                                     (1.0, (pe.vg_fill_r,
                                           pe.vg_fill_g,
                                           pe.vg_fill_b,
                                           pe.vg_fill_a))]
        VG.set_paint(gradient_fill_paint, VG_FILL_PATH)

        # Draw the lines that connect the dots
        p = VG.Path()
        p.move_to((self.points[0,0], self.points[1,0]))
        for i in range(1,num_points):
            p.line_to((self.points[0,i], self.points[1,i]));
        p.close()
        p.draw(VG_FILL_PATH);                             # Draw the Fill
        p.draw(VG_STROKE_PATH);                           # Draw the stroke

        # Draw the dots at the vertices (disabled for now)
        #p = VG.Path()
        #dot_width = pe.vg_stroke_width * 10
        #for i in range(num_points):
        #    VGU.rect(p,
        #             (self.points[0,i]-dot_width/2.0, self.points[1,i]-dot_width/2.0),
        #             (dot_width, dot_width))
        #p.draw(VG_FILL_PATH);                             # Draw the Fill
        #p.draw(VG_STROKE_PATH);                           # Draw the stroke

