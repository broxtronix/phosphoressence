import math, random

# Preset management
class PePresets(object):
    
    _presets = []
    _current_preset = 0

    def register(preset):
        _presets.append(preset)

    def current_preset():
        return _presets[_current_preset]

    def next_preset():
        _current_preset += 1
        if (_current_preset >= len(_presets)):
            _current_preset = 0
        print("Switched forward to " + _current_preset)


    def prev_preset():
        _current_preset -= 1
        if (_current_preset < 0):
            _current_preset = len(_presets)-1
        print("Switched back to " + _current_preset)

    def random_preset():
        _current_preset = int(math.random.uniform(0, len(_presets)-1))
        print("Switched ramdomly to " + _current_preset)

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
    

