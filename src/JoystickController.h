// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <string>
#include <Controller.h>

#include <vw/Core/Thread.h>

class JoystickTask;
class PeJoystick;

class JoystickController : public Controller {  
  std::vector<boost::shared_ptr<PeJoystick> > m_joysticks;

  boost::shared_ptr<JoystickTask> m_task;
  boost::shared_ptr<vw::Thread> m_thread;

public:
  JoystickController();
  virtual ~JoystickController();

  static void list_joysticks();

  void update();
  virtual void send(std::string path, float value) {} // Does nothing 

};
