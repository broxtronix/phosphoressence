// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <vw/Core/Exception.h>
#include <AudioEngine.h>
using namespace vw;

// ---------------------------------------------------------------------------
//                              Audio Listener
// ---------------------------------------------------------------------------

AudioListener::AudioListener(bool mono, float buffer_length, int sample_rate) : 
  m_mono(mono), 
  m_buffer_length(buffer_length), 
  m_sample_rate(sample_rate),
  m_circular_buffer(buffer_length * sample_rate) {
}

void AudioListener::set_sample_rate( int sample_rate ) {
  Mutex::Lock lock(m_mutex);
  m_sample_rate = sample_rate;
  m_circular_buffer.rset_capacity(sample_rate * m_buffer_length);
}

void AudioListener::audio_callback(float* input, unsigned long frame_count, int num_channels) {
  vw::Mutex::Lock lock(m_mutex);

  const float *rptr = (const float*)input;
  
  for( int i=0; i<frame_count; ++i) {
    
    // Gather data from all channels
    float channel_data[num_channels];
    for (int c = 0; c < num_channels; ++c) {
      
      // If the input in NULL, then there is no audio available for
      // us.  We fill the ring buffer with empty entries.
      if( input == NULL ) {
        channel_data[c] = 0.0;
      } else {
        channel_data[c] = *rptr++;
      }
    }

    if (m_mono) {

      // If this is a mono listener, then we simply average the channels together.
      float avg_channel_data;
      for (int c = 0; c < num_channels; ++c) 
        avg_channel_data += channel_data[c];
      m_circular_buffer.push_back(avg_channel_data / num_channels);

    } else {

      // Otherwise, we push all channels onto the ring buffer.
      for (int c = 0; c < num_channels; ++c) 
        m_circular_buffer.push_back(channel_data[c]);                           

    }
  }
}

// ---------------------------------------------------------------------------
//                               Audio Thread
// ---------------------------------------------------------------------------

AudioThread::AudioThread(int num_channels, int sample_rate) : 
  m_sample_rate(sample_rate), m_num_channels(num_channels) {

  if ( m_adc.getDeviceCount() < 1 ) {
    std::cout << "\t--> WARNING: No audio devices found!\n";
    return;
  }
  
  for (unsigned i = 0; i < m_adc.getDeviceCount(); ++i) {
    std::cout << "\t    Found device: " << m_adc.getDeviceInfo(i).name << "\n";
  }

  RtAudio::StreamParameters parameters;
  parameters.deviceId = m_adc.getDefaultInputDevice();
  parameters.nChannels = num_channels;
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
    vw_throw(vw::LogicErr() << "Could not close input audio stream: " << e.what());
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
    (*iter)->audio_callback((float*) inputBuffer, nBufferFrames, m_num_channels);
  }

  // Signal that everything worked ok.
  return 0;
}
