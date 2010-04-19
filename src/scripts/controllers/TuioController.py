from parameters import pe
from bindings import PeBindings
import math, time
import tuio

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

class TuioController(object):

    def __init__(self, tuio_debug = False, host="antiprism.local", port=3333):

        print "\t--> Loading TUIO Controller"
        self.tuio_handler = None
        self.osc_handler = None
        self.fingers = {}
	self.smoothing = False
	self.thisframe = 0

        # Set up tracking of messages from OSC
	self.tracking = tuio.Tracking(host=host,port=port)
	self.tracking.manager.add(self.osc_callback,"/*")

        # Set up some bindings
        self.bindings = PeBindings()
        self.bindings.add(self, "/msaremote/fader/11", "rot", 0.785, -0.785, 0.0)
        self.bindings.add(self, "/msaremote/fater/12", "decay", 0.9, 1.1, 0.99, "log10")

    def multitouch_update(self):
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


    def render_callback(self): 
	
        # Call the tracking update to fetch new OSC data.
        self.tracking.update()

        self.multitouch_update()

        if (self.tuio_handler):
            self.tuio_handler.render_callback()

        if (self.osc_handler):
            self.osc_handler.render_callback()

    def osc_callback(self, source, msg):
        if (self.osc_handler):
            self.osc_handler.osc_callback(source,msg)

    def set_tuio_handler(self,o):
	self.tuio_handler = o

    def set_osc_handler(self,o):
	self.osc_handler = o

