
# PhosphorEssence parameters
from parameters import pe

# Import various sprites
from shapes.border import BorderSprite
from shapes.polygon import PolygonSprite
from shapes.bezier import BezierSprite
from shapes.polybouncer import PolyBouncerSprite
from shapes.random_walk import RandomWalkSprite
from shapes.aimless_bit import AimlessBitSprite
# from shapes.wheelsprite import *
# from shapes.earthquakesprite import *
# from shapes.vu_spirals import *
# from shapes.vectorbrush import *

# ---------------------------------------------------------------------------
#                               PeGraphics
# ---------------------------------------------------------------------------

class PeGraphics(object):

    def __init__(self):
        self.sprites = []
        self.vg_sprites = []

    def register(self, sprite, always_render = True):
        if always_render:
            self.sprites.append(sprite)
        else:
            self.vg_sprites.append(sprite)

    # Render in front of the feedback buffer
    def render(self):
        for sprite in self.sprites:
            if hasattr(sprite, "render"):
                sprite.render()

        if (pe.vg_mode >= 0 and pe.vg_mode < len(self.vg_sprites)):
            vg_sprite = self.vg_sprites[pe.vg_mode]
            if hasattr(vg_sprite, "render"):
                vg_sprite.render()

    # Render behind the feedback buffer
    def render_back(self):
        for sprite in self.sprites:
            if hasattr(sprite, "render_back"):
                sprite.render_back()

        if (pe.vg_mode >= 0 and pe.vg_mode < len(self.vg_sprites)):
            vg_sprite = self.vg_sprites[pe.vg_mode]
            if hasattr(vg_sprite, "render_back"):
                vg_sprite.render_back()

    # Render in the background, and not into the feedback buffer at all
    def render_bg(self):
        for sprite in self.sprites:
            if hasattr(sprite, "render_bg"):
                sprite.render_bg()

        if (pe.vg_mode >= 0 and pe.vg_mode < len(self.vg_sprites)):
            vg_sprite = self.vg_sprites[pe.vg_mode]
            if hasattr(vg_sprite, "render_bg"):
                vg_sprite.render_bg()

    # Render in the background, and not into the feedback buffer at all
    def render_fg(self):

        for sprite in self.sprites:
            if hasattr(sprite, "render_fg"):
                sprite.render_fg()
                
        if (pe.vg_mode >= 0 and pe.vg_mode < len(self.vg_sprites)):
            vg_sprite = self.vg_sprites[pe.vg_mode]
            if hasattr(vg_sprite, "render_fg"):
                vg_sprite.render_fg()

# ---------------------------------------------------------------------------
#                    Instantiation and Initialization
# ---------------------------------------------------------------------------

# Instantiate the graphics object
pe_graphics = PeGraphics()

# The always-on sprites
pe_graphics.register(BorderSprite())

# The render-one-at-a-time sprites
pe_graphics.register(PolygonSprite(), False)
pe_graphics.register(BezierSprite(), False)
pe_graphics.register(PolyBouncerSprite(5), False)
pe_graphics.register(AimlessBitSprite(), True)
#pe_graphics.register(RandomWalkSprite(), False)
#pe_graphics.register(EarthquakeSprite())
#pe_graphics.register(VectorBrush())
#pe_graphics.register(VuSpiralSprite(1))
