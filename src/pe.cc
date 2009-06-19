// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file pe.cc
///
/// PhosphorEssence
/// An audio and video delight.
///

// Qt
#include <QApplication>
#include <QWidget>

// // VW
#include <vw/Core.h>
#include <vw/Image.h>
#include <vw/Math.h>
#include <vw/FileIO.h>
#include <vw/Stereo.h>

// Local files
#include <MainWindow.h>
#include <AudioEngine.h>
#include <GraphicsEngine.h>
#include <ScriptEngine.h>
#include <PeParameters.h>
#include <OscController.h>
#include <MidiController.h>
#include <JoystickController.h>
#include <OScopeShape.h>
#include <VectorShape.h>
#include <PhasescopeShape.h>
#include <SpectrographShape.h>

using namespace vw;

void setup_parameters() {
  // -------------------------------------------------------------------------------
  //                           READ-ONLY PARAMETERS
  //
  // These are listed here first since the parameter list is search in
  // the order that paramaters are added.
  // -------------------------------------------------------------------------------
  pe_parameters().add_parameter("x", true, 0.0,
                                "Retrieves the x-position of the current pixel (for per-pixel equations)");
  pe_parameters().add_parameter("y", true, 0.0,
                                "Retrieves the x-position of the current pixel (for per-pixel equations)");
  pe_parameters().add_parameter("rad", true, 0.0,
                                "Retrieves the x-position of the current pixel (for per-pixel equations)");
  pe_parameters().add_parameter("ang", true, 0.0,
                                "Retrieves the x-position of the current pixel (for per-pixel equations)");
  pe_parameters().add_parameter("time", true, 0.0,
                                "(readonly) retrieves the current time, in seconds, since PhosphorEssence started running");
  pe_parameters().add_parameter("fps", true, 30.0,
                                ">0 (readonly)       retrieves the current framerate, in frames per second.");
  pe_parameters().add_parameter("frame", true, 0.0,
                                "(readonly) retrieves the number of frames of animation elapsed since the program started");
  // pe_parameters().add_parameter("progress", true, 0.0,
  //                               "0..1 (readonly)     progress through the current preset; if preset was just loaded, this is closer to 0; if preset is about to end, this is closer to 1."
  //                               "-note that if Scroll Lock is on, 'progress' will freeze!");


  pe_parameters().add_parameter("bass", true, 0.0,
                                ">0 (readonly)       retrieves the current amount of bass.  1 is normal; below ~0.7 is quiet; above ~1.3 is loud bass");
  pe_parameters().add_parameter("mid", true, 0.0,
                                ">0 (readonly)         -same, but for mids (middle frequencies)");
  pe_parameters().add_parameter("treb", true, 0.0,
                                ">0 (readonly)         -same, but for treble (high) frequencies");
  pe_parameters().add_parameter("bass_att", true, 0.0,
                                ">0 (readonly)       retrieves an attenuated reading on the bass, meaning that it is damped in time and doesn't change so rapidly.");
  pe_parameters().add_parameter("mid_att", true, 0.0,
                                ">0 (readonly)         -same, but for mids (middle frequencies)");
  pe_parameters().add_parameter("treb_att", true, 0.0,
                                ">0 (readonly)         -same, but for treble (high) frequencies");

  pe_parameters().add_parameter("bass_r", true, 0.0,
                                ">0 (readonly)       retrieves the current amount of bass.  1 is normal; below ~0.7 is quiet; above ~1.3 is loud bass");
  pe_parameters().add_parameter("mid_r", true, 0.0,
                                ">0 (readonly)         -same, but for mids (middle frequencies)");
  pe_parameters().add_parameter("treb_r", true, 0.0,
                                ">0 (readonly)         -same, but for treble (high) frequencies");
  pe_parameters().add_parameter("bass_att_r", true, 0.0,
                                ">0 (readonly)       retrieves an attenuated reading on the bass, meaning that it is damped in time and doesn't change so rapidly.");
  pe_parameters().add_parameter("mid_att_r", true, 0.0,
                                ">0 (readonly)         -same, but for mids (middle frequencies)");
  pe_parameters().add_parameter("treb_att_r", true, 0.0,
                                ">0 (readonly)         -same, but for treble (high) frequencies");


  pe_parameters().add_parameter("meshx", true, 0.0,
                                "8-128 (readonly)  tells you the user's mesh size in the X direction.  always an integer value.");
  pe_parameters().add_parameter("meshy", true, 0.0,
                                "6-96   tells you the user's mesh size in the Y direction.  always an integer value.");


  // -------------------------------------------------------------------------------
  //                           READ/WRITE PARAMETERS
  // -------------------------------------------------------------------------------

  pe_parameters().add_parameter("decay", false, 0.98,
                                "0..1   controls the eventual fade to black; 1=no fade, 0.9=strong fade, 0.98=recommended");
  pe_parameters().add_parameter("invert", false, 0.0,
                                "0/1    inverts the colors in the image");
  pe_parameters().add_parameter("gamma", false, 1.0,
                                ">0     controls display brightness; 1=normal, 2=double, 3=triple, etc.");

  // pe_parameters().add_parameter("zoom", false, 1.0, 
  //                               "controls inward/outward motion.  0.9=zoom out 10% per frame, 1.0=no zoom, 1.1=zoom in 10%");
  // pe_parameters().add_parameter("zoomexp", false, 1.0, 
  //                               ">0     controls the curvature of the zoom; 1=normal");
  // pe_parameters().add_parameter("rot", false, 0.0,
  //                               "controls the amount of rotation.  0=none, 0.1=slightly right, -0.1=slightly clockwise, 0.1=CCW");
  // pe_parameters().add_parameter("warp", false, 0.0, 
  //                               "controls the magnitude of the warping; 0=none, 1=normal, 2=major warping...\n");
  // pe_parameters().add_parameter("warp_speed", false, 1.0, 
  //                               "controls the speed of the warping;");
  // pe_parameters().add_parameter("warp_scale", false, 1.0, 
  //                               "controls the size of the warp effects.");
  // pe_parameters().add_parameter("cx", false, 0.0, 
  //                               "0..1   controls where the center of rotation and stretching is, horizontally.  0=left, 0.5=center, 1=right");
  // pe_parameters().add_parameter("cy", false, 0.0,
  //                               "0..1   controls where the center of rotation and stretching is, vertically.  0=top, 0.5=center, 1=bottom");
  // pe_parameters().add_parameter("dx", false, 0.0, 
  //                               "controls amount of constant horizontal motion; -0.01 = move left 1% per frame, 0=none, 0.01 = move right 1%");
  // pe_parameters().add_parameter("dy", false, 0.0,
  //                               "controls amount of constant vertical motion; -0.01 = move up 1% per frame, 0=none, 0.01 = move down 1%");
  // pe_parameters().add_parameter("sx", false, 1.0,
  //                               ">0     controls amount of constant horizontal stretching; 0.99=shrink 1%, 1=normal, 1.01=stretch 1%");
  // pe_parameters().add_parameter("sy", false, 1.0,
  //                               ">0     controls amount of constant vertical stretching; 0.99=shrink 1%, 1=normal, 1.01=stretch 1%");



  pe_parameters().add_parameter("wave_mode", false, 0, 
                                "0,1,2,3,4,5,6,7  controls which of the 8 types of waveform is drawn");
  pe_parameters().add_parameter("wave_x", false, 0.5,
                                "position of the waveform: 0 = far left edge of screen, 0.5 = center, 1 = far right");
  pe_parameters().add_parameter("wave_y", false, 0.5,
                                "position of the waveform: 0 = very bottom of screen, 0.5 = center, 1 = top");
  pe_parameters().add_parameter("wave_r", false, 0.0,
                                "amount of red color in the wave (0..1)");
  pe_parameters().add_parameter("wave_g", false, 1.0,         
                                "amount of green color in the wave (0..1)");
  pe_parameters().add_parameter("wave_b", false, 0.0, 
                                "amount of blue color in the wave (0..1)");
  pe_parameters().add_parameter("wave_a", false, 1.0, 
                                "opacity of the wave (0..1) [0=transparent, 1=opaque]");
  // pe_parameters().add_parameter("wave_mystery", false, 0.0,
  //                               "-1..1  what this parameter does is a mystery.  (honestly, though, this value does different things for each "
  //                               "waveform; for example, it could control angle at which the waveform was drawn.)");
  pe_parameters().add_parameter("wave_usedots", false, 0.0,
                                "0/1    if 1, the waveform is drawn as dots (instead of lines)");
  pe_parameters().add_parameter("wave_thick", false, 1.0,
                                "0/1    if 1, the waveform's lines (or dots) are drawn with double thickness");
  // pe_parameters().add_parameter("wave_additive", false, 0.0,
  //                               "if 1, the wave is drawn additively, saturating the image at white");
  pe_parameters().add_parameter("wave_brighten", false, 1.0, 
                                "0/1    if 1, all 3 r/g/b colors will be scaled up until at least one reaches 1.0");
  pe_parameters().add_parameter("wave_enabled", false, 0.0,
                                "Enable the audio waveform rendered on screen.");
  pe_parameters().add_parameter("wave_frequency", false, 0.1,
                                "Frequency of the waveshape drawing loop.");

  // // Outer border
  // pe_parameters().add_parameter("ob_size", false, 0.01,
  //                               "0..0.5 thickness of the outer border drawn at the edges of the screen every frame");
  // pe_parameters().add_parameter("ob_r", false, 0.0,
  //                               "0..1   amount of red color in the outer border");
  // pe_parameters().add_parameter("ob_g", false, 0.0,
  //                               "0..1   amount of green color in the outer border");
  // pe_parameters().add_parameter("ob_b", false, 0.0,
  //                               "0..1   amount of blue color in the outer border");
  // pe_parameters().add_parameter("ob_a", false, 0.0,
  //                               "0..1   opacity of the outer border (0=transparent, 1=opaque)");

  // Inner border
  pe_parameters().add_parameter("ib_size", false, 0.25,
                                "0..0.5 thickness of the inner border drawn at the edges of the screen every frame");
  pe_parameters().add_parameter("ib_r", false, 0.0,
                                "0..1   amount of red color in the inner border");
  pe_parameters().add_parameter("ib_g", false, 0.0,
                                "0..1   amount of green color in the inner border");
  pe_parameters().add_parameter("ib_b", false, 0.0,
                                "0..1   amount of blue color in the inner border");
  pe_parameters().add_parameter("ib_a", false, 0.0,
                                "0..1   opacity of the inner border (0=transparent, 1=opaque)");

  // Motion Vectors
  pe_parameters().add_parameter("mv_r", false, 0.5, 
                                "0..1   amount of red color in the motion vectors");
  pe_parameters().add_parameter("mv_g", false, 0.5,
                                "0..1   amount of green color in the motion vectors");
  pe_parameters().add_parameter("mv_b", false, 0.5,
                                "0..1   amount of blue color in the motion vectors");
  pe_parameters().add_parameter("mv_a", false, 0.0,
                                "0..1   opacity of the motion vectors (0=transparent, 1=opaque)");
  pe_parameters().add_parameter("mv_x", false, 64.0,
                                "the number of motion vectors in the X direction");
  pe_parameters().add_parameter("mv_y", false, 48.0,
                                "0..48  the number of motion vectors in the Y direction");
  pe_parameters().add_parameter("mv_l", false, 1.0,
                                "the length of the motion vectors (0=no trail, 1=normal, 2=double...)");
  pe_parameters().add_parameter("mv_dx", false, 0.0,
                                "-1..1  horizontal placement offset of the motion vectors");
  pe_parameters().add_parameter("mv_dy", false, 0.0,
                                "-1..1  vertical placement offset of the motion vectors");

  // pe_parameters().add_parameter("echo_zoom", false, 1.0,
  //                               ">0     controls the size of the second graphics layer");
  // pe_parameters().add_parameter("echo_alpha", false, 0.0,
  //                               ">0     controls the opacity of the second graphics layer; 0=transparent (off), 0.5=half-mix, 1=opaque");
  // pe_parameters().add_parameter("echo_orient", false, 0.0,
  //                               "0,1,2,3 selects an orientation for the second graphics layer.  0=normal, 1=flip on x, 2=flip on y, 3=flip on both");
  // pe_parameters().add_parameter("darken_center", false, 0.0,
  //                               "0/1    if 1, help keeps the image from getting too bright by continually dimming the center point");
  // pe_parameters().add_parameter("wrap", false, 0.0,
  //                               "0/1    sets whether or not screen elements can drift off of one side and onto the other");
  // pe_parameters().add_parameter("brighten", false, 0.0,
  //                               "0/1    brightens the darker parts of the image (nonlinear; square root filter)");
  // pe_parameters().add_parameter("darken", false, 0.0,
  //                               "0/1    darkens the brighter parts of the image (nonlinear; squaring filter)");
  // pe_parameters().add_parameter("solarize", false, 0.0,
  //                               "0/1    emphasizes mid-range colors");
  pe_parameters().add_parameter("monitor", false, 0.0,
                                "any    set this value for debugging your preset code; if you hit the 'N' key, "
                                "the value of 'monitor' will be posted in the upper-right corner of milkdrop.  "
                                "for example, setting \"monitor = q3;\" would let you keep an eye on q3's value. ");
  
  // pe_parameters().add_parameter("q1", false, 1.0,
  //                               "Used to carry information between the per-frame code and per-pixel code.");
  // pe_parameters().add_parameter("q2", false, 0.0,
  //                               "Used to carry information between the per-frame code and per-pixel code.");
  // pe_parameters().add_parameter("q3", false, 0.0,
  //                               "Used to carry information between the per-frame code and per-pixel code.");
  // pe_parameters().add_parameter("q4", false, 0.0,
  //                               "Used to carry information between the per-frame code and per-pixel code.");
  // pe_parameters().add_parameter("q5", false, 0.0,
  //                               "Used to carry information between the per-frame code and per-pixel code.");
  // pe_parameters().add_parameter("q6", false, 0.0,
  //                               "Used to carry information between the per-frame code and per-pixel code.");
  // pe_parameters().add_parameter("q7", false, 1.0,
  //                               "Used to carry information between the per-frame code and per-pixel code.");
  // pe_parameters().add_parameter("q8", false, 0.0,
  //                               "Used to carry information between the per-frame code and per-pixel code.");
 

  pe_parameters().add_parameter("ifs_mode", false, 0.0,
                                "Select IFS (fractal feedback) mode.");

  pe_parameters().add_parameter("square_frequency", false, 0.01,
                                "Speed of rotation of the square shape.");
  pe_parameters().add_parameter("square_r", false, 0.0,
                                "amount of red color in the wave (0..1)");
  pe_parameters().add_parameter("square_g", false, 1.0,         
                                "amount of green color in the wave (0..1)");
  pe_parameters().add_parameter("square_b", false, 0.0, 
                                "amount of blue color in the wave (0..1)");
  pe_parameters().add_parameter("square_a", false, 1.0, 
                                "opacity of the wave (0..1) [0=transparent, 1=opaque]");
  pe_parameters().add_parameter("square_thick", false, 1.0,
                                "<FILL ME IN>");
  pe_parameters().add_parameter("square_scale", false, 1.0,
                                "<FILL ME IN>");



  pe_parameters().add_parameter("edge_extend", false, 1.0,
                                "Turn edge extension on and off.");
  pe_parameters().add_parameter("show_fps", false, 0.0,
                                "Turn fps display on and off.");

  pe_parameters().add_parameter("lj_A", false, 1.0,
                                "Amplitude for horizontal lissajous pattern.");
  pe_parameters().add_parameter("lj_B", false, 1.0,
                                "Amplitude for vertical lissajous pattern.");
  pe_parameters().add_parameter("lj_omega", false, 1.0,
                                "Angular frequency for horizontal lissajous pattern.");
  pe_parameters().add_parameter("lj_ratio_a", false, 1.0,
                                "Angular frequency for vertical lissajous pattern.");
  pe_parameters().add_parameter("lj_ratio_b", false, 1.0,
                                "Angular frequency for vertical lissajous pattern.");
  pe_parameters().add_parameter("lj_phase", false, 1.0,
                                "Phase shift for horizontal lissajous pattern.");
  

  pe_parameters().add_parameter("aspect", true, 1.0,
                                "Aspect ratio of the screen.  The screen coordinates vary horizontally from [-aspect +aspect] and vertically from [-1 +1]");

  // pe_parameters().add_parameter("warpSpeed", "/2/fader1", 0.0, 1.0, 0.5);
  // pe_parameters().add_parameter("warpScale", "/2/fader2", 0.01, 1.0, 1.0);

  // pe_parameters().add_parameter("rd_width", "/3/fader1", 0.0, 50.0, 1.0);
  // pe_parameters().add_parameter("rd_D_g", "/3/fader2", 0.0, 0.5, 0.25);
  // pe_parameters().add_parameter("rd_D_b", "/3/fader3", 0.0, 0.5, 0.0625);
  // pe_parameters().add_parameter("rd_s", "/3/fader4", 0.0, 0.05, 0.03125);
  // pe_parameters().add_parameter("rd_beta", "/3/fader5", 0.0, 24.0, 12);
  // pe_parameters().add_parameter("rd_blur", "/3/fader8", 0.0, 4.0, 0.0);
}

