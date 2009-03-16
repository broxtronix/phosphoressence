// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <ScriptEngine.h>
#include <PeParameters.h>
#include <ostream>

// ---------------------------------------------------------------------
//      C++ Callbacks & Basic JavaScript Utility Functions
// ---------------------------------------------------------------------

// Function Prototypes
bool ExecuteString(v8::Handle<v8::String> source,
                   v8::Handle<v8::Value> name,
                   bool print_result,
                   bool report_exceptions);
v8::Handle<v8::Value> Print(const v8::Arguments& args);
v8::Handle<v8::Value> Load(const v8::Arguments& args);
v8::Handle<v8::Value> Quit(const v8::Arguments& args);
v8::Handle<v8::Value> Version(const v8::Arguments& args);
v8::Handle<v8::String> ReadFile(const char* name);
void ReportException(v8::TryCatch* handler);


// Extracts a C string from a V8 Utf8Value.
const char* ToCString(const v8::String::Utf8Value& value) {
  return *value ? *value : "<string conversion failed>";
}


// The callback that is invoked by v8 whenever the JavaScript 'print'
// function is called.  Prints its arguments on stdout separated by
// spaces and ending with a newline.
v8::Handle<v8::Value> Print(const v8::Arguments& args) {
  bool first = true;
  for (int i = 0; i < args.Length(); i++) {
    v8::HandleScope handle_scope;
    if (first) {
      first = false;
    } else {
      printf(" ");
    }
    v8::String::Utf8Value str(args[i]);
    const char* cstr = ToCString(str);
    printf("%s", cstr);
  }
  printf("\n");
  return v8::Undefined();
}


// The callback that is invoked by v8 whenever the JavaScript 'load'
// function is called.  Loads, compiles and executes its argument
// JavaScript file.
v8::Handle<v8::Value> Load(const v8::Arguments& args) {
  for (int i = 0; i < args.Length(); i++) {
    v8::HandleScope handle_scope;
    v8::String::Utf8Value file(args[i]);
    if (*file == NULL) {
      return v8::ThrowException(v8::String::New("Error loading file"));
    }
    v8::Handle<v8::String> source = ReadFile(*file);
    if (source.IsEmpty()) {
      return v8::ThrowException(v8::String::New("Error loading file"));
    }
    if (!ExecuteString(source, v8::String::New(*file), false, false)) {
      return v8::ThrowException(v8::String::New("Error executing file"));
    }
  }
  return v8::Undefined();
}


// The callback that is invoked by v8 whenever the JavaScript 'quit'
// function is called.  Quits.
v8::Handle<v8::Value> Quit(const v8::Arguments& args) {
  // If not arguments are given args[0] will yield undefined which
  // converts to the integer value 0.
  int exit_code = args[0]->Int32Value();
  exit(exit_code);
  return v8::Undefined();
}


v8::Handle<v8::Value> Version(const v8::Arguments& args) {
  return v8::String::New(v8::V8::GetVersion());
}


// Reads a file into a v8 string.
v8::Handle<v8::String> ReadFile(const char* name) {
  FILE* file = fopen(name, "rb");
  if (file == NULL) return v8::Handle<v8::String>();

  fseek(file, 0, SEEK_END);
  int size = ftell(file);
  rewind(file);

  char* chars = new char[size + 1];
  chars[size] = '\0';
  for (int i = 0; i < size;) {
    int read = fread(&chars[i], 1, size - i, file);
    i += read;
  }
  fclose(file);
  v8::Handle<v8::String> result = v8::String::New(chars, size);
  delete[] chars;
  return result;
}


// Executes a string within the current v8 context.
bool ExecuteString(v8::Handle<v8::String> source,
                   v8::Handle<v8::Value> name,
                   bool print_result,
                   bool report_exceptions) {
  v8::HandleScope handle_scope;
  v8::TryCatch try_catch;
  v8::Handle<v8::Script> script = v8::Script::Compile(source, name);
  if (script.IsEmpty()) {
    // Print errors that happened during compilation.
    if (report_exceptions)
      ReportException(&try_catch);
    return false;
  } else {
    v8::Handle<v8::Value> result = script->Run();
    if (result.IsEmpty()) {
      // Print errors that happened during execution.
      if (report_exceptions)
        ReportException(&try_catch);
      return false;
    } else {
      if (print_result && !result->IsUndefined()) {
        // If all went well and the result wasn't undefined then print
        // the returned value.
        v8::String::Utf8Value str(result);
        const char* cstr = ToCString(str);
        printf("%s\n", cstr);
      }
      return true;
    }
  }
}


