# ----------------------------------------------------
#                   OSC Controller
# ----------------------------------------------------

def osc_receive_callback(path, value):
    if (DEBUG):
	print("[OSC]    Path: " + path + "   Value: " + value)
    bindings.controller_to_parameter(osc, path, value)

def osc_render_callback(): 
    lj_ratio_a = Math.round(lj_ratio_a)
    lj_ratio_b = Math.round(lj_ratio_b)

def setup_osc(): 
    # Setup the receive callbacks for controllers
    osc.receive_callback = osc_receive_callback

    # Set up some basic control bindings
    # bindings.add(osc, "/1/fader1", "decay", 0.9, 1.1, 0.99, "log10")
    # bindings.add(osc, "/1/xy/0", "zoom", 0.5, 1.5, 1.0)
    # bindings.add(osc, "/1/xy/1", "rot", 0.785, -0.785, 0.0)
    # bindings.add(osc, "/1/fader2", "warp", 0.0, 2.0, 0.0)
    # bindings.add(osc, "/1/fader3", "wave_frequency", 0.01, 300, 100, "log10")
    # bindings.add(osc, "/1/toggle3", "wave_enabled", 0.0, 1.0, 0.0)
    # bindings.add(osc, "/1/fader4", "zoomexp", 0.25, 5.0, 1.0, "log10")  
    # bindings.add(osc, "/1/push1", "ib_size", 0, 0, 0)  
    # bindings.add(osc, "/1/push2", "ib_size", 1, 1, 0)  
    # bindings.add(osc, "/1/push3", "ib_size", 10, 10, 0)  

    # bindings.add(osc, "/2/fader1", "sx", 0.5, 1.5, 1.0)
    # bindings.add(osc, "/2/fader2", "sy", 0.5, 1.5, 1.0)
    # bindings.add(osc, "/2/fader3", "dx", -0.5, 0.5, 0.0)
    # bindings.add(osc, "/2/fader4", "dy", -0.5, 0.5, 0.0)
    # bindings.add(osc, "/2/fader5", "cx", -1.5, 1.5, 0.0)
    # bindings.add(osc, "/2/fader6", "cy", -1.5, 1.5, 0.0)
    # bindings.add(osc, "/2/toggle8", "square_a", 0.0, 1.0, 1.0)
    # bindings.add(osc, "/2/fader8", "square_frequency", 0.001, 1.0, 0.03)

    # bindings.add(osc, "/3/fader2", "warp_speed", 0.0, 1.0, 0.5)
    # #    bindings.add(osc, "/3/fader3", "warp_scale", 0.01, 1.0, 0.5)
    # bindings.add(osc, "/3/fader4", "mv_x", 0, 64.0, 64.0)
    # bindings.add(osc, "/3/fader5", "mv_y", 0, 48.0, 48.0)
    # bindings.add(osc, "/3/fader6", "mv_dx", 0.0, 0.1, 0.0)
    # bindings.add(osc, "/3/fader7", "mv_dy", 0.0, 0.1, 0.0)
    # bindings.add(osc, "/3/fader8", "mv_l", 0.01, 0.2, 0.01)

    # bindings.add(osc, "/2/fader1", "lj_A", 0, 1.0, 1.0) 
    # bindings.add(osc, "/2/fader2", "lj_B", 0, 1.0, 1.0) 
    # bindings.add(osc, "/2/fader3", "lj_omega", 0.01, 10000.0, 1.0, "log10") 
    # bindings.add(osc, "/2/fader4", "lj_ratio_a", 1.0, 10.0, "log10") 
    # bindings.add(osc, "/2/fader5", "lj_ratio_b", 1.0, 10.0, "log10") 
    # bindings.add(osc, "/2/fader6", "lj_phase", 0.9, 1.1, 1.0)     

    # bindings.add(osc, "/3/fader1", "q1", 0, 2, 1.0) # a
    # bindings.add(osc, "/3/fader2", "q2", 0, 6.28, 0.0)
    # bindings.add(osc, "/3/fader3", "q3", -2, 2, 0.0) # b
    # bindings.add(osc, "/3/fader4", "q4", 0, 6.28, 0.0)
    # bindings.add(osc, "/3/fader5", "q5", 0, 2, 0.0) # c
    # bindings.add(osc, "/3/fader6", "q6", 0, 6.28, 0.0)
    # bindings.add(osc, "/3/fader7", "q7", -2, 2, 1.0) # d
    # bindings.add(osc, "/3/fader8", "q8", 0, 6.28, 0.0)

    # pe_parameters().add_parameter("rd_width", "/3/fader1", 0.0, 50.0, 1.0)
    # pe_parameters().add_parameter("rd_D_g", "/3/fader2", 0.0, 0.5, 0.25)
    # pe_parameters().add_parameter("rd_D_b", "/3/fader3", 0.0, 0.5, 0.0625)
    # pe_parameters().add_parameter("rd_s", "/3/fader4", 0.0, 0.05, 0.03125)
    # pe_parameters().add_parameter("rd_beta", "/3/fader5", 0.0, 24.0, 12)
    # pe_parameters().add_parameter("rd_blur", "/3/fader8", 0.0, 4.0, 0.0)


