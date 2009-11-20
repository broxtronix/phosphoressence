from parameters import pe
import math

class Binding(object):
    def __init__(self, controller, path, parameter, lo, hi, default_value, mode):
	self.controller = controller
	self.path = path
	self.parameter = parameter
	self.lo = lo
	self.hi = hi
	self.default_value = default_value
        pe.set_value(self.parameter, default_value)
        if (mode):
	    self.mode = mode
        else:
	    self.mode = "linear"

class PeBindings(object):
    def __init__(self, debug = False):
        self._bindings = {}
        self.DEBUG = False

        # Send updates from the controller to the parameters
    def controller_to_parameter(self, controller, path, value):
        for b in self._bindings.values():
            if (b.controller == controller and b.path == path):
	      
		# Mode == linear (the default)
		gain = b.hi - b.lo
		offset = b.lo
		param_val = gain*value + offset
                if (b.mode == "log10"):
		    gain = math.log10(b.hi) - math.log10(b.lo)
		    offset = math.log10(b.lo)
		    param_val = math.pow(10,gain*value + offset)
                if (self.DEBUG):
                    print("controller (" + path + ") : " + str(value) 
                          + "   -->   parameter (" + b.parameter + ") : " + str(param_val))
		pe.set_control_value(b.parameter, param_val)


    # Send updated paramater adjustments to the controller
    def parameter_to_controller(self, name, value):
        if (self._bindings.has_key(name)):
            binding = self._bindings[name]
	    gain = binding.hi - binding.lo
	    offset = binding.lo
	    control_value = (value - offset) / gain
            if (binding.mode == "log10"):
		gain = math.log10(binding.hi) - math.log10(binding.lo)
		offset = math.log10(binding.lo)
		control_value = (math.log10(value) - offset) / gain

	    if (control_value > 1.0): control_value = 1.0
            if (control_value < 0.0): control_value = 0.0
            if (self.DEBUG):
		print("parameter --> controller: " + name + " " + control_value 
		      + " " + binding.path)
            # binding.controller.send(binding.path, control_value)


    def add(self, controller, path, parameter, lo, hi, default_value = 0.0, mode = "linear"):
	self._bindings[parameter] = Binding(controller, path, parameter, lo, hi, default_value, mode)
	#        this.parameter_to_controller(parameter, default_value)

    def reset(self):
        for b in self._bindings:
	    pe.set_control_value(self._bindings[b].parameter, param_val)
            # self._bindings[b].controller.send(_bindings[b].path, 
	    # 				  _bindings[b].default_value)

