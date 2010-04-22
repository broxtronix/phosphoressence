// __BEGIN_LICENSE__
// Copyright (C) 2006, 2007 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


// \file  GpuProgram.cc
//
//  Created by Ian Saxton on 5/17/06.

#include <map>
#include <vector>
#include <fstream>
#include <iostream>

#include <boost/algorithm/string.hpp>

#include <pe/Core/Exception.h>
#include <pe/Core/Log.h>
#include <pe/Graphics/GpuProgram.h>
#include <pe/Graphics/Utilities.h>
#include <pe/Graphics/StandardShaders.h>

using std::string;
using std::pair;
using std::vector;
using std::map;

namespace pe { 
namespace graphics {

  int maxErrorLength = 2048;

  char errorString[2048];

  string shader_base_path = "";

  bool shader_assembly_cache_enabled = false;

  string shader_assembly_cache_path = "";


  ShaderCompilationStatusEnum shaderCompilationStatus = SHADER_COMPILATION_STATUS_SUCCESS;

  typedef pair<pair<string, string>, pair<vector<int>, vector<int> > > GpuProgramKey;
  static std::map<GpuProgramKey, boost::shared_ptr<GpuProgram_GLSL> > program_cache_glsl;


  // --------------------------------------------------------------
  //                       GLSL DEBUGGING
  // --------------------------------------------------------------
  std::string get_shader_info_log(GLuint obj) {
    int infologLength = 0;
    int charsWritten  = 0;
    char *infoLog;

    glGetShaderiv(obj, GL_INFO_LOG_LENGTH,&infologLength);
    
    if (infologLength > 1) {
      infoLog = (char *)malloc(infologLength);
      glGetShaderInfoLog(obj, infologLength, &charsWritten, infoLog);
      std::ostringstream err;
      err << "<h4>An error occured while compiling the GLSL shader:</h4><p><h5><tt>" << infoLog << "</tt></h5>";
      // QMessageBox::critical(0, "GLSL Shader Error", 
      //                       err.str().c_str());
      free(infoLog);
      return err.str();
    }
    return "";
  }

  std::string get_program_info_log(GLuint obj) {
    int infologLength = 0;
    int charsWritten  = 0;
    char *infoLog;
  
    glGetProgramiv(obj, GL_INFO_LOG_LENGTH,&infologLength);
    if (infologLength > 1) {
      infoLog = (char *)malloc(infologLength);
      glGetProgramInfoLog(obj, infologLength, &charsWritten, infoLog);
      std::ostringstream err;
      err << "<h4>An error occured while linking the GLSL program:</h4><p><h5><tt>" << infoLog << "</tt></h5>";
      // QMessageBox::critical(0, "GLSL Program Error", 
      //                       err.str().c_str());
      free(infoLog);
      return err.str();
    }
    return "";
  }

  //########################################################################
  //#    GLSL - Program
  //########################################################################

  bool GpuProgram_GLSL::Link(GPUVertexShader_GLSL& vertex, GPUFragmentShader_GLSL& fragment) {   
    program = glCreateProgramObjectARB();
    if(vertex.is_compiled())
      glAttachObjectARB(program, vertex.get_shader());
    if(fragment.is_compiled())
      glAttachObjectARB(program, fragment.get_shader());
    glLinkProgramARB(program);
    GLsizei errorStringLength;
    GLint isCompiled;
    glGetInfoLogARB(program, maxErrorLength, &errorStringLength, errorString);
    glGetObjectParameterivARB(program, GL_OBJECT_LINK_STATUS_ARB, &isCompiled);
    if(!isCompiled) {
      printf("***PROGRAM LINKER***\n%s\n", errorString);
      program = 0;
      return false;
    }
    return true;
  }

  //########################################################################
  //#    GLSL - Vertex Shader
  //########################################################################


  bool GPUVertexShader_GLSL::compile(const string& vertexString) {   
    const char* cStr = vertexString.c_str();
    shader = glCreateShaderObjectARB(GL_VERTEX_SHADER_ARB);
    glShaderSourceARB(shader, 1, (const GLcharARB**) &cStr, NULL);	
    glCompileShaderARB(shader);
    GLsizei errorStringLength;
    GLint isCompiled;
    glGetInfoLogARB(shader, maxErrorLength, &errorStringLength, errorString);
    glGetObjectParameterivARB(shader, GL_OBJECT_COMPILE_STATUS_ARB, &isCompiled);
    if(!isCompiled) {
      pe_out(ErrorMessage, "GPU") << "*********GLSL Vertex Shader Compilation Error*********\n";
      pe_out(ErrorMessage, "GPU") << errorString;
      //      pe_out(ErrorMessage, "GPU") << vertexString.c_str();
      return false;
    }
    return true;
  }

