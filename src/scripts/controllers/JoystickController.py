from parameters import pe
from bindings import PeBindings
import math, time

# ----------------------------------------------------
#                Joystick Controller
# ----------------------------------------------------

class JoystickController(object):

    def __init__(self, joystick_debug = False):

        self.JOY_DEBUG = joystick_debug
        self.bindings = PeBindings()

        # Priceless
        self.bindings.add(self, "/joystick0/axis4", "decay", 0.85, 1.01, 1.0, "log10")
        self.bindings.add(self, "/joystick0/axis5", "warp", 3.0, 0.0, 0.0)
#        self.bindings.add(self, "/joystick0/axis5", "q3", 1.0, -1.0, 0.0)
        self.bindings.add(self, "/joystick0/axis2", "echo_alpha", 0.0, 0.98, 0.0)
#        self.bindings.add(self, "/joystick0/axis2", "q7", 0.01, 1.0, 0.01)
#        self.bindings.add(self, "/joystick0/axis5", "q8", 0.01, 1.0, 0.01)

        # Local variables, for helping us to keep track of various
        # joystick settings.
        self.chord = 0.0
        self.sx_coefficient = 0.0
        self.sy_coefficient = 0.0
        self.cx_coefficient = 0.0
        self.cy_coefficient = 0.0
        self.warp_coefficient = 0.0
        self.reflect_coefficient = 0.0
        self.dx_coefficient = 0.0
        self.dy_coefficient = 0.0
        self.sqfreq_coefficient = 0.0
        self.wave_frequency_coeff = 0.0
        self.mv_l_coeff = 0.0
        self.square_scale_coeff = 0.0
        self.square_thick_coeff = 0.0

        # Default parameters for PhosphorEssence
        pe.wave_enabled = 1.0
        pe.wave_mode = 1.0
        pe.square_a = 1.0
        pe.ib_size=10.0
        pe.ib_a = 0.0
        pe.mv_a = 0.0
        pe.mv_x = 36
        pe.mv_y = 36
        pe.mv_l = 0
        pe.warp=0.0
        pe.rot = -0.001
        pe.sx=0.999
        pe.kaleidoscope_radius=0.25
        pe.fluid_viscosity=0.0005
        pe.fluid_diffusion=0.001
        

    def receive_callback(self, path, value):


        # Darken the center when gain is high!  This helps to keep
        # things "under control."
        if (pe.decay > 1.01):
            pe.darken_center = 1.0
        else:
            pe.darken_center = 0.0
        

        # -------------------------------------
        # Fixed settings for PRICELESS!!
        # -------------------------------------
    
        # RESET!!
        if (path == "/joystick0/button3" and value == 1): 
            print("Resetting to defaults!!\n>> ")
            pe.reset_all()
            pe.set_control_value('mv_a', 0.0)
            pe.set_control_value('mv_x', 36)
            pe.set_control_value('mv_y', 36)
            pe.set_control_value('mv_l', 0)
            pe.set_control_value('rot', 0)
            pe.set_control_value('sx',1.0)
            pe.set_control_value('q1',0.0)
            pe.set_control_value('q2',0.0)
            pe.set_control_value('rot', -0.001)
            pe.set_control_value('sx',0.999)
            pe.set_control_value('wave_mode', 2)
            pe.set_control_value('wave_enabled',1.0)
            pe.set_control_value('square_a', 1.0)
            pe.set_control_value('ib_size',10.0)
    
        # Waveshape Enable
        if (path == "/joystick0/button0" and value == 1):
            pe.vg_mode = pe.vg_mode + 1;
            if (pe.vg_mode > 3):
                pe.vg_mode = 0

        # Motion Vectors
        if (path == "/joystick0/button1" and value == 1):
            if (pe.ib_a): pe.set_control_value('ib_a', 0.0)
            else: pe.set_control_value('ib_a', 1.0);    

        # Border Enable
        if (path == "/joystick0/button2" and value == 1):
            if (pe.warp_scale == 1.0):
                pe.set_control_value('warp_scale', 5.0)
            else:
                pe.warp_scale=1.0
                pe.set_control_value('warp_scale', 1.0)
#            if (pe.wave_move): pe.set_control_value('wave_move', 0.0)
#            else: pe.set_control_value('wave_move', 1.0)

        # Kaleidoscope
        if (path == "/joystick0/button4" and value == 1.0):
            if (pe.kaleidoscope):
                pe.set_control_value('kaleidoscope', 0.0)
            else:
                pe.set_control_value('kaleidoscope', 1.0)

        # Video fractal enable
        if (path == "/joystick0/button5" and value == 1.0):
            if (pe.video_fractal):
                pe.set_control_value('video_fractal', 0.0)
                pe.set_control_value('brighten', 0.0)
            else:
                pe.set_control_value('video_fractal', 1.0)
                pe.set_control_value('brighten', 1.0)

        # Squareshape Enable
        if (path == "/joystick0/button6" and value == 1):
            if (pe.wave_enabled): pe.set_control_value('wave_enabled', 0.0)
            else: pe.set_control_value('wave_enabled', 1.0)

        # Vector Field
        if (path == "/joystick0/button7" and value == 1):
            if (pe.invert): pe.set_control_value('invert', 0.0)
            else: pe.set_control_value('invert', 1.0)
