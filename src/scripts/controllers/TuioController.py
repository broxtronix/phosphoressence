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

    def __init__(self,sid,x,y,source,frame):
	self.sid = sid
	self.x = x
	self.y = y
        self.source = source
	self.xvel = 0
	self.yvel = 0
        self.frame = frame

    
    def drag(self, new_x, new_y, new_frame):
        self.xvel = new_x - self.x
        self.yvel = new_y - self.y
        self.x = new_x
        self.y = new_y
        self.frame = new_frame

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
	self.tracking.manager.add(self.osc_callback,"/msaremote/*")

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

            # Finger Down
            if not (id in self.fingers):
	 	f = FingerState(sid=id,
                                x=obj.xpos,
                                y=obj.ypos,
                                source=obj.source,
                                frame=self.thisframe)
	 	self.fingers[id] = f
                if (self.tuio_handler):
                    self.tuio_handler.got_fingerdown(f)

            # Finger Drag
            elif id in self.fingers:
		f = self.fingers[id]
                f.drag(obj.xpos, obj.ypos, self.thisframe)
                if (self.tuio_handler):
                    self.tuio_handler.got_fingerdrag(f)

        # Finger Up
        todelete = []
        for id in self.fingers:
            if self.fingers[id].frame != self.thisframe:
                # print "Should be doing FINGER UP of id=",id
                todelete.append(id)
        for id in todelete:
            if (self.tuio_handler):
                self.tuio_handler.got_fingerup(self.fingers[id])
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