  //########################################################################
  //#    GLSL - Fragment Shader
  //########################################################################

  bool GPUFragmentShader_GLSL::compile(const string& fragmentString) {   
    const char* cStr = fragmentString.c_str();
    shader = glCreateShaderObjectARB(GL_FRAGMENT_SHADER_ARB);
    glShaderSourceARB(shader, 1, (const GLcharARB**) &cStr, NULL);	

    glCompileShaderARB(shader);
    GLint isCompiled;
    GLsizei errorStringLength;
    glGetInfoLogARB(shader, maxErrorLength, &errorStringLength, errorString);
    glGetObjectParameterivARB(shader, GL_OBJECT_COMPILE_STATUS_ARB, &isCompiled);
    if(!isCompiled) { 
      pe_out(ErrorMessage, "GPU") << "*********GLSL Fragment Shader Compilation Error*********\n";
      pe_out(ErrorMessage, "GPU") << errorString;
      //      pe_out(ErrorMessage, "GPU") << fragmentString.c_str();
      return false;
    }
    return true;
  }


  //#############################################################################################
  //#    Creation Free Functions - GLSL
  //#############################################################################################

  boost::shared_ptr<GpuProgram_GLSL> create_gpu_program_glsl_string(const string& fragmentString, 
                                                                    const vector<int>& fragmentAttributes,
                                                                    const string& vertexString, 
                                                                    const vector<int>& vertexAttributes) {

    shaderCompilationStatus = SHADER_COMPILATION_STATUS_SUCCESS_FILE;	
    static char charBuffer1[32];
    static char charBuffer2[32];

    // Vertex
    GPUVertexShader_GLSL vertexShader;
    if(!vertexString.empty()) {
      string vertReplacedString;
      const string* sourceString = &vertexString;
      if(vertexAttributes.size()) {
        TokenReplacer tr;
	for(unsigned i=0; i < vertexAttributes.size(); i++) {
	  sprintf(charBuffer1, "%i", i+1);
	  sprintf(charBuffer2, "%i", vertexAttributes[i]);
	  tr.AddVariable(charBuffer1, charBuffer2);
	}
	tr.Replace(vertexString, vertReplacedString);
	sourceString = &vertReplacedString;
      }
      if(!vertexShader.compile(*sourceString)) {
	shaderCompilationStatus = SHADER_COMPILATION_STATUS_ERROR_COMPILE;
	throw(Exception("GpuProgram creation failed."));	
      }	
    }					

    // Fragment
    GPUFragmentShader_GLSL fragmentShader;
    if(!fragmentString.empty()) {
      string fragReplacedString;
      const string* sourceString = &fragmentString;
      if(fragmentAttributes.size()) {
	TokenReplacer tr;
	string variable;
	for(unsigned i=0; i < fragmentAttributes.size(); i++) {
	  sprintf(charBuffer1, "%i", i+1);
	  sprintf(charBuffer2, "%i", fragmentAttributes[i]);
	  tr.AddVariable(charBuffer1, charBuffer2);
	}
	tr.Replace(fragmentString, fragReplacedString);
	sourceString = &fragReplacedString;
      }
      if(!fragmentShader.compile(*sourceString)) {
	shaderCompilationStatus = SHADER_COMPILATION_STATUS_ERROR_COMPILE;
	throw(Exception("GpuProgram creation failed."));	
      }
    }						

    // Program
    GpuProgram_GLSL* program = new GpuProgram_GLSL;
    if(!program->Link(vertexShader, fragmentShader)) {
      shaderCompilationStatus = SHADER_COMPILATION_STATUS_ERROR_LINK;
      delete program;
      throw(Exception("GpuProgram creation failed."));	
    }
    return boost::shared_ptr<GpuProgram_GLSL>(program);
  }

