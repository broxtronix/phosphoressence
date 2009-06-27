from parameters import pe
import math, random, sys, os

#----------------------------------------------------------------------
#                               Preset Class
#----------------------------------------------------------------------
class Preset(object):

    def empty_initialize(self):
        pass

    def empty_per_frame(self):
        pass

    def empty_per_pixel(self):
        pass

    def __init__(self, name, per_frame_func, init_func = None, per_pixel_func = None):
        self.name = name

        if (init_func):
            self.initialize = init_func
        else:
            self.initialize = self.empty_initialize

        if (per_frame_func):
            self.per_frame = per_frame_func
        else:
            self.per_frame = self.empty_per_frame

        if (per_pixel_func):
            self.per_pixel = per_pixel_func
        else:
            self.per_pixel = self.empty_per_pixel

#----------------------------------------------------------------------
#                          Global PePresets Object
#----------------------------------------------------------------------

# Preset management
class PePresets(object):

    def __init__(self):
        self._presets = []
        self._current_preset = None
        self._current_index = 0

    def register(self, name, per_frame_func, init_func = None, per_pixel_func = None):
        p = Preset(name, per_frame_func, init_func, per_pixel_func)
        self._presets.append(p)
        if self._current_preset == None:
            self._current_preset = p
            self._current_index = len(self._presets) - 1

    def current_preset(self):
        return self._current_preset

    def next_preset(self):
        self._current_index += 1
        if (self._current_index >= len(self._presets)):
            self._current_index = 0
        try:
            self._current_preset = self._presets[self._current_index]
            print("[Preset " + str(self._current_index) + '] ' + self._current_preset.name)
        except (IndexError):
            self._current_preset = None
            print 'An unexpected error occurred when switching presets.'

    def prev_preset(self):
        self._current_index -= 1
        if (self._current_index < 0):
            self._current_index = len(self._presets)-1
        try:
            self._current_preset = self._presets[self._current_index]
            print("[Preset " + str(self._current_index) + '] ' + self._current_preset.name)
        except (IndexError):
            self._current_preset = None
            print 'An unexpected error occurred when switching presets.'

    def random_preset(self):
        self._current_index = int(math.random.uniform(0, len(self._presets)-1))
        try:
            self._current_preset = self._presets[self._current_index]
            print("[Preset " + str(self._current_index) + '] ' + self._current_preset.name)
        except (IndexError):
            self._current_preset = None
            print 'An unexpected error occurred when switching presets.'

    def size(self):
        return len(self._presets)

    # Loads all presets found in a directory.
    def load_directory(self, directory):
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
                
# Create an instance of the presets object
pe_presets = PePresets()

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
    

