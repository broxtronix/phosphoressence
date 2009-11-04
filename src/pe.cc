// __BEGIN_LICENSE__
//
// PhosphorEssence
// An open framework for the visual exploration of mathematics
//
//  Copyright (C) 2009 Michael J. Broxton
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
// __END_LICENSE__

/// \file pe.cc
///
/// PhosphorEssence
/// An audio and video delight.
///

// Qt
#include <QApplication>
#include <QWidget>

// VW
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
//#include <MidiController.h>
#include <JoystickController.h>
#include <OScopeShape.h>
#include <VectorShape.h>
#include <PhasescopeShape.h>
#include <SpectrographShape.h>

using namespace vw;

void setup_parameters() {
  pe_parameters().add_parameter("exit", true, 0.0,
                                "Causes the program to exit.");
}

int main(int argc, char *argv[]) {

  std::cout << "\nStarting PhosphorEssence v0.3\n\n";

  // Set up bindings for the OSC Controller
  setup_parameters();

  // Start up the Qt GUI
  QApplication app(argc, argv);
  MainWindow main_window;

  // Start up the OSC control thread.  It listens in the background,
  // changing the values in PeParameters as it receives updates.
  std::cout << "\t--> Initializing OSC driver\n";
  std::string osc_ip = "10.0.1.2";
  if (argc == 2) 
    osc_ip = argv[1];
  OscController osc_controller("60002", osc_ip.c_str() , "60000");

  //  std::cout << "\t--> Initializing MIDI driver\n";
  //  MidiController midi_controller;

  std::cout << "\t--> Initializing Joystick drivers\n";
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
  boost::shared_ptr<VectorShape> lissajous( new VectorShape() );
  audio_thread.register_listener(oscope);
  audio_thread.register_listener(phasescope);
  audio_thread.register_listener(spectrograph);
  main_window.gl_widget()->register_drawable(phasescope);
  main_window.gl_widget()->register_drawable(spectrograph);
  main_window.gl_widget()->register_drawable(oscope);
  main_window.gl_widget()->register_drawable(lissajous);

  // Start the script engine & start the command interpreter
  pe_script_engine().start();

  // As a last step, call the javascript initialize_callback() to give
  // use a chance to set everything up in the javascript VM.
  pe_script_engine().execute("pe_initialize()");

  // Enter the run loop
  //  main_window.show();
  return app.exec(); 
}

