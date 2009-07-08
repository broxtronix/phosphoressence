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
ENABLE_PRESETS = 0
ENABLE_CONTROLLERS = 1

# Switches for debugging
DEBUG = 0;
JOY_DEBUG = 1;
pe.show_fps = 0;

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
    pass

    # Load Milkdrop Presets & Bookmarks
    # pe_presets.load_directory(PE_RESOURCES + '/presets/milkdrop')
    # pe_presets.load_directory(PE_RESOURCES + '/presets/bookmarks')


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

        if pe.wave_move:
            # Cause elements to move
            pe.wave_x = 0.5;
            pe.wave_y = 0.5;
            pe.set_control_value('wave_x', pe.wave_x + 0.02*( 0.60*math.sin(2.121*pe.time) + 0.40*math.sin(1.621*pe.time) ))
            pe.set_control_value('wave_y', pe.wave_y + 0.02*( 0.60*math.sin(1.742*pe.time) + 0.40*math.sin(2.322*pe.time) ))


        # wave_x = wave_x + 0.200*( 0.60*sin(1.321*time) + 0.40*sin(1.621*time) );
        # wave_y = wave_y + 0.200*( 0.60*sin(1.742*time) + 0.40*sin(1.422*time) );

        # wave_x = wave_x + 0.200*( 0.60*sin(0.394*time) + 0.40*sin(0.475*time) );
        # wave_y = wave_y + 0.200*( 0.60*sin(0.442*time) + 0.40*sin(0.321*time) );

        # wave_x = wave_x + 0.0200*( 0.60*sin(0.821*time) + 0.40*sin(0.621*time) );
        # wave_y=0.5

        # wave_x = 0.5 + 0.3*sin(time*0.177);
        # wave_y=0.47