void ReportException(v8::TryCatch* try_catch) {
  v8::HandleScope handle_scope;
  v8::String::Utf8Value exception(try_catch->Exception());
  const char* exception_string = ToCString(exception);
  v8::Handle<v8::Message> message = try_catch->Message();
  if (message.IsEmpty()) {
    // V8 didn't provide any extra information about this error; just
    // print the exception.
    printf("%s\n", exception_string);
  } else {
    // Print (filename):(line number): (message).
    v8::String::Utf8Value filename(message->GetScriptResourceName());
    const char* filename_string = ToCString(filename);
    int linenum = message->GetLineNumber();
    printf("%s:%i: %s\n", filename_string, linenum, exception_string);
    // Print line of source code.
    v8::String::Utf8Value sourceline(message->GetSourceLine());
    const char* sourceline_string = ToCString(sourceline);
    printf("%s\n", sourceline_string);
    // Print wavy underline (GetUnderline is deprecated).
    int start = message->GetStartColumn();
    for (int i = 0; i < start; i++) {
      printf(" ");
    }
    int end = message->GetEndColumn();
    for (int i = start; i < end; i++) {
      printf("^");
    }
    printf("\n");
  }
}

// --------------------------------------------------------------------------
//                        CommandPromptTask Class
// --------------------------------------------------------------------------

void CommandPromptTask::operator()() {
  std::cout << "\n\n---------------------------------------------------------\n";
  std::cout << "                                                         \n";
  std::cout << "                     PHOSPHOR ESSENCE                    \n";
  std::cout << "                 JavaScript Command Shell                \n";
  std::cout << "                                                         \n";
  std::cout << "              Copyright 2009 Michael J. Broxton          \n";
  std::cout << "                    All Rights Reserved                  \n";
  std::cout << "                                                         \n";
  std::cout << "---------------------------------------------------------\n";

  static const int buffer_size = 256;
  char buffer[buffer_size];
  while (true) {
    std::cout << ">> " << std::flush;
    char* str = fgets(buffer, buffer_size, stdin);
    if (str == NULL) break;
    m_script_engine->execute_js(str);
  }
  std::cout << "\n";
  printf("\n");
}

// --------------------------------------------------------------------------
//                            Parameters Bindings
// --------------------------------------------------------------------------

v8::Handle<v8::Value> ParamsMethod_List(const v8::Arguments& args)
{
  v8::Local<v8::Object> self = args.Holder();
  v8::Local<v8::External> wrap = v8::Local<v8::External>::Cast(self->GetInternalField(0));
  void* ptr = wrap->Value();
  static_cast<PeParameters*>(ptr)->print_list();
  return v8::Undefined();
}

v8::Handle<v8::Value> ParamsMethod_Reset(const v8::Arguments& args)
{
  v8::Local<v8::Object> self = args.Holder();
  v8::Local<v8::External> wrap = v8::Local<v8::External>::Cast(self->GetInternalField(0));
  void* ptr = wrap->Value();
  static_cast<PeParameters*>(ptr)->reset_all();
  return v8::Undefined();
}

v8::Handle<v8::Value> ParamsMethod_Set(const v8::Arguments& args) {
  v8::HandleScope handle_scope;
  if (args.Length() != 2) {
    std::cout << "Error: Parameters::set(name, value) takes two and no more " 
              << "than three arguments, but you supplied " << args.Length() << ".\n";
    return v8::Undefined();
  }
  v8::String::Utf8Value name_str(args[0]);
  const char* name = ToCString(name_str);
  v8::String::Utf8Value value_str(args[1]);
  float value = atof(ToCString(value_str));
  v8::Local<v8::Object> self = args.Holder();
  v8::Local<v8::External> wrap = v8::Local<v8::External>::Cast(self->GetInternalField(0));
  void* ptr = wrap->Value();
  static_cast<PeParameters*>(ptr)->set_value(name, value);
  return v8::Undefined();
}

