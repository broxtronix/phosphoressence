import math, random, sys

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
            self.initialize = empty_initialize

        if (per_frame_func):
            self.per_frame = per_frame_func
        else:
            self.per_frame = empty_per_frame

        if (per_pixel_func):
            self.per_pixel = per_pixel_func
        else:
            self.per_pixel = empty_per_pixel



#----------------------------------------------------------------------
#                          Global PePresets Object
#----------------------------------------------------------------------

# Preset management
class PePresets(object):

    def __init__(self):
        self._presets = []
        self._current_preset = 0

    def register(self, name, per_frame_func, init_func = None,  per_pixel_func = None):
        self._presets.append(Preset(name, per_frame_func, init_func, per_pixel_func))

    def current_preset(self):
        return self._presets[_current_preset]

    def next_preset(self):
        self._current_preset += 1
        if (self._current_preset >= len(self._presets)):
            self._current_preset = 0
        print("Switched forward to " + self._current_preset)


    def prev_preset(self):
        self._current_preset -= 1
        if (self._current_preset < 0):
            self._current_preset = len(self._presets)-1
        print("Switched back to " + self._current_preset)

    def random_preset(self):
        self._current_preset = int(math.random.uniform(0, len(self._presets)-1))
        print("Switched ramdomly to " + self._current_preset)

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

def sign(val):
    if (val > 0):
        return 1 
    elif (val == 0):
        return 0 
    else:
        return -1 

def sigmoid(val):
    print("WARNING : sigmoid() has not yet been implemented.\n")

def random_integer(val):
    return int(random.uniform(0,val))

def bor (val1, val2):
    if (val1 != 0 or val2 != 0):
        return 1.0 
    else:
        return 0.0 

def bnot (val):
    if (val != 0):
        return 0.0 
    else:
        return 1.0 

def equal (val1, val2):
    if (val1 == val2):
        return 1.0 
    else:
        return 0.0 

def above (val1, val2):
    if (val1 > val2):
        return 1.0 
    else:
        return 0.0 

def below (val1, val2):
    if (val1 < val2):
        return 1.0 
    else:
        return 0.0 
    
def if_milk (pred, cond1, cond2):
    if (pred):
        return cond1 
    else:
        return cond2 
    

