class path:

	def __init__(self):
		self.points = []
		self.deleteme = False

class segment:

	def __init__(self,x,y):
		self.weight = 1.0
		self.pos = (x,y)

	def setweight(self,f):
		self.weight = f