#            if (pe.wave_usedots): pe.set_control_value('wave_usedots', 0.0)
#            else: pe.set_control_value('wave_usedots', 1.0)

        # Translation
        if (path == "/joystick0/hat0" and value == 2):
            #            pe.set_control_value('brighten', 1.0);
            #            pe.set_control_value('darken', 0.0);
            self.square_thick_coeff = 1.0
        if (path == "/joystick0/hat0" and value == 8):
            #pe.set_control_value('darken', 1.0);
            #pe.set_control_value('brighten', 0.0);
            self.square_thick_coeff = -1.0
        if (path == "/joystick0/hat0" and value == 1): 
            #pe.set_control_value('darken', 0.0);
            #pe.set_control_value('solarize', 0.0);
            #pe.set_control_value('brighten', 0.0);
            self.square_scale_coeff = 1.0
        if (path == "/joystick0/hat0" and value == 4): 
            #pe.set_control_value('solarize', 1.0);
            self.square_scale_coeff = -1.0
        if (path == "/joystick0/hat0" and value == 0.0):
            self.square_thick_coeff = 0.0
            self.square_scale_coeff = 0.0
            self.wave_frequency_coeff = 0.0


        # Wave Movement
#         if (path == "/joystick0/button6"):
#             if (pe.wave_move == 1.0):
#                 pe.set_control_value('wave_move', 0.0)
#                 pe.set_control_value('wave_x',0.5)
#                 pe.set_control_value('wave_y',0.5)
#             else: pe.set_control_value('wave_move', 1.0)


        # Capture the rotation rate
        rot_rate_gain = -0.01
        if (path == "/joystick0/axis0"):
            delta = (value-0.5) * rot_rate_gain
            if (math.fabs(value-0.5) > 0.05):
                pe.set_control_value('rot_rate', delta)

        # Capture the zoom rate
        zoom_rate_gain = 0.02
        if (path == "/joystick0/axis1"): 
            delta = (value-0.5) * zoom_rate_gain
            if (math.fabs(value-0.5) > 0.05): 
                pe.set_control_value('zoom_rate', delta)

        # Rotation
        rot_gain = 0.01
        if (path == "/joystick0/axis0"):
            delta = -(value-0.5) * rot_gain
            if (math.fabs(value-0.5) > 0.05): 
                if (self.chord):
                    pe.set_control_value('q2', pe.q2 + 2.0*delta)
                else:
                    pe.set_control_value('rot', pe.rot - delta)

        # Zoom
        zoom_gain = 0.002
        if (path == "/joystick0/axis1"): 
            if (math.fabs(value-0.5) > 0.05):
                if (self.chord):
                    delta = -(value-0.5) * rot_gain
                    pe.set_control_value('q1', pe.q1 - delta)
                else:
                    delta = (value-0.5) * zoom_gain
                    pe.set_control_value('zoom', pe.zoom - delta)
                    if (pe.zoom > 1.16): pe.set_control_value('zoom', 1.16)
                    if (pe.zoom < 0.5): pe.set_control_value('zoom', 0.5)


        # Zoomexp & Kaliedoscope_raidus share this control
        if (path == "/joystick0/axis3"):
            if (pe.kaleidoscope == 1.0):
                delta = (value-0.5)/80.0
                if (math.fabs(value-0.5) > 0.05):
                    pe.set_control_value('kaleidoscope_radius', pe.kaleidoscope_radius - delta)
                if (pe.kaleidoscope_radius < 0.0): pe.set_control_value('kaleidoscope_radius', 0.0)
                if (pe.kaleidoscope_radius > 1.0): pe.set_control_value('kaleidoscope_radius', 1.0)
            else:
                delta = (value-0.5)/80.0
                if (math.fabs(value-0.5) > 0.05):
                    pe.set_control_value('zoomexp', pe.zoomexp - delta)
                if (pe.zoomexp < 0.25): pe.set_control_value('zoomexp', 0.25)
                if (pe.zoomexp > 2.0): pe.set_control_value('zoomexp', 2.0)


        # Scaling
        sx_increase ="/joystick0/button17" 
        sx_decrease ="/joystick0/button15" 
        sy_increase ="/joystick0/button16" 
        sy_decrease ="/joystick0/button14"

        # swap for vertical orientation
        if (pe.orientation == 1.0): 
            sy_increase ="/joystick0/button17" 
            sy_decrease ="/joystick0/button15" 
            sx_increase ="/joystick0/button16" 
            sx_decrease ="/joystick0/button14"
        
        if (path == sx_increase and value == 1.0): 
            self.sx_coefficient = 1.0
        if (path == sx_increase and value == 0.0): 
            self.sx_coefficient = 0.0
        if (path == sx_decrease and value == 1.0): 
            self.sx_coefficient = -1.0
        if (path == sx_decrease and value == 0.0): 
            self.sx_coefficient = 0.0

        if (path == sy_increase and value == 1.0): 
            self.sy_coefficient = 1.0
        if (path == sy_increase and value == 0.0): 
            self.sy_coefficient = 0.0
        if (path == sy_decrease and value == 1.0): 
            self.sy_coefficient = -1.0
        if (path == sy_decrease and value == 0.0): 
            self.sy_coefficient = 0.0

        # Translation
        dx_increase ="/joystick0/button25" 
        dx_decrease ="/joystick0/button23" 
        dy_decrease ="/joystick0/button24" 
        dy_increase ="/joystick0/button22"

        # swap for vertical orientation
        if (pe.orientation == 1.0): 
            dy_decrease ="/joystick0/button25" 
            dy_increase ="/joystick0/button23" 
            dx_decrease ="/joystick0/button24" 
            dx_increase ="/joystick0/button22"

        if (path == dx_decrease and value == 1.0): 
            self.dx_coefficient = -1.0
        if (path == dx_decrease and value == 0.0): 
            self.dx_coefficient = 0.0
        if (path == dx_increase and value == 1.0): 
            self.dx_coefficient = 1.0
        if (path == dx_increase and value == 0.0): 
            self.dx_coefficient = 0.0

        if (path == dy_increase and value == 1.0): 
            self.dy_coefficient = 1.0
        if (path == dy_increase and value == 0.0): 
            self.dy_coefficient = 0.0
        if (path == dy_decrease and value == 1.0): 
            self.dy_coefficient = -1.0
        if (path == dy_decrease and value == 0.0): 
            self.dy_coefficient = 0.0


        # IFS Mode
        if (path == "/joystick0/button19" and value == 1.0):
            pe.set_control_value('ifs_mode', pe.ifs_mode + 1)
            if (pe.ifs_mode > 4):
                pe.set_control_value('ifs_mode', 0)
        if (path == "/joystick0/button21" and value == 1.0): 
            pe.set_control_value('ifs_mode', pe.ifs_mode - 1)
            if (pe.ifs_mode < 0):
                pe.set_control_value('ifs_mode', 4)
        if (path == "/joystick0/button20" and value == 1.0): 
            pe.set_control_value('ifs_mode', 0)
        if (path == "/joystick0/button18" and value == 1.0): 
            pe.set_control_value('ifs_mode', 0)


        # Activate the edge filter
