#!/usr/bin/env python
#
# milk_to_js.py
#
# This script converts milkdrop preset files to PhosphorEssence
# javascript presets

import os;
import sys;
import glob;

def fix_strange_variable_names(line):
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
    return l

def fix_standard_objects(line):
    l = line.replace("if", "if_milk")
    l = l.replace("int", "floor")
    l = l.replace("rand", "random_integer")
    return l

def fix_syntax(line):
    if line.find("[preset") >= 0:
        return ""
    elif line.find("per_frame") >= 0:
        idx = line.find("=")
        return "    " + line[idx+1:].strip() + "\n";
    elif line.find("per_pixel") >= 0:
        return "    // " + line.strip() + "\n";
    else:
        return "    " + line.strip() + ";\n"

# MAIN
files = glob.glob("*.milk")
master_file = open("milk_presets.js","w")

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
    js_file = open(preset_name + ".js","w")
    js_file.write("function " + preset_name + "() {\n")
    js_file.write("  with (Math) {\n");
    for l in milk_file:
        l2 = fix_syntax(l)
        l2 = fix_standard_objects(l2)
        l2 = fix_strange_variable_names(l2)
        js_file.write( l2 )
    js_file.write("  }\n}\n");
    js_file.write("register_preset( " + preset_name + ");\n");

    milk_file.close()
    js_file.close()

    master_file.write("print(\"Loading " + preset_name + ".js\");\n");
    master_file.write("load(\"/Users/mbroxton/projects/PhosphorEssence/src/presets/milkdrop/" + preset_name + ".js\");\n");

master_file.close();
