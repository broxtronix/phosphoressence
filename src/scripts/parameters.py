import time

# --------------------------------------------------------------
#                  The Parameter Object
# --------------------------------------------------------------

class Parameter(object):
    
    
    def __init__(self, name, description,
                 default_value = 0.0, read_only = False):

        # Constants
        self.CONTROL_AUTOMATE = 0
        self.CONTROL_OVERRIDE = 1
        self.TIMEOUT_LENGTH = 120.0   # seconds

        # Store the parameters specific to this parameter in the class
        # instance.
        self.name = name
        self.description = description
        self.default_value = default_value
        self.read_only = read_only
        self.value = default_value

        # Automation parameters
        self.control_mode = self.CONTROL_AUTOMATE
        self.last_control_time = 0.0

    def set_value(self, value):
        if (self.control_mode == self.CONTROL_OVERRIDE and
            time.time() - self.last_control_time > self.TIMEOUT_LENGTH):
            self.control_mode = self.CONTROL_AUTOMATE

        if (self.control_mode == self.CONTROL_AUTOMATE):
            self.value = value

    def set_control_value(self, value):
        self.control_mode = self.CONTROL_OVERRIDE
        self.last_control_time = time.time()
        self.value = value

    def get_value(self):
        return self.value

    def __unicode__(self):
        return "Parameter: " + self.name
        

# --------------------------------------------------------------
#              Initializing the C/Python Bridge
# --------------------------------------------------------------

# Bring in the read only parameters which are exposed through the
# c/python bridge and loaded into the module space by ScriptEngine.cc
try:
    import pe_cpp_bridge
except:
    # If we are running the python environment in "debug mode" without
    # the C code at the same time, we have to spoof a few things,
    # including the pe_readonly_bindings module.
    class PeCppBridgeDummy:
        def pe_time(self, value): return 0.0;
    pe_cpp_bridge = PeCppBridgeDummy()


# --------------------------------------------------------------
#        The PhosphorEssence Class and 'pe' Instance
#
# In the scripting environment, the 'pe' object gives access to
# phosphoressence parameters.  Parameters can be accessed directly
# 'attributes' (e.g. 'pe.time' or 'pe.decay'), or they can be set
# using the methods defined below.  Parameters are defined at the
# bottom of this file.
# --------------------------------------------------------------

class PhosphorEssence(object):

    # --------------------- Attribute Methods ------------------------
    #
    # We jump through quite a few hoops here in order to expose the PE
    # parameters as attributes of the PhosphorEssence class instance.
    # These functions forward lookups for unknown attributes along to
    # the 'self.params' dictionary.  

    def __getattr__(self, item):
        try:
           # print 'falling back to params dict!'
            return self.__dict__['params'][item].get_value()
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        # this test allows attributes to be set in the __init__ method
        if not self.__dict__.has_key('_PhosphorEssence__initialised'):
            return dict.__setattr__(self, item, value)

        # any normal attributes are handled normally
        elif self.__dict__.has_key(item):
            dict.__setattr__(self, item, value)

        # the remaining attributes are delegated to the 'params' dictionary 
        elif  self.__dict__['params'].has_key(item): 
            self.__dict__['params'][item].set_value(value)

        else:
            raise AttributeError(item)        

    # ------------------------- Properties ---------------------------
    #
    # In a similar fashion to the attributes above, we establish a set
    # of properties for accessing read-only data from the python/c
    # bridge.  Right now this is only used to access the time object,
    # but it could easily be used to access other read-only parameters
    # as well.

    # No-Op method for setting read-only parameters
    def set_read_only(self, key, value):
        pass

    # The time parameter is special, so we bind it by hand.
    time = property(pe_cpp_bridge.pe_time, set_read_only)    

    # ------------------------- --------- ---------------------------

    def __init__(self):
        self.params = {}
        self.__initialised = True  # for __setattr__

    # Register a new paramater.  This store the parameter in a
    # dictionary, and then creates a class property for its access.
    def register(self, parameter):
        self.params[parameter.name] = parameter

    # There are two flavors for setting parameter values.  The first,
    # set_value(), is equivelent to setting the attribute value
    # directly from the script.  This form of setting the value may be
    # overridden by the set_control_value() method below.
    def set_value(self, name, value):
        self.params[name].set_value(value)

    # Set the value of a parameter using a physical controller.  This
    # method of setting parameter values always takes precedence over
    # set_value(), and may leave the parameter at this value for a
    # certain amount of time before it reverts to being controllable
    # from the scripting environment.
    def set_control_value(self, name, value):
        self.params[name].set_control_value(value)

    def reset_all(self):
        for p in self.params.values():
            p.value = p.default_value

    def has_parameter(self, name):
        return self.params.has_key(name)

    # Returns a list of paramters
    def param_list(self):
        l = self.params.keys()
        l.append("time")
        return l
    
