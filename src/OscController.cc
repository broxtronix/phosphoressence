// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>

#include <vw/Core/Log.h>
using namespace vw;

#include <OscController.h>
#include <PeParameters.h>


// --------------------------------------------------------------------

// Here are the various server callbacks.
void error(int num, const char *msg, const char *path) {
  printf("OscControl error -- %d in path %s: %s\n", num, path, msg);
}

int generic_handler(const char *path, const char *types, lo_arg **argv,
		    int argc, void *data, void *user_data) {
  for (int i = 0; i < argc; ++i) {
    float value = argv[i]->f32;
    ((OscController*)user_data)->member_callback(path, value, i);
  }
  return 1;
}

// --------------------------------------------------------------------

OscController::OscController(std::string receive_port, 
                             std::string send_address, 
                             std::string send_port ) : Controller("osc") {
  
  // start a new server on the port specified
  m_server_thread = lo_server_thread_new(receive_port.c_str(), error);

  // add method that will match any path and args
  lo_server_thread_add_method(m_server_thread, NULL, NULL, generic_handler, this);
  lo_server_thread_start(m_server_thread);

  // Set up the address for outgoing packets
  m_send_addr = lo_address_new(send_address.c_str(), send_port.c_str());
}

void OscController::send(std::string path, float value) {
  vw_out(DebugMessage, "Controller") << "Controller send: " << path << " -- " << value << "\n";
  lo_send(m_send_addr, path.c_str(), "f", value);
}

// void OscController::send(std::string path, float value1, float value2) {
//   std::cout << "Controller Reset: " << path << " -- " << value1 << " " << value2 << "\n";
//   lo_send(m_send_addr, path.c_str(), "ff", value1, value2);
// }

void OscController::member_callback(std::string path, float value, int index) {
  if (index == 1) 
    std::cout << "WARNING: xy controllers not yet supported in OSC!\n";
  this->receive_callback(path, value);
}

