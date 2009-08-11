// __BEGIN_LICENSE__
// Copyright (C) 2006, 2007 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


#ifndef __VW_GPU_GPUPROGRAM_H__
#define __VW_GPU_GPUPROGRAM_H__

#include <map>
#include <stdlib.h>
#include <stdio.h>

#ifdef __linux__
// This is required to get prototypes, according to the opengl linux abi
#define GL_GLEXT_PROTOTYPES 1
#endif

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glext.h>
#endif 

//#include <vw/GPU/Setup.h>
//#include <vw/GPU/GPUImage.h>

namespace vw { namespace GPU {


  extern std::string shader_base_path;

  extern bool shader_assembly_cache_enabled;

  extern std::string shader_assembly_cache_path;


  //########################################################################
  //#                  
  //########################################################################

  enum ShaderCompilationStatusEnum  {
    SHADER_COMPILATION_STATUS_SUCCESS = 0,
    SHADER_COMPILATION_STATUS_FILE_ERROR,
    SHADER_COMPILATION_STATUS_COMPILE_ERROR,
    SHADER_COMPILATION_STATUS_SUCCESS_FILE,
    SHADER_COMPILATION_STATUS_SUCCESS_CACHE,
    SHADER_COMPILATION_STATUS_ERROR_FILE,
    SHADER_COMPILATION_STATUS_ERROR_COMPILE,
    SHADER_COMPILATION_STATUS_ERROR_LINK
  };

  extern ShaderCompilationStatusEnum shaderCompilationStatus;

  inline ShaderCompilationStatusEnum get_shader_compilation_status() {
    return shaderCompilationStatus;
  }

  //########################################################################
  //#    Class: GPUProgram  (abstract)             
  //########################################################################

  class GpuProgram {
  public:
    // Virtual	
    virtual ~GpuProgram() { }
    virtual void install() = 0;
    virtual void uninstall() = 0;
    //    virtual void set_input_image(const char* name, const GPUImageBase& texture) = 0;
    virtual void set_input_int(const char* name, int value) = 0;
    virtual void set_input_float(const char* name, float value) = 0;
  };

  //################################################################################################################
  //  GLSL:    
  //    GPUVertexShader_GLSL
  //    GPUFragmentShader_GLSL
  //    GpuProgram_GLSL (subclass), 
  //    GpuProgramSet_GLSL (subclass)      
  //################################################################################################################

  class GPUVertexShader_GLSL {
    GLhandleARB shader;
  public:
    bool compile(const std::string& vertexString);
    // Inline	
    GPUVertexShader_GLSL() { shader = 0; }
    ~GPUVertexShader_GLSL() { if(shader) glDeleteObjectARB(shader); }

    bool is_compiled() { return shader != 0; }
    GLhandleARB get_shader() { return shader; }
  };


  class GPUFragmentShader_GLSL {
    GLhandleARB shader;
  public:
    bool compile(const std::string& fragmentString);
    // Inline	
    GPUFragmentShader_GLSL() { shader = 0; }
    ~GPUFragmentShader_GLSL() { if(shader) glDeleteObjectARB(shader); }

    bool is_compiled() { return shader != 0; }
    GLhandleARB get_shader() { return shader; }
	
  };


  class GpuProgram_GLSL : public GpuProgram {
    GLhandleARB program;
    int bound_texture_count;
  public:
    bool Link(GPUVertexShader_GLSL& vertex, GPUFragmentShader_GLSL& fragment);

    GpuProgram_GLSL() { program = 0; bound_texture_count = 0; }
    ~GpuProgram_GLSL() { if(program) glDeleteObjectARB(program); }

    GLhandleARB get_program() { return program; }

    // Over-Riden
    void install() { 
      glUseProgramObjectARB(program); 
      bound_texture_count = 0;
    }

    void uninstall() {
      glUseProgramObjectARB(0); 
    }

    // void set_input_image(const char* name, const GPUImageBase& texture) { 
    //   glUniform1i(glGetUniformLocationARB(program, name), bound_texture_count);
    //   glGetError();
    //   glActiveTexture(GL_TEXTURE0 + bound_texture_count);
    //   if(glGetError() != GL_NO_ERROR)
    //     throw(Exception("[GpuProgram::set_input_image] Error: Too many textures bound."));
    //   texture.bind();
    //   bound_texture_count++;
    // }

    void set_input_int(const char* name, int value) {
      glUniform1i(glGetUniformLocationARB(program, name), value);	
    }

    void set_input_float(const char* name, float value) {
      glUniform1f(glGetUniformLocationARB(program, name), value);	
    }

  };


  //#############################################################################################
  //#    Creation Free Functions   
  //#############################################################################################

    boost::shared_ptr<GpuProgram> create_gpu_program(const std::string& fragmentPath, 
                                                     const std::vector<int>& fragmentAttributes = std::vector<int>(),
                                                     const std::string& vertexPath = "", 
                                                     const std::vector<int>& vertexAttributes = std::vector<int>());

    boost::shared_ptr<GpuProgram_GLSL> create_gpu_program_glsl_string(const std::string& fragmentString, 
                                                                      const std::vector<int>& fragmentAttributes = std::vector<int>(),
                                                                      const std::string& vertexString = "", 
                                                                      const std::vector<int>& vertexAttributes = std::vector<int>());

    boost::shared_ptr<GpuProgram_GLSL> create_gpu_program_glsl(const std::string& fragmentPath, 
                                                               const std::vector<int>& fragmentAttributes = std::vector<int>(),
                                                               const std::string& vertexPath = "", 
                                                               const std::vector<int>& vertexAttributes = std::vector<int>());
    
    
    void clear_gpu_program_cache();

} } // namespaces GPU, vw

#endif

