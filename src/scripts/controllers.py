from parameters import pe
from bindings import PeBindings
import math, time
from traceback import format_exc
from graphics import ergo
from nosuch.midiutil import *


# ----------------------------------------------------
#                   OSC Controller
# ----------------------------------------------------

class OscController(object):

    def register_shape(self, shape):
        self._shapes.append(shape)

    def __init__(self, osc_debug = False):
        self._shapes = []
        self.OSC_DEBUG = osc_debug
        self.bindings = PeBindings()

        # Set up some basic control bindings
        self.bindings.add(self, "/1/decay", "decay", 0.9, 1.1, 0.99, "log10")
        self.bindings.add(self, "/1/xy1/0", "zoom", 1.1, 0.9, 1.0)
        self.bindings.add(self, "/1/xy1/1", "rot", 0.785, -0.785, 0.0)

        # Warp Effect
        self.bindings.add(self, "/1/warp", "warp", 0.0, 3.0, 0.0)
#        self.bindings.add(self, "/1/warp_speed", "warp_speed", 0.1, 10.0, 1.0, "log10")
#        self.bindings.add(self, "/1/warp_scale", "warp_scale", 0.2, 2.0, 1.0)
        self.bindings.add(self, "/1/warp_speed", "square_a", 0.0, 1.0, 1.0)
        self.bindings.add(self, "/1/warp_scale", "ib_a", 0.0, 1.0, 0.0)

        # Video Echo Effect
        self.bindings.add(self, "/1/echo_alpha", "echo_alpha", 0.0, 1.0, 0.33)
        self.bindings.add(self, "/1/echo_zoom", "echo_zoom", 0.9, 1.1, 1.0)

        # Kaleidoscope
        self.bindings.add(self, "/1/kaleidoscope", "kaleidoscope", 0.0, 1.0, 0.0)
        self.bindings.add(self, "/1/kaleidoscope_radius", "kaleidoscope_radius", 0.1, 0.8, 0.3)

        # Fluid Effects
        self.bindings.add(self, "/1/fluid_viscosity", "wave_frequency", 1e-2, 500, 0.01, "log10")
#        self.bindings.add(self, "/1/fluid_viscosity", "fluid_viscosity", 1e-5, 0.008, 1e-4, "log10")
#        self.bindings.add(self, "/1/fluid_diffusion", "fluid_diffusion", 1e-10, 1e10, 1.0, "log10")

        self.bindings.add(self, "/2/fader30", "sx", 0.9, 1.1, 1.0)
        self.bindings.add(self, "/2/fader5", "sy", 0.9, 1.1, 1.0)

        # Other
#        self.bindings.add(self, "/1/invert", "invert", 0.0, 1.0, 0.0)
        self.bindings.add(self, "/1/q1", "q1", 0.0, 1.0, 0.0)
        self.bindings.add(self, "/1/q2", "q2", 0.0, 1.0, 0.0)

        # Bindings for the wiimote
#        self.bindings.add(self, "/wii/1/ir/0", "vg_x", -1.6, 1.6, 0.0)
#        self.bindings.add(self, "/wii/1/ir/1", "vg_y", -1.0, 1.0, 0.0)
#        self.bindings.add(self, "/wii/1/button/A", "vg_stroke_a", 0.0, 1.0, 0.0)
#        self.bindings.add(self, "/wii/1/button/B", "vg_fill_a", 0.0, 1.0, 0.0)
        

