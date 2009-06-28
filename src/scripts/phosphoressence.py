# PHOSPHORESSENCE MASTER CONTROL PROGRAM
#
import math, sys
PE_RESOURCES = '/Users/mbroxton/projects/pe/src/'

# Load various python modules
from parameters import pe
from presets import pe_presets
from controllers import OscController, JoystickController
from bindings import Binding

# Use these controls to effect whether phosphoressence behaves as a
# visualization plugin, an interactive VJ rig, or both!
ENABLE_PRESETS = 1
ENABLE_CONTROLLERS = 1

# Switches for debugging
DEBUG = 0;
JOY_DEBUG = 1;
pe.show_fps = 1;

# Instantiate hardware controllers
osc = OscController()
joystick = JoystickController(JOY_DEBUG)

# Default initialization handler
#
# This function can be used to set up the environment in the embedded
# python environment.  This is called once when the rest of
# Phosphoressence has been initialized, but the main application loop
# has not yet started.
def pe_initialize():
    # Load Milkdrop Presets & Bookmarks
    pe_presets.load_directory(PE_RESOURCES + '/presets/milkdrop')
    #pe_presets.load_directory(PE_RESOURCES + '/presets/bookmarks')


# Default render callback
#
# This method is called by the GraphicsEngine just prior to rendering
# each frame.  By overriding or augmenting this method, programmers
# can animate PhosphorEssence parameters.
def pe_render():

    if ( ENABLE_PRESETS ) :
        preset = pe_presets.current_preset()
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
        #	 osc.render_callback()

        # Cycle through OB colors
        pe.ib_r = 0.5
        pe.ib_g = 0.5
        pe.ib_b = 0.5
        pe.ib_r += 0.35 * math.sin(7/10.0*pe.time)
        pe.ib_g += 0.35 * math.sin(11/10.0*pe.time)
        pe.ib_b += 0.35 * math.sin(13/10.0*pe.time)
	
        # Cycle through Wave colors
        pe.wave_brighten = 1.0
        pe.wave_r=0.65
        pe.wave_g=0.65
        pe.wave_b=0.65
        pe.wave_r = pe.wave_r + 0.350*( 0.60*math.sin(0.742*pe.time) + 
                                        0.40*math.sin(1.021*pe.time) )
        pe.wave_g = pe.wave_g + 0.350*( 0.60*math.sin(0.703*pe.time) + 
                                        0.40*math.sin(0.969*pe.time) )
        pe.wave_b = pe.wave_b + 0.350*( 0.60*math.sin(1.090*pe.time) + 
                                        0.40*math.sin(0.963*pe.time) )

        # Cycle through waveshape colors
        pe.square_r=0.65
        pe.square_g=0.65
        pe.square_b=0.65
        pe.square_r += 0.35 * math.sin(17/10.0*pe.time)
        pe.square_g += 0.35 * math.sin(13/10.0*pe.time)
        pe.square_b += 0.35 * math.sin(12/10.0*pe.time)

        # Cycle through motion vecton colors
        pe.mv_r=0.65
        pe.mv_g=0.65
        pe.mv_b=0.65
        pe.mv_r += 0.5 * math.sin(15/10.0*pe.time)
        pe.mv_g += 0.5 * math.sin(19/10.0*pe.time)
        pe.mv_b += 0.5 * math.sin(14/10.0*pe.time)

