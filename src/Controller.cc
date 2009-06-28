// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file Controller.cc
///
#include <Controller.h>
#include <ScriptEngine.h>

void Controller::receive_callback(std::string path, float value) {
  pe_script_engine().controller_receive_callback(m_name.c_str(), path.c_str(), value);
}




