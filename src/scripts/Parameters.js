
// -------------------------------------------------------------------------------
//                           The Parameter Object
// -------------------------------------------------------------------------------

var parameter = function(spec) {
    var that = {};

    // These are specified as part of the constructor
    that.name = spec.name;
    that.description = spec.description;

    that.default_value = spec.default_value || 0.0;
    if (spec.read_only !== undefined) {
	that.readonly = spec.read_only;
    } else {
	that.read_only = true;
    }

    // Create the global instance of this parameter
    GLOBAL[spec.name] = that.default_value;

    // Private members are set to default values
    _control_mode = "automation";
    _controller_timeout = 0.0;
    _last_time = 0.0;

    return that;
};

// -------------------------------------------------------------------------------
//                           READ/WRITE PARAMETERS
// -------------------------------------------------------------------------------
parameters = [


// decay = parameter({ name : "decay",
// 		    description : "0..1   controls the eventual fade to black; " + 
// 		                  "1=no fade, 0.9=strong fade, 0.98=recommended",
// 		    default_value : 0.98});

// invert = parameter({ name : "invert",
// 		     description : "0/1    inverts the colors in the image"});
		     
// gamma = parameter({ name : "gamma",
// 		    description : ">0     controls display brightness; " +
// 		                  "1=normal, 2=double, 3=triple, etc.",
// 		    default_value : 1.0});

 parameter({ name : "zoom",
	     description : "controls inward/outward motion.  " + 
	                   "0.9=zoom out 10% per frame, 1.0=no zoom, 1.1=zoom in 10%",
	     default_value : 1.0}),

 parameter({ name : "zoomexp",
	     description : ">0     controls the curvature of the zoom; 1=normal",
	     default_value : 1.0 }),

 parameter({ name : "rot",
	     description : "controls the amount of rotation.  " + 
	     "0=none, 0.1=slightly right, -0.1=slightly clockwise, 0.1=CCW" }),

 parameter({ name : "warp", 
	     description : "controls the magnitude of the warping; " + 
	     "0=none, 1=normal, 2=major warping..."}),
 
 parameter({ name : "warp_speed",
	     description : "controls the speed of the warping;",
	     default_value : 1.0 }),
 
 parameter({ name : "warp_scale",
	     description : "controls the size of the warp effects.",
	     default_value : 1.0 }),
 
 parameter({ name : "cx",
	     description : "0..1   controls where the center of rotation and " + 
	     "stretching is, horizontally.  0=left, 0.5=center, 1=right"}),
 
 parameter({ name : "cy",
	     description : "0..1   controls where the center of rotation and " + 
	     "stretching is, vertically.  0=left, 0.5=center, 1=right"}),
 
 parameter({ name : "dx",
	     description : "controls amount of constant horizontal motion; " + 
	     "-0.01 = move left 1% per frame, 0=none, 0.01 = move right 1%"}),
 
 parameter({ name : "dy",
	     description : "controls amount of constant vertical motion; " + 
	     "-0.01 = move up 1% per frame, 0=none, 0.01 = move down 1%"}),
 
 parameter({ name : "sx",
	     description : ">0     controls amount of constant horizontal stretching; " + 
	     " 0.99=shrink 1%, 1=normal, 1.01=stretch 1%",
	     default_value : 1.0 }),
 
 parameter({ name : "sy",
	     description : ">0     controls amount of constant vertical stretching; " + 
	     " 0.99=shrink 1%, 1=normal, 1.01=stretch 1%",
	     default_value : 1.0 }),
 
 parameter({ name : "q1",
	     description : "Used to carry information between the per-frame code " + 
	     "and per-pixel code." }),
 parameter({ name : "q2",
	     description : "Used to carry information between the per-frame code " + 
	     "and per-pixel code." }),
 parameter({ name : "q3",
	     description : "Used to carry information between the per-frame code " + 
	     "and per-pixel code." }),
 parameter({ name : "q4",
	     description : "Used to carry information between the per-frame code " + 
	     "and per-pixel code." }),
 parameter({ name : "q5",
	     description : "Used to carry information between the per-frame code " + 
	     "and per-pixel code." }),
 parameter({ name : "q6",
	     description : "Used to carry information between the per-frame code " + 
	     "and per-pixel code." }),
 parameter({ name : "q7",
	     description : "Used to carry information between the per-frame code " + 
	     "and per-pixel code." }),
 parameter({ name : "q8",
	     description : "Used to carry information between the per-frame code " + 
	     "and per-pixel code." })
 ];