int main(int argc, char *argv[]) {

  std::cout << "\nStarting PhosphorEssence v0.2\n";

  // Set up bindings for the OSC Controller
  setup_parameters();

  // Start up the Qt GUI
  QApplication app(argc, argv);
  MainWindow main_window;

  // Start up the OSC control thread.  It listens in the background,
  // changing the values in PeParameters as it receives updates.
  // std::cout << "\t--> Initializing OSC driver\n";
  // std::string osc_ip = "10.0.1.2";
  // if (argc == 2) 
  //   osc_ip = argv[1];
  // OscController osc_controller("60002", osc_ip.c_str() , "60000");

  std::cout << "\t--> Initializing MIDI driver\n";
  MidiController midi_controller;

  // std::cout << "\t--> Initializing Joystick drivers\n";
  JoystickController joystick_controller;

  // Create the audio thread, and create the sound statistics listener
  // that keeps up-to-date sound statistics (moving averages, etc).
  std::cout << "\t--> Opening audio stream\n";
  AudioThread audio_thread;
  boost::shared_ptr<SoundStatsListener> stats_listener( new SoundStatsListener() );
  audio_thread.register_listener(stats_listener);

  // Create some Waveshapes
  boost::shared_ptr<OScopeShape> oscope( new OScopeShape() );
  boost::shared_ptr<PhasescopeShape> phasescope( new PhasescopeShape() );
  boost::shared_ptr<SpectrographShape> spectrograph( new SpectrographShape() );
  //  boost::shared_ptr<VectorShape> lissajous( new VectorShape() );
  audio_thread.register_listener(oscope);
  audio_thread.register_listener(phasescope);
  audio_thread.register_listener(spectrograph);
  main_window.gl_widget()->register_drawable(phasescope);
  main_window.gl_widget()->register_drawable(spectrograph);
  main_window.gl_widget()->register_drawable(oscope);
  //  main_window.gl_widget()->register_drawable(lissajous);

  // Create the script engine & start the command interpreter
  //  pe_script_engine().register_controller(osc_controller, "OscController", "osc");
  pe_script_engine().register_controller(midi_controller, "MidiController", "midi");
  pe_script_engine().register_controller(joystick_controller, "JoystickController", "joystick");

  // As a last step, call the javascript initialize_callback() to give
  // use a chance to set everything up in the javascript VM.
  pe_script_engine().execute_js("pe_initialize()");

  // Enter the run loop
  main_window.show();
  return app.exec(); 
}

