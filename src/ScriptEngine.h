// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#ifndef __SCRIPT_ENGINE_H__
#define __SCRIPT_ENGINE_H__

#include <Python.h>
#include <iostream>
#include <vector>
#include <vw/Core/Stopwatch.h>
#include <vw/Core/Thread.h>

/// CommandPromptThread
///
/// This thread runs a simple read-eval-print loop that forwards
/// commands to our embedded python interpreter.
// 
class CommandPromptTask {
  PyObject *m_global_dict, *m_main_module, *m_pe_dict;
  bool m_interpreter_active;
  
public:
  CommandPromptTask() : m_interpreter_active(false) {}
  void operator()();

  PyObject* global_dict() const { return m_global_dict; }
  PyObject* main_module() const { return m_main_module; }
  PyObject* pe_dict() const { return m_pe_dict; }
  bool active() const { return m_interpreter_active; }
};

class ScriptEngine {

  vw::Mutex m_mutex;
  boost::shared_ptr<CommandPromptTask> m_command_prompt_task;
  boost::shared_ptr<vw::Thread> m_thread;

public: 
  ScriptEngine();
  ~ScriptEngine();

  void start();

  double get_parameter(const char* name);
  void set_parameter(const char* name, double value);  
  virtual void execute(std::string const& cmd);

  void controller_receive_callback(const char* controller_name, const char* path, double value);
  void controller_receive_callback(const char* controller_name, const char* path, std::vector<float> value);

};

/// Return the singleton instance of the PhosphorEssence parameters
/// structure.  The parameters struct is created the first time this
/// method is invoked.  You should *always* access the script engine
/// through this function.
ScriptEngine& pe_script_engine();

#endif // __SCRIPT_ENGINE_H__


