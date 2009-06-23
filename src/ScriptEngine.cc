// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <ScriptEngine.h>
#include <PeParameters.h>
#include <ostream>
#include <CoreFoundation/CoreFoundation.h>

// -----------------------------------------------------------
// Create a single instance of the ScriptEngine
// -----------------------------------------------------------

namespace {
  vw::RunOnce pe_script_engine_once = VW_RUNONCE_INIT;
  boost::shared_ptr<ScriptEngine> pe_script_engine_ptr;
  void init_pe_script_engine() {
    pe_script_engine_ptr = boost::shared_ptr<ScriptEngine>(new ScriptEngine());
  }
}

ScriptEngine& pe_script_engine() {
  pe_script_engine_once.run( init_pe_script_engine );
  return *pe_script_engine_ptr;
}

// ---------------------------------------------------------------------
//              PhosphorEssence Python Module Methods
//
// 
// ---------------------------------------------------------------------

// These are disabled for now.  They will serve as a useful template
// for binding c functions to python objects at some point, but not
// yet!


// static PyObject* pe_time(PyObject *self, PyObject *args) {
//   return Py_BuildValue("f", pe_time());
// }

// #define PE_READONLY_PARAM(func, param_name)                           \
// static PyObject* func(PyObject *self, PyObject *args) {               \
//   return Py_BuildValue("f", pe_parameters().get_value(param_name));   \
// }

// // General purpose read-only values
// PE_READONLY_PARAM(pe_fps, "fps")
// PE_READONLY_PARAM(pe_frame, "frame")
// PE_READONLY_PARAM(pe_aspect, "aspect")
// PE_READONLY_PARAM(pe_meshx, "meshx")
// PE_READONLY_PARAM(pe_meshy, "meshy")

// // Per-pixel values
// PE_READONLY_PARAM(pe_x, "x")
// PE_READONLY_PARAM(pe_y, "y")
// PE_READONLY_PARAM(pe_rad, "rad")
// PE_READONLY_PARAM(pe_ang, "ang")

// // Band pass filters (left audio channel)
// PE_READONLY_PARAM(pe_bass, "bass")
// PE_READONLY_PARAM(pe_mid, "mid")
// PE_READONLY_PARAM(pe_treb, "treb")
// PE_READONLY_PARAM(pe_bass_att, "bass_att")
// PE_READONLY_PARAM(pe_mid_att, "mid_att")
// PE_READONLY_PARAM(pe_treb_att, "treb_att")

// // Band pass filters (right audio channel)
// PE_READONLY_PARAM(pe_bass_r, "bass_r")
// PE_READONLY_PARAM(pe_mid_r, "mid_r")
// PE_READONLY_PARAM(pe_treb_r, "treb_r")
// PE_READONLY_PARAM(pe_bass_att_r, "bass_att_r")
// PE_READONLY_PARAM(pe_mid_att_r, "mid_att_r")
// PE_READONLY_PARAM(pe_treb_att_r, "treb_att_r")


// #define PE_METHOD_DESCRIPTION(name, callback)    \
//   {name,  callback, METH_VARARGS, "callback"}

// static PyMethodDef PeMethods[] = {
//   {"pe_time",  pe_time, METH_VARARGS, 
//    "(readonly) retrieves the current time, in seconds, since PhosphorEssence started running"},
//   PE_METHOD_DESCRIPTION("pe_fps", pe_fps),
//   PE_METHOD_DESCRIPTION("pe_frame", pe_frame),
//   PE_METHOD_DESCRIPTION("pe_aspect", pe_aspect),
//   PE_METHOD_DESCRIPTION("pe_meshx", pe_meshx),
//   PE_METHOD_DESCRIPTION("pe_meshy", pe_meshy),
//   PE_METHOD_DESCRIPTION("pe_y", pe_x),
//   PE_METHOD_DESCRIPTION("pe_x", pe_y),
//   PE_METHOD_DESCRIPTION("pe_ang", pe_ang),
//   PE_METHOD_DESCRIPTION("pe_rad", pe_rad),
//   PE_METHOD_DESCRIPTION("pe_bass", pe_bass),
//   PE_METHOD_DESCRIPTION("pe_mid", pe_mid),
//   PE_METHOD_DESCRIPTION("pe_treb", pe_treb),
//   PE_METHOD_DESCRIPTION("pe_bass", pe_bass_att),
//   PE_METHOD_DESCRIPTION("pe_mid", pe_mid_att),
//   PE_METHOD_DESCRIPTION("pe_treb", pe_treb_att),
//   PE_METHOD_DESCRIPTION("pe_bass", pe_bass_r),
//   PE_METHOD_DESCRIPTION("pe_mid", pe_mid_r),
//   PE_METHOD_DESCRIPTION("pe_treb", pe_treb_r),
//   PE_METHOD_DESCRIPTION("pe_bass", pe_bass_att_r),
//   PE_METHOD_DESCRIPTION("pe_mid", pe_mid_att_r),
//   PE_METHOD_DESCRIPTION("pe_treb", pe_treb_att_r),
//   {NULL, NULL, 0, NULL}        /* Sentinel */
// };