#        self.bindings.add(self, "/wii/1/accel/pry/0", "zoom", 0.9, 1.1, 1.0)
#        self.bindings.add(self, "/wii/1/accel/pry/1", "rot", 0.785, -0.785, 1.0)
#        self.bindings.add(self, "/wii/1/accel/pry/2", "decay", 0.9, 1.1, 1.0)

    def receive_callback(self, path, values):

        if (path == "/1/invert"):
            pe.set_control_value('vg_mode', pe.vg_mode + 1);
            if pe.vg_mode > 4:
                pe.set_control_value("vg_mode", 0)

        if (path == "/2/toggle6"):
            pe.reset_all()

        if (path == "/xyxyM"):
            for s in self._shapes:
                s.add_video_shape(values)

        if (path == "/xy"):
            pe.set_control_value('kaleidoscope_x', values[0])
            pe.set_control_value('kaleidoscope_y', values[1])
            

        # Capture the rotation rate
        rot_rate_gain = 0.25
        zoom_rate_gain = 0.22
        if (path == "/1/xy1"):

            pe.rot = -1*(values[1]-0.5)*0.707
            pe.zoom = -(values[0]-0.5)*0.1+1.0
            
            delta = (values[1]-0.5) * rot_rate_gain
            if (math.fabs(values[1]-0.5) > 0.05):
                pe.set_control_value('rot_rate', delta)

            delta = (values[0]-0.5) * zoom_rate_gain
            if (math.fabs(values[0]-0.5) > 0.05): 
                pe.set_control_value('zoom_rate', delta)

        if (path == "/1/xy1/z" and value == 0):
            pe.set_control_value('zoom_rate', 0.0);
            pe.set_control_value('rot_rate', 0.0);

        if (self.OSC_DEBUG and (path.find("pry") == -1)):
            print("[OSC]    Path: " + path + "   Value: " + str(values))
        self.bindings.controller_to_parameter(self, path, values[0])
    
    def render_callback(self): 
        pass

# ----------------------------------------------------
#                   Tuio Controller
# ----------------------------------------------------

class FingerState:
    """
    Provides accumulated state for tracking fingers.
    """

    def __init__(self,sid,x=0.0,y=0.0,prox=0.0,orient=0.0,eccent=0.0,xvel=0.0,yvel=0.0,time=0.0):
	self.sid = sid
	self.x = x
	self.y = y
	self.prox = prox
	self.orient = orient
	self.eccent = eccent
	self.xvel = xvel
	self.yvel = yvel
	self.ang = 0.0
	self.path = None
	self.lastpt = None

import tuio

class TuioController(object):

    def __init__(self, tuio_debug = False, host="antiprism.local", port=3333):

	print "HI from TUIO Controller!\n"
	self.tracking = tuio.Tracking(host=host,port=port)
	self.tracking.manager.add(self.osc_callback,"/msaremote/*")
	self.tracking.manager.add(self.osc_callback,"/mrmr/*")
	self.tracking.manager.add(self.pe_callback,"/pe/*")
	self.tracking.manager.add(self.nth_callback,"/nth/*")
	self.tracking.manager.add(self.nth_callback,"/midi/*")
        self.bindings = PeBindings()
        self.bindings.add(self, "/msaremote/fader/11", "rot", 0.785, -0.785, 0.0)
        self.bindings.add(self, "/msaremote/fater/12", "decay", 0.9, 1.1, 0.99, "log10")
	self.fingers = {}
	self.finger_callback_func = None
	self.smoothing = False
	self.thisframe = 0

    def pe_callback(self, source, msg):
	addr = msg[0]
	f = msg[2]
	nm = addr[4:]
	print "PE OSC control nm=",nm," f=",f
	pe.set_control_value(nm,f)

    def nth_callback(self, source, msg):
	addr = msg[0]
	f = msg[1]
