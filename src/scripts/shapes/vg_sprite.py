from color import ColorScheme
from parameters import pe

# OpenGL and OpenVG
import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenVG import VG
from OpenVG import VGU
from OpenVG.constants import *

# Python
import colorsys

# ---------------------------------------------------------------------------
#                               OpenVgSprite
#
# This is the parent class for all OpenVG-based sprites.  It creates a
# standard OpenVG canvas in the current OpenGL context and prepares it
# for rendering.
# ---------------------------------------------------------------------------

class OpenVgSprite(object):
    def __init__(self):
        VG.create_context((2048,2048))
        self.colorscheme = ColorScheme()
        self.colorscheme.set_color_scheme(5)

    # Children call this method to set up the OpenVG canvas.  This is
    # an odd bit of scaling gymnastics, but it seems to result in a
    # canvas that behaves normally with the appropriate scaling for
    # line width, etc.
    def setup_canvas(self):
        smack = 1/2048.0
        glLoadIdentity()
        glScale(smack,smack,1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        VG.set(VG_MATRIX_MODE, VG_MATRIX_PATH_USER_TO_SURFACE)
        VG.load_identity()
        VG.scale(1.0/smack, 1.0/smack)

        # Set up nice corner join angles
        VG.set(VG_STROKE_JOIN_STYLE, VG_JOIN_ROUND)

        # Compute root hue
        self.colorscheme.set_root_rgba(pe.vg_stroke_r,
                                       pe.vg_stroke_g,
                                       pe.vg_stroke_b,
                                       pe.vg_stroke_a)
        colorscheme_rgba = self.colorscheme.sample()

        # Set up stroke and fill color properties (these can be
        # overridden by sub-classes, of course...)
        VG.set(VG_STROKE_LINE_WIDTH, pe.vg_stroke_width)      # Stroke width
        stroke_paint = VG.ColorPaint((colorscheme_rgba[0],
                                      colorscheme_rgba[1],
                                      colorscheme_rgba[2],
                                      colorscheme_rgba[3]))    # Stroke color
        VG.set_paint(stroke_paint, VG_STROKE_PATH)

        fill_paint = VG.ColorPaint((pe.vg_fill_r,
                                    pe.vg_fill_g,
                                    pe.vg_fill_b,
                                    pe.vg_fill_a))        # Fill color
        VG.set_paint(fill_paint, VG_FILL_PATH)

        # Affine transformations for the model view matrix
        VG.translate(pe.vg_x, pe.vg_y)                    # Translation
        VG.rotate(pe.vg_rot * 360)                        # Rotation
        VG.shear(pe.vg_shear_x, pe.vg_shear_y)            # Shearing
