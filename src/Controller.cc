// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file Controller.cc
///
#include <Controller.h>
#include <ScriptEngine.h>

void Controller::register_script_engine(boost::shared_ptr<ScriptEngine> script_engine) {
  m_script_engine = script_engine;
}

void Controller::receive_callback(std::string path, float value) {
  if (m_script_engine) {
    m_script_engine->execute_js(m_name + ".receive_callback", path, value);
  }
}



// #include <vw/Core/Thread.h>
// #include <fstream>