# ----------------------------------------------------
#                Joystick Controller
# ----------------------------------------------------

def joystick_receive_callback(path, value): 

    # -------------------------------------
    # Fixed settings for the langton bEATS!
    # -------------------------------------
    
    # RESET!!
    if (path == "/joystick0/button3" and value == 1): 
	print("Resetting to defaults!!\n>> ")
	p.reset_all()
	mv_a = 1.0
	mv_x = 0
	mv_y = 0
	mv_l = 0
	rot = -0.001
	sx=0.999
	wave_mode=0
    	wave_enabled = 1
    

    # IFS Mode
    if (path == "/joystick0/button0" and value == 1): 
	ifs_mode = ifs_mode + 1
        if (ifs_mode > 4):
	    ifs_mode = 0
    


    if (path == "/joystick0/button6" and value == 1): 
	ifs_mode = ifs_mode - 1
        if (ifs_mode < 0):
	    ifs_mode = 4
    

    # Squareshape Enable
    if (path == "/joystick0/button1" and value == 1): 
	if (square_a): square_a = 0.0
        else: square_a = 1.0	
    

    # Border Enable
    if (path == "/joystick0/button2" and value == 1): 
	if (ib_a): ib_a = 0.0
        else: ib_a = 1.0	
    
    # Invert
    if (path == "/joystick0/button4" and value == 1): 
	if (invert): invert = 0.0
        else: invert = 1.0
    

    # Translation
    if (path == "/joystick0/hat0" and value == 2): 
	square_thick_coeff = 1.0
    #	wave_frequency_coeff = 1.0
    if (path == "/joystick0/hat0" and value == 8): 
	square_thick_coeff = -1.0
    #	wave_frequency_coeff = -1.0
    if (path == "/joystick0/hat0" and value == 1): 
    	square_scale_coeff = 1.0
    if (path == "/joystick0/hat0" and value == 4): 
    	square_scale_coeff = -1.0
    if (path == "/joystick0/hat0" and value == 0.0): 
    	square_thick_coeff = 0.0
	square_scale_coeff = 0.0
	wave_frequency_coeff = 0.0
    

    # Gamma
    if (path == "/joystick0/button7" and value == 1): 
	if (gamma == 1.0): gamma = 1.5
	else: gamma = 1.0
    

    # Rotation
    rot_gain = 0.01
    if (path == "/joystick0/axis0"): 
	delta = -(value-0.5) * rot_gain
	if (Math.abs(value-0.5) > 0.05): 
	    rot += -delta
	    # if (rot > 0.785): rot = 0.785   # Turn off rotation 
	    # if (rot < -0.785): rot = -0.785 # limits for now.
	
    

    # Zoom
    zoom_gain = 0.002
    if (path == "/joystick0/axis1"): 
	delta = (value-0.5) * zoom_gain
	if (Math.abs(value-0.5) > 0.05): 
	    zoom += -delta
	    if (zoom > 1.16): zoom = 1.16
	    if (zoom < 0.5): zoom = 0.5
	
    

    # Zoomexp
    if (path == "/joystick0/axis3"): 
	delta = (value-0.5)/20.0
        if (Math.abs(value-0.5) > 0.05):
	    zoomexp -= delta
	if (zoomexp < 0.25): zoomexp = 0.25 
	if (zoomexp > 2.0): zoomexp = 2.0
    

    # Scaling
    if (path == "/joystick0/button21" and value == 1.0): 
	sx_coefficient = 1.0
    if (path == "/joystick0/button21" and value == 0.0): 
	sx_coefficient = 0.0
    if (path == "/joystick0/button19" and value == 1.0): 
	sx_coefficient = -1.0
    if (path == "/joystick0/button19" and value == 0.0): 
	sx_coefficient = 0.0

    if (path == "/joystick0/button20" and value == 1.0): 
	sy_coefficient = 1.0
    if (path == "/joystick0/button20" and value == 0.0): 
	sy_coefficient = 0.0
    if (path == "/joystick0/button18" and value == 1.0): 
	sy_coefficient = -1.0
    if (path == "/joystick0/button18" and value == 0.0): 
	sy_coefficient = 0.0

    # Center of rotation
    if (path == "/joystick0/button23" and value == 1.0): 
    	dx_coefficient = -1.0
    if (path == "/joystick0/button23" and value == 0.0): 
    	dx_coefficient = 0.0
    if (path == "/joystick0/button25" and value == 1.0): 
	dx_coefficient = 1.0
    if (path == "/joystick0/button25" and value == 0.0): 
	dx_coefficient = 0.0

    if (path == "/joystick0/button22" and value == 1.0): 
	dy_coefficient = -1.0
    if (path == "/joystick0/button22" and value == 0.0): 
	dy_coefficient = 0.0
    if (path == "/joystick0/button24" and value == 1.0): 
	dy_coefficient = 1.0
    if (path == "/joystick0/button24" and value == 0.0): 
	dy_coefficient = 0.0

    # Motion Vectors
    if (path == "/joystick0/button15" and value == 1.0): 
	if (mv_x == 0 or mv_y == 0): 
	    mv_x = 2
	    mv_y = 2
        elif (mv_x < 64 and mv_y < 64): 
	    mv_x *= 2
	    mv_y *= 2
	
    if (path == "/joystick0/button17" and value == 1.0): 
	if (mv_x == 2 or mv_y == 2): 
	    mv_x = 0
	    mv_y = 0
        else: 
	    mv_x /= 2
	    mv_y /= 2
	
    
    if (path == "/joystick0/button14" and value == 1.0): 
	mv_l_coeff = 1.0
    if (path == "/joystick0/button14" and value == 0.0): 
	mv_l_coeff = 0.0
    if (path == "/joystick0/button16" and value == 1.0): 
	mv_l_coeff = -1.0
    if (path == "/joystick0/button16" and value == 0.0): 
	mv_l_coeff = 0.0

    # Reset center of rotation, scaling, and zoom exponent
    if (path == "/joystick0/button5" and value == 1.0): 
	sx= 1.0
	sy= 1.0
	dx = 0.0
	dy = 0.0
    	wave_enabled = 1
	wave_mode = 0
	square_a = 1.0
	ib_a = 0.0
	zoomexp = 1.0
    

    # Warp
    if (path == "/joystick0/button0" and value == 1.0):
	warp_coefficient = 1.0
    if (path == "/joystick0/button0" and value == 0.0):
	warp_coefficient = 0.0
    if (path == "/joystick0/button6" and value == 1.0):
	warp_coefficient = -1.0
    if (path == "/joystick0/button6" and value == 0.0): 
	warp_coefficient = 0.0


    # Wave mode
    if (path == "/joystick0/button8" and value == 1): 
    	wave_mode = 0
    	wave_enabled = 1
    elif (path == "/joystick0/button9" and value == 1): 
    	wave_mode = 1
    	wave_enabled = 1
    elif (path == "/joystick0/button10" and value == 1): 
    	wave_mode = 2
    	wave_enabled = 1
    

    # PRECIOUS UPPER SWITCH 
    if (path == "/joystick0/button11" and value == 1): 
	wave_frequency = 0.03
	wave_mode=2
    elif (path == "/joystick0/button12" and value == 1): 
	wave_frequency = 0.5
	wave_mode=2
    elif (path == "/joystick0/button13" and value == 1): 
	wave_frequency = 10.0
	wave_mode=2
    

    # Debugging
    if (JOY_DEBUG and (path.search("axis") == -1)):
	print("[JOYSTICK]    Path: " + path + "   Value: " + value)

    # Otherwise, delegate to the bindings.
