import math
import sys
# import pygame
import time
import string
import types

import sprite
import path

import splines
import profile

import sprite

# numpy includes array
from numpy import *

from threading import Thread
from random import randint, random
from util import *
from sprite import *

from parameters import pe

ESCAPE = '\033'
twopi = 2.0*math.pi
degree2rad = twopi/360.0
rad2degree = 360.0/twopi
ThrottleVel = 0.4

doaudio = False

class Ergo(object):

	__single = None

	def __init__(self):

		width = 800
		height = 600
		if Ergo.__single:
			raise Ergo.__single
		Ergo.__single = self

		self.active = False

# 		self.spriteclasses = []				#
# 
#  		self.spriteclasses.append(sprite_disc)		# 0
#  		self.spriteclasses.append(sprite_circle)		# 1
#  		self.spriteclasses.append(sprite_vectorV)	# 2
#  		self.spriteclasses.append(sprite_triangle)	# 3
#  		self.spriteclasses.append(sprite_fillbox)	# 4
#  		self.spriteclasses.append(sprite_emptybox)	# 5
#  		self.spriteclasses.append(sprite_path)		# 12
#  		self.spriteclasses.append(sprite_sine)		# 13

 		# self.spriteclasses.append(sprite_text)		# 8
 		# self.spriteclasses.append(sprite_image)		# 14
 		# self.spriteclasses.append(sprite_image2)		# 15
 		# self.spriteclasses.append(sprite_vbar)		# 10
 		# self.spriteclasses.append(sprite_hbar)		# 11
 		# self.spriteclasses.append(sprite_vbar2)		# 6
 		# self.spriteclasses.append(sprite_hbar2)		# 7
 		# self.spriteclasses.append(sprite_vectorH)	# 2
 		# self.spriteclasses.append(sprite_trace)		# 15

 		# self.spriteclasses.append(sprite_triangle2)	# 3
 		# self.spriteclasses.append(sprite.sprite_box)		# 4
 		# self.spriteclasses.append(sprite.sprite_square)	# 5
 		# self.spriteclasses.append(sprite_image2)	# 8
 		# self.spriteclasses.append(sprite_text)	# 8
 		# self.spriteclasses.append(sprite_image)	# 8
 		# self.spriteclasses.append(sprite_image)	# 9

		self.savepatch = False

		self.action = None

		# print("Loading Clipart List...")
		# loadClipartList()
		# print("Done loading list.")

		self.notesdown = {}
		self.pitchesdown = {}

		self.width = width
		self.height = height

		self.xdir = 1.0
		self.rdir = 1
		self.xmult = 0.1
		self.xval = []
		self.lastf = 0

		self.lastspritetime = 0.0

		# print "Ergo setaction is creating action_0"
		self.setaction(action_0(0))

		self.setcurrpad(0)

		# perspective
		self.xval.append(29.0)  # 0  (multiplied by 5)

		# translate
		self.xval.append(-4.0)  # 1
		self.xval.append(0.1)  # 2
		self.xval.append(0.0)  # 3

		# scale
		self.xval.append(8.2)  # 4
		self.xval.append(2.25)  # 5
		self.xval.append(1.0)  # 6

		# rotate
		self.xval.append(-2.3)  # 7

		# ??
		self.xval.append(0.0)  # 8

			# glTranslate(0.0,0.8,0.0)

		self.spriteoutline = False
		self.doclear = 1
		self.posX = width/2
		self.posY = height/2
		self.facing = 0
		self.doblend = 1
		# self.setfps(16)
		self.setfps(1)
		self.timefactor = 1.0
		self.decayfactor = 1.0

		self.debug = 1
		self.verbose = 0

		self.dooffscreen = 0

		self.myoffscreen = 0
		self.pixels = 1

		self.font = 0
		self.sprites = []
		self.envelopes = []
		self.spritelimit = 300

		bw = 0.001

		self.frames = 0
	
		self.lastFrame = time.clock() * self.timefactor

		# self.server = ErgoListener(3930,self)

	def render(self):
            glLoadIdentity()
            glEnable(GL_BLEND);
            glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glEnable(GL_LINE_SMOOTH)

            # Compute rotation
            theta = pe.time * pe.square_frequency * 2.0 * math.pi;
            rot = array([[cos(theta), sin(theta)],
                         [-sin(theta), cos(theta)]])

            # Create & rotate the square
            square = array([[-0.25, -0.25, 0.25, 0.25],
                            [-0.25, 0.25, 0.25, -0.25]]) * pe.square_scale
            vertices = dot(rot, square)

            # Set up drawing parameters
            glLineWidth(pe.square_thick*200.0)
            glPointSize(200.0*pe.square_thick/2.0)

            color = array([pe.square_r, pe.square_g, pe.square_b])
            norm_color = color
            if (pe.wave_brighten):
                norm_color = color / sqrt(dot(color,color.conj()))
            glColor4f(norm_color[0], norm_color[1], norm_color[2], pe.square_a)

            if pe.wave_move:
                x = 0.60*math.sin(2.121*pe.time*0.1) + 0.40*math.sin(1.621*pe.time*0.1)
                y = 0.60*math.sin(1.742*pe.time*0.1) + 0.40*math.sin(2.322*pe.time*0.1)
                glTranslate(x,y,0.0)
            else:
                glTranslate(pe.wave_x * 2.0 - 1.0,
                            pe.wave_y * 2.0 - 1.0,
                            0.0)

            # Draw the sq1uare
            glLineWidth(20.0)