v8::Handle<v8::Value> PeStandardGetter(v8::Local<v8::String> property, 
                                       const v8::AccessorInfo& info) {
  v8::HandleScope handle_scope;
  v8::String::Utf8Value str(property);
  return v8::Number::New( pe_parameters().get_value( ToCString(str) ) );
}
    
void PeStandardSetter(v8::Local<v8::String> property, v8::Local<v8::Value> value,
                      const v8::AccessorInfo& info) {
  v8::HandleScope handle_scope;
  v8::String::Utf8Value str(property);
  pe_parameters().set_value( ToCString(str), value->NumberValue() );

  std::ostringstream ostr;
  ostr << "bindings.parameter_to_controller(\"" << ToCString(str) << "\", " << value->NumberValue() << ");";
  ExecuteString(v8::String::New(ostr.str().c_str()),
                v8::String::New("(shell)"),
                true,
                true);  
}

void create_pe_param_objects(v8::Handle<v8::ObjectTemplate> &global_templ) {
  std::list<std::string> l = pe_parameters().param_list();
  std::list<std::string>::iterator iter = l.begin();

  for (; iter != l.end(); ++iter) {
    global_templ->SetAccessor(v8::String::New(iter->c_str()), PeStandardGetter, PeStandardSetter);
  }
 }

void ScriptEngine::setup_pe_parameters() {
  v8::HandleScope handle_scope;
  v8::Context::Scope context_scope(m_context);

  v8::Handle<v8::FunctionTemplate> params_templ = v8::FunctionTemplate::New();
  params_templ->SetClassName(v8::String::New("Parameters"));

  // Set up the javascript prototype for the Parameters object
  v8::Handle<v8::ObjectTemplate> params_proto = params_templ->PrototypeTemplate();
  params_proto->Set("list", v8::FunctionTemplate::New(ParamsMethod_List));
  params_proto->Set("reset_all", v8::FunctionTemplate::New(ParamsMethod_Reset));
  params_proto->Set("set", v8::FunctionTemplate::New(ParamsMethod_Set));

  // Create an instance of the template and bind it to our C++ instance.
  v8::Handle<v8::ObjectTemplate> params_inst = params_templ->InstanceTemplate();
  params_inst->SetInternalFieldCount(1);
  v8::Handle<v8::Function> params_ctor = params_templ->GetFunction();
  v8::Local<v8::Object> obj = params_ctor->NewInstance();
  obj->SetInternalField(0, v8::External::New( &(pe_parameters()) ));

  m_context->Global()->Set(v8::String::New("p"), obj);
}


// --------------------------------------------------------------------------
//                            Controller Bindings
// --------------------------------------------------------------------------

// Default receive_callback in javascript is an empty function that
// does nothing.
v8::Handle<v8::Value> ControllerMethod_ReceiveCallback(const v8::Arguments& args)
{
  return v8::Undefined();
}

v8::Handle<v8::Value> ControllerMethod_Send(const v8::Arguments& args)
{
  if (args.Length() != 2) {
    std::cout << "Error: Controller::send(path, value) takes two arguments, "
              << "but you supplied " << args.Length() << ".\n";
    return v8::Undefined();
  }
  v8::String::Utf8Value path_str(args[0]);
  const char* path = ToCString(path_str);
  v8::String::Utf8Value value_str(args[1]);
  float value = atof(ToCString(value_str));

  v8::Local<v8::Object> self = args.Holder();
  v8::Local<v8::External> wrap = v8::Local<v8::External>::Cast(self->GetInternalField(0));
  void* ptr = wrap->Value();
  static_cast<Controller*>(ptr)->send(path, value);
  return v8::Undefined();
}

