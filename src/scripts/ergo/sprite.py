import math
import os
import sys
# import pygame
import time 
import string
import util
import splines
# import Image
import traceback
import random

from threading import Thread
# from math import pi, sin, cos, sqrt, atan2
from util import *
from traceback import *
from numpy import *

twopi = 2.0*pi
degree2rad = twopi/360.0

spritegen = 0
quad_obj = None

fakerender = 0

def SpriteGen():
	global spritegen
	return spritegen

class sprite:

	def __init__(self,e,x0,y0,size,fing,params):
		# print "HI from sprite __init__!"
		self.ergo = e
		self.padi = None
		self.mass = 1.0
		self.too_old = 0.0
		self.params = params
		self.note = None
		self.printed = False
		self.ispainting = False
		self.isreversed = 0
		self.centerx = x0
		self.centery = y0
		self.motionsofar = 0
		self.size = size
		self.dirx = 1.0
		self.diry = 1.0
		self.rotatespeed = 0.0
		self.movespeed = 0.0
		self.movedir = 0.0
		self.rotatemovedir = 0.0
		self.scalex = 1.000 # 1.0
		self.scaley = 1.000 # 1.0
		self.r1 = 1.0
		self.g1 = 0.0
		self.b1 = 0.0
		self.fing = fing
		# self.r2 = 0.0
		# self.g2 = 1.0
		# self.b2 = 0.0

		self.envelopes = {}
		self.deleteme = 0
		self.hasTexture = 0
		global spritegen
		self.gen = spritegen
		spritegen += 1
		# self.resetbound()
		# self.set_ang(0.0)
		self.coords = [[0.0,1.0],[1.0,1.0],[1.0,0.0],[0.0,0.0]]
		self.text = "No Text"
		self.bounce = 1

		self.fading = True
		self.origsaved = 0
		self.enabled = 0
		self.notrendered = 0

		self.too_old = time.time() + self.param("LIFETIME")
		self.last_allang = self.param("ALLANG")
		self.set_ang(self.last_allang)

		self.set_ang(self.ang + self.param("INITANG"))
		if self.param("AUTOANG") and fing != None and fing.ang != None :
			# print "AUTOANG = f.ang=",f.ang
			self.set_ang(self.ang + fing.ang)

		# self.initialalpha = self.param("ALPHA_INITIAL")

		self.initialang = self.get_ang()

	def getDimensions(self):
		print("BASE getDimensions called!")
		return (self.size, self.size)

	def quad(self):
		global quad_obj
		if quad_obj == None:
			quad_obj = gluNewQuadric()
		return quad_obj

	def init_noise(self):
		if self.param("INITIALNOISE"):
			# I.e. noise is only added when the sprite is created
			nvx = self.param("NOISEX")/4.0
			nvy = self.param("NOISEY")/4.0
		else:
			nvx = 0.0
			nvy = 0.0

		self.noisex0 = nvx * ( random.random() - 0.5)
		self.noisex1 = nvx * ( random.random() - 0.5)
		self.noisex2 = nvx * ( random.random() - 0.5)
		self.noisex3 = nvx * ( random.random() - 0.5)

		self.noisey0 = nvy * ( random.random() - 0.5)
		self.noisey1 = nvy * ( random.random() - 0.5)
		self.noisey2 = nvy * ( random.random() - 0.5)
		self.noisey3 = nvy * ( random.random() - 0.5)

	def setlinewidth(self):
		# glLineWidth(3)
		glLineWidth(self.param("LINEWIDTH"))

	def randomcolor(self):
		# print "SPRITE RANDOMCOLOR"
		mx = 500
		self.r1 = random.randint(0,mx)/1000.0
		self.g1 = random.randint(0,mx)/1000.0
		self.b1 = random.randint(0,mx)/1000.0
		# self.r2 = random.randint(0,mx)/1000.0
		# self.g2 = random.randint(0,mx)/1000.0
		# self.b2 = random.randint(0,mx)/1000.0

	def clonefrom(self,clone):
		self.face = clone.face
		self.text = clone.text
		self.movespeed = clone.movespeed
		self.rotatespeed = clone.rotatespeed
		self.r1 = clone.r1
		self.g1 = clone.g1
		self.b1 = clone.b1
		self.scalex = clone.scalex
		self.scaley = clone.scaley
		self.alpha = clone.alpha

		self.orig_x0 = clone.orig_x0
		self.orig_y0 = clone.orig_y0
		self.orig_scalex = clone.orig_scalex
		self.orig_scaley = clone.orig_scaley
		self.orig_ang = clone.orig_ang
		self.orig_size = clone.orig_size
		self.orig_movespeed = clone.orig_movespeed
		self.orig_alpha = clone.orig_alpha
		self.origsaved = clone.origsaved

	def saveorig(self):
		if self.origsaved:
			return
		self.orig_x0 = self.centerx
		self.orig_y0 = self.centery
		self.orig_scalex = self.scalex
		self.orig_scaley = self.scaley
		# self.orig_ang = self.ang
		self.orig_size = self.size
		self.orig_movespeed = self.movespeed
		self.orig_alpha = self.alpha
		self.origsaved = 1

	def restoreorig(self):
		self.centerx = self.orig_x0
		self.centery = self.orig_y0
		self.scalex = self.orig_scalex
		self.scaley = self.orig_scaley
		self.size = self.orig_size
		self.movespeed = self.orig_movespeed
		self.alpha = self.orig_alpha

	def fingerdown(self, f):
		print "BASE FINGERDOWN CALLED?"

	def fingerdrag(self, f):
		print "BASE FINGERDRAG CALLED?"

	def fingerup(self, f):
		print "BASE FINGERUP CALLED?"


	def ismovable(self):
		return 1

	def istext(self):
		return 0

	def isimage(self):
		return 0

	def setbounce(self,b):
		self.bounce = b

	def settext(self,f):
		self.text = f

	def setpadi(self,padi):
		self.padi = padi

	# def set_note(self,note):
	# 	self.note = note

	def finishinit(self):
		self.saveorig()

	def setfontface(self,face):
		pass

	def startTexture(self):
		# Save the old value to be restored later
		self.bf = glGetTexParameterfv(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glEnable(GL_TEXTURE_2D)

	def bindTexture(self):
 		glBindTexture( GL_TEXTURE_2D, self.texture)
		# print "Binding to self.texture = ",self.texture

	def endTexture(self):
		# For some reason, if I don't restore the previous value,
		# all the other graphics don't display...
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.bf)

	def texCorner1(self):
		global gTextures
		glTexCoord2f(self.coords[0][0], self.coords[0][1])
	
	def texCorner2(self):
		global gTextures
		glTexCoord2f(self.coords[1][0], self.coords[1][1])
	
	def texCorner3(self):
		global gTextures
		glTexCoord2f(self.coords[2][0], self.coords[2][1])
	
	def texCorner4(self):
		global gTextures
		glTexCoord2f(self.coords[3][0], self.coords[3][1])
	
	def setcolor1(self,h):
		(self.r1,self.g1,self.b1) = HLS(h,0.5,1.0).rgb()
		# print "setcolor1 h=",h

	# def setcolor2(self,h):
	# 	(self.r2,self.g2,self.b2) = HLS(h,0.5,1.0).rgb()

	def oldresetbound(self):
		self.boundx0 = 0.0
		self.boundy0 = 0.0
		self.boundx1 = 0.0
		self.boundy1 = 0.0

	def param(self,nm):
		return self.params[nm]

	def get_ang(self):
		return self.ang

	def oldsetbound(self,x,y):
		if x < self.boundx0:
			self.boundx0 = x
		if y < self.boundy0:
			self.boundy0 = y
		if x > self.boundx1:
			self.boundx1 = x
		if y > self.boundy1:
			self.boundy1 = y

	def vertex_norotate(self,x,y):
		glVertex3f(x, y, 0.0)
		# self.setbound(x,y)

	def vertex(self,x0,y0):
		# No more rotating here
		if hasattr(self,"sinv"):
			# print "vertex sees sinv = ",self.sinv," ang=",self.ang
			x = -y0 * self.sinv + x0 * self.cosv
			y = x0 * self.sinv + y0 * self.cosv
		else:
			x = x0
			y = y0
		p = self.get_pos_relative_to(x,y)
		x = p[0]
		y = p[1]
		# print "Vertex xy=",x0,y0," rel=",x,y

		if self.param("VERTEXNOISE"):
			# meaning new noise is present in every frame
			xnoise = self.param("NOISEX")/4.0
			x = x + random.random()*xnoise - xnoise/2
			ynoise = self.param("NOISEY")/4.0
			y = y + random.random()*ynoise - ynoise/2

		glVertex3f(x, y, 0.0)
		# self.setbound(x,y)

	def vertexa(self,x0,y0,ang):
		# first rotate by sprite's angle
		xa = -y0 * self.sinv + x0 * self.cosv
		ya = x0 * self.sinv + y0 * self.cosv
		cv = cos(ang * degree2rad)
		sv = sin(ang * degree2rad)
		x = -ya * sv + xa * cv
		y = xa * sv + ya * cv
		x = x * self.scalex
		y = y * self.scaley

		if self.param("VERTEXNOISE"):
			# meaning new noise is present in every frame
			xnoise = self.param("NOISEX")/4.0
			x = x + random.random()*xnoise - xnoise/2
			ynoise = self.param("NOISEY")/4.0
			y = y + random.random()*ynoise - ynoise/2

		glVertex3f(x, y, 0.0)
		# self.setbound(x,y)

	def attach(self,name,e):
		self.envelopes[e] = name
		# print("SPRITE ATTACH! num env is now = ",len(self.envelopes))

	def detachbyname(self,nm):
		todelete = []
		for e in self.envelopes:
			if self.envelopes[e] == nm:
				todelete.append(e)
		for e in todelete:
			del self.envelopes[e]


	def detach(self,e):
		if e in self.envelopes:
			del self.envelopes[e]

	def kill(self):
		# print "kill, self=",self
		self.deleteme = 1

	def isdead(self):
		return self.deleteme

	def move(self,dt):

		deletes = []
		for e in self.envelopes:
			if e.isdone():
				deletes.append(e)
		for e in deletes:
			del self.envelopes[e]

		if self.fading:
			for e in self.envelopes:
				if self.ergo != 0:
					e.advance(dt*self.ergo.getdecayfactor())
					v = e.getvalue()
					setattr(self,self.envelopes[e],v)
					# print "Setting %s to %f" % (self.envelopes[e],v)

		a = self.get_alpha()
		if a <= 0.00001:
			# print "ALPHA too low (",a,") killing sprite self=",self
			self.kill()
			return
		# print "sprite.move, alpha=",a

		if self.scalex == 0.0 or self.scaley == 0.0:
			print "scalexy too low, killing sprite self=",self
			self.kill()
			return

		if time.time() > self.too_old:
			# print "Sprite too old, killing"
			self.kill()
			return

		thisallang = self.param("ALLANG")
		if thisallang != self.last_allang:
			self.set_ang(self.ang + (thisallang - self.last_allang))
			self.last_allang = thisallang

		if self.param("MOVEABLE"):
			self.movesprite(dt)

		# f = self.param("B7")
		# self.alpha = self.alpha * f

	def xmin(self):
		return self.centerx + self.boundx0

	def xmax(self):
		return self.centerx + self.boundx1

	def ymin(self):
		return self.centery + self.boundy0

	def ymax(self):
		print "ymax = ",self.centery + self.boundy1
		return self.centery + self.boundy1

	def get_speed(self):
		return (self.movespeed,self.movedir,self.rotatespeed)

	def setspeed(self,movespeed,movedir,rotatespeed):

		self.movespeed = movespeed
		self.movedir = movedir
		self.rotatespeed = rotatespeed
		# print "setspeed, movedir=",movedir

	def get_speedxy(self):
		# print "get_speedxy movedir=",self.get_movedir()
		sx = self.get_movespeed() * sin(360.0 * self.get_movedir() * degree2rad)
		sy = self.get_movespeed() * cos(360.0 * self.get_movedir() * degree2rad)
		return (sx,sy)

	def set(self,name,val):
		setattr(self,name,val)

	def setrandomimage(self):
		r = randimagetexture("images")
		if r == None:
			pass
			# print("No images? (setrandom)")
		else:
			self.settexture(r)

	def setrandomtexture(self):
		print("SETRANDOMTEXTURE disabled")
		return
		r = randtexturetexture()
		if r == None:
			print("No textures?")
		else:
			self.settexture(r)

	def settexture(self,t):
		self.texture = t
		self.hasTexture = 1

	def get_aspect(self):
		if self.aspect_envval >= 0.0:
			e = self.aspect_envval * self.aspect
		else:
			e = self.aspect
		# print "get_aspect self.aspect = ",self.aspect
		a = e
		if a <= 0.1:
			a = 0.1
		return a

	def get_alpha(self):
		if self.alpha_envval >= 0.0:
			a = self.alpha_envval * self.alpha
		else:
			a = self.alpha
		# want it to be weighted more toward 0
		a = a * a
		# print "get_alpha, alpha_envval=",self.alpha_envval," self.alpha=",self.alpha," a=",a
		return a

	def get_movespeed(self):
		if self.movespeed_envval >= 0.0:
			return self.movespeed_envval * self.movespeed
		else:
			return self.movespeed

	def get_rotatespeed(self):
		if self.rotatespeed_envval >= 0.0:
			return self.rotatespeed_envval * self.rotatespeed
		else:
			return self.rotatespeed

	def get_movedir(self):
		if self.movedir_envval >= 0.0:
			return self.movedir_envval * self.movedir
		else:
			return self.movedir

	def get_rotatemovedir(self):
		if self.rotatemovedir_envval >= 0.0:
			return self.rotatemovedir_envval * self.rotatemovedir
		else:
			return self.rotatemovedir

	def render(self):
		if not self.enabled:
			self.notrendered += 1
			if self.notrendered > 8:
				print "render, not enabled! self=",self
			return
		# self.resetbound()

		# print "MAIN RENDER alpha=",self.alpha," initialalpha=",self.initialalpha

		if self.hasTexture:
			self.startTexture()
			self.bindTexture()
			self.renderme()
			self.endTexture()
		elif fakerender:
			print "fakerender s=",self," xy=",self.centerx,self.centery
		else:
			self.renderme()

	def length(self,vec):
		try:
			return sqrt(vec[0]**2 + vec[1]**2)
		except:
			print "EXCEPTION in length, vec=",vec
			return -1.0

	def check(self):
		return self.throttleStuffOf()

	def makespline(self,f):
		print "makespline called"
		self.points = []
		if len(self.knots) <= 2:
			return
		# print("knots=",self.knots)
		c = f(splines.tuples2points(self.knots))
		u = 0.0
		du = 0.1
		trim = False
		if (trim):
			lim = (len(c) - 1) + du
		else:
			lim = len(c) + du
		while (u < lim):
			p = c(u)
			self.points.append(tuple(p))
			u = u + du

	def drawspline(self):

		if self.broken:
			return

		# print("drawspline, points=",self.points)
		try:
			self.setlinewidth()
			glBegin(GL_LINE_STRIP)
			glColor4f(self.r1,self.g1,self.b1,self.get_alpha())
			lng = len(self.points)
			i = 0
			while i < lng:
				p = self.points[i]
				glVertex3f(p[0], p[1], 0.0)
				i += 1
			glEnd()
		except:
			if not self.broken:
				print("Error during processing of drawspline - %s\n"%(format_exc()))
			self.broken = True

	def movesprite(self,dt):

		m = self.ergo.action.motion

		# See what pull the other sprites have
		# print "Computing magnetic attraction for s=%.3f,%.3f"%(self.centerx,self.centery)

		(speedx,speedy) = self.get_speedxy()

		speedxadd = 0.0
		speedyadd = 0.0
		changed = False

		# print "Movesprite original speed is %.3f,%.3f" % (speedx,speedy)
		magfactor = self.param("MAGNETFACTOR")
		# print "MAGNETFACTOR=",magfactor
		if magfactor >= 20.0:
			domag = False
		else:
			domag = True

		(xx,yy) = self.getxysize_noaspect()
		mass = (xx+yy)/2.0
		mass = mass * 50
		# print "SELF mass=",mass

		if domag:
		    for s in self.ergo.sprites:
			if s == self or not s.param("MAGNET"):
				continue
			dx = self.centerx - s.centerx
			dy = self.centery - s.centery
			dist = sqrt(dx**2 + dy**2)
			if dist <= 0.1:
				# print "REAL CLOSE - doing nothing"
				dist = 0.1
				continue
			mag = dt / (dist**2)
			# if mag > 1.0:
			# 	print "from %.3f,%.3f to %.3f,%.3f mag=%.3f  mvdir=%.3f" % (self.centerx,self.centery,s.centerx,s.centery,mag,self.movedir)

			(xx,yy) = s.getxysize_noaspect()
			mass = (xx+yy)/2.0
			# print "mass=",mass

			speedxadd -= dx * mag * mass / magfactor
			speedyadd -= dy * mag * mass / magfactor
			changed = True

		if changed:
			# convert updated speed back to movedir/movespeed
			newx = speedx + speedxadd
			newy = speedy + speedyadd
			newa = rad2degree * atan2(newx,newy) / 360.0
			deltaa = newa - self.get_movedir()

			# print "Changed self.size=%.3f" % (self.size)
			# print "Changed origspeedxy=%.3f,%.3f  newspeedxy=%.3f,%.3f" % (speedx,speedy,newx,newy)
			# print "Changed, orig ang = %.3f  new ang = %.3f  delta=%.6f" % (self.get_movedir(), newa, deltaa)
			sss = sin(newa * 360.0 * degree2rad)
			if sss == 0.0:
				sss = 0.001
			newms = newx / sss
			# print "    orig movespeed = %.3f  newms= %.3f" % (self.get_movespeed(), newms)
			self.movespeed = newms
			self.movedir += deltaa

		speedr = 180.0 * self.get_rotatespeed()
		speedrm = 3.0 * self.get_rotatemovedir()

		# print "movesprite m=",m
		if m == 0:
			self.centerx += self.dirx * dt * speedx
			self.centery += self.diry * dt * speedy
			# print "movesprite m0 centerxy = ",self.centerx,self.centery," speedxy=",speedx,speedy
			self.set_ang(self.ang + dt * speedr)
			self.set_movedir(self.movedir + dt * speedrm)
			# print "Updated movedir to ",self.movedir," speedrm=",speedrm
		elif m == 1:
			self.centerx += self.dirx * dt * speedx
			v1 = self.param("VAL1")
			if v1 == 0.0:
				v1 = 0.0001
			v2 = self.param("VAL2")
			if v2 == 0.0:
				v2 = 0.0001
			ia = self.initialang * util.degree2rad
			self.centerx += sin(ia+self.motionsofar/(10.0*v1))/(100.0*v2)
			self.centery += self.diry * dt * speedy
			self.centery += cos(ia+self.motionsofar/(10.0*v1))/(100.0*v2)
			self.set_ang(self.ang + dt * speedr)
		elif m == 2:
			self.centerx += self.dirx * dt * speedx
			self.centerx += sin(self.motionsofar/10.0)/100.0
			self.centery += self.diry * dt * speedy
			self.centery += cos(self.motionsofar/10.0)/100.0
			self.set_ang(self.ang + dt * speedr)

		self.motionsofar += (2.0 * self.get_movespeed())

		if self.ang > 360.0:
			self.set_ang(self.ang - 360.0)
		elif self.ang < 0.0:
			self.set_ang(self.ang + 360.0)

		if self.centerx < -2.0 or self.centerx > 2.0 or self.centery < -2.0 or self.centery > 2.0:
			# print "Sprite out of range, killing it"
			self.kill()

	def get_pos_relative_to(self,x0,y0):
		return (x0+self.centerx,y0+self.centery,0.0)

	def get_pos(self):
		return (self.centerx,self.centery)

	def set_ang(self,ang):
		self.ang = ang
		self.cosv = cos(self.ang * util.degree2rad)
		self.sinv = sin(self.ang * util.degree2rad)

	def set_movedir(self,movedir):
		self.movedir = movedir

	def getxysize_noaspect(self):
		allsize = self.ergo.global_param("ALLSIZE")
		if self.size_envval >= 0.0:
			xs = self.size * self.size_envval
			ys = self.size * self.size_envval
		else:
			xs = self.size
			ys = self.size
		# print "      getxysize_noaspect, final xs/ys = ",xs,ys," size_envval=",self.size_envval
		x = xs*self.scalex*allsize
		y = ys*self.scaley*allsize
		xy = (x,y)
		return xy

	def getxysize_aspect(self):
		(x,y) = self.getxysize_noaspect()
		a = self.get_aspect()
		# print "getxysize, aspect=",a
		x = x * a
		y = y / a
		xy = (x,y)
		return xy

	def throttleStuffOf(self):
		return

