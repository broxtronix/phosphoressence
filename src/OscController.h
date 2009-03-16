// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <string>
#include <lo/lo.h>
#include <Controller.h>

// TODO: Need to think about how to shut down the Osc Server thread
// cleanly.
class OscController : public Controller {
  bool m_done;
  lo_server_thread m_server_thread;
  lo_address m_send_addr;

public:
  OscController(std::string receive_port, 
                std::string send_address, 
                std::string send_port );
  virtual ~OscController() {}

  virtual void send(std::string path, float value);
  void member_callback(std::string path, float value, int index);
};
