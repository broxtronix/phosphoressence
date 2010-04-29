#include <pe/Core/Thread.h>
#include <StandardShaders.h>

#include <iostream>

static std::map<std::string, const char*> standard_shaders_map;

namespace {
  pe::RunOnce standard_shaders_once = PE_RUNONCE_INIT;
  void init_standard_shaders() {
  }
}

std::string pe::graphics::find_standard_shader(std::string path) {
  standard_shaders_once.run( init_standard_shaders );

  std::map<std::string, const char*>::iterator iter_map = standard_shaders_map.find((path).c_str());
  if(iter_map != standard_shaders_map.end()) {
    return (*iter_map).second;
  } else {
    std::cout << "ERROR: Could not find requested shader: " << path << "\n";    exit(0);  } 
}