#		avel = self.body.getAngularVel()
#		alng = self.length(avel)
#		if alng < 0.0:
#			return 1
#
#		# Throttle velocity
#		if alng > 1.0:
#			self.setAngularVel((avel[0]/2.0,avel[1]/2.0,avel[2]/2.0))
#		print "NEEDS IMPLEMENTATION"
#
#		# Make sure it stays on screen
#		g = self.geom
#		pos = g.getPosition()
#		lengths = g.getLengths()
#
#		dy = lengths[1]/2.0
#		dx = lengths[0]/2.0
#		p0 = pos[0]
#		p1 = pos[1]
#		if p1 > 1.0 - dy:
#			p1 = 1.0 - dy
#		if p1 < dy:
#			p1 = dy
#		if p0 > 1.0 - dx:
#			p0 = 1.0 - dx
#		if p0 < dx:
#			p0 = dx
#		if p0 != pos[0] or p1 != pos[1]:
#			g.setPosition((p0,p1,pos[2]))
#		return 0

	def getLinearVelOf(self):
		return 0.0

	def setLinearVelOf(self,vel):
		pass

	def makeHeavy(self):
		pass

class sprite_disc(sprite):

	def __init__(self, e,x0, y0, size, fing, param):
		sprite.__init__(self,e,x0,y0,size,fing,param)

	def getDimensions(self):
		return (self.size, self.size)

	def renderme(self):
		glPushMatrix()

		p = self.get_pos_relative_to(0.0,0.0)
		x = p[0]
		y = p[1]
		glTranslatef(x, y, 0.0)
		a = self.get_aspect()
		glScale(a,1.0/a,1.0)

		(dx,dy) = self.getxysize_noaspect()

		# print "disc render, dxy=%f,%f\n" % (dx,dy)

		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())

		self.setlinewidth()

		sz = dx
		if sz > 0:
			gluDisk(self.quad(),0.0,sz,32,32)

		glPopMatrix()

