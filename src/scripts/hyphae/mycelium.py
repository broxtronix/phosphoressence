from parameters import pe
import math, time
from random import random

class Mycelium(object):

    def __init__(self):
        hyphae = []


    def spawn(self, x, y):
        hypha.append( Hyphae(x,y) )


    # pass the list of hypha to each hyphae
    def render(self):
        for h in hypha:
            h.render(hypha); 

class Hyphae(object):

    # Initialize a hyphae with the specified center location.
    def __init__(self, x, y):
        self.center = [x, y]
        self.tendrils = []

        for i in range(1,30*random()):
            self.add_tendril( Tendril(x,y,2,1.0) )

    # We pass in the complete list of hypha so that hyphae children
    # can access those center loctaions.
    def render(self, hypha):
        for t in self.tendrils:
            t.render(hypha)

    def add_tendril(self, tendril):
        self.tendrils.append(tendril)
            