# Create the instance of the PhosphorEssence class.  Note: don't go
# creating your own instance.  This should be the only one!!  (TODO:
# Maybe it should be a singleton class?)
pe = PhosphorEssence()



# --------------------------------------------------------------
#                   Parameter Definition
# --------------------------------------------------------------


# ---------------------
# READ-ONLY PARAMETERS
# ---------------------
#
# You should not change these, even though you technically can.
# Someday when I have more time these might get properly moved to the
# python/c bridge where thery can be locked down properly.

pe.register(Parameter( name = "initialized",
                       description = "This special parameter is set to true once the scripting engine has be activated",
                       default_value = 1.0,
                       read_only = True))
pe.register(Parameter( name = "x",
                       description = "Retrieves the x-position of the current pixel" +
                       "(for per-pixel equations)",
                       read_only = True))
pe.register(Parameter( name = "y",
                       description = "Retrieves the y-position of the current pixel" +
                       "(for per-pixel equations)",
                       read_only = True ))
pe.register(Parameter( name = "rad",
                       description = "Retrieves the radius (from center) of the current pixel" +
                       "(for per-pixel equations)",
                       read_only = True ))
pe.register(Parameter( name = "ang",
                       description = "Retrieves the angle of the current pixel" +
                       "(for per-pixel equations)",
                       read_only = True ))

pe.register(Parameter( name = "fps",
                       description = ">0 (readonly)       retrieves the current framerate, " +
                       "in frames per second.",
                       default_value = 30.0,
                       read_only = True))
pe.register(Parameter( name = "frame",
                       description = "(readonly) retrieves the number of frames of animation " +
                       "elapsed since the program started",
                       read_only = True))
pe.register(Parameter( name = "aspect",
                       description = "Aspect ratio of the screen.  The screen coordinates " +
                       "vary horizontally from [-aspect +aspect] and vertically from [-1 +1]",
                       read_only = True))
pe.register(Parameter( name = "meshx",
                       description = "(readonly)  tells you the user's mesh size in the " +
                       " X direction.",
                       read_only = True))
pe.register(Parameter( name = "meshy",
                       description = "(readonly)  tells you the user's mesh size in the " +
                       "Y direction.",
                       read_only = True))

pe.register(Parameter( name = "bass",
                       description = ">0 (readonly)       retrieves the current amount of " +
                       "bass.  1 is normal; below ~0.7 is quiet; above ~1.3 is loud bass",
                       read_only = True ))
pe.register(Parameter( name = "mid",
                       description = ">0 (readonly)         -same, but for mids (middle frequencies)",
                       read_only = True))
pe.register(Parameter( name = "treb",
                       description = ">0 (readonly)         -same, but for treble (high) frequencies",
                       read_only = True))
pe.register(Parameter( name = "bass_att",
                       description = ">0 (readonly)       retrieves an attenuated reading on the bass, " +
                             "meaning that it is damped in time and doesn't change so rapidly",
                       read_only = True))
pe.register(Parameter( name = "mid_att",
                       description = ">0 (readonly)         -same, but for mids (middle frequencies)",
                       read_only = True))
pe.register(Parameter( name = "treb_att",
                       description = ">0 (readonly)         -same, but for treble (high) frequencies",
                       read_only = True))

