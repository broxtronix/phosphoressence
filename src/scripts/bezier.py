import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from parameters import pe


class BezierSprite(object):

    def point_on_bezier_curve(self, p1, p2, p3, p4, t):

        # Below is the equation for a 4 control point bezier curve:
        #
        #   B(t) = P1 * ( 1 - t )^3 + P2 * 3 * t * ( 1 - t )^2 +
        #          P3 * 3 * t^2 * ( 1 - t ) + P4 * t^3 
  
        # Store the (1 - t) in a variable because it is used frequently
        var1 = 1 - t;
  
        # Store the (1 - t)^3 into a variable to cut down computation
        # and create clean code
        var2 = math.pow(var1,3)
  
        # Store the t^3 in a variable to cut down computation and
        # create clean code
        var3 = math.pow(t,3)
  
        point = [var2*p1[0] + 3*t*var1*var1*p2[0] + 3*t*t*var1*p3[0] + var3*p4[0],
                 var2*p1[1] + 3*t*var1*var1*p2[1] + 3*t*t*var1*p3[1] + var3*p4[1],
                 var2*p1[2] + 3*t*var1*var1*p2[2] + 3*t*t*var1*p3[2] + var3*p4[2]]

        return point
        
    
    def render(self):
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
 
        glLoadIdentity()
        glLineWidth(pe.square_thick)

        glColor3f( 0.0, 1.0, 1.0)

        glBegin(GL_LINE_STRIP)
        for i in range(200): 
            t = float(i)/200.0

            # Get the current point on the curve, depending on the time.
            curvePoint = self.point_on_bezier_curve(start_point, control_point1, control_point2, control_point3, t)
	   
            # Draw the current point at distance "t" of the curve.
            glVertex3f(curvePoint[0], curvePoint[1], curvePoint[2]);
	 	   
        glEnd()
