
import math
import sys
import traceback
import os
import os.path
import shutil
# import pygame
import time
import string

from random import randint
from math import pi

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

Clipart_drive = "c:"
Clipart = []
Clipart_word = ""
Clipart_sofar = 0
Clipart_len = 0
Clipart_dowork = 0

twopi = 2.0*pi
degree2rad = twopi/360.0
rad2degree = 360.0/twopi

gTextures = {} # textures that have been loaded 
imageList = {"images":[],"imagestage":[],"textures":[],"wordimages":[]}
imageDirMtime = {"images":0,"imagestage":0,"textures":0}

def loadClipartList():
	global Clipart, Clipart_sofar, Clipart_len, Clipart_dowork
	if len(Clipart) != 0:
		return
	f = open("png.list","r")
	while 1:
		line = f.readline()
		if not(line):
			break
		i = line.lower().strip()
		Clipart.append(i)
	f.close()
	print("Clipart list has been loaded, length=",len(Clipart))
	
def getwordimages(word):
	global Clipart, Clipart_sofar, Clipart_len, Clipart_dowork, Clipart_word
	loadClipartList()
	imageList["wordimages"] = []
	Clipart_word = word
	Clipart_len = len(Clipart)
	Clipart_sofar = 0
	Clipart_dowork = 1
	print "LOOKING FOR ",word," Clipart_len=",Clipart_len," time=",time.clock()

def clipartwork():
	global Clipart, Clipart_sofar, Clipart_len, Clipart_dowork, Clipart_word
	if Clipart_dowork == 0:
		return
	cnt = 0
	while Clipart_sofar < Clipart_len and cnt < 10000:
		cnt += 1
		line = Clipart[Clipart_sofar]
		Clipart_sofar += 1
		i = line.find(Clipart_word)
		if i >= 0:
			global Clipart_drive
			fname1 = Clipart_drive+"/Clipart_png/"+line
			imageList["wordimages"].append(fname1)
	if Clipart_sofar >= Clipart_len:
		print("wordimages = ",len(imageList["wordimages"]))
		Clipart_dowork = 0

def filelist(dir,list=None,suffix=""):

	if list == None:
		list = []
	ls = os.listdir(dir)
	for i in ls:
		d = os.path.join(dir,i)
		if i.endswith(suffix):
			list.append(d)
		if os.path.isdir(d):
			filelist(d,list,suffix)
	return list

def pnglist(dir,list=None):
	return filelist(dir,list,".png")

def updateimagelist(dir):
	global imageList, imageDirMtime
	dirmtime = os.path.getmtime(dir)
	if imageDirMtime[dir] < dirmtime:
		imageList[dir] = filelist(dir,suffix=".png")
		imageDirMtime[dir] = dirmtime
	return len(imageList[dir])

def loadImage(filename):
	print "loadImage disabled...\n"
	return None
# 	"""load or lookup an image and return the OpenGL Handle to it.    
# 	 *** this is in internal method ***
# 	"""
# 	global gTextures
# 	if gTextures.has_key(filename):
# 	    return gTextures[filename]
# 
# 	# Load the texture into memory
# 	surface = pygame.image.load(filename)
# 	surface = pygame.transform.flip(surface,0,1)
# 	data = pygame.image.tostring(surface, "RGBA", 1)
# 	ix = surface.get_width()
# 	iy = surface.get_height()
# 	print "LOADIMAGE ix,iy=",ix,iy
# 
# 	# Create the OpenGL Texture
# 	texture = glGenTextures(1)
# 	glBindTexture(GL_TEXTURE_2D, texture)   # 2d texture (x and y size)
# 	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
# 	try:
# 		glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
# 	except OpenGL.GL.GLerror:
# 		print("Bad data in filename=",filename)
# 		return
# 	bf = glGetTexParameterfv(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER)
# 	print "bf=",bf
# 	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
# 	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
# 	if bf != None:
# 		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, bf)
#  
# 	# add the texture to global dictionary
# 	gTextures[filename] = texture
# 
# 	return texture

def randimagetexture(dir):
	l = len(imageList[dir])
	if l == 0:
		return None
	r = randint(0,l-1)
	return loadImage(imageList[dir][r])
    
def loadallimagetexture(dir):
	print("LOADING ALL IMAGES in dir=",dir)
	for i in range(len(imageList[dir])):
		loadImage(imageList[dir][i])
    
