

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
        print "Finger down: ", f

    def got_fingerdrag(self,f):
        print "Finger drag: ", f

    def got_fingerup(self,f):
        print "Finger up: ", f

    def render_callback(self):
        
        



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
