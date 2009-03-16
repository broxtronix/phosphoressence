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
#include <list>

#include <vw/Core/Thread.h>

class PeParameters {

  struct Parameter {
    std::string name;
    bool read_only;
    float value;
    float default_value;
    std::string description;

    Parameter(std::string name_, bool read_only_, float default_value_, std::string description_) :
      name(name_), read_only(read_only_), value(default_value_), default_value(default_value_), description(description_) {}
  };
    
  std::list<Parameter> m_parameters;
  float m_time;
  long long m_last_time;
  vw::Mutex m_mutex;

public:
  PeParameters();

  void add_parameter(std::string name, bool read_only, float default_value, std::string description);

  void set_value(std::string name, float val);
  float get_value(std::string name);
  void reset_value(std::string name);
  void reset_all();

  // Return a list of the currently bound parameters.
  std::list<std::string> param_list();

  // Print out a list of parameters and their limits to the screen.
  void print_list();
  // template <class FuncT>
  // void map(FuncT const& func) {
  //   vw::Mutex::Lock lock(m_mutex);
    
  //   std::list<Binding>::iterator iter = m_bindings.begin();
  //   while (iter != m_bindings.end()) {
  //     std::string path = iter->path;
  //     float ratio = (iter->hi - iter->lo);
  //     float value_x = (iter->x-iter->lo)/ratio;
  //     float value_y = (iter->y-iter->lo)/ratio;
  //     func(path, value_x, value_y, iter->dual_axis);
  //     ++iter;
  //   }
  // }
};

/// Return the singleton instance of the PhosphorEssence parameters
/// structure.  The parameters struct is created the first time this
/// method is invoked.  You should *always* access the settings
/// through this function.
PeParameters& pe_parameters();

#endif // __PE_PARAMETERS_H__
