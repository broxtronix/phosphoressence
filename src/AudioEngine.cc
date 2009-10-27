// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <AudioEngine.h>
using namespace vw;

AudioThread::AudioThread(int sample_rate) {

  if ( m_adc.getDeviceCount() < 1 ) {
    std::cout << "\t--> WARNING: No audio devices found!\n";
    return;
  }
  
  for (unsigned i = 0; i < m_adc.getDeviceCount(); ++i) {
    std::cout << "\t    Found device: " << m_adc.getDeviceInfo(i).name << "\n";
  }

  RtAudio::StreamParameters parameters;
  parameters.deviceId = m_adc.getDefaultInputDevice();
  parameters.nChannels = NUM_CHANNELS;
  parameters.firstChannel = 0;
  unsigned int sampleRate = sample_rate;
  unsigned int bufferFrames = 512;  // FRAMES_PER_BUFFER (callback happens at ~86 Hz)

  try {
    m_adc.openStream( NULL, &parameters, RTAUDIO_FLOAT32,
                    sampleRate, &bufferFrames, &AudioThread::static_callback, this);
    m_adc.startStream();
  }
  catch ( RtError& e ) {
    e.printMessage();
    exit( 0 );
  }
}

AudioThread::~AudioThread() {
  vw::Mutex::Lock lock(m_mutex);
  m_listeners.clear();

  // Stop the stream
  try {
    m_adc.stopStream();
  }
  catch (RtError& e) {
    vw::vw_throw(vw::LogicErr() << "Could not close input audio stream: " << e.what());
  }

  if ( m_adc.isStreamOpen() ) m_adc.closeStream();
}

int AudioThread::member_callback( void *outputBuffer, void *inputBuffer, 
                                  unsigned int nBufferFrames,
                                  double streamTime, RtAudioStreamStatus status ) {

  typedef std::list<boost::shared_ptr<AudioListener> >::iterator iter_type;
  vw::Mutex::Lock lock(m_mutex);

  // Pass the audio samples along to each of the registered listeners.
  for (iter_type iter = m_listeners.begin(); iter != m_listeners.end(); ++iter ) {
    (*iter)->audio_callback((float*) inputBuffer, nBufferFrames, NUM_CHANNELS);
  }

  // Signal that everything worked ok.
  return 0;
}