pe.register(Parameter( name = "bass_r",
                       description = ">0 (readonly)       retrieves the current amount of bass. " +
                       "  1 is normal; below ~0.7 is quiet; above ~1.3 is loud bass",
                       read_only = True ))
pe.register(Parameter( name = "mid_r",
                       description = ">0 (readonly)         -same, but for mids (middle frequencies)",
                       read_only = True))
pe.register(Parameter( name = "treb_r",
                       description = ">0 (readonly)         -same, but for treble (high) frequencies",
                       read_only = True))
pe.register(Parameter( name = "bass_att_r",
                       description = ">0 (readonly)       retrieves an attenuated reading on the bass, " +
                       "meaning that it is damped in time and doesn't change so rapidly",
                       read_only = True))
pe.register(Parameter( name = "mid_att_r",
                       description = ">0 (readonly)         -same, but for mids (middle frequencies)",
                       read_only = True))
pe.register(Parameter( name = "treb_att_r",
                       description = ">0 (readonly)         -same, but for treble (high) frequencies",
                       read_only = True))


# ---------------------
# READ-WRITE PARAMETERS
# ---------------------

# FEEDBACK PARAMETERS
pe.register(Parameter( name = "decay",
                       description = "0..1   controls the eventual fade to black; " + 
                       "1=no fade, 0.9=strong fade, 0.98=recommended",
                       default_value = 0.98 ))

pe.register(Parameter( name = "invert",
                       description = "0/1    inverts the colors in the image" ))

pe.register(Parameter( name = "gamma",
                       description = ">0     controls display brightness; " +
                       "1=normal, 2=double, 3=triple, etc.",
                       default_value = 1.0))

pe.register(Parameter( name = "edge_filter",
                       description = "0/1    turns on an edge filter in the frontbuffer",
                       default_value = 0.0))

# ZOOM PARAMETERS
pe.register(Parameter( name = "zoom",
                       description = "controls inward/outward motion.  " + 
                       "0.9=zoom out 10% per frame, 1.0=no zoom, 1.1=zoom in 10%",
                       default_value = 1.0 ))

pe.register(Parameter( name = "zoom_rate",
                       description = "Rate of inward/outward zoom",
                       default_value = 0.0 ))

pe.register(Parameter( name = "zoomexp",
                       description = ">0     controls the curvature of the zoom; 1=normal",
                       default_value = 1.0 ))

# WARP PARAMETERS
pe.register(Parameter( name = "warp", 
                       description = "controls the magnitude of the warping; " + 
                       "0=none, 1=normal, 2=major warping..."))

pe.register(Parameter( name = "warp_speed",
                       description = "controls the speed of the warping;",
                       default_value = 1.0 ))

pe.register(Parameter( name = "warp_scale",
                       description = "controls the size of the warp effects.",
                       default_value = 1.0 ))

pe.register(Parameter( name = "fluid_viscosity",
                       description = "controls the viscosity of the fluid dynamics effect.",
                       default_value = 0.00001 ))
pe.register(Parameter( name = "fluid_diffusion",
                       description = "controls the diffusion rate of pressure in the fluid effect.",
                       default_value = 1.0 ))



# AFFINE PARAMETERS
pe.register(Parameter( name = "rot",
                       description = "controls the amount of rotation.  " + 
                       "0=none, 0.1=slightly right, -0.1=slightly clockwise, 0.1=CCW" ))

pe.register(Parameter( name = "rot_rate",
                       description = "The rate of rotation",
                       default_value = 0.0 ))

pe.register(Parameter( name = "cx",
                       description = "0..1   controls where the center of rotation and " + 
                       "stretching is, horizontally.  0=left, 0.5=center, 1=right"))

pe.register(Parameter( name = "cy",
                       description = "0..1   controls where the center of rotation and " + 
                       "stretching is, vertically.  0=left, 0.5=center, 1=right"))

pe.register(Parameter( name = "dx",
                       description = "controls amount of constant horizontal motion; " + 
                       "-0.01 = move left 1% per frame, 0=none, 0.01 = move right 1%"))

