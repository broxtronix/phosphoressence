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

#ifdef __APPLE__
#include <CoreFoundation/CoreFoundation.h>
#endif

// -----------------------------------------------------------
// Utilities
// -----------------------------------------------------------

// Returns the base directory where phosphoressence scripts, shaders,
// and presets are stored.
std::string pe_resources_directory() {
  std::string resources_dir;
#ifdef __APPLE__
  // The following code is used to find the "Resources" directory in a
  // MacOSX Application Bundle.  I should add some code here to deal
  // with the linux case.
  CFURLRef appUrlRef = CFBundleCopyBundleURL(CFBundleGetMainBundle());
  CFStringRef macPath = CFURLCopyFileSystemPath(appUrlRef,
                                                kCFURLPOSIXPathStyle);
  std::string bundle_base_str = std::string( CFStringGetCStringPtr(macPath, CFStringGetSystemEncoding()) );
  resources_dir = bundle_base_str + "/Contents/Resources";
  CFRelease(appUrlRef);
  CFRelease(macPath);

#else

  std::cout << "Error: pe_resources_directory() not yet implemented on this platform.  Please contact the author!\n";

#endif
  return resources_dir;
}

// Erases a file suffix if one exists and returns the base string
std::string prefix_from_filename(std::string const& filename) {
  std::string result = filename;
  int index = result.rfind(".");
  if (index != -1) 
    result.erase(index, result.size());
  return result;
}


// -----------------------------------------------------------
// Create a single instance of the Parameters and Time Structs
// -----------------------------------------------------------

namespace {
  vw::RunOnce pe_parameters_once = VW_RUNONCE_INIT;
  boost::shared_ptr<PeParameters> pe_parameters_ptr;
  void init_pe_parameters() {
    pe_parameters_ptr = boost::shared_ptr<PeParameters>(new PeParameters());
  }

  vw::RunOnce pe_time_once = VW_RUNONCE_INIT;
  boost::shared_ptr<PeTime> pe_time_ptr;
  void init_pe_time() {
    pe_time_ptr = boost::shared_ptr<PeTime>(new PeTime());
  }
}

PeParameters& pe_parameters() {
  pe_parameters_once.run( init_pe_parameters );
  return *pe_parameters_ptr;
}

double pe_time() {
  pe_time_once.run( init_pe_time );
  return (*pe_time_ptr)();
}

// ---------------------------------------------------------------------
// PeTime
// ---------------------------------------------------------------------

PeTime::PeTime() {
  m_time = 0;    
  m_last_time = vw::Stopwatch::microtime();
}

double PeTime::operator()() {
    vw::Mutex::Lock lock(m_mutex);
    long long new_time = vw::Stopwatch::microtime();
    m_time += double(new_time - m_last_time) / 1e6;
    m_last_time = new_time;
    return m_time;
  }

// ---------------------------------------------------------------------
// VectorSpaceDimension
// ---------------------------------------------------------------------

VectorSpaceDimension::VectorSpaceDimension(std::string name, std::string description,
                                           double default_value, bool read_only) {
  m_name = name;
  m_description = description;
  m_default_value = default_value;
  m_read_only = read_only;
  m_control_mode = eAutomation;
  m_value = default_value;
}

void VectorSpaceDimension::set_internal(double val) {
  if (!m_read_only)
    m_value = val;
}

void VectorSpaceDimension::set_readonly(double val) {
  m_value = val;
}

// Set the value of the parameter as part of an automated routine.
// Automation con be overriden if a user starts to control this
// parameter with a control.
void VectorSpaceDimension::set_automate(double val) {
  
  // Update the state of the automation override.  
  if (m_controller_timeout > 0) {
    double current_time = pe_time();
    double elapsed = current_time - m_last_poll_time;
    m_last_poll_time = current_time;
    m_controller_timeout -= elapsed;
  }
  
  if (m_controller_timeout < 0) {
    m_control_mode = eAutomation;
  }
  
  // If the controller timeout has fully elapsed, we switch back
  // into automation mode and accept this value.  Otherwise we
  // ignore it.
  if (m_control_mode == eAutomation)
    set_internal(val);
}