#             glBegin(GL_LINES)
#             glVertex( vertices[:,0] )
#             glVertex( vertices[:,1] )
#             glVertex( vertices[:,1] )
#             glVertex( vertices[:,2] )
#             glVertex( vertices[:,2] )
#             glVertex( vertices[:,3] )
#             glVertex( vertices[:,3] )
#             glVertex( vertices[:,0] )
#             glEnd()    
# 
#             glBegin(GL_POINTS)
#             glVertex( vertices[:,0] )
#             glVertex( vertices[:,1] )
#             glVertex( vertices[:,2] )
#             glVertex( vertices[:,3] )
#             glEnd();

	    self.drawscene()

	def setactive(self,b):
		print "ERGO setactive=",b
		self.active = b

	def setcurrpad(self,pn):
		# print "====== ERGO Setting current pad to ",pn
		self.currsource = pn
		a = self.action
		a.setcurrpad(pn)

	# def run(self):
	# 	# Start Event Processing Engine	
	# 	glutMainLoop()

	def settimefactor(self,f):
		self.timefactor = f
		now = time.clock() * self.timefactor
		self.lastFrame = now
		print("Ergo.settimefactor f=",f)

	def gettimefactor(self):
		return self.timefactor

	def setdecayfactor(self,f):
		self.decayfactor = f
		print("Ergo.setdecayfactor f=",f)

	def getdecayfactor(self):
		return self.decayfactor

	def toggleverbose(self):
		self.verbose = 1 - self.verbose
		print("VERBOSE=",self.verbose)

	def toggledebug(self):
		self.debug = 1 - self.debug
		print("DEBUG=",self.debug)

	def getdebug(self):
		return self.debug

	def setfont(self,f):
		print("ERGO SETFONT to f=",f)
		self.font = f

	def getfont(self,f):
		return self.font

	def setaction(self,a):
		self.action = a
		# self.action.setspriteclasses(self.spriteclasses)
		self.action.setergo(self)

	def getblend(self):
		return self.doblend

	def setblend(self,v):
		self.doblend = v
		if self.doblend:
			glEnable(GL_BLEND)
		else:
			glDisable(GL_BLEND)

	def setclear(self,v):
		self.doclear = v

	def getclear(self):
		return self.doclear

	def colorshiftit(self,param,v):
		# print("COLORSHIFTIT v=",v)
		self.coloradjust(param,"HUE1",v)
		self.coloradjust(param,"HUE2",v)

	def adjustparam(self,name,factor):
		print("ADJUSTPARAM name=",name)
		self.action.param[name] *= factor

	def nofunc(self):
		pass

	def resizefunc(self,width,height):
		if height == 0:
			height = 1

		self.width = width
		self.height = height
		self.setview()

	def setview(self):
		# print "SETVIEW wh=",self.width,self.height
		glViewport(0, 0, self.width, self.height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		normal = True
		if normal:
			gluPerspective(55.0, float(self.width)/float(self.height), 0.1, 30.0)
			glMatrixMode(GL_MODELVIEW)
			return
				
		leftsmaller = False
		leftsmaller = True
		if leftsmaller:
			gluPerspective(5.0*self.xval[0], float(self.width)/float(self.height), 0.1, 30.0)
			# glRotate(30.0,-1.0,0.0,0.0)
			# glTranslate(0.0,0.8,0.0)

			glTranslate(self.xval[1],self.xval[2],self.xval[3])
			glScale(self.xval[4],self.xval[5],self.xval[6])
			if self.rdir == 0:
				glRotate(10*self.xval[7],1.0,0.0,0.0)
			elif self.rdir == 1:
				glRotate(10*self.xval[7],0.0,1.0,0.0)
			else:
				glRotate(10*self.xval[7],0.0,0.0,1.0)

			# glScale(1.0,1.0,1.0)
			# glRotate(30.0,0.0,-1.0,0.0)
			# glTranslate(0.0,1.0,0.0)
		else:
			gluPerspective(65.0, float(self.width)/float(self.height), 0.1, 30.0)
			glRotate(20.0,0.0,1.0,0.0)
			glTranslate(0.5,0.0,0.0)
		# glFrustum(-5.0,3.0,-3.0,2.0,1.5,30.0)
		# glFrustum(-1.0,1.0,-1.0,1.0,1.5,30.0)
		# glTranslatef(-0.5, 0.0, 0.0)
		glMatrixMode(GL_MODELVIEW)
		# print("SETVIEW called")

	def InitGL(self):
		glClearColor(0.0, 0.0, 0.0, 0.0)

		# glBlendFunc(GL_SRC_ALPHA,GL_ONE)
		glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

		glEnable(GL_BLEND)

		## These are really expensive
		# glEnable(GL_LINE_SMOOTH)
		# glEnable(GL_POLYGON_SMOOTH)
		
		self.setview()

	def newenvelope(self,v1,v2,tm):
		e = envelope(v1,v2,tm)
		print "NEW ERGO ENVELOPE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		self.envelopes.append(e)
		return e

	def newnoise(self,v1,v2,tm):
		e = noise(v1,v2,tm)
		self.envelopes.append(e)
		return e

	def global_param(self,nm):
		return self.action.param[nm]

	def drawoffscreen(self):

		if not self.myoffscreen:
			return

		if self.pixels:
			glPushMatrix()
			glColor4ub(255,255,255,255)
			# HACK
			# glRasterPos2f(-0.02,-0.02)

			f = self.action.param["SCREENFADE"]

			if f != self.lastf:
				self.lastf = f
				# print "screen fade f=",f

			glPixelTransferf(GL_RED_BIAS,-f)
			glPixelTransferf(GL_GREEN_BIAS,-f)
			glPixelTransferf(GL_BLUE_BIAS,-f)

			glDrawPixels(self.pixwidth,self.pixheight,GL_RGB,GL_UNSIGNED_BYTE,self.myoffscreen)
			glPopMatrix()

		else:
			bf = glGetTexParameterfv(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
			glEnable(GL_TEXTURE_2D)
			print "Binding to offscreen"
			glBindTexture(GL_TEXTURE_2D,self.myoffscreen)

			glPushMatrix()
			# glTranslatef(0.0, 0.0, 0.0)
			# glRotatef(0.0,0.0,0.0,1.0)
			# glScale(1.0,1.0,1.0)

			glColor4ub(255,255,255,255)

			glBegin(GL_QUADS)
			self.coords = [[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0]]
			self.coords = [[0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0]]
			glTexCoord2f(self.coords[0][0], self.coords[0][1])
			glVertex2f( 0.0, 0.0)
			glTexCoord2f(self.coords[1][0], self.coords[1][1])
			glVertex2f( 1.0, 0.0) 
			glTexCoord2f(self.coords[2][0], self.coords[2][1])
			glVertex2f( 1.0, 1.0)
			glTexCoord2f(self.coords[3][0], self.coords[3][1])
			glVertex2f( 0.0, 1.0)
			glEnd()

			glPopMatrix()

			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, bf)

#	def fadethings(self):
#		for s in self.sprites:
#			s.detachbyname("alpha")
#			s.alpha = 0.0
#			# s.attach("alpha",self.action.envelope(s.alpha,0.0,2.0))

	def drawthings(self,dt,painting=True,forcealpha=0.0):

# 		# First, update all the envelopes
# 		print "drawthings, envelopes=",len(self.envelopes)
# 		for e in self.envelopes:
# 			if e.sprite == None or e.sprite.fading == True:
# 				print "ERGO ADVANCING e=",e
# 				e.advance(dt*self.getdecayfactor())
# 			else:
# 				print "ERGO NOT ADVANCING e=",e

		# Now draw sprites
		for s in self.sprites:
			if s.check():
				print "Check of s=",s," failed, removing it"
				s.deleteme = 1
				continue
			if forcealpha > 0.0:
				savealpha = s.alpha
				s.alpha = forcealpha
				print "FORCALPHA setting to ",s.alpha
				s.render()
				s.alpha = savealpha
				s.move(dt)
			elif painting and s.ispainting:
				s.render()
				s.move(dt)
			elif not painting and not s.ispainting:
				s.render()
				s.move(dt)
			# s.move(dt)


		# Now delete any sprites that are no longer needed
		deletes = []
		for s in self.sprites:
			if s.deleteme:
				deletes.append(s)
		for s in deletes:
			# print "Deleting sprite padi=",s.padi,"  gen=",s.gen
			self.removesprite(s)

		# Now delete any envelopes that are done
		deletes = []
		for e in self.envelopes:
			if e.isdone():
				print "DELETING envelope e=",e
				deletes.append(e)
		for e in deletes:
			self.envelopes.remove(e)
			for s in self.sprites:
				s.detach(e)

	def drawscene(self):

		now = time.clock() * self.timefactor
		dt = now - self.lastFrame

		dt /= self.action.param["TIMEFACTOR"]

		# print "DRAWTHINGS dt=",dt
		self.drawthings(dt,painting=True)

		# self.server.update()

		self.lastFrame = now
		self.frames += (dt / self.framesecs)

	def setfps(self,fps):
		self.framesecs = 1.0 / fps
		self.fps = fps
		print "FPS is now ",self.fps

	def get_pad_param(self,pad,nm):
		param = self.action.padparamvals[pad]
		return param[nm]

	def setparam(self,source,nm,v):
		self.action.setparam(source,nm,v)

	def do_global_action(self,act):
		print "DO_GLOBAL_ACTION = ",act
		if act == "clearsprites" or act == "clear":
			self.removeall()

	def do_chan_action(self,ch,act):
		print "DO_CHAN_ACTION, ch=",ch," act=",act
		if act == "clearsprites" or act == "clear":
			self.removeall_chan(ch)

	def got_finger(self, t, f):
		if t == "fingerdown":
			self.got_fingerdown(f)
		elif t == "fingerdrag":
			self.got_fingerdrag(f)
		elif t == "fingerup":
			self.got_fingerup(f)
		else:
			print "Unknown value t=",t," in got_finger!?"

	def got_fingerdown(self,f):
		# f.x = f.x * 1.4 - 0.2
		self.action.got_fingerdown(f)

	def got_fingerdrag(self,f):
		# f.x = f.x * 1.4 - 0.2
		self.action.got_fingerdrag(f)

	def got_fingerup(self,f):
		# f.x = f.x * 1.4 - 0.2
		self.action.got_fingerup(f)

	def rotateVel(self, vel, aa):
		xv = vel[0]
		yv = vel[1]

		# rotate the velocity by the angle adjustment
		cosaa = cos(aa * degree2rad)
		sinaa = sin(aa * degree2rad)
		newxv = -yv * sinaa + xv * cosaa
		newyv = xv * sinaa + yv * cosaa

		return (newxv,newyv,0.0)

	# def pad_for_channel(self,ch):
	# 	return (ch-1) % 3

	def got_noteon(self, m):
		self.notesdown[m.pitch] = 1
		self.pitchesdown[m.pitch] = 1
		self.action.got_noteon(m)

	def got_noteoff(self, m):
		if m.pitch in self.notesdown:
			del self.notesdown[m.pitch]
		if m.pitch in self.pitchesdown:
			del self.pitchesdown[m.pitch]
		self.action.got_noteoff(m)

	def is_note_down(self,pitch):
		return (pitch in self.notesdown)

	def is_pitch_down(self,pitch):
		return (pitch in self.pitchesdown)

	def got_controller(self, chan,ct,cv):
		self.action.got_controller(chan,ct,cv)

	def coloradjust(self,param,nm,rand1):
		v = param[nm]
		# r = rand1 * randint(-500,500)/1000.0
		r = rand1
		v += r
		while v < 0:
			v += 360.0
		while v > 360:
			v -= 360.0
		param[nm] = v
		# print("coloradjust, param r=",r," nm=",nm," rand1=",rand1," v=",v)
		return v


	def removeoldestoftype(self,s):
		sg = SpriteGen()
		lowg = sg
		for o in self.sprites:
			if o.__class__ == s.__class__ and o.gen < lowg and o != s and o.padi == s.padi:
				lowo = o
				lowg = o.gen
		if lowg < sg:
			# print "Deleting old sprite padi=",lowo.padi,"  sg=",sg,"  lowgen=",lowo.gen
			self.removesprite(lowo)
		
	def removesprite(self,s):
		# We want this to work even if s isn't in the list of sprites
		try:
			self.sprites.remove(s)
			del s
		except:
			# print formatExceptionInfo()
			pass

	def numberofspriteslike(self,s):
		n = 0
		for s2 in self.sprites:
			if s2.__class__ == s.__class__ and s2.padi == s.padi:
				n += 1
		return n
	
	def addsprite(self,s):

		# Throttle
		now = time.time()
		dt = now - self.lastspritetime
		limit = s.param("NSPRITES")
		if dt < s.param("SPRITEFREQ") or limit == 0:
			s.kill()
			return
		self.lastspritetime = now

		# print "Add sprite! xy=",s.centerx,s.centery,"  gen=",s.gen
		s.fresh = 1
		s.finishinit()
		self.sprites.append(s)

		nspr = self.numberofspriteslike(s)

		nremoved = 0
		orignspr = nspr
		origtotal = len(self.sprites)

		while nspr > limit:
			self.removeoldestoftype(s)
			nspr -= 1
			nremoved += 1

		# if nremoved > 0:
		# 	print "limit=",limit," removed ",nremoved," sprites of type ",s
		# 	print "  Orignspr=",orignspr," new nspr=",nspr
		# 	print "  Origtotal=",origtotal," new total=",len(self.sprites)

		s.enabled = 1

	def removeall(self):
		print "REMOVING ALL SPRITES!"
		tokill = []
		for s in self.sprites:
			tokill.append(s)
		for s in tokill:
			self.removesprite(s)

	def removeall_chan(self,ch):
		print "REMOVING ALL SPRITES ON CHAN ",ch
		tokill = []
		for s in self.sprites:
			if s.note != None and s.note.channel == ch:
				tokill.append(s)
		for s in tokill:
			self.removesprite(s)

	def removeone(self):
		tokill = []
		for s in self.sprites:
			tokill.append(s)
			break
		for s in tokill:
			print "REMOVING ONE SPRITE!?  padi=",s.padi
			self.removesprite(s)

getting = 0
adding = 0
gotten = ""
gettincn = 0

class action:
	def __init__(self,prevaction):

		self.okay = False

		self.okay = True
		# print "ACTION is BEING FORCED TO TRUE!"

		self.recentpitches = pitchbuffer()
		self.nextfingerchan = 1
		self.fingersources = {}
		self.fsimage = None
		self.ndirections = 8
		self.nmotions = 3
		self.velocitymin = 0
		self.velocitymax = 127
		self.xoff = 0.05
		self.yoff = 0.05
		self.nchannels = 16
		self.lastx0 = []
		self.lasty0 = []
		self.lastxsize = []
		self.lastysize = []
		for n in range(self.nchannels+1):
			self.lastx0.append(0.0)
			self.lasty0.append(0.0)
			self.lastxsize.append(0.0)
			self.lastysize.append(0.0)
		self.direction = 0
		self.motion = 0
		self.noise = 0
		self.envelopeval = 0
		self.texturetype = 0
		self.fontindex = 1
		self.pitchesdown = {}
		self.env = {}
		self.slottext = ""
		self.lastcontrolx = -1
		self.lastcontroly = -1
		self.lastx = -1
		self.lasty = -1
		self.lastang = 0.0
		self.pulsetime = -1.0
		self.colorval = [
			(0.0,0.0,1.0, 0.0,0.0,1.0),	# 0
			(0.0,1.0,0.0, 0.0,1.0,0.0),	# 1
			(0.0,1.0,1.0, 0.0,1.0,1.0),	# 2
			(1.0,0.0,0.0, 1.0,0.0,0.0),	# 3
			(1.0,0.0,1.0, 1.0,0.0,1.0),	# 4
			(1.0,1.0,0.0, 1.0,1.0,0.0),	# 5
			(1.0,1.0,1.0, 1.0,1.0,1.0),	# 6
			(1.0,1.0,1.0, 1.0,1.0,1.0),	# 7
			(1.0,1.0,1.0, 1.0,1.0,1.0),	# 8
			(1.0,1.0,1.0, 1.0,1.0,1.0)	# 9
			]

		# The 0 index in this array is ignored, 1-16 are used
		self.channelEnabled = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

		self.control = {}

		################ These parameters have been added to Nth Control

		self.createstringparam("SPRITE","fillbox")
		self.createparam("NSPRITES",32.0,1.0,100.0)
		self.createparam("LIFETIME",2.0,0.1,10.0)
		self.createstringparam("POSALG","random")
		self.createparam("LINEWIDTH",1.0,1.0,24.0)
		self.createparam("ALPHA",0.5,0.01,1.0)
		self.createparam("HUE1",0.0,0.0,360.0)
		self.createparam("HUE2",0.0,0.0,360.0)
		self.createparam("SIZE",0.1,0.01,4.0)
		self.createparam("ASPECT",1.0,0.1,10.0)
		self.createparam("SPEED",0.5,0.0,1.0)

		self.createparam("MOVEDIR",0.5,0.0,1.0)
		self.createparam("MOVEDIRR",0.0,0.0,1.0)
		self.createstringparam("DIRINIT","random")
		self.createparam("DIRINITANG",0.0,0.0,1.0)
		self.createparam("ROTSPEED",0.0,0.0,1.0)
		self.createtoggleparam("ROTDIRRAND","False")
		self.createparam("INITANG",0.0,0.0,360.0)
		self.createparam("CYCLES1",1.5,0.0,5.0)
		self.createparam("CYCLES2",2.0,0.0,5.0)
		self.createparam("NOISEX",0.0,0.0,1.0)
		self.createparam("NOISEY",0.0,0.0,1.0)

		self.createtoggleparam("COLORCHANGING",False)
		self.createtoggleparam("MIRRORED",False)
		self.createtoggleparam("MOVING",True)
		self.createparam("COLORSPEED",10.0,0.0,30.0)

		################ End of parameters that have been added to Nth Control

		self.createparam("SPRITEFREQ",0.0,0.0,1.0)
		self.createparam("VAL1",0.0,0.0,1.0)
		self.createparam("VAL2",0.0,0.0,1.0)
		self.createparam("TIMEFACTOR",1.0,3.0,0.2)
		self.createparam("ALLSIZE",0.2,0.001,2.0)


		self.createparam("ALLANG",0.0,0.0,270.0)
		self.createparam("DELTAX",0.02,0.0,0.5)
		self.createparam("DELTAY",0.02,0.0,0.5)
		self.createparam("SCREENFADE",0.005,0.000000001,0.05)
		# self.createparam("B7",0.999,1.0,0.96)
		self.createparam("B8",0.00001,0.000000001,0.005)

		self.createparam("MAGNETFACTOR",5.0,20.0,0.1)

		self.nenv = 4
		for en in range(1,self.nenv+1):
			self.createparam("ENV%dTIME"%en,1.0,0.0,1.0)
			self.createparam("ENV%dVAL1"%en,0.0,0.0,1.0)
			self.createparam("ENV%dVAL2"%en,1.0,0.0,1.0)
			self.createstringparam("ENV%dTARGET"%en,"none")

		self.createtoggleparam("COLORTWO",False)
		self.createtoggleparam("COLORPERFINGER",False)
		self.createtoggleparam("UNUSED",False)
		self.createtoggleparam("AUTOANG",False)
		self.createtoggleparam("MOVEABLE",True)
		self.createtoggleparam("MAGNET",False)
		self.createtoggleparam("ANGDIR1",False)
		self.createtoggleparam("ANGDIRRAND",False)
		self.createtoggleparam("DIR2",False)
		self.createtoggleparam("POSNOISE",False)
		self.createtoggleparam("SPLINE",False)
		self.createtoggleparam("WIDE",True)
		self.createtoggleparam("VERTEXNOISE",False)
		self.createtoggleparam("INITIALNOISE",False)
		self.createtoggleparam("DRAWACTION",True)
		self.createtoggleparam("VSTACTION",False)
		self.createtoggleparam("VSTRAND",False)
		self.createtoggleparam("AUTOMOVEDIR",True)
		self.createtoggleparam("COLORFAST",True)

		self.createtrigger("ERASE")
		self.createtrigger("DIRECTION")
		self.createtrigger("RESETDIRECTION")
		self.createtrigger("POSITION")
		# self.createtrigger("MOTION")
		self.createtrigger("TEXTURE")

		self.padparamvals = {}

		self.setcurrpad(None)

		self.envable = {
				"MOVEDIRR":"rotatemovedir_envval",
				"MOVEDIR":"movedir_envval",
				"ROTSPEED":"rotatespeed_envval",
				"SPEED":"movespeed_envval",
				"SIZE":"size_envval",
				"ALPHA":"alpha_envval",
				"ASPECT":"aspect_envval"
				}

	def initparam(self,p,nm):
		p[nm] = self.defaultvalueof(nm)

	def paramvalarray(self):
		p = {}
		for nm in self.control:
			o = self.control[nm]
			if o["type"] == "control" or o["type"] == "toggle" or o["type"] == "string":
				self.initparam(p,nm)
		return p

	def setcurrpad(self,source):
		# print "ACTION setting current source to ",source
		self.currsource = source
		if not (source in self.padparamvals):
			self.padparamvals[source] = self.paramvalarray()
		self.param = self.padparamvals[source]
	
	def createparam(self,nm,default,low,high):
		self.control[nm] = {}
		self.control[nm]["type"] = "control"
		self.control[nm]["default"] = default
		self.control[nm]["low"] = low
		self.control[nm]["high"] = high

	def defaultvalueof(self,nm):
		return self.control[nm]["default"]

	def createtrigger(self,nm):
		self.control[nm] = {}
		self.control[nm]["type"] = "trigger"

	def createtoggleparam(self,nm,default):
		self.control[nm] = {}
		self.control[nm]["type"] = "toggle"
		self.control[nm]["default"] = default
		self.control[nm]["low"] = False
		self.control[nm]["high"] = True

	def createstringparam(self,nm,default):
		self.control[nm] = {}
		self.control[nm]["type"] = "string"
		self.control[nm]["default"] = default

	def midipitch(self,nm,chan,pitch):
		self.control[nm]["chan"] = chan
		self.control[nm]["pitch"] = pitch
	
	def character(self,nm,c):
		self.control[nm]["character"] = c

	def spriteclassforsource(self,source):
		padparamvals = self.padparamvals[source]
		nm = padparamvals["SPRITE"]
		g = globals()
		nm = "sprite_"+nm
		if not (nm in g):
			print "There's no such sprite class as: ",nm," using sprite_fillbox"
			nm = "sprite_fillbox"
		constructor = g[nm]
		return constructor

	def debug(self):
		return self.ergo.debug

	def verbose(self):
		return self.ergo.verbose

	def envelope(self,v1,v2,tm,sprite=None):
		if self.envelopeval == 1:
			return lfo(v1,v2,tm)
		e = envelope(v1,v2,tm)
		if sprite != None:
			e.sprite = sprite
		return e

	def enableChannel(self,cn,v):
		if v:
			print "CHANNEL ",cn," IS ENABLED"
		else:
			print "CHANNEL ",cn," IS DISABLED"
		self.channelEnabled[cn] = v

#	def setAction(self,cn):
#		print "setAction called!"
#		if cn == 0:
#			self.ergo.setaction(action_0(self))
#		else:
#			print("There is no action ",cn)

	def set_initial_direction_and_speed(self,s):

		# movedir = s.param("MOVEDIR")
		# print "movedir_initial = ",movedir
		rotatemovedir = s.param("MOVEDIRR")

		if s.param("AUTOMOVEDIR"):
			if s.fing != None:
				movedir = s.ang + s.fing.ang/360.0
			else:
				movedir = s.ang

		movespeed = s.param("SPEED")
		rotatespeed = s.param("ROTSPEED")
		if s.param("ROTDIRRAND") and randint(0,1) == 0:
			rotatespeed = - rotatespeed

		if s.param("ANGDIR1"):
			rotatespeed = -rotatespeed
		if s.param("ANGDIRRAND"):
			if randint(0,1) == 0:
				rotatespeed = -rotatespeed
		# dir1 = s.param("DIR1")
		# dir2 = s.param("DIR2")
		dir1 = False
		dir2 = True
		# print "dir1=",dir1,"  dir2=",dir2

		dirinit = s.param("DIRINIT")
		# print "DIRINIT = ",dirinit

		if dirinit == "random":
			movedir = random()
		elif dirinit == "angle":
			# one direction, movedir
			movedir = s.param("DIRINITANG")/360.0
		else:
			print "Unknown value of dirinit: ",dirinit

		# print "FINAL movedir=",movedir," for sprite with f=",s.fing.finger
		s.setspeed(movespeed,movedir,rotatespeed)
		s.rotatemovedir = rotatemovedir

	def setfontindex(self,fn):
		if indexedface(fn) != "":
			self.fontindex = fn
		else:
			print("No font numbered ",fn)

	def getfontface(self):
		if self.fontindex == 0:
			face = randface()
		else:
			face = indexedface(self.fontindex)
		return face

# 	def setspriteclasses(self,c):
# 
# 		self.spriteclasses = c
# 		self.nclasses = len(self.spriteclasses)

	def setparam(self,source,nm,v):
		# print "In Action setparam source=",source," nm=",nm," v=",v
		import copy
		self.setcurrpad(source)
		self.padparamvals[source] = copy.copy(self.padparamvals[source])
		self.param = self.padparamvals[source]
		if self.control[nm]["type"] == "toggle":
			v = v.lower()
			if v == "on" or v == "true":
				v = True
			else:
				v = False
			# print "Setting toggle parameter nm=",nm," to ",v
			self.param[nm] = v
		else:
			# print "Setting normal parameter nm=",nm," to ",v
			self.param[nm] = v

	def got_pulse(self):
		self.pulsetime = time.clock()
		if self.debug():
			print("got pulse time=",self.pulsetime)

	def setergo(self,e):
		self.ergo = e

	def got_controller(self, chan,ct,cv):
		found = 0
		print "ERGO GOT A CONTROLLER? ANYTHING GOING ON THERE? chan=%d ct=%d cv=%d"%(chan,ct,cv)
		for i in self.control:
			o = self.control[i]
			if o["type"] == "control":
				if o["chan"] == chan and o["val"] == ct:
					newv = o["low"] + (o["high"]-o["low"])*(cv/127.0)
					self.setparam(self.currsource,i,newv)
					if self.debug() and self.verbose():
						print "GOT control CONTROL! i=",i," val=",cv," realval=",self.param[i]
					found = 1
		if found == 0:
			if self.debug():
				print "BASE got_controller, Not Found! chan=%d ct=%d cv=%d"%(chan,ct,cv)
			# print "Ordinary control, to play: ",ct,cv
			pass
		return

	def removeall(self):
		self.ergo.removeall()

	def removeone(self):
		self.ergo.removeone()

	def set_finger_color(self,f):
		ch = self.fingerchan(f.source)
		param = self.padparamvals[ch]
		# print("set_finger_color, f.source=",f.source," changing=",param["COLORCHANGING"])
		if param["COLORCHANGING"]:
			print "finger_color speed = ",param["COLORSPEED"]
			self.ergo.colorshiftit(param,param["COLORSPEED"])
		f.hue1 = param["HUE1"]

	def got_trigger(self, nm):
		try:
			a = getattr(self,nm)
			# print("GOT ATTR FOR nm=",nm)
			a()
			found = 1
		except:
			# print "got_trigger: No attribute ",nm
			print formatExceptionInfo()

	def got_toggle(self, nm):
		try:
			a = getattr(self,nm)
			a()
			found = 1
		except:
			print "got_toggle: No attribute ",nm

	def velocity2f(self,v):
		# convert a velocity value (range=velocitymin-to-velocitymax)
		# to a float value (range=0.0-to-1.0)
		vv = v - self.velocitymin
		if vv < 0:
			return 0.0
		vv = vv * 128 / (self.velocitymax-self.velocitymin)
		return vv/127.0

	# def chan2f(self,v):
	# 	return v / 16.0

	def ERASE(self):
		print("ERASE CALLED!")
		self.ergo.removeall()
		pass

	def MOTION(self):
		self.motion = (self.motion + 1) % (self.nmotions)
		print "MOTION is now ",self.motion

	def DIRECTION(self):
		self.direction = ((self.direction + 2) % (self.ndirections+1)) - 1
		print "DIRECTION is now ",self.direction

	def RESETDIRECTION(self):
		self.direction = 0
		print "RESET - DIRECTION is now ",self.direction

	def POSITION(self):
		pass

	def TEXTURE(self):
		if self.texturetype == 1:
			self.texturetype = 2
		elif self.texturetype == 2:
			self.texturetype = 3
		else:
			self.texturetype = 1
		print "TEXTURE is ",self.texturetype

	def make_fullscreen_image(self):

		param = self.padparamvals[padi]
		s = sprite.sprite_image2(0.0, 0.0, 0.5, None, param)

		s.setspeed(0,0,0.0)

		tm = 2.0

		# s.attach("scalex",self.envelope(1.0,1.0,0.2))
		# s.attach("scaley",self.envelope(1.0,1.0,0.2))
		# s.attach("alpha",self.envelope(1.0,0.0,tm))
		s.alpha = 1.00

		s.finishinit()
		return s

class pitchbuffer:
	def __init__(self):
		self.ring = []
		self.ringsize = 10
		for n in range(self.ringsize):
			self.ring.append(64)
		self.nextpos = 0

	def add(self,pitch):
		self.ring[self.nextpos] = pitch
		self.nextpos = (self.nextpos + 1) % self.ringsize

	def getrange(self):
		min = 127
		max = 0
		for n in range(self.ringsize):
			p = self.ring[n]
			if p < min:
				min = p
			if p > max:
				max = p
		return (min,max)

# class action_none(action):
# 	def __init__(self,prevaction):
# 		action.__init__(self,prevaction)

class action_0(action):
	def __init__(self,prevaction):
		action.__init__(self,prevaction)

	def make_sprites(self,x,y,note=None,fing=None):
		ss = []

		if fing != None:
			# padi = fing.source
			padi = self.fingerchan(fing.source)
		elif note != None:
			if note.channel >= 1:
				padi = note.channel
		else:
			print "HEY, neither chan nor fing is set!?"
			return ss

		param = self.padparamvals[padi]

		if not param["MIRRORED"]:
			s = self.makeSpriteOne(x,y,note=note,fing=fing,padi=padi)
			if s != None:
				ss.append(s)
		else:
			s = self.makeSpriteOne(x,y,note=note,fing=fing,padi=padi)
			if s != None:
				ss.append(s)
			s = self.makeSpriteOne(-x,y,note=note,fing=fing,padi=padi)
			if s != None:
				ss.append(s)
			s = self.makeSpriteOne(-x,-y,note=note,fing=fing,padi=padi)
			if s != None:
				ss.append(s)
			s = self.makeSpriteOne(x,-y,note=note,fing=fing,padi=padi)
			if s != None:
				ss.append(s)
		return ss

	def makeSpriteOne(self,x,y,note=None,fing=None,padi=None):

		if fing != None and note != None:
			print "Hey, both fing and note shouldn't be non-None!"

		# if self.debug():
		# 	if fing != None:
		# 		print "makeSpriteOne prox=",fing.prox," xy=",fing.x,fing.y
		# 	else:
		# 		print "makeSpriteOne chan/vel=",note.channel,"/",note.velocity

		padparamvals = self.padparamvals[padi]

		if fing != None:
			sc = fing.spriteclass
		else:
			sc = None

		if sc == None:
			if fing == None:
				pn = note.channel
			else:
				pn = fing.source
			sc = self.spriteclassforsource(pn)

		if sc == None:
			print "NO SPRITE CLASSES ENABLED!"
			return None

		# print "SC = ",sc
		if padparamvals["POSNOISE"]:
			noisex = 4.0*random()*padparamvals["NOISEX"] - 2.0
			noisey = 4.0*random()*padparamvals["NOISEY"] - 2.0
			x += noisex
			y += noisey
			while x > 1.0:
				x -= 1.0
			while x < 0.0:
				x += 1.0
			while y > 1.0:
				y -= 1.0
			while y < 0.0:
				y += 1.0

		# print("padparamvals of SIZE_INITIAL is ",padparamvals["SIZE"]
		sizeinit = padparamvals["SIZE"]
		high = self.control["SIZE"]["high"]
		low = self.control["SIZE"]["low"]
		if sizeinit > high:
			sizeinit = high
		if sizeinit < low:
			sizeinit = low

		####################################
		# Here's where a sprite is created #
		####################################
		s = sc(self.ergo, x, y, sizeinit, fing, padparamvals)

		s.note = note
		s.size = sizeinit
		s.alpha = padparamvals["ALPHA"]
		s.aspect = padparamvals["ASPECT"]
		# print "CREATING sprite, aspect=",s.aspect

		# Set all of the envvals of things that can be
		# controlled by envelopes to -1.0 (i.e not controlled by the envelope)
		for i in self.envable:
			setattr(s,self.envable[i],-1.0)

		s.size_factor = self.get_size_factor(fing,note)

		# print "NEW SPRITE sizeinit=",sizeinit,"  s.size_envval is ",s.size_envval,"  size_factor=",s.size_factor

		# s.set_note(note)
		s.setpadi(padi)

		if padparamvals["COLORCHANGING"]:
			# print "s color speed = ",padparamvals["COLORSPEED"]," hue1 was ",padparamvals["HUE1"]
			self.ergo.colorshiftit(padparamvals,padparamvals["COLORSPEED"])
			# print "   after shiftit, hue1 is ",padparamvals["HUE1"]
			if fing != None:
				fing.hue1 = padparamvals["HUE1"]
				# print "fing! setting hue1 to ",fing.hue1

		if fing != None:
			s.setcolor1(fing.hue1)
		else:
			s.setcolor1(padparamvals["HUE1"])

		if self.texturetype == 1:
			s.setrandomimage()
		elif self.texturetype == 2:
			s.setrandomtexture()

		moving = padparamvals["MOVING"]
		if moving:
			self.set_initial_direction_and_speed(s)

		# Attach envelopes to their parameters
		# print "ENVELOPE STUFF!"
		for i in range(1,self.nenv+1):
		    tg = padparamvals["ENV%dTARGET"%i].upper()
		    # print "ENV i=",i," tg=",tg
		    if tg != "" and tg != "NONE":
			if not tg in self.envable:
				print "Hey, target ",tg," not envable!?"
				continue
			attname = self.envable[tg]
			tm = padparamvals["ENV%dTIME"%i]
			iv1 = padparamvals["ENV%dVAL1"%i]
			iv2 = padparamvals["ENV%dVAL2"%i]
			# print "   TIME=",tm," iv1=",iv1," iv2=",iv2
			if tm == 0.0:
				tm = 0.001
			if iv2 != iv1:
				# print "Attaching tm=",tm," iv1=",iv1," iv2=",iv2," to ",attname
				setattr(s,attname,iv1)
				s.attach(attname,self.envelope(iv1,iv2,tm))

		# s.attach("alpha",self.envelope(1.0,0.0,alphafadetime,sprite=s))
		s.finishinit()

		# (dx,dy) = s.getDimensions()

		s.ispainting = True

		return s

	# def pad_for_channel(self,ch):
	# 	return (ch-1) % 3

	def get_size_factor(self,fing,note):

		# Figure out the size factor of the sprite based on
		# either the note velocity or the finger proximity

		if fing != None:
			# The prox goes from about 0.5 to 4.0
			size_factor = (fing.prox-0.5)/4.0
			if size_factor > 1.0:
				size_factor = 1.0
			elif size_factor < 0.02:
				size_factor = 0.02
		else:
			size_factor = self.velocity2f(note.velocity)
			size_factor /= 2.0
			# print "note sprite velocity=",note.velocity," size_factor=",size_factor

		# Increase dynamic range of size factor
		dyn = 2.0
		mid = 0.5
		size_factor = (((size_factor - 0.5) * dyn ) + (dyn*mid)) / dyn
		size_factor *= 5.0
		return size_factor

	def got_noteoff(self, m):
		# print("got_noteoff m=",m.channel," pitch=",m.pitch)
		if self.channelEnabled[m.channel] == 0:
			return
		return

	def got_noteon(self, m):

		self.setcurrpad(m.channel)

		param = self.padparamvals[m.channel]

		if self.channelEnabled[m.channel] == 0:
			return

		self.recentpitches.add(m.pitch)

		# print "Enabled m.channel=",m.channel

		(minp,maxp) = self.recentpitches.getrange()
		if minp == maxp:
			maxp = minp + 1
		pv = -0.9 + 1.8 * ((m.pitch - minp) / float(maxp-minp))

		# print "GOT NOTE chan=",m.channel," pitch=",m.pitch," range=",minp,maxp," pv=",pv

		lastx0 = self.lastx0[m.channel]
		lasty0 = self.lasty0[m.channel]
		posalg = param["POSALG"].lower()
		if posalg == "random":
			x0 = random() * 2.0 - 1.0
			y0 = random() * 2.0 - 1.0
		elif posalg == "randwalk":
			# position is based on position/dimension of last shape,
			# but in a random direction
			xdir = 1 - 2*randint(0,1)
			x0 = lastx0 + xdir * 2 * self.lastxsize[m.channel]
			ydir = 1 - 2*randint(0,1)
			y0 = lasty0 + ydir * 2 * self.lastysize[m.channel]
		elif posalg == "left":
			x0 = -0.9
			y0 = pv
		elif posalg == "vertical" or posalg == "vert":
			x0 = 0.0
			y0 = pv
		elif posalg == "right":
			x0 = 0.9
			y0 = pv
		elif posalg == "top":
			x0 = pv
			y0 = 0.9
		elif posalg == "horizontal" or posalg == "horiz":
			x0 = pv
			y0 = 0.0
		elif posalg == "bottom":
			x0 = pv
			y0 = -0.9
		elif posalg == "center":
			x0 = 0.0
			y0 = 0.0
		elif posalg == "scanlr":
			x0 = lastx0 + 0.1
			if x0 > 1.0:
				x0 -= 2.0
			y0 = pv
		elif posalg == "scanrl":
			x0 = lastx0 - 0.1
			if x0 < -1.0:
				x0 += 2.0
			y0 = pv
		elif posalg == "scandu":
			y0 = lasty0 + 0.1
			if y0 > 1.0:
				y0 -= 2.0
			x0 = pv
		elif posalg == "scanud":
			y0 = lasty0 - 0.1
			if y0 < -1.0:
				y0 += 2.0
			x0 = pv
		else:
			# position is based on time from last pulse
			if self.pulsetime >= 0.0:
				dt = time.clock() - self.pulsetime
			else:
				# print("No pulsetime?  Not getting pulse?")
				dt = 0.0
			# print("dt=",dt)
			x0 = 0.1 + (dt/2.0)
			# print("dt=",dt," x0=",x0)
			y0 = (((m.pitch-12) * 3)%128) / 128.0

		if self.noise != 0:
			dnoise = 0.05 * self.noise
			x0 = x0 + random()*dnoise - dnoise/2
			y0 = y0 + random()*dnoise - dnoise/2

		while x0 > 1.0:
			x0 -= 1.0
		while x0 < -1.0:
			x0 += 1.0

		while y0 > 1.0:
			y0 -= 1.0
		while y0 < -1.0:
			y0 += 1.0

		# print "XY = ",x0,y0," pitch=",m.pitch

		self.lastx0[m.channel] = x0
		self.lasty0[m.channel] = y0

		ss = self.make_sprites(x0,y0,note=m)
		if len(ss) == 0:
			return
		for s in ss:
			self.ergo.addsprite(s)

		(self.lastxsize[m.channel],self.lastysize[m.channel]) = s.getxysize_aspect()

		return

	def full_screen_image(self):
		print "NO LONGER USING full_screen_image"
		return

		if self.fsimage != None:
			print("Removing fsimage = ",self.fsimage)
			self.ergo.removesprite(self.fsimage)
			self.fsimage = None

		s = self.make_fullscreen_image()
		self.ergo.addsprite(s)
		self.fsimage = s

		return

	def fingerchan(self,ip):
		# The source is a pair - ip address and port
		print "fingerchan, ip=",ip
		if not ip in self.fingersources:
			self.fingersources[ip] = self.nextfingerchan
			print "NEW FINGER SOURCE!! ip=",ip," chan=",self.nextfingerchan
			self.nextfingerchan += 1
		return self.fingersources[ip];

	def got_fingerdown(self, f):

		if not self.okay:
			print "ACTION not active yet, ignoring finger f=",f
			return

		ch = self.fingerchan(f.source)
		self.xpos = f.x
		self.ypos = f.y
		self.setcurrpad(ch)

		if self.debug():
			print "ERGO got_fingerdown dfxyprox= %d %f %f %f\n" % (f.sid,f.x,f.y,f.prox)
			print "     finger.source = ",f.source," ch=",ch

		# SHOULD THIS BE WHERE INITANG and ALLANG are done?
		if f.ang == None:
			f.ang = 0.0

		f.spriteclass = self.spriteclassforsource(ch)

		self.set_finger_color(f)
		ss = self.new_finger_sprite(f)
		if f.spriteclass == sprite_path:
			f.sprites = ss
		else:
			f.sprites = None

		# print "SHOULD I BE CALLING sprite.fingerdown?"

		f.lastpt = (f.x,f.y)
		# print "Setting lastpt to ",f.lastpt," B"

	def got_fingerdrag(self, f):

		if not self.okay:
			print "ACTION not active yet, ignoring finger f=",f
			return

		ch = self.fingerchan(f.source)

		# print "fingerdrag is no longer generating a sprite..."
		# return

		self.xpos = f.x
		self.ypos = f.y
		self.setcurrpad(ch)

		if self.debug() > 1:
			print "ERGO got_fingerdrag dfxyprox= %d %f %f %f\n" % (f.sid,f.x,f.y,f.prox)

		if not hasattr(f,"spriteclass"):
			print "HEY! dragged finger has no spriteclass?"
			f.spriteclass = self.spriteclassforsource(ch)
			f.lastpt = None

		if f.lastpt == None:
			print "Hey, got_fingerdrag, but f.lastpt = None?"
			f.lastpt = (f.x,f.y)
			return

		vec = (f.lastpt[0]-f.x,f.lastpt[1]-f.y)
		lng = sqrt(vec[0]**2 + vec[1]**2)

		lng_for_ang_change = 0.00

		if lng > lng_for_ang_change:
			ang = rad2degree*math.atan2(vec[0],vec[1]) - 180.0
			if ang < 0.0:
				ang += 360.0

			# smooth the rate of angle changing
			lagtimes = 5.0
			dang = ang - f.ang
			if dang < -180.0:
				ang += 360.0
			elif dang > 180.0:
				ang -= 360.0
			f.ang = ((lagtimes-1.0)*f.ang + ang) / lagtimes
			if f.ang < 0.0:
				f.ang += 360.0
			elif f.ang > 360.0:
				f.ang -= 360.0

			self.lastang = f.ang
			f.lastpt = (f.x,f.y)
		else:
			# print "NOT updating lastpt = ",f.lastpt," lng=",lng
			pass

		# adjust prox of finger, gradually
		oldprox = f.prox
		gradfactor = 20.0
		f.prox = (f.prox + gradfactor*f.prox)/(gradfactor+1.0)
		param = self.padparamvals[ch]
		if not param["COLORPERFINGER"]:
			self.set_finger_color(f)

		if hasattr(f,"sprites") and f.sprites != None:
			for s in f.sprites:
				s.fingerdrag(f)
		else:
			self.new_finger_sprite(f)


	def got_fingerup(self, f):

		if not self.okay:
			print "ACTION not active yet, ignoring finger f=",f
			return

		ch = self.fingerchan(f.source)

		self.xpos = f.x
		self.ypos = f.y
		self.setcurrpad(ch)

		if hasattr(f,"sprites") and f.sprites != None:
			for s in f.sprites:
				s.fingerup(f)
			f.sprites = None

		# print "FINGER UP !!!    ang = ",f.ang

	def new_finger_sprite(self, f):

		# print "\nNEW FINGER SPRITE(s) f=",f
		ss = self.make_sprites(f.x, f.y,fing=f)
		for s in ss:
			self.ergo.addsprite(s)
		return ss

from random import randint,random

class envelope:
	def __init__(self,v1,v2,tm):
		self.v1 = v1
		self.v2 = v2
		self.tm = tm
		self.v = v1
		self.tmsofar = 0.0
		self.done = 0
		self.sprite = None

	def advance(self,dt):
		if self.done:
			return
		self.v = self.v1 + (self.v2-self.v1)*(self.tmsofar/self.tm)
		self.tmsofar += dt
		# print "ENV advance e=",self
		# print "env advance, v=",self.v

	def getvalue(self):
		# print "getvalue e=",self," self.v=",self.v," v12=",self.v1,self.v2," done=",self.done," tm=",self.tm,"  sofar=",self.tmsofar
		if self.tmsofar >= self.tm:
			self.done = 1
			self.v = self.v2
		return self.v

	def stop(self):
		self.done = 1

	def isdone(self):
		return self.done

class noise:
	def __init__(self,vmin,vmax,dtime):
		self.vmin = vmin
		self.vmax = vmax
		self.dtime = dtime
		self.tmsofar = 0.0
		self.v = self.randval()
		self.done = 0

	def randval(self):
		return self.vmin + random() * (self.vmax-self.vmin)
	
	def advance(self,dt):
		if not self.done:
			self.tmsofar += dt
			if self.tmsofar >= self.dtime:
				self.tmsofar -= self.dtime
				self.v = self.randval()

	def getvalue(self):
		return self.v

	def stop(self):
		self.done = 1

	def isdone(self):
		return self.done