class sprite_circle(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		# print "CIRCLE"
		sprite.__init__(self,e, x0,y0,size, fing, param)
		self.borderwidth = 0.001 * self.param("LINEWIDTH")

	def getDimensions(self):
		return (self.size, self.size)

	def renderme(self):
		glPushMatrix()

		p = self.get_pos_relative_to(0.0,0.0)
		x = p[0]
		y = p[1]
		# print "CIRCLE xy=",x,y
		glTranslatef(x, y, 0.0)
		a = self.get_aspect()
		if not self.printed:
			# print "aspect=",a," 1/a=",1.0/a
			self.printed = True
		glScale(a,1.0/a,1.0)

		(dx,dy) = self.getxysize_noaspect()

		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())

		self.setlinewidth()

		sz = dx
		if sz > 0:
			b1 = sz-self.borderwidth
			if b1 < 0.0: b1 = 0.0
			b2 = sz+self.borderwidth
			gluDisk(self.quad(),b1,b2,32,32)

		glPopMatrix()

class sprite_vectorV(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		# print "VECTORV ang=%f\n" % ang
		sprite.__init__(self,e, x0,y0,size,fing, param)
		self.init_noise()

	def getDimensions(self):
		return (0.02, self.size)

	def renderme(self):
		glPushMatrix()

		self.setlinewidth()
		glBegin(GL_LINE_STRIP)
		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())

		(dx,dy) = self.getxysize_noaspect()
		if self.fresh:
			# print "fresh vector, dxy=",dx,dy
			self.fresh = 0

		# print "rendervector dxy=%.4f %.4f  scalexy=%.4f %.4f" % (dx,dy,self.scalex,self.scaley)

		self.vertex(0.0+self.noisex0,-dy+self.noisey0)
		# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
		self.vertex(0.0+self.noisex0,dy+self.noisey1)

		glEnd()

		glPopMatrix()

