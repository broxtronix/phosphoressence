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

static PyObject* pe_py_time(PyObject *self, PyObject *args) {
  return Py_BuildValue("f", pe_time());
}

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

static PyMethodDef PeMethods[] = {
  {"pe_time",  pe_py_time, METH_VARARGS, 
   "(readonly) retrieves the current time, in seconds, since PhosphorEssence started running"},
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
  {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initpe(void) { (void) Py_InitModule("pe_readonly_bindings", PeMethods); }

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
  // std::cout << "Issuing command to quit.";
  // if (m_command_prompt_task->active())
  //   this->execute("quit()");
  // std::cout << "Joining thread!\n";
  // m_thread->join();
}

double ScriptEngine::get_parameter(const char* name) {
  if (!m_command_prompt_task->active()) 
    return 0.0;

  // Acquire the python Global Interpreter Lock (GIL)
  PyGILState_STATE gstate = PyGILState_Ensure();
  
  // Extract a reference to the object from the global dictionary
  PyObject *a = PyObject_GetAttrString(m_command_prompt_task->pe_dict(), name);
  
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
  PyObject_SetAttrString(m_command_prompt_task->pe_dict(), name, a);
  // Py_DECREF(a);  // Do I need this?

  // Release the thread. No Python API allowed beyond this point. 
  PyGILState_Release(gstate);
}

void ScriptEngine::controller_receive_callback(const char* controller_name, const char* path, double value) {
  if (!m_command_prompt_task->active())
    return;

  // Acquire the python Global Interpreter Lock (GIL)
  PyGILState_STATE gstate = PyGILState_Ensure();
  


  // Create the Python float object and set it's value in the global
  // dictionary.
  PyObject* controller = PyObject_GetAttrString(m_command_prompt_task->main_module(), controller_name);  
  if (controller == NULL) { PyErr_Print(); return; }
  PyObject* receive_callback = PyObject_GetAttrString(controller, "receive_callback");  
  if (receive_callback == NULL) { PyErr_Print(); return; }

  PyEval_CallFunction(receive_callback, "sf", path, value);
  Py_DECREF(controller);
  Py_DECREF(receive_callback);

  // Release the thread. No Python API allowed beyond this point. 
  PyGILState_Release(gstate);
}

void ScriptEngine::execute(std::string const& cmd) {
  if (!m_command_prompt_task->active()) {
    //    std::cout << "Warning in execute() -- Could not execute python code. " 
    //              << "The interpreter is not currently running.\n";
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
  initpe();

  // Append the PE scripts directory to the PYTHON_PATH via the
  // sys.path variable, and then load in the default PhosphorEssence
  // python script.
  std::cout << "\t--> Loading default PhosphorEssence preset script\n";
  std::string resources_dir = pe_resources_directory();

  std::ostringstream ostr;
  ostr << "import sys\n" 
       << "sys.path.append('" << resources_dir << "/scripts')\n"
       << "\'PE_RESOURCES = " << resources_dir << "\'\n"
       << "from phosphoressence import *\n";
  PyRun_SimpleString( ostr.str().c_str() );

  m_interpreter_active = true;

  // Grab a reference to the "pe" object's __dict__, which should exist by now...
  m_pe_dict = PyObject_GetAttrString(m_main_module, "pe");  
  if (m_pe_dict == NULL) {
    PyErr_Print();
    std::cout << "\n--------------------------------------------------\n"
              << "Error: the 'pe' object is not found in the python\n" 
              << "environment.  This probably means that an error \n"
              << "occurred during startup.  Exiting.\n"
              << "--------------------------------------------------\n\n";
  } else {

    // Start the main python interpreter loop
    char* dummy = "xxx";
    char** argv = &dummy;
    Py_Main(1, argv);
  }

  // Close down the python environment
  m_interpreter_active = false;
  Py_Finalize();

  // Send the signal for the rest of the program to exit.
  pe_parameters().set_readonly("exit", 1.0);
}
