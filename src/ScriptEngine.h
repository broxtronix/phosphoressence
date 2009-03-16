// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#ifndef __SCRIPT_ENGINE_H__
#define __SCRIPT_ENGINE_H__

#include <vw/Core/Thread.h>
#include <v8.h>
#include <Controller.h>

struct ScriptEngineBase {
  // Execute an arbitrary string of javascript on the V8 instance.
  virtual void execute_js(std::string const& code_string) = 0;
};

/// CommandPromptThread
///
/// This thread runs a simple read-eval-print loop that forwards
/// commands to our instance of the V8 virtual machine.
// 
class CommandPromptTask {
  ScriptEngineBase* m_script_engine;

public:
  CommandPromptTask(ScriptEngineBase* script_engine) : m_script_engine(script_engine) {}
  void operator()();
};

/// ScriptEngine
///
/// This object creates an instance of Google's V8 Javascript engine.
///
/// Note: you can only have one V8 instance per process, so you should
/// not try to create more than one instance of this class.  At some
/// point I should guard this with a singleton method, but for now be
/// careful!
class ScriptEngine : public ScriptEngineBase {
  vw::Mutex m_mutex;
  boost::shared_ptr<CommandPromptTask> m_command_prompt_task;
  boost::shared_ptr<vw::Thread> m_thread;
  v8::Persistent<v8::Context> m_context;

  void setup_pe_parameters();

public:
  ScriptEngine();
  ~ScriptEngine();

  void register_controller(Controller& controller, 
                           std::string class_name, 
                           std::string instance_name);

  virtual void execute_js(std::string const& code_string);
  virtual void execute_js(std::string const& function, std::string arg1, float arg2);
};

#endif // __SCRIPT_ENGINE_H__


