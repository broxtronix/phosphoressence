// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file PeParameters.h
///
#include <PeParameters.h>

#include <vw/Core/Thread.h>
#include <vw/Core/Stopwatch.h>
#include <fstream>

// ---------------------------------------------------
// Create a single instance of the StereoSettings
// ---------------------------------------------------
namespace {
  vw::RunOnce pe_parameters_once = VW_RUNONCE_INIT;
  boost::shared_ptr<PeParameters> pe_parameters_ptr;
  void init_pe_parameters() {
    pe_parameters_ptr = boost::shared_ptr<PeParameters>(new PeParameters());
  }
}

PeParameters& pe_parameters() {
  pe_parameters_once.run( init_pe_parameters );
  return *pe_parameters_ptr;
}

void PeParameters::add_parameter(std::string name, bool read_only, float default_value, std::string description) {
  Parameter p(name, read_only, default_value, description);

  vw::Mutex::Lock lock(m_mutex);
  m_parameters.push_back(p);
}

void PeParameters::set_value(std::string name, float val) {
  vw::Mutex::Lock lock(m_mutex);
  
  Parameter* match = NULL;
  std::list<Parameter>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    if (iter->name == name) {
      match = &(*iter);
      break;
    }
    ++iter;
  }

  if (match) {
    match->value = val;
  } else {
    std::cout << "Warning in Parameter::set_value() -- Unknown parameter: " << name << "\n";
  }
}

PeParameters::PeParameters() {
  m_time = 0;    
  m_last_time = vw::Stopwatch::microtime();
}

float PeParameters::get_value(std::string name) {
  if (name == "time") {
    long long new_time = vw::Stopwatch::microtime();
    m_time += double(new_time - m_last_time) / 1e6;
    m_last_time = new_time;
    return m_time;
  }

  vw::Mutex::Lock lock(m_mutex);
  Parameter* match = NULL;
  std::list<Parameter>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    if (iter->name == name) {
      match = &(*iter);
      break;
    }
    ++iter;
  }

  if (match) {
    return match->value;
  } else {
    std::cout << "Warning in Parameter::get_value() -- Unknown parameter: " << name << "\n";
  }

  // Fail silently for now?
  return 0;
}

void PeParameters::reset_value(std::string name) {
  vw::Mutex::Lock lock(m_mutex);
  
  Parameter* match = NULL;
  std::list<Parameter>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    if (iter->name == name) {
      match = &(*iter);
      break;
    }
    ++iter;
  }

  if (match) {
    match->value = match->default_value;
  } else {
    std::cout << "Warning in Parameter::set_value() -- Unknown parameter: " << name << "\n";
  }
}

void PeParameters::reset_all() {
  vw::Mutex::Lock lock(m_mutex);
  
  Parameter* match = NULL;
  std::list<Parameter>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    if (!iter->read_only)
      iter->value = iter->default_value;
    ++iter;
  }
}

std::list<std::string> PeParameters::param_list() {
  vw::Mutex::Lock lock(m_mutex);
  std::list<std::string> result;

  std::list<Parameter>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    result.push_back(iter->name);
    ++iter;
  }
  return result;
}

void PeParameters::print_list() {    
  vw::Mutex::Lock lock(m_mutex);

  std::cout << "Here are the knobs you can tweak:\n\n";
    
  std::list<Parameter>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    std::cout << "\tName: " << iter->name;
    std::cout << "\tValue: " << iter->value;
    std::cout << "\t(" << iter->default_value << ")\n";
    ++iter;
  }
}
