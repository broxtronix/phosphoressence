from parameters import pe
from bindings import pe_bindings
import math

# ----------------------------------------------------
#                   OSC Controller
# ----------------------------------------------------

class OscController(object):

    def __init__(self):
        pass
        # # Set up some basic control bindings
        # pe_bindings.add(self, "/1/fader1", "decay", 0.9, 1.1, 0.99, "log10")
        # pe_bindings.add(self, "/1/xy/0", "zoom", 1.25, 0.75, 1.0)
        # pe_bindings.add(self, "/1/xy/1", "rot", 0.785, -0.785, 0.0)
        # #pe_bindings.add(self, "/1/fader2", "warp", 0.0, 2.0, 0.0)
        # #pe_bindings.add(self, "/1/fader3", "wave_frequency", 0.01, 300, 100, "log10")
        # pe_bindings.add(self, "/1/toggle3", "wave_enabled", 0.0, 1.0, 0.0)
        # pe_bindings.add(self, "/1/fader4", "zoomexp", 0.25, 5.0, 1.0, "log10")  
        # pe_bindings.add(self, "/1/push1", "ib_size", 0, 0, 0)  
        # pe_bindings.add(self, "/1/push2", "ib_size", 1, 1, 0)  
        # pe_bindings.add(self, "/1/push3", "ib_size", 10, 10, 0)  


    # bindings.add(osc, "/2/fader1", "sx", 0.5, 1.5, 1.0)
    # bindings.add(osc, "/2/fader2", "sy", 0.5, 1.5, 1.0)
    # bindings.add(osc, "/2/fader3", "dx", -0.5, 0.5, 0.0)
    # bindings.add(osc, "/2/fader4", "dy", -0.5, 0.5, 0.0)
    # bindings.add(osc, "/2/fader5", "cx", -1.5, 1.5, 0.0)
    # bindings.add(osc, "/2/fader6", "cy", -1.5, 1.5, 0.0)
    # bindings.add(osc, "/2/toggle8", "square_a", 0.0, 1.0, 1.0)
    # bindings.add(osc, "/2/fader8", "square_frequency", 0.001, 1.0, 0.03)

    # bindings.add(osc, "/3/fader2", "warp_speed", 0.0, 1.0, 0.5)
    # #    bindings.add(osc, "/3/fader3", "warp_scale", 0.01, 1.0, 0.5)
    # bindings.add(osc, "/3/fader4", "mv_x", 0, 64.0, 64.0)
    # bindings.add(osc, "/3/fader5", "mv_y", 0, 48.0, 48.0)
    # bindings.add(osc, "/3/fader6", "mv_dx", 0.0, 0.1, 0.0)
    # bindings.add(osc, "/3/fader7", "mv_dy", 0.0, 0.1, 0.0)
    # bindings.add(osc, "/3/fader8", "mv_l", 0.01, 0.2, 0.01)

    # bindings.add(osc, "/2/fader1", "lj_A", 0, 1.0, 1.0) 
    # bindings.add(osc, "/2/fader2", "lj_B", 0, 1.0, 1.0) 
    # bindings.add(osc, "/2/fader3", "lj_omega", 0.01, 10000.0, 1.0, "log10") 
    # bindings.add(osc, "/2/fader4", "lj_ratio_a", 1.0, 10.0, "log10") 
    # bindings.add(osc, "/2/fader5", "lj_ratio_b", 1.0, 10.0, "log10") 
    # bindings.add(osc, "/2/fader6", "lj_phase", 0.9, 1.1, 1.0)     

    # bindings.add(osc, "/3/fader1", "q1", 0, 2, 1.0) # a
    # bindings.add(osc, "/3/fader2", "q2", 0, 6.28, 0.0)
    # bindings.add(osc, "/3/fader3", "q3", -2, 2, 0.0) # b
    # bindings.add(osc, "/3/fader4", "q4", 0, 6.28, 0.0)
    # bindings.add(osc, "/3/fader5", "q5", 0, 2, 0.0) # c
    # bindings.add(osc, "/3/fader6", "q6", 0, 6.28, 0.0)
    # bindings.add(osc, "/3/fader7", "q7", -2, 2, 1.0) # d
    # bindings.add(osc, "/3/fader8", "q8", 0, 6.28, 0.0)

    # pe_parameters().add_parameter("rd_width", "/3/fader1", 0.0, 50.0, 1.0)
    # pe_parameters().add_parameter("rd_D_g", "/3/fader2", 0.0, 0.5, 0.25)
    # pe_parameters().add_parameter("rd_D_b", "/3/fader3", 0.0, 0.5, 0.0625)
    # pe_parameters().add_parameter("rd_s", "/3/fader4", 0.0, 0.05, 0.03125)
    # pe_parameters().add_parameter("rd_beta", "/3/fader5", 0.0, 24.0, 12)
    # pe_parameters().add_parameter("rd_blur", "/3/fader8", 0.0, 4.0, 0.0)

    def receive_callback(self, path, value):
        #        if (DEBUG):
        # print("[OSC]    Path: " + path + "   Value: " + str(value))
        pe_bindings.controller_to_parameter(self, path, value)
    
    def render_callback(self): 
        pass

