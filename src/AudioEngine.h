// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#ifndef __AUDIO_ENGINE_H__
#define __AUDIO_ENGINE_H__

#include <vw/Core/Thread.h>
#include <RtAudio.h>
#include <boost/circular_buffer.hpp>

// ---------------------------------------------------------------------------
//                              Audio Listener
// ---------------------------------------------------------------------------

class AudioListener {
  
  bool m_mono;
  float m_buffer_length; // seconds
  int m_sample_rate;     // hz

protected:
  boost::circular_buffer<float> m_circular_buffer;

  // This mutex must be locked by child classes when they access the
  // AudioBuffer.  Perhaps this should be abstracted away behind some
  // function call?
  vw::Mutex m_mutex;

public:

  AudioListener(bool mono, float buffer_length = 5.0, int sample_rate = 96000);

  /// This is called by the AudioThread to set the proper sampling
  /// rate when this listener is registered.
  void set_sample_rate( int sample_rate );

  float buffer_length() const { return m_buffer_length; }
  int sample_rate() const { return m_sample_rate; }
  bool mono() const { return m_mono; }

  /// This audio callback is called whenever there is new data
  /// available on the audio input device.
  void audio_callback(float* input, unsigned long frame_count, int num_channels);
};

// ---------------------------------------------------------------------------
//                              Audio Thread
// ---------------------------------------------------------------------------

/// AudioThread
///
/// This thread capture audio input using RtAudio.  Classes can
/// register as "AudioListeners" to have their callback called when
/// new audio samples become available.  
/// 
/// Note: once QT 4.6 is released, we will switch to using their audio
/// API so as to remove this dependency.
///
class AudioThread {
  vw::Mutex m_mutex;
  int m_sample_rate;
  int m_num_channels;

  // RtAudio device
  RtAudio m_adc;

  // List of Audio Listeners
  std::list<boost::shared_ptr<AudioListener> > m_listeners;

public:

  int member_callback( void *outputBuffer, void *inputBuffer, unsigned int nBufferFrames,
                       double streamTime, RtAudioStreamStatus status );

  // This static class helps to bridge the gap between RtAudio's C
  // API and the world of C++.  It simply forwards the callback to
  // this instance's member_callback() method.
  static int static_callback(void *outputBuffer, void *inputBuffer, unsigned int nBufferFrames,
                             double streamTime, RtAudioStreamStatus status, void *userData ) {
    return ((AudioThread*)userData)->member_callback(outputBuffer, inputBuffer, nBufferFrames,
                                                     streamTime, status);

  }
  
  AudioThread(int num_channels = 2, int sample_rate = 96000);
  ~AudioThread();

  void register_listener(boost::shared_ptr<AudioListener> listener) {
    vw::Mutex::Lock lock(m_mutex);
    m_listeners.push_back(listener);
    listener->set_sample_rate(m_sample_rate);
  }

  void clear_listeners() {
    vw::Mutex::Lock lock(m_mutex);
    m_listeners.clear();
  }

};

#endif // __AUDIOENGINE_H__
