// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file StereoSettings.h
///
#ifndef __PE_PARAMETERS_H__
#define __PE_PARAMETERS_H__

#include <iostream>
#include <string>
#include <map>
#include <list>

#include <pe/Core/Thread.h>
#include <pe/Core/Time.h>
#include <pe/Math/Vector.h>

// -----------------------------------------------------------
// Utilities
// -----------------------------------------------------------

// Returns the base directory where phosphoressence scripts, shaders,
// and presets are stored.
std::string pe_resources_directory();

// Erases a file suffix if one exists and returns the base string
std::string prefix_from_filename(std::string const& filename);

// ---------------------------------------------------------------------
// VectorSpaceDimension
// ---------------------------------------------------------------------

class VectorSpaceDimension {

  // Class enums

  enum ControlType  { eAutomation, eController }; 

  // Class private members

  std::string m_name;
  std::string m_description;

  double m_value;               // Current value of the parameter
                                // (could be in mid-animation)

  double m_default_value;       // Default value for this parameter

  bool m_read_only;             // true if the parameter is read-only

  ControlType m_control_mode;   // [ automation, controller ] 

  float m_controller_timeout;   // Amount of time (seconds) left
                                // before automation can
                                // resume. Counts down to zero.
  double m_last_poll_time;

  
  // Sets the actual value of the parameter, clamping to the limits if
  // necessary.
  void set_internal(double val);

public:

  VectorSpaceDimension(std::string name, std::string description,
                       double default_value, bool read_only); 

  // Return the name
  std::string name() const { return m_name; }

  // Return the default value
  double default_value() const { return m_default_value; }

  // Return the description
  std::string description() const { return m_description; }

  // Reset the parameter to the default value;
  void reset();


  // Set the value of the parameter as part of an automated routine.
  // Automation con be overriden if a user starts to control this
  // parameter with a control.
  void set_automate(double val);

  // Set the value of the parameter using a human operated control.
  // Controls can overide
  void set_control(double val);

  // Set the value of a readonly parameter
  void set_readonly(double val);

  // Force the parameter to return to automated control.
  void automate();

  // Get the current value for a parameter
  // 
  // Can be overriden by a subclass to, e.g., return an interpolated
  // or animated value.
  virtual double operator()();
};

// ---------------------------------------------------------------------
// PeParameters
// ---------------------------------------------------------------------

class PeParameters {

  std::map<std::string, VectorSpaceDimension> m_parameters;
  pe::Mutex m_mutex;

public:
  void add_parameter(std::string name, 
                     bool read_only, 
                     float default_value, 
                     std::string description);

  void set_value(std::string name, float val);
  void set_readonly(std::string name, float val);
  float get_value(std::string name);
  std::string get_description(std::string name);
  void reset_value(std::string name);
  void reset_all();

  // Return a list of the currently bound parameters.
  std::list<std::string> param_list();

  // Print out a list of parameters and their limits to the screen.
  void print_list();
};

/// Return the singleton instance of the PhosphorEssence parameters
/// structure.  The parameters struct is created the first time this
/// method is invoked.  You should *always* access the settings
/// through this function.
PeParameters& pe_parameters();


#endif // __PE_PARAMETERS_H__
