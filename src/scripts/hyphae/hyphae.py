from parameters import pe
import math, time
from mycelium import Mycelium

class HyphaeController(object):

    def __init__(self):
#        pe.decay=0.99999999
#        pe.warp=0.001
#        pe.q7 = 0.5
#        pe.q8 = 0.5

        self.mycelium = Mycelium()
        self.mycelium.spawn(0,250)
        self.mycelium.spawn(180,0)
        self.mycelium.spawn(199,32)
        self.mycelium.spawn(-132,323)
        self.mycelium.spawn(-233,-22)

    def render_callback(self):

#        self.mycelium.render()

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

class MultitouchHandler(object):

    def finger_callback(self, event_type, location):
        if event_type == "fingerdown":
            self.got_fingerdown(f)
        elif event_type == "fingerdrag":
            self.got_fingerdrag(f)
        elif event_type == "fingerup":
            self.got_fingerup(f)
        else:
            print "Unknown event type: ", event_type

    def got_fingerdown(self,f):
        print "Finger down: ", f.sid

    def got_fingerdrag(self,f):
        print "Finger drag: ", f.sid

    def got_fingerup(self,f):
        print "Finger up: ", f.sid

    def render_callback(self):
        pass

class OscHandler(object):

    def osc_callback(self, source, msg):
        print "OSC message: ",msg
	f = msg[2]

	if msg[0] == "/msaremote/fader/11":
	    pe.set_control_value('rot',f)
	elif msg[0] == "/msaremote/fader/12":
	    pe.set_control_value("decay",f*2.0)
	elif msg[0] == "/msaremote/fader/13":
	    pe.set_control_value('zoom',f)
	elif msg[0] == "/msaremote/fader/14":
	    pe.set_control_value('sx',f)
	elif msg[0] == "/msaremote/fader/15":
	    pe.set_control_value('sy',f)
	elif msg[0] == "/msaremote/fader/16":
	    pe.set_control_value('vision_threshold',f)
	elif msg[0] == "/msaremote/fader/17":
	    pe.set_control_value('vision_num_blobs',100.0*f)
	elif msg[0] == "/msaremote/fader/18":
	    pe.set_control_value('kaleidoscope_radius',f)
	elif msg[0] == "/msaremote/trigger/18" and f > 0.0:
	    k = 1.0 - pe.kaleidoscope
	    pe.set_control_value('kaleidoscope',k)
	elif msg[0] == "/msaremote/trigger/17" and f > 0.0:
	    if (pe.wave_move == 1.0):
		print "Setting wave_move to 0\n"
		pe.set_control_value('wave_move', 0.0)
		pe.set_control_value('wave_x',0.5)
		pe.set_control_value('wave_y',0.5)
	    else:
		pe.set_control_value('wave_move', 1.0)
		print "Setting wave_move to 1\n"
        elif msg[0] == "/msaremote/trigger/16" and f > 0.0:
	    if (pe.wave_enabled):
		pe.set_control_value('wave_enabled', 0.0)
            else:
		pe.set_control_value('wave_enabled', 1.0)
        elif msg[0] == "/msaremote/trigger/15" and f > 0.0:
	    wm = pe.wave_mode
	    we = pe.wave_enabled
	    we = 1
	    if wm == 0:
		wm = 1
	    elif wm == 1:
		wm = 2
	    elif wm == 2:
		wm = 0
	    print "Set wave_mode to ",wm
	    pe.set_control_value('wave_mode', wm)
	    pe.set_control_value('wave_enabled', we)
            pe.set_control_value('wave_frequency', 0.2)

        elif msg[0] == "/msaremote/trigger/11" and f > 0.0:
            pe.vg_mode = pe.vg_mode + 1;
            if (pe.vg_mode > 3):
                pe.vg_mode = 0
	    print "vg_mode = ",pe.vg_mode

    def render_callback(self):
        pass