# ----------------------------------------------------
#                Joystick Controller
# ----------------------------------------------------

class JoystickController(object):

    def __init__(self, joystick_debug = False):

        self.JOY_DEBUG = joystick_debug

        # Langton bEATS
        pe_bindings.add(self, "/joystick0/axis2", "decay", 0.85, 1.05, 0.98, "log10")
        pe_bindings.add(self, "/joystick0/axis4", "warp", 4.0, 0.0, 0.0)
        #pe_bindings.add(self, "/joystick0/axis5", "warp_scale", 0.25, 2.0)
        #pe_bindings.add(self, "/joystick0/axis4", "echo_zoom", 0.0, 2.0, 1.0)
        pe_bindings.add(self, "/joystick0/axis5", "echo_alpha", 0.0, 1.0, 0.0)
        #pe_bindings.add(self, "/joystick0/axis4", "reflect_theta", 0., 6.28, 0.0)
        #pe_bindings.add(self, "/joystick0/axis5", "reflect_offset", -1.0, 1.0, 0.0)
#        pe_bindings.add(self, "/joystick0/axis4", "reflect_theta", 0.0, 6.28, 0.0)
#        pe_bindings.add(self, "/joystick0/axis5", "reflect_offset", 0.0, 6.28, 0.0)

        # Local variables, for helping us to keep track of various
        # joystick settings.
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
        pe.wave_enabled = 1
        pe.wave_mode = 2
        pe.square_a = 1.0
        pe.ib_size=10.0
        pe.ib_a = 0.0
        pe.mv_a = 1.0
        pe.mv_x = 0
        pe.mv_y = 0
        pe.mv_l = 0
        pe.rot = -0.001
        pe.sx=0.999
        

    def receive_callback(self, path, value): 

        # -------------------------------------
        # Fixed settings for the langton bEATS!
        # -------------------------------------
    
        # RESET!!
        if (path == "/joystick0/button3" and value == 1): 
            print("Resetting to defaults!!\n>> ")
            pe.reset_all()
            pe.mv_a = 1.0
            pe.mv_x = 0
            pe.mv_y = 0
            pe.mv_l = 0
            pe.rot = -0.001
            pe.sx=0.999
            pe.wave_mode=2
            pe.wave_enabled = 1
    

        # IFS Mode
        if (path == "/joystick0/button0" and value == 1): 
            pe.set_control_value('ifs_mode', pe.ifs_mode + 1)
            if (pe.ifs_mode > 4):
                pe.set_control_value('ifs_mode', 0)

        if (path == "/joystick0/button6" and value == 1): 
            pe.set_control_value('ifs_mode', pe.ifs_mode - 1)
            if (pe.ifs_mode < 0):
                pe.set_control_value('ifs_mode', 4)
    

        # Squareshape Enable
        if (path == "/joystick0/button1" and value == 1): 
            if (pe.square_a): pe.set_control_value('square_a', 0.0)
            else: pe.set_control_value('square_a', 1.0)


        # Border Enable
        if (path == "/joystick0/button2" and value == 1): 
            if (pe.ib_a): pe.set_control_value('ib_a', 0.0)
            else: pe.set_control_value('ib_a', 1.0)

        # Invert
        if (path == "/joystick0/button4" and value == 1): 
            if (pe.invert): pe.set_control_value('invert', 0.0)
            else: pe.set_control_value('invert', 1.0)


        # Translation
        if (path == "/joystick0/hat0" and value == 2): 
            self.square_thick_coeff = 1.0
        if (path == "/joystick0/hat0" and value == 8): 
            self.square_thick_coeff = -1.0
        if (path == "/joystick0/hat0" and value == 1): 
            self.square_scale_coeff = 1.0
        if (path == "/joystick0/hat0" and value == 4): 
            self.square_scale_coeff = -1.0
        if (path == "/joystick0/hat0" and value == 0.0): 
            self.square_thick_coeff = 0.0
            self.square_scale_coeff = 0.0
            self.wave_frequency_coeff = 0.0


        # Reflect
        if (path == "/joystick0/button7" and value == 1): 
            if (pe.reflect == 1.0): pe.set_control_value('reflect', 0.0)
            else: pe.set_control_value('reflect', 1.0)


        # Rotation
        rot_gain = 0.01
        if (path == "/joystick0/axis0"):
            delta = -(value-0.5) * rot_gain
            if (math.fabs(value-0.5) > 0.05): 
                pe.set_control_value('rot', pe.rot - delta)
                # if (pe.rot > 0.785): pe.rot = 0.785   # Turn off rotation 
                # if (pe.rot < -0.785): pe.rot = -0.785 # limits for now.



        # Zoom
        zoom_gain = 0.002
        if (path == "/joystick0/axis1"): 
            delta = (value-0.5) * zoom_gain
            if (math.fabs(value-0.5) > 0.05): 
                pe.set_control_value('zoom', pe.zoom - delta)
                if (pe.zoom > 1.16): pe.zoom = 1.16
                if (pe.zoom < 0.5): pe.zoom = 0.5



        # Zoomexp
        if (path == "/joystick0/axis3"): 
            delta = (value-0.5)/20.0
            if (math.fabs(value-0.5) > 0.05):
                pe.set_control_value('zoomexp', pe.zoomexp - delta)
            if (pe.zoomexp < 0.25): pe.set_control_value('zoomexp', 0.25)
            if (pe.zoomexp > 2.0): pe.set_control_value('zoomexp', 2.0)


        # Scaling
        if (path == "/joystick0/button21" and value == 1.0): 
            self.sx_coefficient = 1.0
        if (path == "/joystick0/button21" and value == 0.0): 
            self.sx_coefficient = 0.0
        if (path == "/joystick0/button19" and value == 1.0): 
            self.sx_coefficient = -1.0
        if (path == "/joystick0/button19" and value == 0.0): 
            self.sx_coefficient = 0.0

        if (path == "/joystick0/button20" and value == 1.0): 
            self.sy_coefficient = 1.0
        if (path == "/joystick0/button20" and value == 0.0): 
            self.sy_coefficient = 0.0
        if (path == "/joystick0/button18" and value == 1.0): 
            self.sy_coefficient = -1.0
        if (path == "/joystick0/button18" and value == 0.0): 
            self.sy_coefficient = 0.0

        # Center of rotation
        if (path == "/joystick0/button23" and value == 1.0): 
            self.dx_coefficient = -1.0
        if (path == "/joystick0/button23" and value == 0.0): 
            self.dx_coefficient = 0.0
        if (path == "/joystick0/button25" and value == 1.0): 
            self.dx_coefficient = 1.0
        if (path == "/joystick0/button25" and value == 0.0): 
            self.dx_coefficient = 0.0

        if (path == "/joystick0/button22" and value == 1.0): 
            self.dy_coefficient = -1.0
        if (path == "/joystick0/button22" and value == 0.0): 
            self.dy_coefficient = 0.0
        if (path == "/joystick0/button24" and value == 1.0): 
            self.dy_coefficient = 1.0
        if (path == "/joystick0/button24" and value == 0.0): 
            self.dy_coefficient = 0.0

        # Motion Vectors
        if (path == "/joystick0/button15" and value == 1.0): 
            if (pe.mv_x == 0 or pe.mv_y == 0): 
                pe.set_control_value('mv_x', 2)
                pe.set_control_value('mv_y', 2)
            elif (pe.mv_x < 64 and pe.mv_y < 64): 
                pe.set_control_value('mv_x', pe.mv_x * 2)
                pe.set_control_value('mv_y', pe.mv_y * 2)

        if (path == "/joystick0/button17" and value == 1.0): 
            if (pe.mv_x == 2 or pe.mv_y == 2): 
                pe.set_control_value('mv_x', 0)
                pe.set_control_value('mv_y', 0)
            else: 
                pe.set_control_value('mv_x', pe.mv_x / 2)
                pe.set_control_value('mv_y', pe.mv_y / 2)


        if (path == "/joystick0/button14" and value == 1.0): 
            self.mv_l_coeff = 1.0
        if (path == "/joystick0/button14" and value == 0.0): 
            self.mv_l_coeff = 0.0
        if (path == "/joystick0/button16" and value == 1.0): 
            self.mv_l_coeff = -1.0
        if (path == "/joystick0/button16" and value == 0.0): 
            self.mv_l_coeff = 0.0

        # Reset center of rotation, scaling, and zoom exponent
        if (path == "/joystick0/button5" and value == 1.0): 
            pe.sx= 1.0
            pe.sy= 1.0
            pe.dx = 0.0
            pe.dy = 0.0
            pe.wave_enabled = 1
            pe.wave_mode = 0
            pe.square_a = 1.0
            pe.ib_a = 0.0
            pe.zoomexp = 1.0


        # Warp
        if (path == "/joystick0/button0" and value == 1.0):
            self.warp_coefficient = 1.0
        if (path == "/joystick0/button0" and value == 0.0):
            self.warp_coefficient = 0.0
        if (path == "/joystick0/button6" and value == 1.0):
            self.warp_coefficient = -1.0
        if (path == "/joystick0/button6" and value == 0.0): 
            self.warp_coefficient = 0.0


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
            pe.set_control_value('wave_frequency', 0.5)
            pe.set_control_value('wave_mode', 2)
        elif (path == "/joystick0/button13" and value == 1): 
            pe.set_control_value('wave_frequency', 10.0)
            pe.set_control_value('wave_mode', 2)


        # Debugging
        if (self.JOY_DEBUG and (path.find("axis") == -1)):
            print("[JOYSTICK]    Path: " + path + "   Value: " + str(value))

        # Otherwise, delegate to the bindings.
        pe_bindings.controller_to_parameter(self, path, value)


    def render_callback(self):

        # Update scaling
        scaling_stepsize = 0.0005
        pe.set_control_value('sx', pe.sx + scaling_stepsize * self.sx_coefficient)
        pe.set_control_value('sy', pe.sy + scaling_stepsize * self.sy_coefficient)
        if (pe.sx > 1.5): pe.set_control_value('sx', 1.5)
        if (pe.sx < 0.5): pe.set_control_value('sx', 0.5)
        if (pe.sy > 1.5): pe.set_control_value('sy', 1.5)
        if (pe.sy < 0.5): pe.set_control_value('sy', 0.5)