#         if (path == "/joystick0/button5" and value == 1.0):
#             if (pe.edge_filter):
#                 pe.set_control_value('edge_filter', 0.0)
#                 pe.set_control_value('brighten', 0.0)
#                 pe.set_control_value('gamma', 1.0)
#             else:
#                 pe.set_control_value('edge_filter', 1.0)
#                 pe.set_control_value('brighten', 1.0)
#                 pe.set_control_value('gamma', 1.8)

        # Warp
        # if (path == "/joystick0/button0" and value == 1.0):
        #     self.warp_coefficient = 1.0
        # if (path == "/joystick0/button0" and value == 0.0):
        #     self.warp_coefficient = 0.0
        # if (path == "/joystick0/button6" and value == 1.0):
        #     self.warp_coefficient = -1.0
        # if (path == "/joystick0/button6" and value == 0.0): 
        #     self.warp_coefficient = 0.0


        # Wave mode
        if (path == "/joystick0/button8" and value == 1): 
            pe.set_control_value('wave_mode', 0)
            pe.set_control_value('wave_enabled', 1)
        elif (path == "/joystick0/button9" and value == 1): 
            pe.set_control_value('wave_mode', 1)
            pe.set_control_value('wave_enabled', 1)
        elif (path == "/joystick0/button10" and value == 1): 
            pe.set_control_value('wave_mode', 2)
            pe.set_control_value('wave_enabled', 1)


        # PRECIOUS UPPER SWITCH 
        if (path == "/joystick0/button11" and value == 1): 
            pe.set_control_value('wave_frequency', 0.03)
            pe.set_control_value('wave_mode', 2)
        elif (path == "/joystick0/button12" and value == 1): 
            pe.set_control_value('wave_frequency', 0.2)
            pe.set_control_value('wave_mode', 2)
        elif (path == "/joystick0/button13" and value == 1): 
            pe.set_control_value('wave_frequency', 9.0)
            pe.set_control_value('wave_mode', 2)

        # Debugging
        if (self.JOY_DEBUG and (path.find("axis") == -1)):
            print("[JOYSTICK]    Path: " + path + "   Value: " + str(value))

        # Otherwise, delegate to the bindings.
        self.bindings.controller_to_parameter(self, path, value)



    def render_callback(self):

        # Update scaling
        scaling_stepsize = 0.001
        if (self.sx_coefficient):
            pe.set_control_value('sx', pe.sx + scaling_stepsize * self.sx_coefficient)
        else:
            pe.set_control_value('sx', 1.0 + (pe.sx-1.0) * 0.95)
        if (self.sy_coefficient):
            pe.set_control_value('sy', pe.sy + scaling_stepsize * self.sy_coefficient)
        else:
            pe.set_control_value('sy', 1.0 + (pe.sy-1.0) * 0.95)
        if (pe.sx > 1.5): pe.set_control_value('sx', 1.5)
        if (pe.sx < 0.5): pe.set_control_value('sx', 0.5)
        if (pe.sy > 1.5): pe.set_control_value('sy', 1.5)
        if (pe.sy < 0.5): pe.set_control_value('sy', 0.5)

        # Update center of rotation
        crot_stepsize = 1/100.0
        pe.cx += crot_stepsize * self.cx_coefficient
        pe.cy += crot_stepsize * self.cy_coefficient
        if (pe.cx > 1.5): pe.set_control_value('cx', 1.5)
        if (pe.cx < -1.5): pe.set_control_value('cx', -1.5)
        if (pe.cy > 1.5): pe.set_control_value('cy', 1.5)
        if (pe.cy < -1.5): pe.set_control_value('cy', -1.5)

        # Update Square Scale
        square_scale_stepsize = 0.05
        pe.square_scale += square_scale_stepsize * self.square_scale_coeff
        if (pe.square_scale > 4.0): pe.square_scale = 4.0
        if (pe.square_scale < 0.25): pe.square_scale = 0.25

        # Update Square Thickness
        square_thick_stepsize = 1.2
        if (self.square_thick_coeff == 1.0):
            pe.set_control_value('square_thick', pe.square_thick * square_thick_stepsize)
        if (self.square_thick_coeff == -1.0):
            pe.set_control_value('square_thick', pe.square_thick / square_thick_stepsize)
        if (pe.square_thick > 15.0): pe.set_control_value('square_thick', 15.0)
        if (pe.square_thick < 1.0): pe.set_control_value('square_thick', 1.0)

        # Update dx & dy
        dx_stepsize = 0.01
        if (self.dx_coefficient > 0):
            pe.set_control_value('dx', pe.dx + dx_stepsize)
        elif (self.dx_coefficient < 0):
            pe.set_control_value('dx', pe.dx - dx_stepsize)
        if (pe.dx > 0.5): pe.set_control_value('dx', 0.5)
        if (pe.dx < -0.5): pe.set_control_value('dx', -0.5)

        dy_stepsize = 0.01
        if (self.dy_coefficient > 0):
            pe.set_control_value('dy', pe.dy - dy_stepsize)
        elif (self.dy_coefficient < 0):
            pe.set_control_value('dy', pe.dy + dy_stepsize)
        if (pe.dy > 0.5): pe.set_control_value('dy', 0.5)
        if (pe.dy < -0.5): pe.set_control_value('dy', -0.5)

        # Update wave_frequency
        # wave_frequency_stepsize = 1.1
        # if (self.wave_frequency_coeff > 0)
        #     pe.wave_frequency *= wave_frequency_stepsize
        # elif (self.wave_frequency_coeff < 0)
        #     pe.wave_frequency /= wave_frequency_stepsize
        # if (pe.wave_frequency > 10.0) pe.wave_frequency = 10.0
        # if (pe.wave_frequency < 0.03) pe.wave_frequency = 0.03

        # Set these values manually, which forces these parameters to
        # revert to these values after a certain amount of time has
        # passed.
        pe.dx = 0
        pe.dy = 0
        pe.sx = 1
        pe.sy = 1
        pe.zoomexp = 1
        pe.edge_filter = 0
#        pe.brighten = 0
#        pe.gamma = 1.0
        pe.ifs_mode = 0

        # Tweak decay
#         if (pe.decay < 0.851):
#             pe.set_control_value("decay", 0.1);

#         if (pe.decay > 0.99 and pe.decay <1.01):
#             pe.set_control_value("decay", pe.decay+0.01)            
#         elif (pe.decay > 0.99 and pe.decay <1.01):
#             pe.set_control_value("decay", 1.0)
#         elif (pe.decay >= 1.01):
#             pe.set_control_value("decay", pe.decay-0.01)