class sprite_vectorH(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		# print "VECTORH ang=%f\n" % ang
		sprite.__init__(self,e, x0,y0,size,fing, param)
		self.init_noise()

	def getDimensions(self):
		return (self.size, 0.02)

	def renderme(self):
		glPushMatrix()

		self.setlinewidth()
		glBegin(GL_LINE_STRIP)
		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())

		(dx,dy) = self.getxysize_noaspect()
		if self.fresh:
			# print "fresh vector, dxy=%f,%f ang=%f\n" % (dx,dy,self.ang)
			self.fresh = 0

		# print "rendervector dxy=%.4f %.4f  scalexy=%.4f %.4f" % (dx,dy,self.scalex,self.scaley)

		self.vertex(-dx+self.noisex0,0.0+self.noisey0)
		# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
		self.vertex(dx+self.noisex1,0.0+self.noisey1)

		glEnd()

		glPopMatrix()

class sprite_sine(sprite):

	# This array gets in the way of the build-in value!?
	sinval = zeros(360)
	for i in range(360):
		sinval[i] = sin(i*degree2rad)

	def __init__(self, e, x0, y0, size, fing, param):
		sprite.__init__(self,e,x0,y0,size,fing, param)
		self.init_noise()
		self.knots = []
		self.changed = True

	def getDimensions(self):
		return (self.size, self.size)

	def init_noise(self):
		# sine overrides init_noise

		self.noisex0 = 0.0
		self.noisex1 = 0.0
		self.noisex2 = 0.0
		self.noisex3 = 0.0

		self.noisey0 = 0.0
		self.noisey1 = 0.0
		self.noisey2 = 0.0
		self.noisey3 = 0.0

	def changeit(self):
		(sizex,sizey) = self.getxysize_noaspect()
		cycles1 = self.param("CYCLES1")
		cycles2 = self.param("CYCLES2")

		# Use the 2 noise parameters for cycles, sigh
		if self.param("INITIALNOISE"):
			cycles1 = 0.1 + 10.0 * self.param("NOISEX")
			cycles2 = 0.1 + 10.0 * self.param("NOISEY")

		# print("cycles1/2 = ",cycles1,cycles2)
		pointspercycle = 20
		self.points = []

		sizex *= 6.0   # to make the waves bigger
		sizey *= 1.5

		if self.param("WIDE"):
			sizex = 2.5
			sizey = 0.08 + sizey
			# print "sizey=",sizey

		# if self.size_envval >= 0.0:
		# 	sizex = sizex * self.size_envval
		# 	sizey = sizey * self.size_envval

		xoff = -sizex/2.0

		yoff = 0.0

		dy = sizey / 2.0

		x = 0.0
		endx = sizex
		dx = sizex / 100
		while x < endx:
			a = 360 * (x/endx)
			ang1 = int(a * cycles1) % 360
			ang2 = int(a * cycles2) % 360
			v1 = sprite_sine.sinval[ang1]
			v2 = sprite_sine.sinval[ang2]
			v = v1+v2
			p = (x+xoff,dy*v+yoff)
			self.points.append(p)
			x += dx
		# print("sine points = ",self.points)

	def renderme(self):


		# print("sin render ang=",self.ang)
		glPushMatrix()

		self.setlinewidth()
		glBegin(GL_LINE_STRIP)
		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())
		# print("sine render rgb=",self.r1,self.g1,self.b1)

		self.changed = True
		if self.changed:
			self.changeit()
			self.changed = False
		lng = len(self.points)
		i = 0
		while i < lng:
			p = self.points[i]
			self.vertex(p[0]+self.noisex1,p[1]+self.noisey1)
			i += 1
		glEnd()

		glPopMatrix()

class segment:
	def __init__(self,x0,y0,x1,y1):
		# print "SEGMENT INIT, x0=",x0
		self.pos0 = (x0,y0)
		self.pos1 = (x1,y1)

	def __str__(self):
		return "<segment %f,%f -> %f,%f>" % (self.pos0[0],self.pos0[1],self.pos1[0],self.pos1[1])