#--- CONTROLS FIXED TO HERE

        # Update center of rotation
        crot_stepsize = 1/100.0
        pe.cx += crot_stepsize * self.cx_coefficient
        pe.cy += crot_stepsize * self.cy_coefficient
        if (pe.cx > 1.5): pe.cx = 1.5
        if (pe.cx < -1.5): pe.cx = -1.5
        if (pe.cy > 1.5): pe.cy = 1.5
        if (pe.cy < -1.5): pe.cy = -1.5

        # Update Square Scale
        square_scale_stepsize = 0.05
        pe.square_scale += square_scale_stepsize * self.square_scale_coeff
        if (pe.square_scale > 4.0): pe.square_scale = 4.0
        if (pe.square_scale < 0.25): pe.square_scale = 0.25

        # Update Square Thickness
        square_thick_stepsize = 1.2
        if (self.square_thick_coeff == 1.0):
            pe.square_thick *= square_thick_stepsize
        if (self.square_thick_coeff == -1.0):
            pe.square_thick /= square_thick_stepsize
        if (pe.square_thick > 500.0): pe.square_thick = 500.0
        if (pe.square_thick < 1.0): pe.square_thick = 1.0

        # Update dx & dy
        dx_stepsize = 0.01
        if (self.dx_coefficient > 0):
            pe.dx += dx_stepsize
        elif (self.dx_coefficient < 0):
            pe.dx -= dx_stepsize
        if (pe.dx > 0.5): pe.dx = 0.5
        if (pe.dx < -0.5): pe.dx = -0.5

        dy_stepsize = 0.01
        if (self.dy_coefficient > 0):
            pe.dy += dy_stepsize
        elif (self.dy_coefficient < 0):
            pe.dy -= dy_stepsize
        if (pe.dy > 0.5): pe.dy = 0.5
        if (pe.dy < -0.5): pe.dy = -0.5


        # Update wave_frequency
        # wave_frequency_stepsize = 1.1
        # if (self.wave_frequency_coeff > 0)
        #     pe.wave_frequency *= wave_frequency_stepsize
        # elif (self.wave_frequency_coeff < 0)
        #     pe.wave_frequency /= wave_frequency_stepsize
        # if (pe.wave_frequency > 10.0) pe.wave_frequency = 10.0
        # if (pe.wave_frequency < 0.03) pe.wave_frequency = 0.03

        # Update MV length
        mv_l_stepsize = 1/20.0
        pe.mv_l += mv_l_stepsize * self.mv_l_coeff
        if (pe.mv_l > 1.5): pe.mv_l = 1.5
        if (pe.mv_l < 0.0): pe.mv_l = 0.0


