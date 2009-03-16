// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <string>
#include <Controller.h>

#include <CoreMIDI/MIDIServices.h>

// TODO: Need to think about how to shut down the Osc Server thread
// cleanly.
class MidiController : public Controller {

  MIDIPortRef             m_output_port;
  MIDIEndpointRef         m_dest;

public:
  MidiController();
  virtual ~MidiController() {}

  virtual void send(std::string path, float value);
  void member_callback(const MIDIPacketList *pktlist, void *connRefCon);

  void list_destinations();
  void select_destination(int dest);

};
