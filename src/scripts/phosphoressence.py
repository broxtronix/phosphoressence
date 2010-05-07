# PHOSPHORESSENCE MASTER CONTROL PROGRAM
#
import math, sys

PE_RESOURCES = '/Users/mbroxton/projects/pe/src/'

# Load various python modules
from parameters import pe
from presets import PePreset
from graphics import pe_graphics
#from graphics import ergo
#from controllers.OscController import OscController
from controllers.JoystickController import JoystickController
from controllers.TuioController import TuioController

# Bring in the Hyphae-specific environment for Alchemy 2010.
from hyphae import hyphae

# Use these controls to effect whether phosphoressence behaves as a
# visualization plugin, an interactive VJ rig, or both!
ENABLE_PRESETS = 0
ENABLE_CONTROLLERS = 1

# Switches for debugging
JOY_DEBUG = 1;
#OSC_DEBUG = 1;
#TUIO_DEBUG = 1;
pe.show_fps = 1;

# Instantiate hardware controllers
#osc = OscController(OSC_DEBUG)
joystick = JoystickController(JOY_DEBUG)
#tuio = TuioController(TUIO_DEBUG,host="antiprism.local",port=3333)

# Set up Hyphae
#osc_handler = hyphae.OscHandler()
#tuio_handler = hyphae.MultitouchHandler()
hyphae = hyphae.HyphaeController()

#tuio.set_osc_handler(osc_handler)
#tuio.set_tuio_handler(tuio_handler)

# Default initialization handler
#
# This function can be used to set up the environment in the embedded
# python environment.  This is called once when the rest of
# Phosphoressence has been initialized, but the main application loop
# has not yet started.
def pe_initialize():
    pass

    # Load Milkdrop Presets & Bookmarks
    # PePreset.load_directory(PE_RESOURCES + '/presets/milkdrop')
    # PePreset.load_directory(PE_RESOURCES + '/presets/bookmarks')

# Animation callback.
#
# This method is called prior to rendering each frame.  By overriding
# or augmenting this method, programmers can animate PhosphorEssence
# parameters.
def pe_animate():
    
    if ( ENABLE_PRESETS ) :
        preset = PePreset.current_preset()
        if (preset):
            try: 
                preset.per_frame()
            except:
                print '\t ** Failed to run ' + preset.name
                for ei in sys.exc_info():
                    print '\t    ' + str(ei)

    if ( ENABLE_CONTROLLERS ):

        # Update joystick parameters
        joystick.render_callback()

        # Update osc parameters
        #        osc.render_callback()

        # Update tuio parameters
        #        tuio.render_callback()


# Default render callback
#
# This method is called by the GraphicsEngine as it renders each frame.
def pe_render():
    
    # Render Hypae Sprites
    hyphae.render_callback()
    pe_graphics.render()
#    pe.set_control_value('rot_rate',0)
#    pe.set_control_value('zoom_rate',0)

def pe_render_back():
#    pe.set_control_value('vision_threshold',0.5+0.4*math.cos(pe.time))
    pe_graphics.render_back()

def pe_render_bg():
    pe_graphics.render_bg()