#	print "NTH OSC control addr=",addr," f=",f
	try:
		if msg[0] == "/nth/noteon" or msg[0] == "/midi/noteon":
		    m = NoteOn(channel=msg[2],pitch=msg[3],velocity=msg[4])
		    # print "NOTEON = ",m
		    ergo.got_noteon(m)
		elif msg[0] == "/nth/noteoff" or msg[0] == "/midi/noteoff":
		    m = NoteOff(channel=msg[2],pitch=msg[3],velocity=msg[4])
		    # print "MIDI NOTEOFF = ",m
		    ergo.got_noteoff(m)
		elif msg[0] == "/nth/perchan/action":
		    act=msg[2]
		    ch=msg[3]
		    ergo.do_chan_action(ch,act)
		elif msg[0] == "/nth/global/action":
		    act=msg[2]
		    ergo.do_global_action(act)
		elif msg[0] == "/nth/perchan/set":
		    name=msg[2]
		    name = name.upper()
		    channel=int(msg[3])
		    value=msg[4]
		    print "PERCHAN set chan=",channel," name=",name," value=",value
		    ergo.setparam(channel,name,value)
	except:
		print "Error in handling of addr=",addr,": %s"%format_exc()

    def osc_callback(self, source, msg):
	print "OSC CALLBACK!! msg=",msg
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

    def receive_callback(self, path, value):

	print "TuioController.receive_callback, path=",path," value=",value;

        # print("[OSC]    Path: " + path + "   Value: " + str(value))
        # self.bindings.controller_to_parameter(self, path, value)
    
    def render_callback(self): 
	
        # Do the update a few times because the default buffer size in
	# tracking.update is too small to handle all the messages that
	# come in within a frame's time.
        self.tracking.update()
        self.tracking.update()
        self.tracking.update()
        self.tracking.update()
        self.tracking.update()
        self.tracking.update()
        self.tracking.update()
	self.thisframe += 1
        for obj in self.tracking.objects():
            print "TUIO object=",obj
        for obj in self.tracking.cursors():
	    id = obj.sessionid
	    if not (id in self.fingers):
		f = FingerState(sid=id,x=obj.xpos,y=obj.ypos,prox=1.0)
		f.frame = self.thisframe
		f.source = obj.source
		self.fingers[id] = f
		self.processfinger("fingerdown",f)
	    elif id in self.fingers:
		f = self.fingers[id]
		f.frame = self.thisframe
		f.x = obj.xpos
		f.y = obj.ypos
		# print "Dragging of sessionid=",id," xy=",obj.xpos,obj.ypos
		self.processfinger("fingerdrag",f)
	todelete = []
	for id in self.fingers:
	    if self.fingers[id].frame != self.thisframe:
		# print "Should be doing FINGER UP of id=",id
		todelete.append(id)
	for id in todelete:
		self.processfinger("fingerup",self.fingers[id])
		# print "Deleting fingers id=",id
		del self.fingers[id]

    def set_smoothing(self,b):
	self.smoothing = b

    def processfinger(self,t,fing):

        # print "processfinger t=",t," sid=",fing.sid," xy=",fing.x,fing.y
	if fing.x < 0.0 or fing.x > 1.0 or fing.y < 0.0 or fing.y > 1.0:
		print "IGNORING finger out of bounds (%f,%f)" % (fing.x,fing.y)
		return

	fing.time = time.time()

	fing.y = 1.0 - fing.y
	fing.y = 2.0 * fing.y - 1.0
	fing.x = 2.0 * fing.x - 1.0

	if t == "fingerdown":
	    fing.speed = 0.1
	    fing.lastndx = 0.0
	    fing.lastndy = 0.0
	    self.do_finger_callback("fingerdown",fing)

	elif t == "fingerdrag":
	    if self.smoothing:
		self.dofingerdragsmooth(fing)
	    else:
		self.do_finger_callback("fingerdrag",fing)

	elif t == "fingerup":
	    self.do_finger_callback("fingerup",fing)
	    fing = None

	if fing != None:
	    fing.prevx = fing.x
	    fing.prevy = fing.y
	    fing.prevprox = fing.prox
	    fing.prevtime = fing.time

    def set_finger_callback(self,f):
	self.finger_callback_func = f

    def do_finger_callback(self,t,fing):
	# print "DOCALLBACK!  t=",t," sid=",fing.sid," xy=",fing.x,fing.y
	if self.finger_callback_func:
	    self.finger_callback_func(t,fing)

    def dofingerdragsmooth(self,fing):

	# This is where smoothing of the finger
	# values gets done.
	# Also where the angle/direction of
	# finger movement gets done.

	dx = fing.x - fing.prevx
	dy = fing.y - fing.prevy
	dprox = fing.prox - fing.prevprox
	lng = sqrt(dx**2+dy**2)
	dtime = fing.time - fing.prevtime
	
	# No change in position or time, do nothing
	if lng == 0.0 or dtime == 0.0:
		print "NO finger/time CHANGE, doing nothing"
		return

	# print "dx=",dx," dy=",dy," lng=",lng," dtime=",dtime
	thisspeed = lng/dtime

	speedadjust = False
	if speedadjust:
	    accellimit = 1.4
	    speedlimit = fing.speed * accellimit
	    # print "thisspeed=",thisspeed," lastspeed=",fing.speed
	    if thisspeed > speedlimit:
		print "ACC LIMIT!"
		thisspeed = speedlimit
	    abslimit = 3.0
	    if thisspeed > abslimit:
		print "ABS LIMIT!"
		thisspeed = abslimit

	fing.speed = thisspeed
	ndx = fing.speed * dtime * (dx/lng)
	ndy = fing.speed * dtime * (dy/lng)

	damp = 3.0
	ndx = (damp*fing.lastndx + ndx)/(damp+1.0)
	ndy = (damp*fing.lastndy + ndy)/(damp+1.0)
	# print "lastndxy=",fing.lastndx,fing.lastndy," ndxy=",ndx,ndy
	nprox = (damp*fing.prevprox + fing.prox)/(damp+1.0)

	nx = fing.prevx + ndx
	ny = fing.prevy + ndy
	fing.lastndx = ndx
	fing.lastndy = ndy
	fing.x = nx
	fing.y = ny

	if fing.x < 0.0:
	    fing.x = 0.0
	elif fing.x > 1.0:
	    fing.x = 1.0

	if fing.y < 0.0:
	    fing.y = 0.0
	elif fing.y > 1.0:
	    fing.y = 1.0

	fing.prox = nprox
	self.do_finger_callback("fingerdrag",fing)

