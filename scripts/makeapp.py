#!/usr/bin/env python
#
# makeapp.py
#
# Takes a command line executable and build an Apple Style .app bundle
# for it by collecting necessary third party libraries.

import os;
import sys;

plist_text = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>CFBundleDevelopmentRegion</key>
        <string>English</string>
        <key>CFBundleExecutable</key>
        <string>PhosphorEssence</string>
        <key>CFBundleIdentifier</key>
        <string>com.yourcompany.test</string>
        <key>CFBundleInfoDictionaryVersion</key>
        <string>6.0</string>
        <key>CFBundleName</key>
        <string>PhosphorEssence</string>
        <key>CFBundlePackageType</key>
        <string>APPL</string>
        <key>CFBundleSignature</key>
        <string>????</string>
        <key>CFBundleVersion</key>
        <string>1.0</string>
        <key>NSMainNibFile</key>
        <string>MainMenu</string>
        <key>NSPrincipalClass</key>
        <string>NSApplication</string>
</dict>
</plist>
"""

def build_bundle_tree(executable, scripts, presets, appname):
    basedir = appname + ".app/Contents"

    try: os.makedirs(basedir + "/MacOS")
    except: pass
    try: os.makedirs(basedir + "/Resources")
    except: pass
    try: os.makedirs(basedir + "/Frameworks")
    except: pass
    try: os.makedirs(basedir + "/Resources/scripts")
    except: pass
    try: os.makedirs(basedir + "/Resources/presets")
    except: pass
    try: os.makedirs(basedir + "/Resources/shaders")
    except: pass

    os.system("cp " + executable + " " + basedir + "/MacOS/" + appname)
    os.system("cp -r " + presets + "/* " + basedir + "/Resources/presets")
    os.system("cp -r " + scripts + "/*.js " + basedir + "/Resources/scripts")
    os.system("cp -r " + shaders + "/*.glsl " + basedir + "/Resources/shaders")

    f = open(basedir + "/Info.plist","w")
    f.write(plist_text)
    f.close();

def fix_dylib_paths(name):
    libs = os.popen("otool -L " + name)
    for line in libs:
        if (line.find(":") == -1 and
            line.find("@executable_path") == -1 and 
            line.find("/System/Library/") == -1 and 
            line.find("/usr/lib") == -1 and
            line.find("/usr/X11") == -1):
            tokens = line.strip().split('(')

            # Handle Frameworks
            if (line.find("Framework") != -1):
                source_framework = line.strip().split(" ")[0]
                idx = source_framework.rfind(".framework")
                temp = source_framework[0:idx]
                idx2 = temp.rfind("/");
                dest_framework = "@executable_path/../Frameworks/" + source_framework[idx2+1:]
                print "\tReplacing " + source_framework + " with " + dest_framework
                os.system("install_name_tool -change " + source_framework + " " + dest_framework + " " + name)
                
            # Handle dylibs
            else:
                source_token = tokens[0]
                idx = source_token.rfind("/")
                dest_token = "@executable_path" + source_token[idx:]
                print "\tReplacing " + source_token + " with " + dest_token
                os.system("install_name_tool -change " + source_token + " " + dest_token + " " + name)

def install_libraries(executable, appname):
    base_name = appname + ".app/Contents/MacOS"
    app_exec = appname + ".app/Contents/MacOS/"+appname
    libs = os.popen("otool -L " + executable)
    for line in libs:
        if (line.find(":") == -1 and
            line.find("/System/Library/") == -1 and 
            line.find("/usr/lib") == -1 and
            line.find("/usr/X11") == -1):
            tokens = line.strip().split('(')

            # Handle Frameworks
            if (line.find("Framework") != -1):
                idx = tokens[0].find(".framework")
                source_framework = tokens[0][0:idx+10]
                print "Installing " + source_framework 
                os.system("cp -rf " + source_framework + " " + base_name + "/../Frameworks")

                # Ugh... gotta also fix the pathnames for frameworks!
                source_framework2 = line.strip().split(" ")[0]
                idx = source_framework2.rfind(".framework")
                temp = source_framework2[0:idx]
                idx2 = temp.rfind("/");
                dest_framework = base_name + "/../Frameworks/" + source_framework2[idx2+1:]
                fix_dylib_paths(dest_framework)

                # Delete debug libraries (if they exist). This helps
                # to keep the size of the app manageable.
                os.system("rm -f " + dest_framework+"_debug")

            # Handle dylibs
            else:
                source_lib = tokens[0]
                idx = source_lib.rfind("/")
                dest_id = "@executable_path" + source_lib[idx:]
                dest_lib = base_name + source_lib[idx:]
                print "Installing " + source_lib + " in " + dest_lib
                os.system("cp " + source_lib + " " + dest_lib)
                os.system("install_name_tool -id " + dest_id + " " + dest_lib)
                fix_dylib_paths(dest_lib)
    fix_dylib_paths(appname + ".app/Contents/MacOS/" + appname)
                
# MAIN
executable = "src/pe"
scripts = "src/StandardScripts"
shaders = "src/StandardShaders"
presets = "src/presets"
appname = "PhosphorEssence"
print "------------------------------------------------------"
print "        PhosphorEssence App Bundle Builder            "
print ""
print " Run this script from the top level of the source     "
print " tree.                                                "
print "------------------------------------------------------"
print ""
print "Building " + appname + ".app from " + executable

build_bundle_tree(executable, scripts, presets, appname)
install_libraries(executable, appname)
