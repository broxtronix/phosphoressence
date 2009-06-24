# --------------------------------------------------------------
#                  The Parameter Object
# --------------------------------------------------------------

class Parameter(object):
    
    def __init__(self, name, description,
                 default_value = 0.0, read_only = True):

        # Store the parameters specific to this parameter in the class
        # instance.
        self.name = name
        self.description = description
        self.default_value = default_value
        self.read_only = read_only

        # Private members are set to default values
        self.control_mode = "automation";
        self.controller_timeout = 0.0;
        self.last_time = 0.0;

    def __unicode__(self):
        return "Parameter: " + self.name
        
# --------------------------------------------------------------
#                The Parameter Instance
# --------------------------------------------------------------

# Bring in the read only parameters which are exposed through the
# c/python bridge.
import pe_readonly_bindings

class PhosphorEssence(object):

    def __init__(self):
        self.params = {}

    # No-Op method for setting read-only parameters
    def setReadOnly(self, value):        
        pass

    # Read-only parameters
    time = property(pe_readonly_bindings.pe_time, setReadOnly)    

    def register(self, parameter):
        self.params[parameter.name] = parameter
        self.__dict__[parameter.name] = parameter.default_value

pe = PhosphorEssence()


# --------------------------------------------------------------
#                           Parameters
# --------------------------------------------------------------

# READ-ONLY PARAMETERS
#
# You should not change these, even though you technically can.
# Someday when I have more time these might get properly moved to the
# python/c bridge where thery can be locked down properly.
pe.register(Parameter( name = "x",
                       description = "Retrieves the x-position of the current pixel" +
                       "(for per-pixel equations)" ))
pe.register(Parameter( name = "y",
                       description = "Retrieves the y-position of the current pixel" +
                       "(for per-pixel equations)" ))
pe.register(Parameter( name = "rad",
                       description = "Retrieves the radius (from center) of the current pixel" +
                       "(for per-pixel equations)" ))
pe.register(Parameter( name = "ang",
                       description = "Retrieves the angle of the current pixel" +
                       "(for per-pixel equations)" ))

pe.register(Parameter( name = "fps",
                       description = ">0 (readonly)       retrieves the current framerate, " +
                       "in frames per second."))
pe.register(Parameter( name = "frame",
                       description = "(readonly) retrieves the number of frames of animation " +
                       "elapsed since the program started"))
pe.register(Parameter( name = "aspect",
                       description = "Aspect ratio of the screen.  The screen coordinates " +
                       "vary horizontally from [-aspect +aspect] and vertically from [-1 +1]"))
pe.register(Parameter( name = "meshx",
                       description = "(readonly)  tells you the user's mesh size in the " +
                       " X direction."))
pe.register(Parameter( name = "meshy",
                       description = "(readonly)  tells you the user's mesh size in the " +
                       "Y direction."))

pe.register(Parameter( name = "bass",
                       description = ">0 (readonly)       retrieves the current amount of " +
                       "bass.  1 is normal; below ~0.7 is quiet; above ~1.3 is loud bass" ))
pe.register(Parameter( name = "mid",
                       description = ">0 (readonly)         -same, but for mids (middle frequencies)"))
pe.register(Parameter( name = "treb",
                       description = ">0 (readonly)         -same, but for treble (high) frequencies"))
pe.register(Parameter( name = "bass_att",
                       description = ">0 (readonly)       retrieves an attenuated reading on the bass, " +
                             "meaning that it is damped in time and doesn't change so rapidly"))
pe.register(Parameter( name = "mid_att",
                       description = ">0 (readonly)         -same, but for mids (middle frequencies)"))
pe.register(Parameter( name = "treb_att",
                       description = ">0 (readonly)         -same, but for treble (high) frequencies"))

pe.register(Parameter( name = "bass_r",
                       description = ">0 (readonly)       retrieves the current amount of bass. " +
                       "  1 is normal; below ~0.7 is quiet; above ~1.3 is loud bass" ))
pe.register(Parameter( name = "mid_r",
                       description = ">0 (readonly)         -same, but for mids (middle frequencies)"))
pe.register(Parameter( name = "treb_r",
                       description = ">0 (readonly)         -same, but for treble (high) frequencies"))
pe.register(Parameter( name = "bass_att_r",
                       description = ">0 (readonly)       retrieves an attenuated reading on the bass, " +
                       "meaning that it is damped in time and doesn't change so rapidly"))
pe.register(Parameter( name = "mid_att_r",
                       description = ">0 (readonly)         -same, but for mids (middle frequencies)"))
pe.register(Parameter( name = "treb_att_r",
                       description = ">0 (readonly)         -same, but for treble (high) frequencies"))




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

# ZOOM PARAMETERS
pe.register(Parameter( name = "zoom",
                       description = "controls inward/outward motion.  " + 
                       "0.9=zoom out 10% per frame, 1.0=no zoom, 1.1=zoom in 10%",
                       default_value = 1.0 ))

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

# AFFINE PARAMETERS
pe.register(Parameter( name = "rot",
                       description = "controls the amount of rotation.  " + 
                       "0=none, 0.1=slightly right, -0.1=slightly clockwise, 0.1=CCW" ))

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
           default_value = 0.25))

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

        # pe_parameters().add_pe.register(Parameter("echo_zoom", false, 1.0,
        #                               ">0     controls the size of the second graphics layer");
        # pe_parameters().add_pe.register(Parameter("echo_alpha", false, 0.0,
        #                               ">0     controls the opacity of the second graphics layer; 0=transparent (off)) 0.5=half-mix, 1=opaque");
        # pe_parameters().add_pe.register(Parameter("echo_orient", false, 0.0,
        #                               "0,1,2,3 selects an orientation for the second graphics layer.  0=normal, 1=flip on x, 2=flip on y, 3=flip on both");
        # pe_parameters().add_pe.register(Parameter("darken_center", false, 0.0,
        #                               "0/1    if 1, help keeps the image from getting too bright by continually dimming the center point");
 
pe.register(Parameter( name = "wrap",
                       description = "0/1    sets whether or not screen elements " +
                       "can drift off of one side and onto the other",
                       default_value = 0.0))

        # pe_parameters().add_pe.register(Parameter("wrap", false, 0.0,
        #                               "0/1    sets whether or not screen elements can drift off of one side and onto the other");
        # pe_parameters().add_pe.register(Parameter("brighten", false, 0.0,
        #                               "0/1    brightens the darker parts of the image (nonlinear; square root filter)");
        # pe_parameters().add_pe.register(Parameter("darken", false, 0.0,
        #                               "0/1    darkens the brighter parts of the image (nonlinear; squaring filter)");
        # pe_parameters().add_pe.register(Parameter("solarize", false, 0.0,
        #                               "0/1    emphasizes mid-range colors");


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