  boost::shared_ptr<GpuProgram_GLSL> create_gpu_program_glsl(const string& fragmentPath, 
                                                             const vector<int>& fragmentAttributes,
                                                             const string& vertexPath, 
                                                             const vector<int>& vertexAttributes) {

    pe_out(DebugMessage, "GPU") << "create_gpu_program_glsl() -- Attempting to open " 
                                << fragmentPath << " and " << vertexPath << "\n";
    
    // Check cache
    GpuProgramKey programKey = GpuProgramKey(pair<string, string>(fragmentPath, vertexPath), 
                                             pair<vector<int>, vector<int> >(fragmentAttributes, 
                                                                             vertexAttributes));
    map<GpuProgramKey, boost::shared_ptr<GpuProgram_GLSL> >::iterator iter_prog;
    iter_prog = program_cache_glsl.find(programKey);
    if(iter_prog != program_cache_glsl.end()) {
      shaderCompilationStatus = SHADER_COMPILATION_STATUS_SUCCESS_CACHE;
      pe_out(DebugMessage, "GPU") << "create_gpu_program_glsl() -- found cached copy.\n";
      return (*iter_prog).second;
    }	

    // Vertex File Read
    string vertexString;
    GPUVertexShader_GLSL vertexShader;

    if(!vertexPath.empty()) {
      if (!ReadFileAsString(vertexPath, vertexString)) {
        pe_out(DebugMessage, "GPU") << "create_gpu_program_glsl() -- could not find vertex shader: " 
                                    << (shader_base_path + vertexPath) + "\n";
	shaderCompilationStatus = SHADER_COMPILATION_STATUS_ERROR_FILE;
	throw(Exception("GpuProgram creation failed."));	
      }
      std::cout << "vertexString : " << vertexString << "\n";

    }

    // Fragment File Read
    string fragmentString;
    if(!fragmentPath.empty()) {			
      if (!ReadFileAsString(shader_base_path + fragmentPath, fragmentString)) {
        pe_out(DebugMessage, "GPU") << "create_gpu_program_glsl() -- could not find fragment shader: " 
                                    << (shader_base_path + fragmentPath) + "\n";
	shaderCompilationStatus = SHADER_COMPILATION_STATUS_ERROR_FILE;
	throw(Exception("GpuProgram creation failed."));	
      }
    }

    // Compile Strings
    boost::shared_ptr<GpuProgram_GLSL> program = create_gpu_program_glsl_string(fragmentString, 
                                                                                fragmentAttributes, 
                                                                                vertexString, 
                                                                                vertexAttributes);
    if (program)
      program_cache_glsl[programKey] = program;
    return program;
  }





  //#############################################################################################
  //#    Creation Free Functions - Base
  //#############################################################################################


  boost::shared_ptr<GpuProgram> create_gpu_program(const string& fragmentPath, 
                                                   const vector<int>& fragmentAttributes,
                                                   const string& vertexPath, 
                                                   const vector<int>& vertexAttributes) {
    // LOGGING
    static char  buffer1[256];
    static char buffer2[256];
    buffer1[0] = 0;
    if(vertexAttributes.size()) {
      sprintf(buffer1, "< ");
      for(size_t i=0; i<vertexAttributes.size(); i++)
	sprintf(buffer1, "%s%i ", buffer1, vertexAttributes[i]);
      sprintf(buffer1, "%s>", buffer1);
    }

    buffer2[0] = 0;
    if(fragmentAttributes.size()) {
      sprintf(buffer2, "< ");
      for(size_t i=0; i<fragmentAttributes.size(); i++)
	sprintf(buffer2, "%s%i ", buffer2, fragmentAttributes[i]);
      sprintf(buffer2, "%s>", buffer2);
    }

    static char buffer3[512];
    boost::shared_ptr<GpuProgram> program;
    sprintf(buffer3, "create_gpu_program() -- FRAGMENT: %s%s, VERTEX: %s%s     \n", 
            fragmentPath.c_str(), buffer2, vertexPath.c_str(), buffer1 );
    pe_out(DebugMessage, "GPU") << buffer3;

    // FIND PROGRAM
    try {
      program = create_gpu_program_glsl(fragmentPath, 
                                        fragmentAttributes, 
                                        vertexPath, 
                                        vertexAttributes);
    }
    catch(...) {  program.reset(); }

    if(program) {
      if(get_shader_compilation_status() == SHADER_COMPILATION_STATUS_SUCCESS_FILE)
        pe_out(DebugMessage, "GPU") << "SUCCESS (From File)\n";
      if(get_shader_compilation_status() == SHADER_COMPILATION_STATUS_SUCCESS_CACHE)
	pe_out(DebugMessage, "GPU") << "SUCCESS (From Cache)\n";
    }
    else {
      if(get_shader_compilation_status() == SHADER_COMPILATION_STATUS_ERROR_FILE)
	pe_out(DebugMessage, "GPU") << "*** FAILED (File Error) ***\n";
      if(get_shader_compilation_status() == SHADER_COMPILATION_STATUS_ERROR_COMPILE)
	pe_out(DebugMessage, "GPU") << "*** FAILED (Compile Error) ***\n";
      if(get_shader_compilation_status() == SHADER_COMPILATION_STATUS_ERROR_LINK)
	pe_out(DebugMessage, "GPU") << "*** FAILED (Link Error) ***\n";
      pe_throw(LogicErr() << "GpuProgram creation failed.");
    }
    return program;
  }

  void clear_gpu_program_cache() {
    for(map<GpuProgramKey, boost::shared_ptr<GpuProgram_GLSL> >::iterator iter = program_cache_glsl.begin(); 
        iter != program_cache_glsl.end(); iter++)
      (*iter).second.reset();
    program_cache_glsl.clear();
  }

} } // namespaces pe::graphics