# ----------------------------------------------------
#                Joystick Controller
# ----------------------------------------------------

class JoystickController(object):

    def __init__(self, joystick_debug = False):

        self.JOY_DEBUG = joystick_debug
        self.bindings = PeBindings()

        # Priceless
        self.bindings.add(self, "/joystick0/axis2", "decay", 0.85, 1.03, 0.98, "log10")
        self.bindings.add(self, "/joystick0/axis4", "warp", 4.0, 0.0, 0.0)
        self.bindings.add(self, "/joystick0/axis5", "echo_alpha", 0.0, 0.98, 0.0)

        # Local variables, for helping us to keep track of various
        # joystick settings.
        self.chord = 0.0
        self.sx_coefficient = 0.0
        self.sy_coefficient = 0.0
        self.cx_coefficient = 0.0
        self.cy_coefficient = 0.0
        self.warp_coefficient = 0.0
        self.reflect_coefficient = 0.0
        self.dx_coefficient = 0.0
        self.dy_coefficient = 0.0
        self.sqfreq_coefficient = 0.0
        self.wave_frequency_coeff = 0.0
        self.mv_l_coeff = 0.0
        self.square_scale_coeff = 0.0
        self.square_thick_coeff = 0.0

        # Default parameters for PhosphorEssence
        pe.wave_enabled = 1
        pe.wave_mode = 1.0
        pe.square_a = 0.0
        pe.ib_size=10.0
        pe.ib_a = 0.0
        pe.mv_a = 0.0
        pe.mv_x = 36
        pe.mv_y = 36
        pe.mv_l = 0
        pe.rot = 0
        pe.sx=1.0
        pe.rot = -0.001
        pe.sx=0.999
        pe.kaleidoscope_radius=0.25
        

    def receive_callback(self, path, value):


        # Darken the center when gain is high!  This helps to keep
        # things "under control."
        if (pe.decay > 1.01):
            pe.darken_center = 1.0
        else:
            pe.darken_center = 0.0
        

        # -------------------------------------
        # Fixed settings for PRICELESS!!
        # -------------------------------------
    
        # RESET!!
        if (path == "/joystick0/button3" and value == 1): 
            print("Resetting to defaults!!\n>> ")
            pe.reset_all()
            pe.set_control_value('mv_a', 0.0)
            pe.set_control_value('mv_x', 36)
            pe.set_control_value('mv_y', 36)
            pe.set_control_value('mv_l', 0)
            pe.set_control_value('rot', 0)
            pe.set_control_value('sx',1.0)
            pe.set_control_value('q1',0.0)
            pe.set_control_value('q2',0.0)
