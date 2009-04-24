function Bindings() {
    var m_bindings = new Array();
    function Binding(controller, path, parameter, lo, hi, default_value, mode) {
	this.controller = controller;
	this.path = path;
	this.parameter = parameter;
	this.lo = lo;
	this.hi = hi;
	this.default_value = default_value;
	if (mode) {
	    this.mode = mode;
	} else
	    this.mode = "linear";
    }

    // Send updates from the controller to the parameters
    this.controller_to_parameter = function(controller, path, value) {
	for (var b in m_bindings) {
	    match = m_bindings[b];
	    if (match.controller == controller && match.path == path) {
		// Mode == linear (the default)
		gain = match.hi - match.lo;
		offset = match.lo;
		param_val = gain*value + offset;
		if (match.mode == "log10") {
		    gain = Math.log(match.hi)/Math.log(10.0) - Math.log(match.lo)/Math.log(10.0);
		    offset = Math.log(match.lo)/Math.log(10.0);
		    param_val = Math.pow(10,gain*value + offset);
		}
		if (debug)
		    print("controller (" + path + ") : " + value 
			  + "   -->   parameter (" + match.parameter + ") : " + param_val);
		p.set(m_bindings[b].parameter, param_val);
	    }
	}
    }

    // Send updated paramater adjustments to the controller
    this.parameter_to_controller = function(name, value) {
	if (binding = m_bindings[name]) {
	    gain = binding.hi - binding.lo;
	    offset = binding.lo;
	    control_value = (value - offset) / gain;
	    if (binding.mode == "log10") {
		gain = Math.log(binding.hi)/Math.log(10.0) - Math.log(binding.lo)/Math.log(10.0);
		offset = Math.log(binding.lo)/Math.log(10.0);
		control_value = (Math.log(value)/Math.log(10.0) - offset) / gain;
	    }

	    if (control_value > 1.0) control_value = 1.0;
	    if (control_value < 0.0) control_value = 0.0;
	    if (debug)
		print("parameter --> controller: " + name + " " + control_value 
		      + " " + binding.path);
	    binding.controller.send(binding.path, control_value);
	}
    }

    this.add = function(controller, path, parameter, lo, hi, default_value, mode) {
	m_bindings[parameter] = new Binding(controller, path, parameter, lo, hi, default_value, mode);
	//        this.parameter_to_controller(parameter, default_value);
    }

    this.reset = function() {
	for (var b in m_bindings) {
	    p.set(m_bindings[b].parameter, param_val);
	    // m_bindings[b].controller.send(m_bindings[b].path, 
	    // 				  m_bindings[b].default_value);
	}
    }
}
