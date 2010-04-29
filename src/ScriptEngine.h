// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#ifndef __SCRIPT_ENGINE_H__
#define __SCRIPT_ENGINE_H__

#include <iostream>
#include <vector>
#include <pe/Core/Stopwatch.h>
#include <pe/Core/Thread.h>

// Forward Declaration
class CommandPromptTask;

class ScriptEngine {

  pe::Mutex m_mutex;
  boost::shared_ptr<CommandPromptTask> m_command_prompt_task;
  boost::shared_ptr<pe::Thread> m_thread;

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