void ScriptEngine::register_controller(Controller& controller, 
                                       std::string class_name, 
                                       std::string instance_name) {
  v8::HandleScope handle_scope;
  v8::Context::Scope context_scope(m_context);

  v8::Handle<v8::FunctionTemplate> control_templ = v8::FunctionTemplate::New();
  control_templ->SetClassName(v8::String::New(class_name.c_str()));

  // Set up the javascript prototype for the Controller object
  v8::Handle<v8::ObjectTemplate> control_proto = control_templ->PrototypeTemplate();
  control_proto->Set("receive_callback", 
                     v8::FunctionTemplate::New(ControllerMethod_ReceiveCallback));
  control_proto->Set("send", 
                     v8::FunctionTemplate::New(ControllerMethod_Send));

  // Create an instance of the template and bind it to our C++ instance.
  v8::Handle<v8::ObjectTemplate> control_inst = control_templ->InstanceTemplate();
  control_inst->SetInternalFieldCount(1);
  v8::Handle<v8::Function> control_ctor = control_templ->GetFunction();
  v8::Local<v8::Object> obj = control_ctor->NewInstance();
  obj->SetInternalField(0, v8::External::New( &controller ));

  m_context->Global()->Set(v8::String::New(instance_name.c_str()), obj);
}


// --------------------------------------------------------------------------
//                            ScriptEngine Class
// --------------------------------------------------------------------------

ScriptEngine::ScriptEngine() {
  v8::HandleScope handle_scope;

  // Create a template for the global object & registers C++ callback
  // functions.
  v8::Handle<v8::ObjectTemplate> global = v8::ObjectTemplate::New();
  global->Set(v8::String::New("print"), v8::FunctionTemplate::New(Print));
  global->Set(v8::String::New("load"), v8::FunctionTemplate::New(Load));
  global->Set(v8::String::New("quit"), v8::FunctionTemplate::New(Quit));
  global->Set(v8::String::New("version"), v8::FunctionTemplate::New(Version));
  create_pe_param_objects(global);

  // Create a new execution environment containing the built-in
  // functions
  v8::Handle<v8::Context> context = v8::Context::New(NULL, global);

  // Store the context in the processor object in a persistent handle,
  // since we want the reference to remain after we return from this
  // method.
  m_context = v8::Persistent<v8::Context>::New(context);

  // Enter the newly created execution environment.
  v8::Context::Scope context_scope(m_context);

  // Load the default.js file.
  std::cout << "\t--> Loading default PhosphorEssence preset script\n";
  std::string defaults_file = "/Users/mbroxton/projects/PhosphorEssence/src/StandardScripts/default.js";
  v8::Handle<v8::String> source = ReadFile(defaults_file.c_str());
  if (source.IsEmpty()) {
    v8::ThrowException(v8::String::New("Error loading file"));
  }
  if (!ExecuteString(source, v8::String::New(defaults_file.c_str()), true, true)) {
    v8::ThrowException(v8::String::New("Error executing file"));
  }

  // Add the parameters object to the context
  setup_pe_parameters();

  // As a last step, call the javascript initialize_callback() to give
  // use a chance to set everything up in the javascript VM.
  execute_js("pe_load()");

  // Start the command shell
  m_command_prompt_task.reset(new CommandPromptTask(this));
  m_thread.reset(new vw::Thread( m_command_prompt_task ));
}

void ScriptEngine::execute_js(std::string const& function, std::string arg1, float arg2) {
  vw::Mutex::Lock lock(m_mutex);
  
  // Set up the proper handle scope and enter the correct context.
  v8::HandleScope handle_scope;
  v8::Context::Scope context_scope(m_context);

  // For now we create a string and execute it, which may lead to some
  // loss of precision in the floating point number.  This is a
  // cop-out for now, I suppose, until a better solution can be found.
  std::ostringstream ostr;
  ostr << function << "(\"" << arg1 << "\", " << arg2 << ");";

  ExecuteString(v8::String::New(ostr.str().c_str()),
                v8::String::New("(shell)"),
                true,
                true);  
}

void ScriptEngine::execute_js(std::string const& code_string) {
  vw::Mutex::Lock lock(m_mutex);

  // Set up the proper handle scope and enter the correct context.
  v8::HandleScope handle_scope;
  v8::Context::Scope context_scope(m_context);

  ExecuteString(v8::String::New(code_string.c_str()),
                v8::String::New("(shell)"),
                true,
                true);
}

ScriptEngine::~ScriptEngine() {
  // Hmm... I feel like we should join the thread rather than leave it
  //  hanging, but it seems okay to do without for the moment as long
  //  as we only have one ScriptEngine.
  // 
  // m_thread->join();
}
