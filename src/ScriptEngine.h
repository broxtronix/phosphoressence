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

  static bool ExecuteString(v8::Handle<v8::String> source,
                            v8::Handle<v8::Value> name,
                            bool print_result,
                            bool report_exceptions);

  virtual void execute_js(std::string const& code_string);

  template <class Arg1T, class Arg2T>
  void execute_js(std::string const& function, Arg1T arg1, Arg2T arg2) {
    vw::Mutex::Lock lock(m_mutex);
    
    // Set up the proper handle scope and enter the correct context.
    v8::HandleScope handle_scope;
    v8::Context::Scope context_scope(m_context);
    
    // For now we create a string and execute it, which may lead to
    // some loss of precision in the floating point number.  This is
    // fine for now, I suppose, until a better solution can be found.
    std::ostringstream ostr;
    ostr << function << "(\"" << arg1 << "\", " << arg2 << ");";
    
    ScriptEngine::ExecuteString(v8::String::New(ostr.str().c_str()),
                                v8::String::New("(shell)"),
                                true,
                                true);  
  }

  float fetch_parameter(const char* name);

};

/// Return the singleton instance of the PhosphorEssence parameters
/// structure.  The parameters struct is created the first time this
/// method is invoked.  You should *always* access the script engine
/// through this function.
ScriptEngine& pe_script_engine();



#endif // __SCRIPT_ENGINE_H__


