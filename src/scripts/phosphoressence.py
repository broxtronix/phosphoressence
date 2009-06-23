# Load various python modules
from parameters import *
import math

# PhosphorEssence Python Initialization
#
# This function is called when the virtual machine is created.  It
# loads the basic set of PhosphorEssence javascript scripts.
def pe_load():

#    load(PE_RESOURCES + "/scripts/Utilities.js");
#    load(PE_RESOURCES + "/scripts/Parameters.js");
#    load(PE_RESOURCES + "/scripts/PresetFunctions.js");
#    load(PE_RESOURCES + "/scripts/Controllers.js");
#    load(PE_RESOURCES + "/scripts/Bindings.js");

    # Set up bindings object
#    bindings = new Bindings();

    # Turn automatic preset loading on/off
    run_preset = 0;

    # Switches for debugging
    debug = 0;
    joy_debug = 0;
    show_fps = 1;

# Default initialization handler
#
# This function can be used to set up the environment in the JS
# virtual machine.  This is called once when the ScriptEngine is
# initialized.
def pe_initialize():
    pass
    # setup_osc();
#    setup_joystick();

    # Load Milkdrop Presets
    # load(PE_RESOURCES + "/presets/milkdrop/milk_presets.js");

# Default render callback
#
# This method is called by the GraphicsEngine just prior to rendering
# each frame.  By overriding or augmenting this method, programmers
# can animate PhosphorEssence parameters.
def pe_render():
    pass
    #    zoom2 = 2;
    #    print(zoom2.description);
    # cxz.foo = 10;
    # cxz.name = "test";

#     t0 = time;
#     i = 0;
#     while (i < 1000) {
#     	cxz = 220+i;
#     	i += 1;
#     }
#     t1 = time;
#     print("Javascript elapsed: " + ((t1-t0)*1000.0) + " usecs/call");
    

#      if ( run_preset ) {

#     	# Milkdrop preset mode
#     	if ( preset = current_preset() )
#     	    preset();
	
#      } else {
	 
# 	 # Update joystick parameters
# 	 joystick_render_callback();
	 
# 	 # Update osc parameters
# 	 #	 osc_render_callback();
	 
# 	 # Cycle through OB colors
# 	 ib_r = 0.5;
# 	 ib_g = 0.5;
# 	 ib_b = 0.5;
# 	 ib_r += 0.35 * Math.sin(7/10.0*time);
# 	 ib_g += 0.35 * Math.sin(11/10.0*time);
# 	 ib_b += 0.35 * Math.sin(13/10.0*time);
	
# 	 # Cycle through Wave colors
# 	 wave_brighten = 1.0;
# 	 wave_r=0.65;
# 	 wave_g=0.65;
# 	 wave_b=0.65;
# 	 wave_r = wave_r + 0.350*( 0.60*Math.sin(0.742*time) + 
# 				   0.40*Math.sin(1.021*time) );
# 	 wave_g = wave_g + 0.350*( 0.60*Math.sin(0.703*time) + 
# 				   0.40*Math.sin(0.969*time) );
# 	 wave_b = wave_b + 0.350*( 0.60*Math.sin(1.090*time) + 
# 				   0.40*Math.sin(0.963*time) );
	 
# 	 # Cycle through waveshape colors
# 	 square_r=0.65;
# 	 square_g=0.65;
# 	 square_b=0.65;
# 	 square_r += 0.35 * Math.sin(17/10.0*time);
# 	 square_g += 0.35 * Math.sin(13/10.0*time);
# 	 square_b += 0.35 * Math.sin(12/10.0*time);
	 
# 	 # Cycle through motion vecton colors
# 	 mv_r=0.65;
# 	 mv_g=0.65;
# 	 mv_b=0.65;
# 	 mv_r += 0.5 * Math.sin(15/10.0*time);
# 	 mv_g += 0.5 * Math.sin(19/10.0*time);
# 	 mv_b += 0.5 * Math.sin(14/10.0*time);
#      }
# }
