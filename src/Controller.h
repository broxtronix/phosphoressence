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
#include <boost/shared_ptr.hpp>

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