// Set the value of the parameter using a human operated control.
// Controls can overide
void VectorSpaceDimension::set_control(double val) {
  
  // Switch over into controller mode
  m_last_poll_time = pe_time();
  m_controller_timeout = 5.0; // 5 second timeout for now (for testing)
  m_control_mode = eController;
  
  // And set the value
  set_internal(val);
}

// Force the parameter to return to automated control.
void VectorSpaceDimension::automate() { 
  m_controller_timeout = 0; 
  m_control_mode = eAutomation;
}

// Get the current value for a parameter
// 
// Can be overriden by a subclass to, e.g., return an interpolated
// or animated value.
double VectorSpaceDimension::operator()() {
  return m_value;
}

// Reset the parameter to the default value;
void VectorSpaceDimension::reset() { 
  if (!m_read_only)
    m_value = m_default_value;
}

// ---------------------------------------------------------------------
// PeParameters
// ---------------------------------------------------------------------

void PeParameters::add_parameter(std::string name, 
                                 bool read_only, 
                                 float default_value, 
                                 std::string description) {
  VectorSpaceDimension p(name, description, default_value, read_only);

  vw::Mutex::Lock lock(m_mutex);
  m_parameters.push_back(p);
}

void PeParameters::set_value(std::string name, float val) {
  vw::Mutex::Lock lock(m_mutex);
  
  VectorSpaceDimension* match = NULL;
  std::list<VectorSpaceDimension>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    if (iter->name() == name) {
      match = &(*iter);
      break;
    }
    ++iter;
  }

  if (match) {
    match->set_automate(val);
  } else {
    std::cout << "Warning in Parameter::set_value() -- Unknown parameter: " << name << "\n";
  }
}

void PeParameters::set_readonly(std::string name, float val) {
  vw::Mutex::Lock lock(m_mutex);
  
  VectorSpaceDimension* match = NULL;
  std::list<VectorSpaceDimension>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    if (iter->name() == name) {
      match = &(*iter);
      break;
    }
    ++iter;
  }

  if (match) {
    match->set_readonly(val);
  } else {
    std::cout << "Warning in Parameter::set_value() -- Unknown parameter: " << name << "\n";
  }
}

float PeParameters::get_value(std::string name) {
  if (name == "time") {
    return pe_time();
  }

  vw::Mutex::Lock lock(m_mutex);
  VectorSpaceDimension* match = NULL;
  std::list<VectorSpaceDimension>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    if (iter->name() == name) {
      match = &(*iter);
      break;
    }
    ++iter;
  }

  if (match) {
    return (*match)();
  } else {
    std::cout << "Warning in Parameter::get_value() -- Unknown parameter: " << name << "\n";
  }

  // Fail silently for now?
  return 0;
}

void PeParameters::reset_value(std::string name) {
  vw::Mutex::Lock lock(m_mutex);
  
  VectorSpaceDimension* match = NULL;
  std::list<VectorSpaceDimension>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    if (iter->name() == name) {
      match = &(*iter);
      break;
    }
    ++iter;
  }

  if (match) {
    match->reset();
  } else {
    std::cout << "Warning in Parameter::set_value() -- Unknown parameter: " << name << "\n";
  }
}

void PeParameters::reset_all() {
  vw::Mutex::Lock lock(m_mutex);
  
  VectorSpaceDimension* match = NULL;
  std::list<VectorSpaceDimension>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    iter->reset();
    ++iter;
  }
}

std::list<std::string> PeParameters::param_list() {
  vw::Mutex::Lock lock(m_mutex);
  std::list<std::string> result;

  std::list<VectorSpaceDimension>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    result.push_back(iter->name());
    ++iter;
  }
  return result;
}

void PeParameters::print_list() {    
  vw::Mutex::Lock lock(m_mutex);

  std::cout << "Here are the knobs you can tweak:\n\n";
    
  std::list<VectorSpaceDimension>::iterator iter = m_parameters.begin();
  while (iter != m_parameters.end()) {
    std::cout << "\tName: " << iter->name();
    std::cout << "\tValue: " << (*iter)();
    std::cout << "\t(" << iter->default_value() << ")\n";
    ++iter;
  }
}
