#!/usr/bin/env python
#
# milk_to_pe.py
#
# This stand-alone script converts milkdrop preset files to
# PhosphorEssence python presets.  You can invoke it as follows:
#
#    TODO: show how to invoke script!! :)

import os
import sys
import glob
from parameters import pe

# Seperates a string into a list of tokens using a list of possible
# delimeters
def mystrip(string, delim_list):
    r = []
    s = string

    found_one = False
    for d in delim_list:
        idx = s.find(d)
        if ( idx != -1 ):
            r_sub1 = mystrip(s[0:idx], delim_list)
            r_sub2 = mystrip(s[idx+1:], delim_list)
            r.extend(r_sub1)
            r.extend(r_sub2)
            found_one = True
            break

    # Add the last bit of s to r and return it.
    if (not found_one and len(s) != 0):
        r.append(s)
    return r
        

def fix_variable_names(line):

    # First, we replace the wacky milkdrop names with names the names
    # of our parameters.
    l = line.replace("fRating", "fRating")
    l = l.replace("fGammaAdj", "gamma")
    l = l.replace("fDecay", "decay")
    l = l.replace("fVideoEchoZoom", "echo_zoom")
    l = l.replace("fVideoEchoAlpha", "echo_alpha")
    l = l.replace("nVideoEchoOrientation", "echo_orient")
    l = l.replace("nWaveMode", "wave_mode")
    l = l.replace("bAdditiveWaves", "wave_additive")
    l = l.replace("bWaveDots", "wave_usedots")
    l = l.replace("bModWaveAlphaByVolume", "bModWaveAlphaByVolume")
    l = l.replace("bMaximizeWaveColor", "wave_brighten")
    l = l.replace("bTexWrap", "wrap")
    l = l.replace("bDarkenCenter", "darken_center")
    l = l.replace("bMaximizeWaveColor", "wave_brighten")
    l = l.replace("bMotionVectorsOn", "bMotionVectorsOn")
    l = l.replace("bRedBlueStereo", "bRedBlueStereo")
    l = l.replace("nMotionVectorsX", "mv_x")
    l = l.replace("nMotionVectorsY", "mv_y")
    l = l.replace("bBrighten", "brighten")
    l = l.replace("bDarken", "darken")
    l = l.replace("bSolarize", "solarize")
    l = l.replace("bInvert", "invert")
    l = l.replace("fWaveAlpha", "wave_a")
    l = l.replace("fWaveScale", "fWaveScale")
    l = l.replace("fWaveSmoothing", "fWaveSmoothing")
    l = l.replace("fWaveParam", "wave_mystery")
    l = l.replace("fModWaveAlphaStart", "fModWaveAlphaStart")
    l = l.replace("fModWaveAlphaEnd", "fModWaveAlphaEnd")
    l = l.replace("fWarpAnimSpeed", "warp_speed")
    l = l.replace("fWarpScale", "warp_scale")
    l = l.replace("fZoomExponent", "zoomexp")
    l = l.replace("fShader", "fShader")

    # Next, we need to prefix all of the parameters with 'pe.'
    tokens = mystrip(l, ['=', ' ', '+', '-', '*', '/', '%', '(', ')', '[', ']', ';', ','])
    params = pe.param_list()
    for p in params:
        t = l.find(p)
        if (t != -1 and tokens.count(p) > 0):
            l = l.replace(p, "pe." + p)

    # ... and math function with 'math.'
    mathfuncs = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sqr', 'sqrt',
                 'pow', 'log', 'log10', 'sign', 'sigmoid', 'rand', 'bor', 'bnot',
                 'equal', 'above', 'below']
    for f in mathfuncs:
        t = l.find(f)
        if (t != -1 and tokens.count(f) > 0):
            l = l.replace(f, "math." + f)

    # Replace any c-style comments with python style comments
    l = l.replace('//', '#')
    l = l.replace(';;', ';')

    return l

def fix_standard_objects(line):
    l = line.replace("if", "if_milk")
    l = l.replace("int", "math.floor")
    l = l.replace("rand", "math.random_integer")
    l = l.replace("abs", "math.fabs")
    return l

def fix_syntax_pf(line):
    if line.find("[preset") >= 0:
        return ""
    elif line.find("per_frame") >= 0:
        idx = line.find("=")
        return line[idx+1:].strip() + "\n";
    elif line.find("per_pixel") >= 0:
        return ""
    else:
        return line.strip() + "\n"

def fix_syntax_pp(line):
    if line.find("per_pixel") >= 0:
        idx = line.find("=")
        return line[idx+1:].strip() + "\n";
    else:
        return ""

def write_per_frame(pe_file, milk_file):
    milk_file.seek(0)
    numlines = 0
    for l in milk_file:
        l2 = fix_syntax_pf(l)
        l2 = fix_standard_objects(l2)
        l2 = fix_variable_names(l2)
        if (l2 != ""):
            pe_file.write( '        ' + l2 )
            numlines += 1
    if (numlines == 0):
            pe_file.write( '        pass\n' )

def write_per_pixel(pe_file, milk_file):
    milk_file.seek(0)
    numlines = 0
    for l in milk_file:
        l2 = fix_syntax_pp(l)
        l2 = fix_standard_objects(l2)
        l2 = fix_variable_names(l2)
        if (l2 != ""):
            pe_file.write( '        ' + l2 )
            numlines += 1
    if (numlines == 0):
            pe_file.write( '        pass\n' )

# -----------------------------------------------------------------------
#                               MAIN
# -----------------------------------------------------------------------
files = glob.glob("Geiss*.milk")

for f in files:
    idx = f.rfind(".");
    preset_name = f[0:idx]
    preset_name = preset_name.replace(" - ","__")
    preset_name = preset_name.replace(" ","_")
    preset_name = preset_name.replace("-","_")
    preset_name = preset_name.replace("!","")
    preset_name = preset_name.replace("(","")
    preset_name = preset_name.replace(")","")
    preset_name = preset_name.replace("&","and")
    preset_name = preset_name.replace("\'","")
    preset_name = preset_name.replace("\"","")
    print "Processing: " + preset_name

    milk_file = open(f)
    pe_file = open(preset_name + ".pe","w")

    # Write the class declaration
    pe_file.write('from presets import PePreset\n\n')
    pe_file.write('class ' + preset_name + '(PePreset):\n\n')

    # Write the preset name
    pe_file.write('    name = \'' + preset_name + '\'\n\n')

    # Write the per-frame equations
    pe_file.write('\n    def per_frame(self):\n')
    write_per_frame(pe_file, milk_file);

    # Write the per_pixel equations
    pe_file.write('\n    def per_pixel(self):\n')
    write_per_pixel(pe_file, milk_file);

    # Close both files
    milk_file.close()
    pe_file.close()