#    bindings.controller_to_parameter(joystick, path, value)


def setup_joystick(): 
    # Setup the receive callbacks for controllers
    joystick.receive_callback = joystick_receive_callback

    # Langton bEATS
#    bindings.add(joystick, "/joystick0/axis2", "decay", 0.75, 1.05, 0.98)
#    bindings.add(joystick, "/joystick0/axis4", "warp", 4.0, 0.0, 0.0)
#    bindings.add(joystick, "/joystick0/axis5", "warp_scale", 0.25, 2.0)

    sx_coefficient = 0.0
    sy_coefficient = 0.0
    cx_coefficient = 0.0
    cy_coefficient = 0.0
    warp_coefficient = 0.0
    gamma_coefficient = 0.0
    dx_coefficient = 0.0
    dy_coefficient = 0.0
    sqfreq_coefficient = 0.0
    wave_frequency_coeff = 0.0
    mv_l_coeff = 0.0

    square_scale_coeff = 0.0
    square_thick_coeff = 0.0

    wave_enabled = 1
    wave_mode = 0
    square_a = 1.0
    ib_size=10.0
    ib_a = 0.0

    mv_a = 1.0
    mv_x = 0
    mv_y = 0
    mv_l = 0
    rot = -0.001
    sx=0.999


def joystick_render_callback():

    # Update scaling
    scaling_stepsize = 0.0005
    sx += scaling_stepsize * sx_coefficient
    sy += scaling_stepsize * sy_coefficient
    if (sx > 1.5): sx = 1.5
    if (sx < 0.5): sx = 0.5
    if (sy > 1.5): sy = 1.5
    if (sy < 0.5): sy = 0.5

    # Update center of rotation
    crot_stepsize = 1/100.0
    cx += crot_stepsize * cx_coefficient
    cy += crot_stepsize * cy_coefficient
    if (cx > 1.5): cx = 1.5
    if (cx < -1.5): cx = -1.5
    if (cy > 1.5): cy = 1.5
    if (cy < -1.5): cy = -1.5

    # Update warp
    # warp_stepsize = 1/30.0
    # warp += warp_stepsize * warp_coefficient
    # if (warp > 2.0): warp = 2.0
    # if (warp < 0.0): warp = 0.0

    # Update Square Scale
    square_scale_stepsize = 0.05
    square_scale += square_scale_stepsize * square_scale_coeff
    if (square_scale > 4.0): square_scale = 4.0
    if (square_scale < 0.25): square_scale = 0.25

    # Update Square Thickness
    square_thick_stepsize = 1.2
    if (square_thick_coeff == 1.0):
	square_thick *= square_thick_stepsize
    if (square_thick_coeff == -1.0):
	square_thick /= square_thick_stepsize
    if (square_thick > 500.0): square_thick = 500.0
    if (square_thick < 1.0): square_thick = 1.0

    # Update gamma
    # gamma_stepsize = 1/100.0
    # gamma += gamma_stepsize * gamma_coefficient
    # if (gamma > 1.5): gamma = 1.5
    # if (gamma < 0.9): gamma = 0.9

    # Update dx & dy
    dx_stepsize = 0.01
    if (dx_coefficient > 0):
	dx += dx_stepsize
    elif (dx_coefficient < 0):
	dx -= dx_stepsize
    if (dx > 0.5): dx = 0.5
    if (dx < -0.5): dx = -0.5

    dy_stepsize = 0.01
    if (dy_coefficient > 0):
	dy += dy_stepsize
    elif (dy_coefficient < 0):
	dy -= dy_stepsize
    if (dy > 0.5): dy = 0.5
    if (dy < -0.5): dy = -0.5


    # Update wave_frequency
    # wave_frequency_stepsize = 1.1
    # if (wave_frequency_coeff > 0)
    #     wave_frequency *= wave_frequency_stepsize
    # elif (wave_frequency_coeff < 0)
    #     wave_frequency /= wave_frequency_stepsize
    # if (wave_frequency > 10.0) wave_frequency = 10.0
    # if (wave_frequency < 0.03) wave_frequency = 0.03

    # Update MV length
    mv_l_stepsize = 1/20.0
    mv_l += mv_l_stepsize * mv_l_coeff
    if (mv_l > 1.5): mv_l = 1.5
    if (mv_l < 0.0): mv_l = 0.0
