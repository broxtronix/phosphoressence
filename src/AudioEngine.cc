// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <AudioEngine.h>

using namespace vw;

AudioThread::AudioThread(int sample_rate) {
  PaError err = Pa_Initialize();
  if( err != paNoError ) 
    vw::vw_throw(vw::LogicErr() << "Could not initialize PortAudio.\n");

  int numDevices = Pa_GetDeviceCount();
  if( numDevices < 0 ) {
    std::cout << "Warning: No audio devices found!\n";
    exit(0);
  }

  PaStreamParameters input_parameters;
  input_parameters.device = Pa_GetDefaultInputDevice(); // default input device 

  // TODO: Use this code someday to select audio inputs
  //
  // const PaDeviceInfo *deviceInfo;
  // for(int i=0; i<numDevices; i++ ) {
  //   deviceInfo = Pa_GetDeviceInfo( i );
  //   std::cout << "\t    Found " << deviceInfo->name << "\n";
  //   if (std::string(deviceInfo->name) == "FireWire 410 Multichannel") {
  //     std::cout << "\t -->" << input_parameters.device << "\n";
  //     std::cout << "\t -->Overriding default audio input with " << deviceInfo->name << "\n";
  //     input_parameters.device = i;
  //   }
  // }

  input_parameters.device = Pa_GetDefaultInputDevice(); // default input device 
  input_parameters.channelCount = NUM_CHANNELS;         // stereo input 
  input_parameters.sampleFormat = paFloat32;
  input_parameters.suggestedLatency = Pa_GetDeviceInfo( input_parameters.device )->defaultLowInputLatency;
  input_parameters.hostApiSpecificStreamInfo = NULL;

  // Open the audio stream.  We choose to have the callback called
  // every 512 frames, which should result in callbacks approx. 86
  // times per second.  This is high enough above the video frame rate
  // that AudioListeners will have consistently full buffers.
  err = Pa_OpenStream(&m_stream,
                      &input_parameters,
                      NULL,           // &outputParameters,
                      sample_rate,
                      512,            // FRAMES_PER_BUFFER (callback
                                      // happens at ~86 Hz)
                      paClipOff,      // We won't output out of range
                                      // samples so don't bother
                                      // clipping them
                      &AudioThread::pa_callback, this); 
  if( err != paNoError ) 
    vw::vw_throw(vw::LogicErr() << "Could not open the input audio stream.\n");

  // Start listening for audio input.
  err = Pa_StartStream( m_stream );
  if( err != paNoError ) 
    vw::vw_throw(vw::LogicErr() << "Could not initiate recording of the input audio stream.\n");
}

AudioThread::~AudioThread() {
  vw::Mutex::Lock lock(m_mutex);

  m_listeners.clear();
  PaError err = Pa_CloseStream( m_stream );
  if( err != paNoError ) 
    vw::vw_throw(vw::LogicErr() << "Could not close input audio stream.\n");
  Pa_Terminate();
}

int AudioThread::member_callback(const void *input, void *output,
                                 unsigned long frame_count,
                                 const PaStreamCallbackTimeInfo* timeInfo,
                                 PaStreamCallbackFlags statusFlags) {
  typedef std::list<boost::shared_ptr<AudioListener> >::iterator iter_type;
  vw::Mutex::Lock lock(m_mutex);
    
  // Prevent unused variable warnings. 
  (void) output; 
  (void) timeInfo;
  (void) statusFlags;

  // Pass the audio samples along to each of the registered listeners.
  for (iter_type iter = m_listeners.begin(); iter != m_listeners.end(); ++iter ) {
    (*iter)->audio_callback((float*) input, frame_count, NUM_CHANNELS);
  }

  // Signal that everything worked ok.
  return paContinue;
}
