from parameters import pe
from bindings import PeBindings
import math, time

# ----------------------------------------------------
#                   OSC Controller
# ----------------------------------------------------

class OscController(object):

    def register_shape(self, shape):
        self._shapes.append(shape)

    def __init__(self, osc_debug = False):
        self._shapes = []
        self.OSC_DEBUG = osc_debug
        self.bindings = PeBindings()

        # Set up some basic control bindings
        self.bindings.add(self, "/1/decay", "decay", 0.9, 1.1, 0.99, "log10")
        self.bindings.add(self, "/1/xy1/0", "zoom", 1.1, 0.9, 1.0)
        self.bindings.add(self, "/1/xy1/1", "rot", 0.785, -0.785, 0.0)

        # Warp Effect
        self.bindings.add(self, "/1/warp", "warp", 0.0, 3.0, 0.0)
#        self.bindings.add(self, "/1/warp_speed", "warp_speed", 0.1, 10.0, 1.0, "log10")
#        self.bindings.add(self, "/1/warp_scale", "warp_scale", 0.2, 2.0, 1.0)
        self.bindings.add(self, "/1/warp_speed", "square_a", 0.0, 1.0, 1.0)
        self.bindings.add(self, "/1/warp_scale", "ib_a", 0.0, 1.0, 0.0)

        # Video Echo Effect
        self.bindings.add(self, "/1/echo_alpha", "echo_alpha", 0.0, 1.0, 0.33)
        self.bindings.add(self, "/1/echo_zoom", "echo_zoom", 0.9, 1.1, 1.0)

        # Kaleidoscope
        self.bindings.add(self, "/1/kaleidoscope", "kaleidoscope", 0.0, 1.0, 0.0)
        self.bindings.add(self, "/1/kaleidoscope_radius", "kaleidoscope_radius", 0.1, 0.8, 0.3)

        # Fluid Effects
        self.bindings.add(self, "/1/fluid_viscosity", "wave_frequency", 1e-2, 500, 0.01, "log10")
#        self.bindings.add(self, "/1/fluid_viscosity", "fluid_viscosity", 1e-5, 0.008, 1e-4, "log10")
#        self.bindings.add(self, "/1/fluid_diffusion", "fluid_diffusion", 1e-10, 1e10, 1.0, "log10")

        self.bindings.add(self, "/2/fader30", "sx", 0.9, 1.1, 1.0)
        self.bindings.add(self, "/2/fader5", "sy", 0.9, 1.1, 1.0)

        # Other
#        self.bindings.add(self, "/1/invert", "invert", 0.0, 1.0, 0.0)
        self.bindings.add(self, "/1/q1", "q1", 0.0, 1.0, 0.0)
        self.bindings.add(self, "/1/q2", "q2", 0.0, 1.0, 0.0)

        # Bindings for the wiimote
#        self.bindings.add(self, "/wii/1/ir/0", "vg_x", -1.6, 1.6, 0.0)
#        self.bindings.add(self, "/wii/1/ir/1", "vg_y", -1.0, 1.0, 0.0)
#        self.bindings.add(self, "/wii/1/button/A", "vg_stroke_a", 0.0, 1.0, 0.0)
#        self.bindings.add(self, "/wii/1/button/B", "vg_fill_a", 0.0, 1.0, 0.0)
        

#        self.bindings.add(self, "/wii/1/accel/pry/0", "zoom", 0.9, 1.1, 1.0)
#        self.bindings.add(self, "/wii/1/accel/pry/1", "rot", 0.785, -0.785, 1.0)
#        self.bindings.add(self, "/wii/1/accel/pry/2", "decay", 0.9, 1.1, 1.0)

    def receive_callback(self, path, values):
        print 'hi there...'

        if (path == "/1/invert"):
            pe.set_control_value('vg_mode', pe.vg_mode + 1);
            if pe.vg_mode > 4:
                pe.set_control_value("vg_mode", 0)

        if (path == "/2/toggle6"):
            pe.reset_all()

        if (path == "/xyxyM"):
            for s in self._shapes:
                s.add_video_shape(values)

        if (path == "/xy"):
            pe.set_control_value('kaleidoscope_x', values[0])
            pe.set_control_value('kaleidoscope_y', values[1])
            

        # Capture the rotation rate
        rot_rate_gain = 0.25
        zoom_rate_gain = 0.22
        if (path == "/1/xy1"):

            pe.rot = -1*(values[1]-0.5)*0.707
            pe.zoom = -(values[0]-0.5)*0.1+1.0
            
            delta = (values[1]-0.5) * rot_rate_gain
            if (math.fabs(values[1]-0.5) > 0.05):
                pe.set_control_value('rot_rate', delta)

            delta = (values[0]-0.5) * zoom_rate_gain
            if (math.fabs(values[0]-0.5) > 0.05): 
                pe.set_control_value('zoom_rate', delta)

        if (path == "/1/xy1/z" and value == 0):
            pe.set_control_value('zoom_rate', 0.0);
            pe.set_control_value('rot_rate', 0.0);

        if (self.OSC_DEBUG and (path.find("pry") == -1)):
            print("[OSC]    Path: " + path + "   Value: " + str(values))
        self.bindings.controller_to_parameter(self, path, values[0])
    
    def render_callback(self): 
        pass

