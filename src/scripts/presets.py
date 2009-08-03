from parameters import pe
import math, random, sys, os

#----------------------------------------------------------------------
#                          PePreset Class
#----------------------------------------------------------------------

# The following idiom registers presets automatically when they are
# declared as a subclass of PePreset.  This is very handy, because it
# allows us to "load" presets simply by defining them as classes.  The
# code here is based off of an example in Ch. 2 of "Pro Django" by
# Marty Alchin.
class PresetMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'presets'):
            # This branch only executes when processing the moint point
            # itself.  It sets up an empty lists where presets will go.
            cls.presets = []
            cls.current_preset_index = 0
            cls.current_preset_instance = 0
        else:
            # This branch is executed for preset implementations.
            # Each one registers itself in the preset list.
            cls.presets.append(cls)



# This is the superclass for all PhosphorEssence presets.  User
# presets must subclass from this class.  Once they have done so, they
# can overide one of the instance methods defined below.
class PePreset(object):

    # Return the ID of the currently running preset
    @classmethod
    def current_preset(cls):
        return cls.current_preset_instance

    @classmethod
    def select_preset(cls):
        try:
            cls.current_preset_instance = cls.presets[cls.current_preset_index]()
            print("[Preset " + str(cls.current_preset_index) +
                  " : " + cls.current_preset().name + '] ')
        except(IndexError):
            print 'An unknown error occured when changing presets.'
        

    # Next preset
    @classmethod
    def next_preset(cls):
        cls.current_preset_index += 1
        if (cls.current_preset_index >= len(cls.presets)):
            cls.current_preset_index = 0
        cls.select_preset()

    # Previous Preset
    @classmethod
    def prev_preset(cls):
        cls.current_preset_index -= 1
        if (cls.current_preset_index < 0):
            cls.current_preset_index = len(cls.presets)-1
        cls.select_preset()

    # Random Preset
    def random_preset(cls):
        cls.current_preset_index = int(math.random.uniform(0, len(cls.presets)-1))
        print("[Preset " + str(cls.current_preset_index) +
              " : " + str(cls.current_preset()) + '] ')
        cls.select_preset()

    # Loads all presets found in a directory.
    @classmethod
    def load_directory(cls, directory):
        import glob

        print 'Loading presets directory: ' + directory
        preset_files = glob.glob(directory + '/*.pe')
        for f in preset_files:
            print '\t--> loading ' + f
            try:
                execfile(f)
            except:
                print '\t ** Failed to load ' + f
                for ei in sys.exc_info():
                    print '\t    ' + str(ei)

    # -------------- CLASS INSTANCE METHODS -----------------
    #
    # You can override these in the subclass to implement a
    # PhosphorEssence plugin.

    def initialize(self):
        pass

    def per_frame(self):
        pass

    def per_vertex(self):
        pass

    def render(self):
        pass

    # Set up the auto-registering behavior using a metaclass.
    __metaclass__ = PresetMount
                
#----------------------------------------------------------------------
#                        Supplementary Functions
#----------------------------------------------------------------------
#
# These add a few additional mathematical functions that are used in
# some presets.  Most of these are for backwards compatibility with
# milkdrop preset files.

def sqr(val): 
    return math.pow(val,2)
math.sqr = sqr

def sign(val):
    if (val > 0):
        return 1 
    elif (val == 0):
        return 0 
    else:
        return -1
math.sign = sign

def sigmoid(val):
    print("WARNING : sigmoid() has not yet been implemented.\n")
math.sigmoid = sigmoid

def random_integer(val):
    return int(random.uniform(0,val))
math.random_integer = random_integer

def bor (val1, val2):
    if (val1 != 0 or val2 != 0):
        return 1.0 
    else:
        return 0.0 
math.bor = bor

def bnot (val):
    if (val != 0):
        return 0.0 
    else:
        return 1.0 
math.bnot = bnot

def equal (val1, val2):
    if (val1 == val2):
        return 1.0 
    else:
        return 0.0 
math.equal = equal

def above (val1, val2):
    if (val1 > val2):
        return 1.0 
    else:
        return 0.0
math.above = above

def below (val1, val2):
    if (val1 < val2):
        return 1.0 
    else:
        return 0.0 
math.below = below
    
def if_milk (pred, cond1, cond2):
    if (pred):
        return cond1 
    else:
        return cond2 
    

