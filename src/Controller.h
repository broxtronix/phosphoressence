// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file Controller.h
///
#ifndef __PE_CONTROLLER_H__
#define __PE_CONTROLLER_H__

#include <iostream>
#include <string>
#include <list>
#include <vector>

#include <vw/Core/Thread.h>
#include <boost/shared_ptr.hpp>

// Receive
// 1. osc callback
// 1.5 Controller callback
// 2. bindings.set_value_by_path
// 3. params.set_control_value  // Can override
// ...
// Send
// 3. params.set_value          // Can't override (fails silently)
// 4. bindings.value_set
// 4.5 Controller send
// 5. osc send


// class Binding { 
//   boost::shared_ptr<Controller> m_controller;
//   float lo, hi;
//   std::string mode;
//   std::string path;
//   std::string param_name;
// };


// class Controllable {
//   std::list<boost::shared_ptr<Binding> > m_bindings;
// public:
//   void value_updated(std::string name, float value) {
//     // Call all bindings callbacks
//   }
  
// }

// Controller Base class
class Controller {

  std::string m_name;

public:
  Controller(std::string name) : m_name(name) {}
  virtual ~Controller() {}
  void receive_callback(std::string path, float value);
  void receive_callback(std::string path, std::vector<float> value);

  virtual void send(std::string path, float value) = 0;
};

#endif // __PE_CONTROLLER_H__
