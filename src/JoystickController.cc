// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>

#include <vw/Core/Log.h>
using namespace vw;

#include <JoystickController.h>
#include <PeParameters.h>

#include <SDL.h>

// ---------------------------------------------------
// Create a single instance of SDL
// ---------------------------------------------------
struct SdlInstance {
  SdlInstance() {
    Uint32 initflags = SDL_INIT_JOYSTICK;
    if ( SDL_Init(initflags) < 0 )
      std::cout << "WARNING: Failed to initialize SDL.\n";
  }

  ~SdlInstance() {  SDL_Quit(); }
};

namespace {
  vw::RunOnce sdl_instance_once = VW_RUNONCE_INIT;
  boost::shared_ptr<SdlInstance> sdl_instance_ptr;
  void init_sdl() {
    sdl_instance_ptr = boost::shared_ptr<SdlInstance>(new SdlInstance());
  }
}

// ---------------------------------------------------------------------

class JoystickTask {
  JoystickController* m_parent;
  bool m_terminate;

public:
  JoystickTask(JoystickController* parent) : 
    m_parent(parent), m_terminate(false) {}
  void operator()() {
    while (!m_terminate) {
      m_parent->update();
      Thread::sleep_ms(15); // Record updates at 60 Hz
    } 
  }
  void terminate() { m_terminate = true; }
};

// ---------------------------------------------------------------------

struct PeJoystick {
  SDL_Joystick* joystick_ptr;
  int index;
  std::vector<double> axes;
  std::vector<double> axes_prev;
  std::vector<int> buttons;
  std::vector<int> hats;                  

  PeJoystick(int index) {
    joystick_ptr = SDL_JoystickOpen(index); 
    if (joystick_ptr == NULL) {
      std::cout << "Error opening Joystick " << index << "\n";
      return;
    }
    std::cout << "\t    Opened joystick " << index << " : "
              <<  SDL_JoystickName(index) << "\n";

    index = SDL_JoystickIndex(joystick_ptr);
    axes.resize(SDL_JoystickNumAxes(joystick_ptr));
    axes_prev.resize(SDL_JoystickNumAxes(joystick_ptr));
    buttons.resize(SDL_JoystickNumButtons(joystick_ptr));
    hats.resize(SDL_JoystickNumHats(joystick_ptr));

    // Set initial values
    for (int n = 0; n < axes.size(); n++) {
      axes[n] = 0;
      axes_prev[n] = 0;
    }
    for (int n = 0; n < buttons.size(); n++)
      buttons[n] = 0;
    for (int n = 0; n < hats.size(); n++)
      hats[n] = 0;
    
  }

  ~PeJoystick() {
    if (joystick_ptr) 
      SDL_JoystickClose(joystick_ptr);
  }
};

// ---------------------------------------------------------------------

JoystickController::JoystickController() : Controller("joystick") {
  init_sdl();

  if (SDL_NumJoysticks() < 1) {
    std::cout << "\t    No joysticks found.\n";
    return;
  }

  for (int n = 0; n < SDL_NumJoysticks(); ++n) {
    boost::shared_ptr<PeJoystick> joystick(new PeJoystick(n));
    m_joysticks.push_back(joystick);
  }

  m_task.reset(new JoystickTask(this));
  m_thread.reset(new vw::Thread( m_task ));
}

void JoystickController::list_joysticks() {
  // Print out a list of joysticks 
  SDL_Joystick* joystick;
  for (int n = 0; n < SDL_NumJoysticks(); n++) {
    printf("\t    Opened joystick number %d : \n", n);
    printf("Name: %s\n", SDL_JoystickName(n));
    joystick = SDL_JoystickOpen(n);
    printf("NumAxes: %d\n", SDL_JoystickNumAxes(joystick));
    printf("NumBalls: %d\n", SDL_JoystickNumBalls(joystick));
    printf("NumHats: %d\n", SDL_JoystickNumHats(joystick));
    printf("NumButtons: %d\n", SDL_JoystickNumButtons(joystick));
    SDL_JoystickClose(joystick);
  }
}

JoystickController::~JoystickController() {
  if (m_task) {
    m_task->terminate();
    m_thread->join();
  }
}

void JoystickController::update() {

  // Update the joystick state
  SDL_JoystickUpdate();

  // Iterate over the joysticks
  for (int j=0; j<m_joysticks.size(); ++j) {

    // Handle changes to the rotation axes
    for (int i=0; i<m_joysticks[j]->axes.size(); ++i) {
      // Get current axis state and normalize to double from 0 to 1
      float value = float( SDL_JoystickGetAxis(m_joysticks[j]->joystick_ptr,i) / (-2*32768.0) + 0.5 );
      
      // If the value has changed, we pass along an update message.
      // Note, to avoid oscillations when the joystick is left in an
      // in-between position, we also check here to make sure the value
      // is not the same as the value we had two values ago.
      if (1) { //m_joysticks[j]->axes[i] != value) {// && m_joysticks[j]->axes_prev[i] != value) {  
        m_joysticks[j]->axes_prev[i] = m_joysticks[j]->axes[i];
        m_joysticks[j]->axes[i] = value;
        
        std::ostringstream path;
        path << "/joystick" << j << "/axis" << i;
        this->receive_callback(path.str(), value);
      }
    }

    // Handle changes to the buttons
    for (int i=0; i<m_joysticks[j]->buttons.size(); i++) {
      float value = SDL_JoystickGetButton(m_joysticks[j]->joystick_ptr,i);
      
      if (m_joysticks[j]->buttons[i] != value) {
        m_joysticks[j]->buttons[i] = value;
        std::ostringstream path;
        path << "/joystick" << j << "/button" << i;
        this->receive_callback(path.str(), value);
      }
    }

    // Handle changes to the hats
    for (int i=0; i<m_joysticks[j]->hats.size(); i++) {
      float value = SDL_JoystickGetHat(m_joysticks[j]->joystick_ptr,i);

      if (m_joysticks[j]->hats[i] != value) {
        m_joysticks[j]->hats[i] = value;
        std::ostringstream path;
        path << "/joystick" << j << "/hat" << i;
        this->receive_callback(path.str(), value);
      }
    }

  }
}
