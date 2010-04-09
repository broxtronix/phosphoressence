# PHOSPHORESSENCE MASTER CONTROL PROGRAM
#
import math, sys

PE_RESOURCES = '/Users/mbroxton/projects/pe/src/'

# Load various python modules
from parameters import pe
from presets import PePreset
from graphics import pe_graphics
#from graphics import ergo
from controllers import OscController, JoystickController
#from controllers import TuioController
#from shapes.videoshape import VideoShapes


# Use these controls to effect whether phosphoressence behaves as a
# visualization plugin, an interactive VJ rig, or both!
ENABLE_PRESETS = 0
ENABLE_CONTROLLERS = 1

# Switches for debugging
JOY_DEBUG = 1;
OSC_DEBUG = 0;
TUIO_DEBUG = 0;
pe.show_fps = 0;

# Instantiate hardware controllers
osc = OscController(OSC_DEBUG)
joystick = JoystickController(JOY_DEBUG)
#tuio = TuioController(TUIO_DEBUG,host="169.254.81.125",port=3333)
#tuio = TuioController(TUIO_DEBUG,host="169.254.81.125",port=3333)
#tuio.set_finger_callback(ergo.got_finger)

# Create a video shape
#vshape = VideoShapes()

# Default initialization handler
#
# This function can be used to set up the environment in the embedded
# python environment.  This is called once when the rest of
# Phosphoressence has been initialized, but the main application loop
# has not yet started.
def pe_initialize():
    pass
#    pe_graphics.register(vshape)
#    osc.register_shape(vshape)

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
        osc.render_callback()

        # Update tuio parameters
        #tuio.render_callback()

        # Cycle through IB colors
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
            pe.kaleidoscope_x = (0.14*math.cos(1.421*pe.time*0.1) +
                                 0.27*math.cos(1.421*pe.time*0.1))
            pe.kaleidoscope_y = (0.27*math.cos(1.222*pe.time*0.1) +
                                 0.15*math.cos(2.2322*pe.time*0.1))
        else:
            pe.kaleidoscope_x = 0
            pe.kaleidoscope_y = 0

        # wave_x = wave_x + 0.200*( 0.60*sin(1.321*time) + 0.40*sin(1.621*time) );
        # wave_y = wave_y + 0.200*( 0.60*sin(1.742*time) + 0.40*sin(1.422*time) );

        # wave_x = wave_x + 0.200*( 0.60*sin(0.394*time) + 0.40*sin(0.475*time) );
        # wave_y = wave_y + 0.200*( 0.60*sin(0.442*time) + 0.40*sin(0.321*time) );

        # wave_x = wave_x + 0.0200*( 0.60*sin(0.821*time) + 0.40*sin(0.621*time) );
        # wave_y=0.5

        # wave_x = 0.5 + 0.3*sin(time*0.177);
        # wave_y=0.47


# Default render callback
#
# This method is called by the GraphicsEngine as it renders each frame.
def pe_render():
    pe_graphics.render()
    pe.set_control_value('rot_rate',0)
    pe.set_control_value('zoom_rate',0)

def pe_render_back():
    pe_graphics.render_back()

def pe_render_bg():
    pe_graphics.render_bg()
