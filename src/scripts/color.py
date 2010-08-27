# color.py
#
# ColorSche generators are useful for creating pleasing, aesthetic color
# combinations to use in simulation.  They generate colors by picking
# them according to a selected color scheme:
#
# 0 - Monochomatic (variations on lightness and saturation of a single color)
# 1 - Analogous (30 deg. apart on the color wheel)
# 2 - Complementary (180 deg. apart)
# 3 - Split complementary (one root color and two colors split from complementary)
# 4 - Triadic (Three colors 120 deg. apart)
# 5 - Tetradic (Four colors, split around complements)
#
# Use the color_scheme property of the ColorGenerator to set the color
# scheme.
#
# Color generators have several properties that dictate their
# behavior, regardless of color scheme.
#
#  hue - this is the root of the color scheme (red by default).
#        Varying this value from 0.0 to 2 * pi will make one
#        full rotation around the color wheel.
#
#  period - the amount of time that elapsed during one full cycle
#           through the color scheme.
#
#  saturation - the saturation of the colors generated by the color scheme
#
#  luminance - the brighness of the colors generated by the color scheme
#
#  alpha - the alpha value (opacity) of the colors generated by the color scheme
#
# ------
#
# 

import colorsys
from parameters import pe
import math
from numpy import array

# -------------------------------------------------------------------------
#                               ColorScheme
# -------------------------------------------------------------------------

class ColorScheme(object):

    # Color scheme constants
    MONOCHROMATIC = 0
    ANALOGOUS = 1
    COMPLEMENTARY = 2
    SPLIT_COMPLEMENTARY = 3
    TRIADIC = 4
    TETRADIC = 5
        
    def __init__(self):

        # Basic properties
        self.hue = 0.0            
        self.saturation = 1.0
        self.luminance = 1.0
        self.alpha = 1.0

        # Other settings
        self.period = 2.0 # Rate of color change in radians/frame

        # The color scheme.  This can be one of the following:
        #
        # 0 - Monochomatic (variations on lightness and saturation of a single color)
        # 1 - Analogous (30 deg. apart on the color wheel)
        # 2 - Complementary (180 deg. apart)
        # 3 - Split complementary (one root color and two colors split from complementary)
        # 4 - Triadic (Three colors 120 deg. apart)
        # 5 - Tetradic (Four colors, split around complements)
        #
        # Don't set this directly.  Use the set_color_scheme method.
        self._color_scheme = 0

        # Internal variable used to store color offsets for the current scheme.
        self._color_offsets = [0.0]

        # The counter used to cycle through colors
        self._generator_color = 0

        # The RYB color wheel.
        self.ryb_colors = [ array([255, 0, 0]),   # red
                            array([255, 102, 0]), # red-orange
                            array([255, 148, 0]), # orange
                            array([254, 197, 0]), # orange-yellow
                            array([255, 255, 0]), # yellow
                            array([140, 199, 0]), # yellow-green
                            array([15, 173, 0]),  # green
                            array([0, 173, 212]), # green-blue
                            array([0, 100, 181]), # blue
                            array([0, 16, 165]),  # blue-violet
                            array([99, 0, 165]),  # violet
                            array([197, 0, 124])] # violet-red

    def update_color_offsets(self):
        self._generator_color = 0
        if (self._color_scheme == 0):       # Monochromatic
            self._color_offsets = [0.0]        
        elif (self._color_scheme == 1):     # Analogous
            self._color_offsets = [0.0, 30, 330]
        elif (self._color_scheme == 2):     # Complementary
            self._color_offsets = [0.0, 180]
        elif (self._color_scheme == 3):     # Split Complementary
            self._color_offsets = [0.0, 150, 210]
        elif (self._color_scheme == 4):     # Triadic
            self._color_offsets = [0.0, 120, 240]
        elif (self._color_scheme == 5):     # Tetradic
            self._color_offsets = [0.0, 90, 180, 270]
        else:
            raise Exception, "Could not initialize ColorScheme object.  Unkown color_scheme: " + str(self._color_scheme)

        # Normalize so that everything is scaled in between 0.0 and 1.0
        for i in range(len(self._color_offsets)):
            self._color_offsets[i] /= 360.0

    def rgba_from_hsv(self, hue):

        # Normalize the hue to the range [0.0..1.0]
        normalized_hue = hue % 1.0
        rgb = colorsys.hsv_to_rgb(normalized_hue, self.saturation, self.luminance)
        return (rgb[0], rgb[1], rgb[2], self.alpha)

    def rgba_from_ryb(self, hue):

        # Normalize the hue to the range [0.0..1.0)
        normalized_hue = hue % 1.0
        if normalized_hue == 1.0: 
            normalized_hue = 0.0;  

        hue_index1 = int(math.floor(len(self.ryb_colors) * normalized_hue))
        hue_index2 = hue_index1 + 1
        if hue_index1 == len(self.ryb_colors)-1:
            hue_index2 = 0
        alpha = (len(self.ryb_colors) * normalized_hue - hue_index1)
        rgb = (1-alpha) * self.ryb_colors[hue_index1] + alpha * self.ryb_colors[hue_index2]
        return (rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0, self.alpha)

    # Public methods

    def set_root_rgba(self, r, g, b, a):
        hsv = colorsys.rgb_to_hsv(r, g, b)
        self.hue = hsv[0]
        self.saturation = hsv[1]
        self.luminance = hsv[2]
        self.alpha = a
    
    def set_color_scheme(self, color_scheme):
        self._color_scheme = color_scheme
        self.update_color_offsets()

    # The generate() method returns the next color in the color
    # scheme.  
    def generate(self):
        current_hue = self.hue + self._color_offsets[self._generator_color]

        # Increment the generator counter, and reset it if necessary.
        self._generator_color += 1
        if (self._generator_color == len(self._color_offsets)):
            self._generator_color = 0
        return self.rgba_from_ryb(current_hue)

    def sample(self):

        # Increment the absolute position in the color cycle.
        # Renormalize if necessary.  Omega will be somewhere in
        # between [0.0 and 1.0]
        omega = pe.time / self.period % 1.0

        # Step one - figure out which color we are on within the scheme.
        color_index = int(math.floor(omega * len(self._color_offsets)))
        color_subindex = omega * len(self._color_offsets) - color_index - 0.5

        hue_shift = color_subindex / 12.0
        current_hue = self.hue + self._color_offsets[color_index] + hue_shift
        return self.rgba_from_ryb(current_hue)