pe.register(Parameter( name = "dy",
                       description = "controls amount of constant vertical motion; " + 
                       "-0.01 = move up 1% per frame, 0=none, 0.01 = move down 1%"))

pe.register(Parameter( name = "sx",
                       description = ">0     controls amount of constant horizontal stretching; " + 
                       " 0.99=shrink 1%, 1=normal, 1.01=stretch 1%",
                       default_value = 1.0 ))

pe.register(Parameter( name = "sy",
                       description = ">0     controls amount of constant vertical stretching; " + 
                       " 0.99=shrink 1%, 1=normal, 1.01=stretch 1%",
                       default_value = 1.0 ))


# WAVE PARAMETERS
pe.register(Parameter( name = "wave_mode",
                       description = "0,1,2,3,4,5,6,7 " +
                       "controls which of the 8 types of waveform is drawn" ))

pe.register(Parameter( name = "wave_x",
           description = "position of the waveform: " +
           "0 = far left edge of screen, 0.5 = center, 1 = far right",
           default_value = 0.5 ))

pe.register(Parameter( name = "wave_y",
           description = "position of the waveform: " +
           "0 = very bottom of screen, 0.5 = center, 1 = top",
           default_value = 0.5 ))

pe.register(Parameter( name = "wave_r",
           description = "amount of red color in the wave (0..1)",
           default_value = 0.0))

pe.register(Parameter( name = "wave_g",
           description = "amount of green color in the wave (0..1)",
           default_value = 1.0))

pe.register(Parameter( name = "wave_b",
           description = "amount of blue color in the wave (0..1)",
           default_value = 0.0))

pe.register(Parameter( name = "wave_a",
           description = "opacity of the wave [0=transparent .. 1=opaque]",
           default_value = 1.0))

pe.register(Parameter( name = "wave_mystery",
           description = "-1..1  what this parameter does is a mystery. " +
           "(honestly, though, this value does different things for each " + 
           "waveform; for example, it could control angle at which the " +
           "waveform was drawn.)",
           default_value = 0.0))

pe.register(Parameter( name = "wave_usedots",
           description = "0/1    " +
           "if 1, the waveform is drawn as dots (instead of lines)" ))

pe.register(Parameter( name = "wave_thick",
           description = "0/1   if 1, " +
           "the waveform's lines (or dots) are drawn with double thickness",
           default_value = 1.0))

pe.register(Parameter( name = "wave_additive",
           description = "if 1, the wave is drawn additively, " +
           "saturating the image at white",
           default_value = 0.0))

pe.register(Parameter( name = "wave_brighten",
           description = "0/1    if 1, all 3 r/g/b colors " +
           "will be scaled up until at least one reaches 1.0",
           default_value = 1.0))

pe.register(Parameter( name = "wave_enabled",
           description = "Enable the audio waveform rendered on screen.",
           default_value = 0.0))

pe.register(Parameter( name = "wave_frequency",
           description = "Frequency of the waveshape drawing loop.",
           default_value = 0.1))

# OUTER BORDER
pe.register(Parameter( name = "ob_size",
           description = "0..0.5 thickness of the outer border drawn " +
           "at the edges of the screen every frame", 
           default_value = 0.25))

pe.register(Parameter( name = "ob_r",
           description = "0..1   amount of red color in the outer border",
           default_value = 0.0))

pe.register(Parameter( name = "ob_g",
           description = "0..1   amount of green color in the outer border",
           default_value = 1.0))

pe.register(Parameter( name = "ob_b",
           description = "0..1   amount of blue color in the outer border",
           default_value = 0.0))

pe.register(Parameter( name = "ob_a",
           description = "0..1   opacity of the outer border " +
           "(0=transparent, 1=opaque)",
           default_value = 0.0))

# INNER BORDER
pe.register(Parameter( name = "ib_size",
           description = "0..0.5 thickness of the outer border drawn " +
           "at the edges of the screen every frame", 
           default_value = 10.0))