#            pe.set_control_value('rot', -0.001)
#            pe.set_control_value('sx',0.999)
            pe.set_control_value('wave_mode', 2)
            pe.set_control_value('wave_enabled',0.0)
            pe.set_control_value('square_a', 0.0)
            pe.set_control_value('ib_size',10.0)
    
        # Waveshape Enable
        if (path == "/joystick0/button1" and value == 1):
            if (pe.wave_enabled): pe.set_control_value('wave_enabled', 0.0)
            else: pe.set_control_value('wave_enabled', 1.0)

        # Squareshape Enable
#        if (path == "/joystick0/button6" and value == 1):
#            if (pe.square_a): pe.set_control_value('square_a', 0.0)
#            else: pe.set_control_value('square_a', 1.0)
#            if (pe.mv_a): pe.set_control_value('mv_a', 0.0)
#            else: pe.set_control_value('mv_a', 1.0);    


        # Border Enable
        if (path == "/joystick0/button2" and value == 1): 
            if (pe.ib_a): pe.set_control_value('ib_a', 0.0)
            else: pe.set_control_value('ib_a', 1.0)

        # Vector Field
        if (path == "/joystick0/button7" and value == 1):
            if (pe.invert): pe.set_control_value('invert', 0.0)
            else: pe.set_control_value('invert', 1.0)
#            pe.vg_mode = pe.vg_mode + 1;
#            if (pe.vg_mode > 3):
#                pe.vg_mode = 0

        # Kaleidoscope
        if (path == "/joystick0/button0" and value == 1): 
            if (pe.wrap): pe.set_control_value('wrap', 0.0)
            else: pe.set_control_value('wrap', 1.0)


        # Translation
        if (path == "/joystick0/hat0" and value == 2):
            pe.set_control_value('brighten', 1.0);
            pe.set_control_value('darken', 0.0);
            #            self.square_athick_coeff = 1.0
        if (path == "/joystick0/hat0" and value == 8):
            pe.set_control_value('darken', 1.0);
            pe.set_control_value('brighten', 0.0);
            #            self.square_thick_coeff = -1.0
        if (path == "/joystick0/hat0" and value == 1): 
            pe.set_control_value('darken', 0.0);
            pe.set_control_value('solarize', 0.0);
            pe.set_control_value('brighten', 0.0);
            #            self.square_scale_coeff = 1.0
        if (path == "/joystick0/hat0" and value == 4): 
            pe.set_control_value('solarize', 1.0);
            #            self.square_scale_coeff = -1.0
        if (path == "/joystick0/hat0" and value == 0.0):
            pass
#            self.square_thick_coeff = 0.0
#            self.square_scale_coeff = 0.0
#            self.wave_frequency_coeff = 0.0


        # Wave Movement
        if (path == "/joystick0/button6"):
            self.chord = value
