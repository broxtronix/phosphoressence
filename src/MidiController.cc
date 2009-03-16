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

#include <MidiController.h>
#include <PeParameters.h>

#include <CoreMIDI/MIDIServices.h>
#include <CoreFoundation/CFRunLoop.h>


// --------------------------------------------------------------------

static void midi_receive_callback(const MIDIPacketList *pktlist, void *refCon, void *connRefCon) {
  ((MidiController*)refCon)->member_callback(pktlist, connRefCon);
}
 
// --------------------------------------------------------------------

class MidiTask {
  
public:
  void operator()() {
    CFRunLoopRun();
  } 
};

// --------------------------------------------------------------------

MidiController::MidiController() : Controller("midi") {

  m_output_port = NULL;
  m_dest = NULL;

  // create client and ports
  MIDIClientRef client = NULL;
  MIDIClientCreate(CFSTR("PhosphorEssence"), NULL, NULL, &client);
        
  MIDIPortRef inPort = NULL;
  MIDIInputPortCreate(client, CFSTR("Input port"), midi_receive_callback, this, &inPort);
  MIDIOutputPortCreate(client, CFSTR("Output port"), &m_output_port);
        
  CFStringRef pname;
  char name[64];
        
  // open connections from all sources
  int n = MIDIGetNumberOfSources();
  if (n == 0) {
    std::cout << "\t    No MIDI sources detected.\n";
    return;
  }

  std::cout << "\t    Listening on " << n << " source(s):\n";
  for (int i = 0; i < n; ++i) {
    MIDIEndpointRef src = MIDIGetSource(i);
    MIDIPortConnectSource(inPort, src, src);
    MIDIObjectGetStringProperty(src, kMIDIPropertyName, &pname);
    CFStringGetCString(pname, name, sizeof(name), 0);
    CFRelease(pname);
    std::cout << "\t    - " << name << "\n";
  }

  select_destination(0);

  // Spin off the MIDI thread to listen on the receive port
  Thread thread(boost::shared_ptr<MidiTask>( new MidiTask() ));
}

void MidiController::list_destinations() {        
  CFStringRef pname;
  char name[64];

  // find the first destination
  int n = MIDIGetNumberOfDestinations();
  for (int i = 0; i < n; ++i) {
    MIDIEndpointRef dest = MIDIGetDestination(0);
    if (m_dest != NULL) {
      MIDIObjectGetStringProperty(m_dest, kMIDIPropertyName, &pname);
      CFStringGetCString(pname, name, sizeof(name), 0);
      CFRelease(pname);
      std::cout << "Destination " << i << " : " << name << "\n";
    }
  }
}

void MidiController::select_destination(int dest) {
  CFStringRef pname;
  char name[64];

  int n = MIDIGetNumberOfDestinations();
  if (n > 0 && dest <= n)
    m_dest = MIDIGetDestination(dest);
  else 
    m_dest = NULL;
  
  if (m_dest != NULL) {
    MIDIObjectGetStringProperty(m_dest, kMIDIPropertyName, &pname);
    CFStringGetCString(pname, name, sizeof(name), 0);
    CFRelease(pname);
    std::cout << "\t    Selecting MIDI destination: " << name << "\n";
  } else {
    std::cout << "Warning: Failed to select MIDI destination " << dest << "\n";
  }
}

void MidiController::send(std::string path, float value) {

}

void MidiController::member_callback(const MIDIPacketList *pktlist, void *connRefCon)  {
  CFStringRef pname;
  char name[64];

  MIDIEndpointRef src = (MIDIEndpointRef)connRefCon;
  MIDIObjectGetStringProperty(src, kMIDIPropertyName, &pname);
  CFStringGetCString(pname, name, sizeof(name), 0);
  CFRelease(pname);
  //  std::cout << name << ":\n";

  MIDIPacket *packet = (MIDIPacket *)pktlist->packet;   
  for (unsigned int j = 0; j < pktlist->numPackets; ++j) {

    std::ostringstream path;
    float value = 0;

    if (packet->length == 3 && packet->data[0] == 0xB0) {  // MIDI CC
      path << "/0/cc"<< int(packet->data[1]);
      value = float(packet->data[2]) / 127;
      //      std::cout << path.str() << " : " << value << "\n";
      this->receive_callback(path.str(), value);
    } else if (packet->length == 3 && packet->data[0] == 0x90) {  // MIDI Note On/Off
      
      // Both
      path << "/0/note"<< int(packet->data[1]);
      value = float(packet->data[2]) / 127;
      this->receive_callback(path.str(), value);

      // Seperate messages
      if (packet->data[2] != 0) {
        std::ostringstream path2;
        path2 << "/0/on"<< int(packet->data[1]);
        value = float(packet->data[2]) / 127;
        this->receive_callback(path2.str(), value);
      } else {
        std::ostringstream path2;
        path2 << "/0/off"<< int(packet->data[1]);
        value = float(packet->data[2]) / 127;
        this->receive_callback(path2.str(), value);
      }
    } else if (packet->length > 0 && packet->data[0] == 0xFE) {
      // pass on "FE" messages 
    } else {
      // For Debugging
      // for (int i = 0; i < packet->length; ++i) 
      //   printf("%02X ", packet->data[i]);
      // printf("\n");
    }

    packet = MIDIPacketNext(packet);
  }

  
    //    MIDISend(m_output_port, m_dest, pktlist);
}