pe.register(Parameter( name = "ib_r",
           description = "0..1   amount of red color in the outer border",
           default_value = 0.0))

pe.register(Parameter( name = "ib_g",
           description = "0..1   amount of green color in the outer border",
           default_value = 1.0))

pe.register(Parameter( name = "ib_b",
           description = "0..1   amount of blue color in the outer border",
           default_value = 0.0))

pe.register(Parameter( name = "ib_a",
           description = "0..1   opacity of the outer border " +
           "(0=transparent, 1=opaque)",
           default_value = 0.0))


# MOTION VECTORS
pe.register(Parameter( name = "mv_r",
           description = "0..1   amount of red color in the motion vectors",
           default_value = 1.0))

pe.register(Parameter( name = "mv_g",
           description = "0..1   amount of green color in the motion vectors",
           default_value = 0.0))

pe.register(Parameter( name = "mv_b",
           description = "0..1   amount of blue color in the motion vectors",
           default_value = 0.0))

pe.register(Parameter( name = "mv_a",
           description = "0..1   opacity of the motion vectors " +
           "(0=transparent, 1=opaque)",
           default_value = 0.0))

pe.register(Parameter( name = "mv_x",
           description = "the number of motion vectors in the X direction",
           default_value = 64.0))

pe.register(Parameter( name = "mv_y",
           description = "0..48  " + 
           "the number of motion vectors in the Y direction",
           default_value = 48.0))

pe.register(Parameter( name = "mv_l",
           description = "the length of the motion vectors " + 
           "(0=no trail, 1=normal, 2=double...)",
           default_value = 1.0))

pe.register(Parameter( name = "mv_dx",
           description = "-1..1  horizontal placement offset " +
           "of the motion vectors",
           default_value = 0.0))

pe.register(Parameter( name = "mv_dy",
           description = "-1..1  vertical placement offset " +
           "of the motion vectors",
           default_value = 0.0))


# VIDEO ECHO AND SPECIAL EFFECTS

pe.register(Parameter( name = "ifs_mode",
           description = "Select IFS (fractal feedback) mode.",
           default_value = 0.0))

pe.register(Parameter( name = "echo_zoom",
           description = ">0     controls the size of the second graphics layer",
           default_value = 1.0))

pe.register(Parameter( name = "echo_alpha",
                       description = ">0     controls the opacity of the second graphics layer;" +
                       " 0=transparent (off)) 0.5=half-mix, 1=opaque",
                       default_value = 0.33))

pe.register(Parameter( name = "echo_orient",
                       description = "0,1,2,3 selects an orientation for the second graphics layer. " +
                       "  0=normal, 1=flip on x, 2=flip on y, 3=flip on both",
                       default_value = 0.0))

pe.register(Parameter( name = "darken_center",
                       description = "0/1    if 1, help keeps the image from getting too " +
                       "bright by continually dimming the center point",
                       default_value = 0.0))
 
pe.register(Parameter( name = "wrap",
                       description = "0/1    sets whether or not screen elements " +
                       "can drift off of one side and onto the other",
                       default_value = 1.0))

pe.register(Parameter( name = "brighten",
                       description = "0/1    brightens the darker parts of the image (nonlinear; square root filter)",
                       default_value = 0.0))

pe.register(Parameter( name = "darken",
                       description = "0/1    darkens the brighter parts of the image (nonlinear; squaring filter)",
                       default_value = 0.0))

pe.register(Parameter( name = "solarize",
                       description = "0/1    emphasizes mid-range colors",
                       default_value = 0.0))


# CUSTOM PARAMETERS
pe.register(Parameter( name = "q1",
           description = "Used to carry information between the per-frame code " + 
           "and per-pixel code." ))
pe.register(Parameter( name = "q2",
           description = "Used to carry information between the per-frame code " + 
           "and per-pixel code." ))
pe.register(Parameter( name = "q3",
           description = "Used to carry information between the per-frame code " + 
           "and per-pixel code." ))
pe.register(Parameter( name = "q4",
           description = "Used to carry information between the per-frame code " + 
           "and per-pixel code." ))