class sprite_path(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		sprite.__init__(self,e, x0,y0,size,fing,param)
		self.init_noise()
		self.segs = []
		self.knots = []
		self.changed = False
		self.fading = False
		self.lastpt = None
		self.spline = self.param("SPLINE")
		self.broken = False

	def __str__(self):
		r = "<PATH=\n"
		for s in self.segs:
			r += "   <%f,%f %f,%f>\n" % (s.pos0[0],s.pos0[1],s.pos1[0],s.pos1[1])
		r += "\n>"
		return r

	def getDimensions(self):
		return (self.size, self.size)

	def fingerdown(self, f):
		print "SPRITE_PATH fingerdown xy=",f.x," ",f.y
		dx = 0.02*f.prox*f.prox
		self.appendsegment(f.x-dx,f.y,f.x+dx,f.y);
		self.lastpt = (f.x,f.y)

	def fingerdrag(self, f):
		if self.lastpt == None:
			self.lastpt = (f.x,f.y)
			return
		# print "SPRITE_PATH fingerdrag xy=",f.x," ",f.y," lastpt=",self.lastpt
		vec = (self.lastpt[0]-f.x,self.lastpt[1]-f.y)
		lng = sqrt(vec[0]**2 + vec[1]**2)
		if lng > 0.04:
			dx = 0.02*f.prox*f.prox
			# print "Adding segment"
			self.appendsegment(f.x-dx,f.y,f.x+dx,f.y);
			self.lastpt = (f.x,f.y)

	def fingerup(self, f):
		# print "SPRITE_PATH fingerup"
		self.fading = True

	def appendsegment(self,x0,y0,x1,y1):
		self.addsegment(1,x0,y0,x1,y1)
			
	def insertsegment(self,x0,y0,x1,y1):
		self.addsegment(0,x0,y0,x1,y1)

	def lastsegment(self):
		return self.segs[-1]

	def addsegment(self,appendit,x0,y0,x1,y1):

		# The segment points are relative to the starting point
		seg = segment(x0-self.centerx,y0-self.centery,x1-self.centerx,y1-self.centery)
		# print "ADD SEGMENT seg=",seg," xy0=",x0,y0," xy1=",x1,y1
		if appendit:
			self.segs.append(seg)
		else:
			self.segs.insert(0,seg)
		self.changed = True

	def renderme(self):
		if len(self.segs) < 2:
			return

		glPushMatrix()

		n = 1
		lng = len(self.segs)
		s0 = self.segs[0]
		# print "path alpha = ",self.get_alpha()
		if self.changed:
			self.knots = []
		self.setlinewidth()
		while n < lng:
			s1 = self.segs[n]

			if not self.spline:
				glBegin(GL_POLYGON)
				glColor4f(self.r1,self.g1,self.b1,self.get_alpha())

				self.vertex(s0.pos0[0],s0.pos0[1])
				self.vertex(s0.pos1[0],s0.pos1[1])
				self.vertex(s1.pos1[0],s1.pos1[1])
				self.vertex(s1.pos0[0],s1.pos0[1])
				self.vertex(s0.pos0[0],s0.pos0[1])
				glEnd()
			else:
				# spline
				if self.changed:
					p0 = (s0.pos0[0],s0.pos0[1])
					# print("p0=",p0)
					self.knots.append(p0)
					# self.knots.append(s0.pos1)

			s0 = s1
			n += 1

		if self.spline:
			if self.changed:
				self.makespline(splines.NaturalCubicSpline)
				# print "making spline, points=",len(self.points)
				self.changed = False

			glTranslatef(self.centerx, self.centery, 0.0)
			self.drawspline()

		glPopMatrix()

# class sprite_trace(sprite):
# 
# 	mypaths = None
# 	# printed = 0
# 
# 	def getpaths(self) :
# 		if sprite_trace.mypaths == None:
# 			p = Potrace()
# 			# i = Image.open("tiny3.gif").convert("L")
# 			i = Image.open("head.gif").convert("L")
# 			sprite_trace.mypaths = p(i.im.id)
# 			sprite_trace.mysize = i.im.size
# 		return (sprite_trace.mypaths,sprite_trace.mysize)
# 
# 
# 	def printpaths(self):
# 		print "\nprint mypaths=",self.paths
# 		for i in range(len(self.paths)):
# 			print "path i=",i," sign=",self.paths[i]["sign"],"\n"
# 			p = self.paths[i]
# 			c = p["curve"]
# 			for i in range(len(c)):
# 				seg = c[i]
# 				print "seg=",seg,"EOS"
# 		print "\n"
# 
# 	def __init__(self, x0, y0, size, ang):
# 		sprite.__init__(self,x0,y0,size,ang)
# 		self.init_noise()
# 		# print "SPRITE_TRACE INIT, xy0=",x0,y0," alpha=",self.get_alpha()," ang=",ang
# 		(self.paths,self.xysize) = self.getpaths()
# 		# self.printpaths()
# 
# 	def __str__(self):
# 		r = "<TRACE= %f,%f\n" % (self.centerx,self.centery)
# 		r += "\n>"
# 		return r
# 
# 	def getDimensions(self):
# 		return (self.size, self.size)
# 
# 	# def getxysize(self):
# 	# 	return (self.size, self.size)
# 
# 	def fingerdown(self, f):
# 		# print "SPRITE_PATH fingerdown xy=",f.x," ",f.y
# 		# dx = 0.02*f.prox*f.prox
# 		# self.appendsegment(f.x-dx,f.y,f.x+dx,f.y);
# 		pass
# 
# 	def fingerdrag(self, f):
# 		# dx = 0.02*f.prox*f.prox
# 		# self.appendsegment(f.x-dx,f.y,f.x+dx,f.y);
# 		pass
# 
# 	def fingerup(self, f):
# 		# print "SPRITE_PATH fingerup"
# 		# self.fading = True
# 		pass
# 
# 	def renderme(self):
# 
# 		(dx,dy) = self.getxysize()
# 		# print "trace getxysize=",dx,dy
# 
# 		self.scx = 1.0/self.xysize[0]
# 		self.scy = 1.0/self.xysize[1]
# 
# 		self.scx *= dx
# 		self.scy *= dy
# 
# 		glPushMatrix()
# 
# 		n = 1
# 
# 		self.setlinewidth()
# 		glBegin(GL_LINE_STRIP)
# 		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())
# 
# 		printit = 0
# 
# 		for pi in range(len(self.paths)):
# 			if printit:
# 				print "path pi=",pi," sign=",self.paths[pi]["sign"],"\n"
# 			p = self.paths[pi]
# 			c = p["curve"]
# 			for ci in range(len(c)):
# 				seg = c[ci]
# 				# print "seg=",seg,"EOS"
# 				segtype = seg[0]
# 				if segtype == 'M':
# 					if printit:
# 						print "moveto ",seg[1]
# 					lastx = seg[1][0] * self.scx
# 					lasty = seg[1][1] * self.scy
# 					self.vertex(lastx,lasty)
# 
# 				elif segtype == 'C':
# 					if printit:
# 						print "curveto ",seg[1]," ",seg[2]," ",seg[3]
# 					# lastx = seg[3][0] * self.scx
# 					# lasty = seg[3][1] * self.scy
# 					# self.vertex(lastx,lasty)
# 
# 					mypoints = []
# 					knots = []
# 
# 					p = (lastx,lasty)
# 					knots.append(p)
# 
# 					p = (seg[1][0]*self.scx,seg[1][1]*self.scy)
# 					knots.append(p)
# 					self.vertex(p[0],p[1])
# 
# 					p = (seg[2][0]*self.scx,seg[2][1]*self.scy)
# 					knots.append(p)
# 					self.vertex(p[0],p[1])
# 
# 					p = (seg[3][0]*self.scx,seg[3][1]*self.scy)
# 					knots.append(p)
# 					self.vertex(p[0],p[1])
# 
# 					lastx = p[0]
# 					lasty = p[1]
# 
# 					# for i in range(len(knots)):
# 					# 	p = knots[i]
# 					# 	print "p=",p
# 
#  					# f = splines.Polyline
# 
# # 					f = splines.NaturalCubicSpline
# # 					c = f(splines.tuples2points(knots))
# # 					u = 0.0
# # 					du = 0.1
# # 					trim = False
# # 					if (trim):
# # 						lim = (len(c) - 1) + du
# # 					else:
# # 						lim = len(c) + du
# # 					while (u < lim):
# # 						p = c(u)
# # 						# self.mypoints.append(tuple(p))
# # 						tp = tuple(p)
# # 						self.vertex(tp[0],tp[1])
# # 						u = u + du
# 
# 				elif segtype == 'L':
# 					if printit:
# 						print "lineto ",seg[1]," ",seg[2]," ",seg[3]
# 					lastx = seg[1][0] * self.scx
# 					lasty = seg[1][1] * self.scy
# 					self.vertex(lastx,lasty)
# 					# Assume seg[2] is "L"
# 					lastx = seg[3][0] * self.scx
# 					lasty = seg[3][1] * self.scy
# 					self.vertex(lastx,lasty)
# 
# 
# 		# self.vertex(0.25,0.25)
# 		# self.vertex(0.35,0.25)
# 		# self.vertex(0.35,0.35)
# 		# self.vertex(0.25,0.35)
# 		# self.vertex(0.25,0.25)
# 		glEnd()                      # We are done with the polygon
# 
# 		glPopMatrix()
# 		# print "RENDER END\n"
# 
# 	def makespline(self,f):
# 		self.points = []
# 		c = f(splines.tuples2points(self.knots))
# 		u = 0.0
# 		du = 0.1
# 		trim = False
# 		if (trim):
# 			lim = (len(c) - 1) + du
# 		else:
# 			lim = len(c) + du
# 		while (u < lim):
# 			p = c(u)
# 			self.points.append(tuple(p))
# 			u = u + du
# 
# 	def drawspline(self):
# 		glBegin(GL_LINE_STRIP)
# 		lng = len(self.points)
# 		i = 0
# 		while i < lng:
# 			p = self.points[i]
# 			glVertex3f(p[0], p[1], 0.0)
# 			i += 1
# 		glEnd()

class sprite_emptybox(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		sprite.__init__(self,e, x0,y0,size,fing,param)
		self.init_noise()

	def getDimensions(self):
		return (self.size, self.size)

	def renderme(self):
		glPushMatrix()

		self.setlinewidth()
		glBegin(GL_LINE_STRIP)
		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())

		(dx,dy) = self.getxysize_aspect()

		self.vertex(-dx+self.noisex0,-dy+self.noisey0)
		self.vertex(dx+self.noisex1,-dy+self.noisey1)
		# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
		self.vertex(dx+self.noisex2,dy+self.noisey2)
		self.vertex(-dx+self.noisex3,dy+self.noisey3)
		self.vertex(-dx+self.noisex0,-dy+self.noisey0)

		glEnd()                      # We are done with the polygon

		glPopMatrix()

class sprite_fillbox(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		sprite.__init__(self,e, x0,y0,size,fing,param)
		self.init_noise()
		# print "SPRITE_FILLBOX! ASPECT = ",self.param("ASPECT")

	def getDimensions(self):
		return (self.size, self.size)

	def renderme(self):
		glPushMatrix()

		self.setlinewidth()
		# glBegin(GL_LINE_STRIP)
		glBegin(GL_POLYGON)
		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())
		# print "fillbox rgb=",self.r1,self.g1,self.b1," alpha=",self.get_alpha()

		(dx,dy) = self.getxysize_aspect()
		# print "fillbox rend dxy=%f,%f" % (dx,dy)

		self.vertex(-dx+self.noisex0,-dy+self.noisey0)
		self.vertex(dx+self.noisex1,-dy+self.noisey1)
		# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
		self.vertex(dx+self.noisex2,dy+self.noisey2)
		self.vertex(-dx+self.noisex3,dy+self.noisey3)
		self.vertex(-dx+self.noisex0,-dy+self.noisey0)

		glEnd()                      # We are done with the polygon

		glPopMatrix()

fontRegistery = {
    "comic sans ms":"comic.ttf",
    "courier new":"cour.ttf",
    "courier":"cour.ttf",    
    "impact":"impact.ttf",
    "arial":"arial.ttf",
    "times new roman":"times.ttf",
    "times":"times.ttf"
    }

class sprite_text(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		sprite.__init__(self,e, x0,y0,size,fing,param)
		self.text = util.randword()
		self.firsttime = 1
		self.face = "arial"
		self.finished = 0
		self.fixedfactor = -1.0

	def getDimensions(self):
		return (self.size, self.size)

	def istext(self):
		return 1

	def finishinit(self):
		sprite.finishinit(self)
		if not self.finished:
			self.fontinit()
			self.finished = 1

	def settext(self,f):
		self.text = f
		if self.finished:
			self.fontinit()

	def setfixedfactor(self,f):
		self.fixedfactor = f

	def setfontface(self,face):
		self.face = face

	def getfontface(self):
		return self.face

	def fontinit(self):
		print "fontinit is disabled...\n"
		return
# 		face = self.face
# 		if fontRegistery.has_key(face):
# 		    face = os.environ['WINDIR']+"/Fonts/"+fontRegistery[face]
# 		else:
# 		    face = os.environ['WINDIR']+"/Fonts/"+face+".ttf"
# 		self.font = pygame.font.Font(face, 48)
# 		surf = self.font.render(self.text, 1,
# 			(self.r1*255,self.g1*255,self.b1*255,255))
# 		w = surf.get_width()
# 		limit = 1024
# 		if w > limit:
# 			w = limit
# 		h = surf.get_height()
# 		if h > limit:
# 			h = limit
# 		self.width = 16
# 		self.height = 16
# 		while self.width < w:
# 			self.width = self.width * 2
# 		while self.height < h:
# 			self.height = self.height * 2
# 
# 		# print("self.width/height=",self.width,self.height)
# 
# 		x = pygame.surface.Surface((self.width, self.height),
# 			   flags=pygame.HWSURFACE |pygame.SRCALPHA,
# 			   depth=32,
# 			   masks=(0,0,0,0))
# 		x.blit(surf, (0, 0) )
# 		x = pygame.transform.flip(x,0,1)
# 		self.texture = glGenTextures(1)
# 		self.mydata = pygame.image.tostring(x, "RGBA", 1)
# 		self.hasTexture = 1
	
	def renderme(self):
		if self.firsttime == 1:
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
				self.width, self.height,
				0, GL_RGBA, GL_UNSIGNED_BYTE, self.mydata)
			self.firsttime = 0

		extrascale = 4.0
		glPushMatrix()
		glTranslatef(self.centerx, self.centery, 0.0)
		# glRotatef(self.ang,0.0,0.0,1.0)
		glScale(extrascale*self.scalex,extrascale*self.scaley,1.0)
		x = 0.0
		y = 0.0
		if self.fixedfactor < 0:
			fctr = int(len(self.text)/6)
			if fctr == 0:
				fctr = 1
		else:
			fctr = self.fixedfactor
		width = self.size * fctr
		height = self.size
		
		a = int(self.get_alpha() * 255)
		glColor4ub(255,255,255,a)

		glBegin(GL_QUADS)
		self.texCorner1()
		glVertex2f( x, y)
		self.texCorner2()
		glVertex2f( x+width, y) 
		self.texCorner3()
		glVertex2f( x+width, y+height)
		self.texCorner4()
		glVertex2f( x, y+height)
		glEnd()

		glPopMatrix()

class sprite_fixedtext(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		sprite.__init__(self,e, x0,y0,size,fing,param)
		self.text = util.randword()
		self.firsttime = 1
		self.face = "arial"
		self.finished = 0
		self.ntimes = 0
		self.fixedfactor = -1.0

	def istext(self):
		return 1

	def finishinit(self):
		sprite.finishinit(self)
		if not self.finished:
			self.fontinit()
			self.finished = 1

	def settext(self,f):
		self.text = f
		if self.finished:
			self.fontinit()

	def setfixedfactor(self,f):
		self.fixedfactor = f

	def setfontface(self,face):
		self.face = face

	def getfontface(self):
		return self.face

	def setfontvalue(self,v):
		faces = facelist()
		self.face = indexedface(int(len(faces) * v))
		return self.face

	def numfonts(self):
		return len(facelist())

	def setfontindex(self,i):
		self.face = indexedface(i)

	def fontinit(self):
		print "fontinit is disabled...\n"
		return
# 		face = self.face
# 		if fontRegistery.has_key(face):
# 		    face = os.environ['WINDIR']+"/Fonts/"+fontRegistery[face]
# 		else:
# 		    face = os.environ['WINDIR']+"/Fonts/"+face+".ttf"
# 
# 		nlines = 1
# 		lines = []
# 		ln = ""
# 		for i in self.text:
# 			if i == "\n" or i == "\r":
# 				lines = lines + [ln]
# 				ln = ""
# 				nlines += 1
# 			else:
# 				ln = ln + i
# 		if ln != "":
# 			lines = lines + [ln]
# 
# 		linelength = 0
# 		for ln in lines:
# 			if len(ln) > linelength:
# 				linelength = len(ln)
# 		centeredlines = []
# 		for ln in lines:
# 			l = (linelength-len(ln))/2
# 			while l > 0:
# 				ln = " " + ln
# 				l -= 1
# 			centeredlines = centeredlines + [ln]
# 		lines = centeredlines
# 
# 		if linelength > 32:
# 			linelength = 32
# 		elif linelength > 16:
# 			linelength = 16
# 		elif linelength > 8:
# 			linelength = 8
# 		elif linelength > 4:
# 			linelength = 4
# 		elif linelength > 2:
# 			linelength = 2
# 		else:
# 			linelength = 1
# 
# 		if nlines >= 5:
# 			nlines = 4
# 
# 		self.width = 32 * linelength
# 		if self.width < 128:
# 			self.width = 128
# 		self.width = 512
# 		self.height = 128
# 		lineheight = self.height / nlines
# 		# print("self.width/height=",self.width,self.height)
# 
# 		pysurf = pygame.surface.Surface((self.width, self.height),
# 			   flags=pygame.HWSURFACE |pygame.SRCALPHA,
# 			   depth=32,
# 			   masks=(0,0,0,0))
# 
# 		psize = self.height / nlines
# 		psize = 32
# 		self.font = pygame.font.Font(face, psize)
# 
# 		mylinesize = self.font.get_linesize()
# 		mylinesize /= 1.5
# 		ypos = self.height - nlines * mylinesize + self.font.get_descent()
# 		# print("FONTINIT self=",self," RGB = ",self.r1,self.g1,self.b1)
# 		for ln in lines:
# 			# surf = self.font.render(ln, 1,
# 			# 	(self.r1*255,self.g1*255,self.b1*255,255))
# 			surf = self.font.render(ln, 1,
# 				(255,255,255,255))
# 			pysurf.blit(surf, (0, ypos) )
# 			ypos += mylinesize
# 
# 		pysurf = pygame.transform.flip(pysurf,0,1)
# 		self.texture = glGenTextures(1)
# 		self.mydata = pygame.image.tostring(pysurf, "RGBA", 1)
# 		self.hasTexture = 1
	
	def resettimes(self):
		self.ntimes = 0

	def renderme(self):
		self.ntimes += 1
		if self.ntimes <= 1:
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
				self.width, self.height,
				0, GL_RGBA, GL_UNSIGNED_BYTE, self.mydata)
			return

		# If I draw it right away, there's a white box that
		# appears...
		if self.ntimes < 2:
			return

		extrascalex = 8.0
		extrascaley = 2.0
		glPushMatrix()
		glTranslatef(self.centerx, self.centery-0.08*self.scaley, 0.0)
		# glRotatef(self.ang,0.0,0.0,1.0)
		glScale(extrascalex*self.scalex,extrascaley*self.scaley,1.0)
		x = 0.0
		y = 0.0
		if self.fixedfactor < 0:
			fctr = int(len(self.text)/6)
			if fctr == 0:
				fctr = 1
		else:
			fctr = self.fixedfactor
		width = self.size * fctr
		height = self.size
		
		a = int(self.get_alpha() * 255)
		# glColor4ub(255,255,255,a)
		glColor4ub(int(self.r1*255),int(self.g1*255),int(self.b1*255),a)

		glBegin(GL_QUADS)
		self.texCorner1()
		glVertex2f( x, y)
		self.texCorner2()
		glVertex2f( x+width, y) 
		self.texCorner3()
		glVertex2f( x+width, y+height)
		self.texCorner4()
		glVertex2f( x, y+height)
		glEnd()

		glPopMatrix()

class sprite_triangle(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		sprite.__init__(self,e, x0, y0,size,fing,param)
		self.ang1 = degree2rad*120.0
		self.ang2 = degree2rad*240.0
		self.init_noise()

	def getDimensions(self):
		return (self.size, self.size)

	def renderme(self):
		glPushMatrix()
		glTranslatef(self.centerx, self.centery, 0.0)
		a = self.get_aspect()
		glScale(a,1.0/a,1.0)
		glBegin(GL_POLYGON)

		(dx,dy) = self.getxysize_noaspect()

		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())
		self.vertexa(0.0+self.noisex0,dy+self.noisey0,0.0)
		self.vertexa(0.0+self.noisex1,dy+self.noisey1,120.0)
		# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
		self.vertexa(0.0+self.noisex2,dy+self.noisey2,240.0)
		self.vertexa(0.0+self.noisex0,dy+self.noisey0,0.0)

		glEnd()                      # We are done with the polygon

		glPopMatrix()

class sprite_triangle2(sprite_triangle):

	def __init__(self, e, x0, y0, size, fing, param):
		ang = ang + 180.0
		sprite_triangle.__init__(self,e, x0, y0,size,fing, param)

class sprite_triangleimage(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		sprite.__init__(self,e, x0, y0,size,fing,param)
		self.ang1 = degree2rad*120.0
		self.ang2 = degree2rad*240.0

	def renderme(self):
		glPushMatrix()
		glTranslatef(self.centerx, self.centery, 0.0)
		a = self.get_aspect()
		glScale(a,1.0/a,1.0)
		glBegin(GL_POLYGON)

		(dx,dy) = self.getxysize_noaspect()

		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())
		self.texCorner1()
		self.vertexa(0.0,dy,0.0)
		self.texCorner2()
		self.vertexa(0.0,dy,120.0)
		# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
		self.texCorner3()
		self.vertexa(0.0,dy,240.0)
		self.vertexa(0.0,dy,0.0)

		glEnd()                      # We are done with the polygon

		glPopMatrix()

class sprite_image(sprite):

	def __init__(self, e, x0, y0, size, fing, param):

		sprite.__init__(self,e, x0, y0,size,fing,param)
		l = updateimagelist("images")
		r = randimagetexture("images")
		r = loadImage("images/image2.png")
		if r == None:
			pass
			# print("No images? (image)")
		else:
			self.settexture(r)

	def isimage(self):
		return 1

	def renderme(self):

		if not self.hasTexture:
			return
		extrascale = 2.0
		glPushMatrix()
		glTranslatef(self.centerx, self.centery, 0.0)
		a = self.get_aspect()
		glScale(a,1.0/a,1.0)
		# glRotatef(self.ang,0.0,0.0,1.0)

		(dx,dy) = self.getxysize_noaspect()

		glScale(extrascale*dx,extrascale*dy,1.0)
		print "RENDER IMAGE"
		print "glScale ",extrascale*dx,extrascale*dy,1.0
		x = 0.0
		y = 0.0
		width = self.size
		height = self.size
		
		a = int(self.get_alpha() * 255)
		glColor4ub(255,255,255,a)
		print "glTranslate x0=",self.centerx," y0=",self.centery
		print "renderme image a=",a," x=",x," y=",y," width=",width," height=",height

		glBegin(GL_QUADS)
		self.texCorner1()
		glVertex2f( x, y)
		self.texCorner2()
		glVertex2f( x+width, y) 
		self.texCorner3()
		glVertex2f( x+width, y+height)
		self.texCorner4()
		glVertex2f( x, y+height)
		glEnd()

		glPopMatrix()

	def xmin(self):
		return self.centerx

	def xmax(self):
		return self.centerx + self.scalex * self.size

	def ymin(self):
		return self.centery

	def ymax(self):
		return self.centery + self.scaley * self.size

class sprite_image2(sprite):

	def __init__(self, e, x0, y0, size, fing, param):

		sprite.__init__(self,e, x0, y0,size,fing, param)
		r = randimagetexture("wordimages")
		if r == None:
			pass
			# print("No images? (image2)")
		else:
			self.settexture(r)

	def isimage(self):
		return 1

	def renderme(self):

		if not self.hasTexture:
			return
		extrascale = 2.0
		glPushMatrix()
		glTranslatef(self.centerx, self.centery, 0.0)
		# glRotatef(self.ang,0.0,0.0,1.0)
		glScale(extrascale*self.scalex,extrascale*self.scaley,1.0)
		x = 0.0
		y = 0.0
		width = self.size
		height = self.size
		
		a = int(self.get_alpha() * 255)
		glColor4ub(255,255,255,a)

		glBegin(GL_QUADS)
		self.texCorner1()
		glVertex2f( x, y)
		self.texCorner2()
		glVertex2f( x+width, y) 
		self.texCorner3()
		glVertex2f( x+width, y+height)
		self.texCorner4()
		glVertex2f( x, y+height)
		glEnd()

		glPopMatrix()

	def xmin(self):
		return self.centerx

	def xmax(self):
		return self.centerx + self.scalex * self.size

	def ymin(self):
		return self.centery

	def ymax(self):
		return self.centery + self.scaley * self.size


# class sprite_box(sprite):
# 
# 	def __init__(self, x0, y0, size, ang):
# 		sprite.__init__(self,x0, y0,size,ang)
# 
# 	def renderme(self):
# 		glPushMatrix()
# 		glTranslatef(self.centerx, self.centery, 0.0)
# 
# 		glBegin(GL_POLYGON)
# 
# 		dx = self.size * self.scalex / 2
# 		dy = self.size * self.scaley / 2
# 
# 		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())
# 		self.texCorner1()
# 		self.vertex(-dx,-dy)
# 		self.texCorner2()
# 		self.vertex(dx,-dy)
# 		self.texCorner3()
# 		self.vertex(dx,dy)
# 		glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
# 		self.texCorner4()
# 		self.vertex(-dx,dy)
# 		self.vertex(-dx,-dy)
# 
# 
# 		glEnd()                      # We are done with the polygon
# 
# 		glPopMatrix()
# 
# class sprite_box2(sprite_box):
# 
# 	def __init__(self, x0, y0, size, ang):
# 		ang = ang + 45.0
# 		sprite_box.__init__(self,x0, y0,size,ang)

class sprite_vbar(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		sprite.__init__(self,e, x0, y0,size,fing,param)
		
	def getDimensions(self):
		return (self.size, self.size)

	def ismovable(self):
		return 0

	def setspeed(self,movespeed,movedir,rotatespeed):
		sprite.setspeed(self,movespeed,movedir,0.0)

	def getdx(self):
 		return ( self.scalex * self.size / 3.0 )

	def renderme(self):

		glBegin(GL_POLYGON)

 		dx = self.getdx()
		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())

 		self.vertex_norotate(self.centerx,-0.5)
 		self.vertex_norotate(self.centerx,1.5)
		# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
 		self.vertex_norotate(self.centerx+dx,1.5)
 		self.vertex_norotate(self.centerx+dx,-0.5)
 		self.vertex_norotate(self.centerx,-0.5)

		glEnd()                      # We are done with the polygon

	def xmin(self):
		return self.centerx

	def xmax(self):
 		return self.centerx + self.getdx()

	def ymin(self):
		return 0.0

	def ymax(self):
		return 1.0


class sprite_hbar(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		sprite.__init__(self,e, x0, y0,size,fing,param)
		
	def getDimensions(self):
		return (self.size, self.size)

	def ismovable(self):
		return 0

	def setspeed(self,movespeed,movedir,rotatespeed):
		print "Should hbar ang in setspeed be 90?"
		sprite.setspeed(self,movespeed,movedir,0.0)

	def getdy(self):
 		return self.scaley * self.size / 3.0

	def renderme(self):

		glBegin(GL_POLYGON)

 		dy = self.getdy()
		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())

 		self.vertex_norotate(-0.5,self.centery)
 		self.vertex_norotate(1.5,self.centery)
		# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
 		self.vertex_norotate(1.5,self.centery+dy)
 		self.vertex_norotate(-0.5,self.centery+dy)
 		self.vertex_norotate(-0.5,self.centery)

		glEnd()                      # We are done with the polygon

	def ymin(self):
		return self.centery

	def ymax(self):
 		return self.centery + self.getdy()

	def xmin(self):
		return 0.0

	def xmax(self):
		return 1.0

class sprite_hbar2(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		self.left = random.randint(0,1)
		sprite.__init__(self,e, x0, y0,size,fing,param)
		
	def getDimensions(self):
		return (self.size, self.size)

	def ismovable(self):
		return 0

	def setspeed(self,movespeed,movedir,rotatespeed):
		sprite.setspeed(self,movespeed,movedir,0.0)

	def getdy(self):
 		return self.scaley * self.size / 3.0

	def getdx(self):
 		return self.scalex * self.size * 6

	def renderme(self):

		glBegin(GL_POLYGON)

 		dy = self.getdy()
		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())

		x = self.getdx()
		if self.left:
			self.vertex_norotate(0.0,self.centery)
			self.vertex_norotate(x,self.centery)
			# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
			self.vertex_norotate(x,self.centery+dy)
			self.vertex_norotate(0.0,self.centery+dy)
			self.vertex_norotate(0.0,self.centery)
		else:
			self.vertex_norotate(1.0,self.centery)
			self.vertex_norotate(1.0-x,self.centery)
			# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
			self.vertex_norotate(1.0-x,self.centery+dy)
			self.vertex_norotate(1.0,self.centery+dy)
			self.vertex_norotate(1.0,self.centery)

		glEnd()                      # We are done with the polygon

	def ymin(self):
		return self.centery

	def ymax(self):
 		return self.centery + self.getdy()

	def xmin(self):
		if self.left:
			return 0.0
		else:
			return 1.0-self.getdx()

	def xmax(self):
		if self.left:
			return self.getdx()
		else:
			return 1.0

class sprite_vbar2(sprite):

	def __init__(self, e, x0, y0, size, fing, param):
		self.up = random.randint(0,1)
		sprite.__init__(self,e, x0, y0,size,fing,param)
		
	def getDimensions(self):
		return (self.size, self.size)

	def ismovable(self):
		return 0

	def setspeed(self,movespeed,movedir,rotatespeed):
		sprite.setspeed(self,movespeed,movedir,0.0)

	def getdy(self):
 		return self.scaley * self.size * 6

	def getdx(self):
 		return self.scalex * self.size / 3.0

	def renderme(self):

		glBegin(GL_POLYGON)

 		dx = self.getdx()
		glColor4f(self.r1,self.g1,self.b1,self.get_alpha())

		y = self.getdy()
		if self.up:
			self.vertex_norotate(self.centerx,0.0)
			self.vertex_norotate(self.centerx,y)
			# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
			self.vertex_norotate(self.centerx+dx,y)
			self.vertex_norotate(self.centerx+dx,0.0)
			self.vertex_norotate(self.centerx,0.0)
		else:
			self.vertex_norotate(self.centerx,1.0)
			self.vertex_norotate(self.centerx,1.0-y)
			# glColor4f(self.r2,self.g2,self.b2,self.get_alpha())
			self.vertex_norotate(self.centerx+dx,1.0-y)
			self.vertex_norotate(self.centerx+dx,1.0)
			self.vertex_norotate(self.centerx,1.0)

		glEnd()                      # We are done with the polygon

	def ymin(self):
		if self.up:
			return 0.0
		else:
			return 1.0-self.getdy()

	def ymax(self):
		if self.up:
			return self.getdy()
		else:
			return 1.0

	def xmin(self):
		return self.centerx

	def xmax(self):
 		return self.centerx + self.getdx()