// PyMODINIT_FUNC
// initpe(void) { (void) Py_InitModule("pe_readonly_bindings", PeMethods); }

// ---------------------------------------------------------------------
//      C++ Callbacks & Basic Python Utility Functions
// ---------------------------------------------------------------------

ScriptEngine::ScriptEngine() {
  m_command_prompt_task.reset(new CommandPromptTask());
}

void ScriptEngine::start() {
  // Start the command shell
  m_thread.reset(new vw::Thread( m_command_prompt_task ));
}

ScriptEngine::~ScriptEngine() {
  // Should shut down the thread here somehow!
}


double ScriptEngine::get_parameter(const char* name) {
  if (!m_command_prompt_task->active()) 
    return 0.0;

  // Acquire the python Global Interpreter Lock (GIL)
  PyGILState_STATE gstate = PyGILState_Ensure();
  
  // Extract a reference to the object from the global dictionary
  PyObject *a = PyDict_GetItemString(m_command_prompt_task->global_dict(), name);
  
  // Check the validity of the result, and set the return value if the
  // data looks good.
  double result = 0.0;
  if (a && (PyNumber_Check(a))) {
    result = PyFloat_AsDouble(a);
    // Py_DECREF(a);  // Do I need this?  Seems to cause a segfault!!
  } else {
    std::cout << "Warning in get_parameter() -- Unknown parameter: " << name << "\n";
  }

  // Release the thread. No Python API allowed beyond this point. 
  PyGILState_Release(gstate);

  return result;
}

void ScriptEngine::set_parameter(const char* name, double value) {
  if (!m_command_prompt_task->active()) {
    // For debugging:
    //    std::cout << "WARNING: Attempting to set parameter \"" 
    //              << name << "\" before the script engine has been initialized.\n";
    return;
  }

  // Acquire the python Global Interpreter Lock (GIL)
  PyGILState_STATE gstate = PyGILState_Ensure();
  
  // Create the Python float object and set it's value in the global
  // dictionary.
  PyObject *a = PyFloat_FromDouble(value);
  PyDict_SetItemString(m_command_prompt_task->global_dict(), name, a);
  // Py_DECREF(a);  // Do I need this?

  // Release the thread. No Python API allowed beyond this point. 
  PyGILState_Release(gstate);
}

void ScriptEngine::execute(std::string const& cmd) {
  if (!m_command_prompt_task->active()) {
    std::cout << "Warning in execute() -- Could not execute python code. " 
              << "The interpreter is not currently running.\n";
    return;
  }

  // Acquire the python Global Interpreter Lock (GIL)
  PyGILState_STATE gstate = PyGILState_Ensure();

  // Run the string as a command in the python interpreter
  PyRun_SimpleString(cmd.c_str());

  // Release the thread. No Python API allowed beyond this point. 
  PyGILState_Release(gstate);
} 

// --------------------------------------------------------------------------
//                        CommandPromptTask Class
// --------------------------------------------------------------------------

