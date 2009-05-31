// Supplementary Functions
//
// These add a few additional mathematical functions that are used in
// presets.
function sqr(val) {
    return Math.pow(val,2);
}

function log10(val) {
    return Math.log(val)/Math.log(10);
}

function sign(val) {
    if (val > 0) { return 1; }
    else if (val == 0) { return 0; }
    else { return -1; }
}

function sigmoid(val) {
    print("WARNING : sigmoid() has not yet been implemented.\n");
}

function random_integer(val) {
    return Math.round(val * Math.random());
}

function bor (val1, val2) {
    if (val1 != 0 || val2 != 0) { return 1.0; }
    else { return 0.0; }
}

function bnot (val) {
    if (val != 0) { return 0.0; }
    else { return 1.0; }
}

function equal (val1, val2) {
    if (val1 == val2) { return 1.0; }
    else { return 0.0; }
}

function above (val1, val2) {
    if (val1 > val2) { return 1.0; }
    else { return 0.0; }
}

function below (val1, val2) {
    if (val1 < val2) { return 1.0; }
    else { return 0.0; }
}    

function if_milk (pred, cond1, cond2) {
    if (pred) { return cond1; }
    else { return cond2; }
}    

// Preset management
g_presets = new Array();
g_current_preset = 0;

function register_preset(preset) {
    g_presets.push(preset);
}

function current_preset() {
    return g_presets[g_current_preset];
}

function next_preset() {
    g_current_preset += 1;
    if (g_current_preset >= g_presets.length)
	g_current_preset = 0;
    print("Switched forward to " + g_current_preset);
}

function prev_preset() {
    g_current_preset -= 1;
    if (g_current_preset < 0)
	g_current_preset = g_presets.length-1;
    print("Switched back to " + g_current_preset);
}

function random_preset() {
    g_current_preset = Math.round(Math.random()*g_presets.length);
    print("Switched ramdomly to " + g_current_preset);
}
