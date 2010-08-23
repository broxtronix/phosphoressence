import colorsys
from parameters import pe
import math

# Omega here is a value between 0.0 and 1.0.  It represents the
# current "absolute" position in a color cycle using an arbitrary set
# of normalized units.  The color schemes remap this absolute position
# in various ways.

def generate_monochromatic_color(omega, phase):
    return phase

def generate_analogous_color(omega, phase):
#    spread = 30.0 * math.pi / 180.0
#    if (omega > 0.0 and omega < 0.333):
#        return phase - spread
#    elif (omega >= 0.333 and omega < 0.666):
#        return phase
#    else:
#        return phase + spread
    hue_spread = 30.0 * math.pi / 180.0;  # +/- 30 degree range for analogous colors
    return 2*(omega-0.5) * hue_spread + phase

def generate_split_complementary_color(omega, phase):
    spread = 30.0 * math.pi / 180.0
    if (omega > 0.0 and omega < 0.333):
        return phase - spread
    elif (omega >= 0.333 and omega < 0.666):
        return phase
    else:
        return phase + spread
#    hue_spread = 30.0 * math.pi / 180.0;  # +/- 30 degree range for analogous colors
#    return 2*(omega-0.5) * hue_spread + phase

class ColorGenerator(object):

    def __init__(self):

        # This keeps track of the current color.
        self.saturation = 1.0     # 0.0 to 1.0
        self.luminance = 1.0      # 0.0 to 1.0
        self.alpha = 1.0          # 0.0 to 1.0

        # The color scheme.  This can be one of the following:
        #
        # 0 - Monochomatic (variations on lightness and saturation of a single color)
        # 1 - Analogous (30 deg. apart on the color wheel)
        # 2 - Complementary (180 deg. apart)
        # 3 - Split complementary (one root color and two colors split from complementary)
        # 4 - Triadic (Three colors 120 deg. apart)
        # 5 - Tetradic (Four colors, split around complements)
        self.color_scheme = 1

        # Other settings
        self.omega  = 0.0 # 
        self.phase  = 0.0 # Phage of color change in radians
        self.period = 2.0 # Rate of color change in radians/frame

    
    def generate(self):
        """Returns an RGBA color tuple that is next in the generation
        order for the color scheme."""

        self.phase = pe.q8

        # Increment the absolute position in the color cycle.  Renormalize if necessary.
        self.omega = pe.time / self.period % 1.0

        # Apply the color scheme
        colorscheme_hue = 0.0
        if (self.color_scheme == 0):
            colorscheme_hue = generate_monochromatic_color(self.omega, self.phase)
        elif (self.color_scheme == 1):
            colorscheme_hue = generate_analogous_color(self.omega, self.phase)
        elif (self.color_scheme == 2):
            colorscheme_hue = generate_split_complementary_color(self.omega, self.phase)
        else:
            print "Warning -- unkown color scheme identifier: " + self.colorscheme

        # Normalize the hue to the range [0..2*pi] and rescale to the range [0.0..1.0]
        colorscheme_hue = colorscheme_hue % (2 * math.pi) / (2 * math.pi)
#        print str(colorscheme_hue) + " " + str(self.saturation) + " " + str(self.luminance)
        rgb = colorsys.hsv_to_rgb(colorscheme_hue, self.saturation, self.luminance)
#        if (pe.time % 3.0 < 0.03):
#            print self.phase, "  --  ", colorscheme_hue, " ", self.saturation, " ", self.luminance, "  :  ", rgb

        return (rgb[0], rgb[1], rgb[2], self.alpha)
    

    