void CommandPromptTask::operator()() {
  std::cout << "\n\n---------------------------------------------------------\n";
  std::cout << "                                                         \n";
  std::cout << "                     PHOSPHOR ESSENCE                    \n";
  std::cout << "                   Python Command Shell                  \n";
  std::cout << "                                                         \n";
  std::cout << "              Copyright 2009 Michael J. Broxton          \n";
  std::cout << "                    All Rights Reserved                  \n";
  std::cout << "                                                         \n";
  std::cout << "---------------------------------------------------------\n";

  // Set up the embedded Python environment
  Py_Initialize();

  // Get a reference to the main module
  // and global dictionary
  m_main_module = PyImport_AddModule("__main__");
  m_global_dict = PyModule_GetDict(m_main_module);

  // We are going to be accessing the python environment from many
  // different threads, so we need to initialize the python Global
  // Interpreter Lock (GIL) here.  
  PyEval_InitThreads();

  // Load the phosphoressence module, which contains bindings from
  // python to C++.
  //  initpe();

  // Append the PE scripts directory to the PYTHON_PATH via the
  // sys.path variable, and then load in the default PhosphorEssence
  // python script.
  std::cout << "\t--> Loading default PhosphorEssence preset script\n";
  std::string resources_dir = pe_resources_directory();
  std::string scripts_dir = resources_dir + "/scripts";

  std::ostringstream ostr;
  ostr << "import sys\n" 
       << "sys.path.append('" << scripts_dir << "')\n"
       << "PE_RESOURCES = \'" << scripts_dir << "\'\n"
       << "from phosphoressence import *\n";
  PyRun_SimpleString( ostr.str().c_str() );

  m_interpreter_active = true;

  // Start the main python interpreter loop
  char* dummy = "xxx";
  char** argv = &dummy;
  Py_Main(1, argv);

  // static const int buffer_size = 256;
  // char buffer[buffer_size];
  // while (true) {
    // std::cout << ">>> " << std::flush;
    // char* str = fgets(buffer, buffer_size, stdin);

    // // Check to see if the user has chosen to quit.  TODO: I'm not
    // // sure if calling exit() here is really the best way to cleanly
    // // shut down, but it seems to work for now.
    // if (str == NULL || std::string(str) == "quit()\n") {
    //   std::cout << "Exiting\n";
    //   exit(0);
    // }

    // // All other inputs are passed along to the python interpreter.
    // if (str != "\n")
    //   pe_script_engine().execute(str);
  //  }
  // std::cout << "\n";
  // printf("\n");

  m_interpreter_active = false;
  Py_Finalize();
}



// // --------------------------------------------------------------------------
// //                            Parameters Bindings
// // --------------------------------------------------------------------------

// v8::Handle<v8::Value> ParamsMethod_List(const v8::Arguments& args)
// {
//   v8::Local<v8::Object> self = args.Holder();
//   v8::Local<v8::External> wrap = v8::Local<v8::External>::Cast(self->GetInternalField(0));
//   void* ptr = wrap->Value();
//   static_cast<PeParameters*>(ptr)->print_list();
//   return v8::Undefined();
// }

// v8::Handle<v8::Value> ParamsMethod_Reset(const v8::Arguments& args)
// {
//   v8::Local<v8::Object> self = args.Holder();
//   v8::Local<v8::External> wrap = v8::Local<v8::External>::Cast(self->GetInternalField(0));
//   void* ptr = wrap->Value();
//   static_cast<PeParameters*>(ptr)->reset_all();
//   return v8::Undefined();
// }

// v8::Handle<v8::Value> ParamsMethod_Set(const v8::Arguments& args) {
//   v8::HandleScope handle_scope;
//   if (args.Length() != 2) {
//     std::cout << "Error: Parameters::set(name, value) takes two and no more " 
//               << "than three arguments, but you supplied " << args.Length() << ".\n";
//     return v8::Undefined();
//   }
//   v8::String::Utf8Value name_str(args[0]);
//   const char* name = ToCString(name_str);
//   v8::String::Utf8Value value_str(args[1]);
//   float value = atof(ToCString(value_str));
//   v8::Local<v8::Object> self = args.Holder();
//   v8::Local<v8::External> wrap = v8::Local<v8::External>::Cast(self->GetInternalField(0));
//   void* ptr = wrap->Value();
//   static_cast<PeParameters*>(ptr)->set_value(name, value);
//   return v8::Undefined();
// }

// v8::Handle<v8::Value> PeStandardGetter(v8::Local<v8::String> property, 
//                                        const v8::AccessorInfo& info) {
//   v8::HandleScope handle_scope;
//   v8::String::Utf8Value str(property);
//   return v8::Number::New( pe_parameters().get_value( ToCString(str) ) );
// }
    
// void PeStandardSetter(v8::Local<v8::String> property, v8::Local<v8::Value> value,
//                       const v8::AccessorInfo& info) {
//   v8::HandleScope handle_scope;
//   v8::String::Utf8Value str(property);
//   pe_parameters().set_value( ToCString(str), value->NumberValue() );