def randtexturetexture(dir):
	# onetimeload(dir)
	l = len(textureList)
	if l == 0:
		return None
	r = randint(0,l-1)
	return loadImage(textureList[r])
    
# Words = ("Mark","Herb","Sam","Richard","Kate","Micah","Doug","Melissa","Andrew","Shawn","Tim")
Words = ["dud"]
Faces = ("comic sans ms","courier","impact","arial","times")

def wordlist():
	return Words

def randword():
	n = len(Words)
	if n == 0:
		return ""
	else:
		return Words[randint(0,n-1)]

def addword(w):
	Words.insert(0,w)

def clearwords(prefix):
	toremove = []
	for i in range(len(Words)):
		s = Words[i]
		s = s[0:len(prefix)]
		if s == prefix:
			toremove.insert(0,Words[i])
	for i in range(len(toremove)):
		print("Removing word=",toremove[i])
		Words.remove(toremove[i])

def facelist():
	return Faces

def randface():
	i = randint(0,len(Faces)-1)
	return Faces[i]

def indexofface(f):
	for i in Faces:
		if f == Faces[i]:
			return i
	return -1

def indexedface(i):
	if i >= len(Faces):
		return ""
	else:
		return Faces[i-1]

def formatExceptionInfo(maxTBlevel=16):
	cla, exc, trbk = sys.exc_info()
	excName = cla.__name__
	try:
		excArgs = exc.__dict__["args"]
	except KeyError:
		excArgs = "<no args>"
	excTb = traceback.format_tb(trbk, maxTBlevel)
	return (excName, excArgs, excTb)


class HLS:

	def __init__(self,h,l,s):
		self._hue = h
		self._luminance	= l
		self._saturation = s
		self._red = 0
		self._green = 0
		self._blue = 0
		self._ToRGB()

	def rgb(self):
		return(self._red/255.0,self._green/255.0,self._blue/255.0)

	def hls(self):
		return(self._hue,self._luminance,self._saturation)

	def setrgb(self,r,g,b):
		self._red = r
		self._green = g
		self._blue = b
		self._ToHLS()

	def sethls(self,h,l,s):
		self._hue = h
		self._luminance = l
		self._saturation = s
		self._ToRGB();

	def _ToHLS():
		minval = Math.min(self._red, Math.min(self._green, self._blue));
		maxval = Math.max(self._red, Math.max(self._green, self._blue));
		mdiff = maxval-minval;
		msum = maxval + minval;
		self._luminance = msum / 510;
		if maxval == minval:
			self._saturation = 0
			self._hue = 0
		else:
			rnorm = (maxval - _red) / mdiff;
			gnorm = (maxval - _green) / mdiff;
			bnorm = (maxval - _blue) / mdiff;
			if self._luminance <= .5:
				self._saturation = mdiff/msum
			else:
				self._saturation = mdiff / (510 - msum)
			# self._saturation = (self._luminance <= .5) ? (mdiff/msum) : (mdiff / (510 - msum));
			if self._red == maxval:
				self._hue = 60 * (6 + bnorm - gnorm)
			elif self._green == maxval:
				self._hue = 60 * (2 + rnorm - bnorm)
			elif self._blue == maxval:
				self._hue = 60 * (4 + gnorm - rnorm)
			self._hue %= 360;

	def _ToRGB(self):
		if self._saturation == 0:
			self._red = self._green = self._blue = self._luminance * 255
			
		else:
			if self._luminance <= 0.5:
				rm2 = self._luminance + self._luminance * self._saturation
			else:
				rm2 = self._luminance + self._saturation - self._luminance * self._saturation
			rm1 = 2 * self._luminance - rm2;
			self._red = self._ToRGB1(rm1, rm2, self._hue + 120);
			self._green = self._ToRGB1(rm1, rm2, self._hue);
			self._blue = self._ToRGB1(rm1, rm2, self._hue - 120);

	def _ToRGB1(self, rm1, rm2, rh):
		if rh > 360:
			rh -= 360
		elif rh < 0:
			rh += 360

		if rh < 60:
			rm1 = rm1 + (rm2 - rm1) * rh / 60
		elif rh < 180:
			rm1 = rm2
		elif rh < 240:
			rm1 = rm1 + (rm2 - rm1) * (240 - rh) / 60
		return(rm1 * 255)