pe.register(Parameter( name = "q5",
           description = "Used to carry information between the per-frame code " + 
           "and per-pixel code." ))
pe.register(Parameter( name = "q6",
           description = "Used to carry information between the per-frame code " + 
           "and per-pixel code." ))
pe.register(Parameter( name = "q7",
           description = "Used to carry information between the per-frame code " + 
           "and per-pixel code." ))
pe.register(Parameter( name = "q8",
           description = "Used to carry information between the per-frame code " + 
           "and per-pixel code." ))


# SQUARE PARAMETERS
pe.register(Parameter( name = "square_r",
           description = "amount of red color in the wave (0..1)",
           default_value = 0.0))

pe.register(Parameter( name = "square_g",
           description = "amount of green color in the wave (0..1)",
           default_value = 1.0))

pe.register(Parameter( name = "square_b",
           description = "amount of blue color in the wave (0..1)",
           default_value = 0.0))

pe.register(Parameter( name = "square_a",
           description = "opacity of the wave [0=transparent .. 1=opaque]",
           default_value = 1.0))

pe.register(Parameter( name = "square_thick",
           description = "0/1   if 1, " +
           "the waveform's lines (or dots) are drawn with double thickness",
           default_value = 1.0))

pe.register(Parameter( name = "square_scale",
           description = "Change the size of the square on the screen",
           default_value = 1.0))

pe.register(Parameter( name = "square_frequency",
           description = "Frequency of the square drawing loop.",
           default_value = 0.01))

# UTILITES
pe.register(Parameter( name = "monitor",
           description = "any    set this value for debugging your preset " +
           " code; if you hit the 'N' key, the value of 'monitor' will be " +
           "posted in the upper-right corner of milkdrop.  " + 
           "for example, setting \"monitor = q3;\" would let you keep an " +
           "eye on q3's value.",
           default_value = 0.0))

pe.register(Parameter( name = "show_fps",
           description = "Toggle fps display on and off.",
           default_value = 0.0))

pe.register(Parameter( name = "kaleidoscope",
           description = "Activate the kaleidoscope effect.",
           default_value = 0.0))

pe.register(Parameter( name = "kaleidoscope_radius",
           description = "Set the radius for the kaleidoscope effect.",
           default_value = 0.15))

pe.register(Parameter( name = "kaleidoscope_x",
           description = "Set the x position for the kaleidoscope effect.",
           default_value = 0.0))

pe.register(Parameter( name = "kaleidoscope_y",
           description = "Set the y position for the kaleidoscope effect.",
           default_value = 0.0))

pe.register(Parameter( name = "wave_move",
           description = "Cause the wave shapes to move.",
           default_value = 0.0))


# Vector graphics parameters
pe.register(Parameter( name = "vg_mode",
                       description = "",
                       default_value = 0))

pe.register(Parameter( name = "vg_x",
           description = "Position of cursor in X.",
           default_value = 0.0))

pe.register(Parameter( name = "vg_y",
           description = "Position of cursor in Y.",
           default_value = 0.0))


pe.register(Parameter( name = "vg_stroke_r",
           description = "Stroke color.",
           default_value = 0.0))

pe.register(Parameter( name = "vg_stroke_g",
           description = "Stroke color.",
           default_value = 0.0))

pe.register(Parameter( name = "vg_stroke_b",
           description = "Stroke color.",
           default_value = 0.0))

pe.register(Parameter( name = "vg_stroke_a",
           description = "Stroke color.",
           default_value = 0.0))

pe.register(Parameter( name = "vg_fill_r",
           description = "Fill color.",
           default_value = 0.0))

pe.register(Parameter( name = "vg_fill_g",
           description = "Fill color.",
           default_value = 0.0))

pe.register(Parameter( name = "vg_fill_b",
           description = "Fill color.",
           default_value = 0.0))

pe.register(Parameter( name = "vg_fill_a",
           description = "Fill color.",
           default_value = 0.0))

pe.register(Parameter( name = "vg_stroke_thickness",
           description = "Thickness of stroke.",
           default_value = 0.01))