//   // This causes things to crash.  Disabled for now until I can figure it out...
//   // std::string path = ToCString(str);
//   // float val = value->NumberValue();
//   // std::ostringstream ostr;
//   // ostr << "bindings.parameter_to_controller(\"" << path << "\", " << val << ");";
//   // ScriptEngine::ExecuteString(v8::String::New(ostr.str().c_str()),
//   //                             v8::String::New("(shell)"),
//   //                             true,
//   //                             true);  
// }

// void create_pe_param_objects(v8::Handle<v8::ObjectTemplate> &global_templ) {
//   std::list<std::string> l = pe_parameters().param_list();
//   std::list<std::string>::iterator iter = l.begin();

//   for (; iter != l.end(); ++iter) {
//     global_templ->SetAccessor(v8::String::New(iter->c_str()), PeStandardGetter, PeStandardSetter);
//   }
//  }

// void ScriptEngine::setup_pe_parameters() {
//   v8::HandleScope handle_scope;
//   v8::Context::Scope context_scope(m_context);

//   v8::Handle<v8::FunctionTemplate> params_templ = v8::FunctionTemplate::New();
//   params_templ->SetClassName(v8::String::New("Parameters"));

//   // Set up the javascript prototype for the Parameters object
//   v8::Handle<v8::ObjectTemplate> params_proto = params_templ->PrototypeTemplate();
//   params_proto->Set("list", v8::FunctionTemplate::New(ParamsMethod_List));
//   params_proto->Set("reset_all", v8::FunctionTemplate::New(ParamsMethod_Reset));
//   params_proto->Set("set", v8::FunctionTemplate::New(ParamsMethod_Set));

//   // Create an instance of the template and bind it to our C++ instance.
//   v8::Handle<v8::ObjectTemplate> params_inst = params_templ->InstanceTemplate();
//   params_inst->SetInternalFieldCount(1);
//   v8::Handle<v8::Function> params_ctor = params_templ->GetFunction();
//   v8::Local<v8::Object> obj = params_ctor->NewInstance();
//   obj->SetInternalField(0, v8::External::New( &(pe_parameters()) ));

//   m_context->Global()->Set(v8::String::New("p"), obj);
// }


// // --------------------------------------------------------------------------
// //                            Controller Bindings
// // --------------------------------------------------------------------------

// // Default receive_callback in javascript is an empty function that
// // does nothing.
// v8::Handle<v8::Value> ControllerMethod_ReceiveCallback(const v8::Arguments& args)
// {
//   v8::HandleScope handle_scope;

//   return v8::Undefined();
// }

// v8::Handle<v8::Value> ControllerMethod_Send(const v8::Arguments& args)
// {
//   v8::HandleScope handle_scope;

//   if (args.Length() != 2) {
//     std::cout << "Error: Controller::send(path, value) takes two arguments, "
//               << "but you supplied " << args.Length() << ".\n";
//     return v8::Undefined();
//   }
//   v8::String::Utf8Value path_str(args[0]);
//   const char* path = ToCString(path_str);
//   v8::String::Utf8Value value_str(args[1]);
//   float value = atof(ToCString(value_str));

//   v8::Local<v8::Object> self = args.Holder();
//   v8::Local<v8::External> wrap = v8::Local<v8::External>::Cast(self->GetInternalField(0));
//   void* ptr = wrap->Value();
//   static_cast<Controller*>(ptr)->send(path, value);
//   return v8::Undefined();
// }

// void ScriptEngine::register_controller(Controller& controller, 
//                                        std::string class_name, 
//                                        std::string instance_name) {
//   v8::HandleScope handle_scope;
//   v8::Context::Scope context_scope(m_context);

//   v8::Handle<v8::FunctionTemplate> control_templ = v8::FunctionTemplate::New();
//   control_templ->SetClassName(v8::String::New(class_name.c_str()));

//   // Set up the javascript prototype for the Controller object
//   v8::Handle<v8::ObjectTemplate> control_proto = control_templ->PrototypeTemplate();
//   control_proto->Set("receive_callback", 
//                      v8::FunctionTemplate::New(ControllerMethod_ReceiveCallback));
//   control_proto->Set("send", 
//                      v8::FunctionTemplate::New(ControllerMethod_Send));