#            if (pe.wave_move == 1.0):
#                pe.set_control_value('wave_move', 0.0)
#                pe.set_control_value('wave_x',0.5)
#                pe.set_control_value('wave_y',0.5)
#            else: pe.set_control_value('wave_move', 1.0)


        # Capture the rotation rate
        rot_rate_gain = -0.05
        if (path == "/joystick0/axis0"):
            delta = (value-0.5) * rot_rate_gain
            if (math.fabs(value-0.5) > 0.05):
                pe.set_control_value('rot_rate', delta)

        # Capture the zoom rate
        zoom_rate_gain = 0.02
        if (path == "/joystick0/axis1"): 
            delta = (value-0.5) * zoom_rate_gain
            if (math.fabs(value-0.5) > 0.05): 
                pe.set_control_value('zoom_rate', delta)

        # Rotation
        rot_gain = 0.01
        if (path == "/joystick0/axis0"):
            delta = -(value-0.5) * rot_gain
            if (math.fabs(value-0.5) > 0.05): 
                if (self.chord):
                    pe.set_control_value('q2', pe.q2 + 2.0*delta)
                else:
                    pe.set_control_value('rot', pe.rot - delta)

        # Zoom
        zoom_gain = 0.002
        if (path == "/joystick0/axis1"): 
            if (math.fabs(value-0.5) > 0.05):
                if (self.chord):
                    delta = -(value-0.5) * rot_gain
                    pe.set_control_value('q1', pe.q1 - delta)
                else:
                    delta = (value-0.5) * zoom_gain
                    pe.set_control_value('zoom', pe.zoom - delta)
                    if (pe.zoom > 1.16): pe.set_control_value('zoom', 1.16)
                    if (pe.zoom < 0.5): pe.set_control_value('zoom', 0.5)


        # Zoomexp & Kaliedoscope_raidus share this control
        if (path == "/joystick0/axis3"):
            if (pe.kaleidoscope == 1.0):
                delta = (value-0.5)/80.0
                if (math.fabs(value-0.5) > 0.05):
                    pe.set_control_value('kaleidoscope_radius', pe.kaleidoscope_radius - delta)
                if (pe.kaleidoscope_radius < 0.0): pe.set_control_value('kaleidoscope_radius', 0.0)
                if (pe.kaleidoscope_radius > 1.0): pe.set_control_value('kaleidoscope_radius', 1.0)
            else:
                delta = (value-0.5)/80.0
                if (math.fabs(value-0.5) > 0.05):
                    pe.set_control_value('zoomexp', pe.zoomexp - delta)
                if (pe.zoomexp < 0.25): pe.set_control_value('zoomexp', 0.25)
                if (pe.zoomexp > 2.0): pe.set_control_value('zoomexp', 2.0)


        # Scaling
        sx_increase ="/joystick0/button17" 
        sx_decrease ="/joystick0/button15" 
        sy_increase ="/joystick0/button16" 
        sy_decrease ="/joystick0/button14"

        # swap for vertical orientation
        if (pe.orientation == 1.0): 
            sy_increase ="/joystick0/button17" 
            sy_decrease ="/joystick0/button15" 
            sx_increase ="/joystick0/button16" 
            sx_decrease ="/joystick0/button14"
        
        if (path == sx_increase and value == 1.0): 
            self.sx_coefficient = 1.0
        if (path == sx_increase and value == 0.0): 
            self.sx_coefficient = 0.0
        if (path == sx_decrease and value == 1.0): 
            self.sx_coefficient = -1.0
        if (path == sx_decrease and value == 0.0): 
            self.sx_coefficient = 0.0

        if (path == sy_increase and value == 1.0): 
            self.sy_coefficient = 1.0
        if (path == sy_increase and value == 0.0): 
            self.sy_coefficient = 0.0
        if (path == sy_decrease and value == 1.0): 
            self.sy_coefficient = -1.0
        if (path == sy_decrease and value == 0.0): 
            self.sy_coefficient = 0.0

        # Translation
        dx_increase ="/joystick0/button25" 
        dx_decrease ="/joystick0/button23" 
        dy_decrease ="/joystick0/button24" 
        dy_increase ="/joystick0/button22"

        # swap for vertical orientation
        if (pe.orientation == 1.0): 
            dy_decrease ="/joystick0/button25" 
            dy_increase ="/joystick0/button23" 
            dx_decrease ="/joystick0/button24" 
            dx_increase ="/joystick0/button22"

        if (path == dx_decrease and value == 1.0): 
            self.dx_coefficient = -1.0
        if (path == dx_decrease and value == 0.0): 
            self.dx_coefficient = 0.0
        if (path == dx_increase and value == 1.0): 
            self.dx_coefficient = 1.0
        if (path == dx_increase and value == 0.0): 
            self.dx_coefficient = 0.0

        if (path == dy_increase and value == 1.0): 
            self.dy_coefficient = 1.0
        if (path == dy_increase and value == 0.0): 
            self.dy_coefficient = 0.0
        if (path == dy_decrease and value == 1.0): 
            self.dy_coefficient = -1.0
        if (path == dy_decrease and value == 0.0): 
            self.dy_coefficient = 0.0


        # IFS Mode
        if (path == "/joystick0/button19" and value == 1.0):
            pe.set_control_value('ifs_mode', pe.ifs_mode + 1)
            if (pe.ifs_mode > 4):
                pe.set_control_value('ifs_mode', 0)
        if (path == "/joystick0/button21" and value == 1.0): 
            pe.set_control_value('ifs_mode', pe.ifs_mode - 1)
            if (pe.ifs_mode < 0):
                pe.set_control_value('ifs_mode', 4)
        if (path == "/joystick0/button20" and value == 1.0): 
            pe.set_control_value('ifs_mode', 0)
        if (path == "/joystick0/button18" and value == 1.0): 
            pe.set_control_value('ifs_mode', 0)


        # Activate the edge filter
        if (path == "/joystick0/button5" and value == 1.0):
            if (pe.edge_filter):
                pe.set_control_value('edge_filter', 0.0)
                pe.set_control_value('brighten', 0.0)
                pe.set_control_value('gamma', 1.0)
            else:
                pe.set_control_value('edge_filter', 1.0)
                pe.set_control_value('brighten', 1.0)
                pe.set_control_value('gamma', 1.8)

        # Warp
        # if (path == "/joystick0/button0" and value == 1.0):
        #     self.warp_coefficient = 1.0
        # if (path == "/joystick0/button0" and value == 0.0):
        #     self.warp_coefficient = 0.0
        # if (path == "/joystick0/button6" and value == 1.0):
        #     self.warp_coefficient = -1.0
        # if (path == "/joystick0/button6" and value == 0.0): 
        #     self.warp_coefficient = 0.0

        # echo orient
        if (path == "/joystick0/button4" and value == 1.0):
            if (pe.kaleidoscope):
                pe.set_control_value('kaleidoscope', 0.0)
            else:
                pe.set_control_value('kaleidoscope', 1.0)

        # Wave mode
        if (path == "/joystick0/button8" and value == 1): 
            pe.set_control_value('wave_mode', 0)
            pe.set_control_value('wave_enabled', 1)
        elif (path == "/joystick0/button9" and value == 1): 
            pe.set_control_value('wave_mode', 1)
            pe.set_control_value('wave_enabled', 1)
        elif (path == "/joystick0/button10" and value == 1): 
            pe.set_control_value('wave_mode', 2)
            pe.set_control_value('wave_enabled', 1)


        # PRECIOUS UPPER SWITCH 
        if (path == "/joystick0/button11" and value == 1): 
            pe.set_control_value('wave_frequency', 0.03)
            pe.set_control_value('wave_mode', 2)
        elif (path == "/joystick0/button12" and value == 1): 
            pe.set_control_value('wave_frequency', 0.2)
            pe.set_control_value('wave_mode', 2)
        elif (path == "/joystick0/button13" and value == 1): 
            pe.set_control_value('wave_frequency', 9.0)
            pe.set_control_value('wave_mode', 2)

        # Debugging
        if (self.JOY_DEBUG and (path.find("axis") == -1)):
            print("[JOYSTICK]    Path: " + path + "   Value: " + str(value))

        # Otherwise, delegate to the bindings.
        self.bindings.controller_to_parameter(self, path, value)



    def render_callback(self):

        # Update scaling
        scaling_stepsize = 0.001
        if (self.sx_coefficient):
            pe.set_control_value('sx', pe.sx + scaling_stepsize * self.sx_coefficient)
        else:
            pe.set_control_value('sx', 1.0 + (pe.sx-1.0) * 0.95)
        if (self.sy_coefficient):
            pe.set_control_value('sy', pe.sy + scaling_stepsize * self.sy_coefficient)
        else:
            pe.set_control_value('sy', 1.0 + (pe.sy-1.0) * 0.95)
        if (pe.sx > 1.5): pe.set_control_value('sx', 1.5)
        if (pe.sx < 0.5): pe.set_control_value('sx', 0.5)
        if (pe.sy > 1.5): pe.set_control_value('sy', 1.5)
        if (pe.sy < 0.5): pe.set_control_value('sy', 0.5)

        # Update center of rotation
        crot_stepsize = 1/100.0
        pe.cx += crot_stepsize * self.cx_coefficient
        pe.cy += crot_stepsize * self.cy_coefficient
        if (pe.cx > 1.5): pe.set_control_value('cx', 1.5)
        if (pe.cx < -1.5): pe.set_control_value('cx', -1.5)
        if (pe.cy > 1.5): pe.set_control_value('cy', 1.5)
        if (pe.cy < -1.5): pe.set_control_value('cy', -1.5)

        # Update Square Scale
        square_scale_stepsize = 0.05
        pe.square_scale += square_scale_stepsize * self.square_scale_coeff
        if (pe.square_scale > 4.0): pe.square_scale = 4.0
        if (pe.square_scale < 0.25): pe.square_scale = 0.25

        # Update Square Thickness
        square_thick_stepsize = 1.2
        if (self.square_thick_coeff == 1.0):
            pe.set_control_value('square_thick', pe.square_thick * square_thick_stepsize)
        if (self.square_thick_coeff == -1.0):
            pe.set_control_value('square_thick', pe.square_thick / square_thick_stepsize)
        if (pe.square_thick > 15.0): pe.set_control_value('square_thick', 15.0)
        if (pe.square_thick < 1.0): pe.set_control_value('square_thick', 1.0)

        # Update dx & dy
        dx_stepsize = 0.01
        if (self.dx_coefficient > 0):
            pe.set_control_value('dx', pe.dx + dx_stepsize)
        elif (self.dx_coefficient < 0):
            pe.set_control_value('dx', pe.dx - dx_stepsize)
        if (pe.dx > 0.5): pe.set_control_value('dx', 0.5)
        if (pe.dx < -0.5): pe.set_control_value('dx', -0.5)

        dy_stepsize = 0.01
        if (self.dy_coefficient > 0):
            pe.set_control_value('dy', pe.dy - dy_stepsize)
        elif (self.dy_coefficient < 0):
            pe.set_control_value('dy', pe.dy + dy_stepsize)
        if (pe.dy > 0.5): pe.set_control_value('dy', 0.5)
        if (pe.dy < -0.5): pe.set_control_value('dy', -0.5)

        # Update wave_frequency
        # wave_frequency_stepsize = 1.1
        # if (self.wave_frequency_coeff > 0)
        #     pe.wave_frequency *= wave_frequency_stepsize
        # elif (self.wave_frequency_coeff < 0)
        #     pe.wave_frequency /= wave_frequency_stepsize
        # if (pe.wave_frequency > 10.0) pe.wave_frequency = 10.0
        # if (pe.wave_frequency < 0.03) pe.wave_frequency = 0.03

        # Set these values manually, which forces these parameters to
        # revert to these values after a certain amount of time has
        # passed.
        pe.dx = 0
        pe.dy = 0
        pe.sx = 1
        pe.sy = 1
        pe.zoomexp = 1
        pe.edge_filter = 0
        pe.brighten = 0
        pe.gamma = 1.0
        pe.ifs_mode = 0

        # Tweak decay
        if (pe.decay < 0.851):
            pe.set_control_value("decay", 0.1);

        if (pe.decay > 0.99 and pe.decay <1.01):
            pe.set_control_value("decay", pe.decay+0.01)            
        elif (pe.decay > 0.99 and pe.decay <1.01):
            pe.set_control_value("decay", 1.0)
        elif (pe.decay >= 1.01):
            pe.set_control_value("decay", pe.decay-0.01)