//   // Create an instance of the template and bind it to our C++ instance.
//   v8::Handle<v8::ObjectTemplate> control_inst = control_templ->InstanceTemplate();
//   control_inst->SetInternalFieldCount(1);
//   v8::Handle<v8::Function> control_ctor = control_templ->GetFunction();
//   v8::Local<v8::Object> obj = control_ctor->NewInstance();
//   obj->SetInternalField(0, v8::External::New( &controller ));

//   m_context->Global()->Set(v8::String::New(instance_name.c_str()), obj);
// }


// // --------------------------------------------------------------------------
// //                            ScriptEngine Class
// // --------------------------------------------------------------------------

// ScriptEngine::ScriptEngine() {
//   v8::HandleScope handle_scope;

//   // Create a template for the global object & registers C++ callback
//   // functions.
//   v8::Handle<v8::ObjectTemplate> global = v8::ObjectTemplate::New();
//   global->Set(v8::String::New("print"), v8::FunctionTemplate::New(Print));
//   global->Set(v8::String::New("load"), v8::FunctionTemplate::New(Load));
//   global->Set(v8::String::New("quit"), v8::FunctionTemplate::New(Quit));
//   global->Set(v8::String::New("version"), v8::FunctionTemplate::New(Version));
//   create_pe_param_objects(global);

//   // Create a new execution environment containing the built-in
//   // functions
//   v8::Handle<v8::Context> context = v8::Context::New(NULL, global);

//   // Store the context in the processor object in a persistent handle,
//   // since we want the reference to remain after we return from this
//   // method.
//   m_context = v8::Persistent<v8::Context>::New(context);

//   // Enter the newly created execution environment.
//   v8::Context::Scope context_scope(m_context);

//   // Load the default.js file.
//   std::cout << "\t--> Loading default PhosphorEssence preset script\n";
//   std::string resources_dir = pe_resources_directory();
//   std::string defaults_file = resources_dir + "/scripts/default.js";
//   v8::Handle<v8::String> source = ReadFile(defaults_file.c_str());
//   if (source.IsEmpty()) {
//     v8::ThrowException(v8::String::New("Error loading file"));
//   }
//   if (!ScriptEngine::ExecuteString(source, v8::String::New(defaults_file.c_str()), true, true)) {
//     v8::ThrowException(v8::String::New("Error executing file"));
//   }

//   // Add the parameters object to the JavaScript context
//   setup_pe_parameters();

//   // As a last step, we set the RESOURCES directory and call the
//   // javascript pe_load() to give use a chance to set everything up in
//   // the javascript VM.
//   std::ostringstream ostr;
//   ostr << "var PE_RESOURCES = \"" + resources_dir + "\";";
//   execute_js(ostr.str());
//   execute_js("pe_load()");



//   // Start the command shell
//   m_command_prompt_task.reset(new CommandPromptTask(this));
//   m_thread.reset(new vw::Thread( m_command_prompt_task ));
// }

// void ScriptEngine::execute_js(std::string const& code_string) {
//   vw::Mutex::Lock lock(m_mutex);

//   // Set up the proper handle scope and enter the correct context.
//   v8::HandleScope handle_scope;
//   v8::Context::Scope context_scope(m_context);

//   ScriptEngine::ExecuteString(v8::String::New(code_string.c_str()),
//                               v8::String::New("(shell)"),
//                               true,
//                               true);
// }

// float ScriptEngine::fetch_parameter(const char* name) {
//   vw::Mutex::Lock lock(m_mutex);

//   // Set up the proper handle scope and enter the correct context.
//   v8::HandleScope handle_scope;
//   v8::Context::Scope context_scope(m_context);

//   v8::Handle<v8::String> object_name = v8::String::New(name);
//   v8::Handle<v8::Value> result_val = m_context->Global()->Get(object_name);

//   // If there is no object by this name, or it is not a number, then
//   // we bail out.
//   if (!result_val->IsNumber()) return 0.0;

//   // It is a Number; cast it to a Number
//   v8::Handle<v8::Number> result_num = v8::Handle<v8::Number>::Cast(result_val);

//   // return result_num->Value();
//   return 0.0;
// }

// ScriptEngine::~ScriptEngine() {
//   // Hmm... I feel like we should join the thread rather than leave it
//   //  hanging, but it seems okay to do without for the moment as long
//   //  as we only have one ScriptEngine.
//   // 
//   // m_thread->join();
// }
