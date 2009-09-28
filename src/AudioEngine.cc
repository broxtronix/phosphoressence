// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <AudioEngine.h>

using namespace vw;

#include <QAudioDeviceInfo>

AudioInfo::AudioInfo(QObject* parent, QAudioInput* device) :QIODevice( parent ) {
  input = device;
  m_maxValue = 0;
}

AudioInfo::~AudioInfo() {}

void AudioInfo::start() {
  std::cout << "STARTING AUDIOINFO\n";
  open(QIODevice::WriteOnly);
}

void AudioInfo::stop() {
  std::cout << "STOPPING AUDIOINFO\n";
  close();
}

qint64 AudioInfo::readData(char *data, qint64 maxlen) {
  std::cout << "AudioInfo::readData called!!!\n";
  Q_UNUSED(data)
  Q_UNUSED(maxlen)
  return 0;
}

qint64 AudioInfo::writeData(const char *data, qint64 len) {
  std::cout << "AudioInfo::writeData called: " << len << "!!!\n";
  // int samples = len/2; // 2 bytes per sample
  // int maxAmp = 32768; // max for S16 samples
  // bool clipping = false;

  // m_maxValue = 0;
  
  // qint16* s = (qint16*)data;
  
  // // sample format is S16LE, only!
  
  // for(int i=0;i<samples;i++) {
  //   qint16 sample = *s;
  //   s++;
  //   if(abs(sample) > m_maxValue) m_maxValue = abs(sample);
  // }
  // // check for clipping
  // if(m_maxValue>=(maxAmp-1)) clipping = true;
  
  // float value = ((float)m_maxValue/(float)maxAmp);
  // if(clipping) m_maxValue = 100;
  // else m_maxValue = (int)(value*100);
  
  emit update();
  
  return len;
}

int AudioInfo::LinearMax() {
  return m_maxValue;
}

AudioEngine::AudioEngine(QObject *parent, int sample_rate) : QObject(parent) {

  m_buffer = new char[sample_rate * sizeof(float) * 2];
  m_pullMode = true;

  // Select the default audio format settings.
  m_format.setFrequency(44100);
  m_format.setChannels(2);
  m_format.setSampleSize(32);
  m_format.setSampleType(QAudioFormat::Float);
  m_format.setByteOrder(QAudioFormat::LittleEndian);
  m_format.setCodec("audio/pcm");

  // Check to make sure that the audio format is supported.
  QAudioDeviceInfo info(QAudioDeviceInfo::defaultInputDevice());
  vw_out(0) << "\t    Audio input: " << info.deviceName().toStdString() << "\n";
  if (!info.isFormatSupported(m_format)) {
    vw_out(0) << "------------------------------------------------------------------\n";
    vw_out(0) << "WARNING : " << info.deviceName().toStdString() 
              << " does not support the default audio format.  Selecting the nearest"
              << " compatible format.  Strange things may happen.\n\n";
    vw_out(0) << "------------------------------------------------------------------\n";
    m_format = info.nearestFormat(m_format);
  }

  m_audioInput = new QAudioInput(m_format,this);
  //  m_audioInput->setNotifyInterval(5);
  //  m_audioInput->setBufferSize(sample_rate * sizeof(float) * 2);
  std::cout << "Notify interval : " << m_audioInput->notifyInterval() << "\n";
  std::cout << "buffer size : " << m_audioInput->bufferSize() << "\n";
  connect(m_audioInput,SIGNAL(notify()),SLOT(audio_callback()));
  connect(m_audioInput,SIGNAL(stateChanged(QAudio::State)),SLOT(state(QAudio::State)));

  // m_audioinfo  = new AudioInfo(this,m_audioInput);
  // connect(m_audioinfo,SIGNAL(update()),SLOT(test_callback()));
  // m_audioinfo->start();
  std::cout << "Starting...\n";
  //  m_audioInput->start(m_audioinfo);
  std::cout << "Started...\n";
  m_input = m_audioInput->start(0);
  // m_pullMode = false;
}

void AudioEngine::toggleMode() {
  // Change bewteen pull and push modes
  // m_audioInput->stop();
  
  // if (m_pullMode) {
  //   m_input = m_audioInput->start(0);
  //   connect(m_input,SIGNAL(readyRead()),SLOT(readMore()));
  //   m_pullMode = false;
  // } else {
  //   m_pullMode = true;
  //   m_audioInput->start(m_audioinfo);
  // }
}


void AudioEngine::deviceChanged(int idx) {
  // m_audioinfo->stop();
  // m_audioInput->stop();
  // m_audioInput->disconnect(this);
  // delete m_audioInput;
  
  //  device = deviceBox->itemData(idx).value<QAudioDeviceInfo>();
  // m_audioInput = new QAudioInput(m_device, m_format, this);
  // connect(m_audioInput,SIGNAL(notify()),SLOT(status()));
  // connect(m_audioInput,SIGNAL(stateChanged(QAudio::State)),SLOT(state(QAudio::State)));
  // m_audioinfo->start();
  // m_audioInput->start(audioinfo);
}


void AudioEngine::test_callback() {
  vw_out(0) << "\n\n*** CALL TO TEST CALLBACK() \n";
  vw_out(0) <<"bytesReady = "<<m_audioInput->bytesReady()<<" bytes, clock = "<<m_audioInput->clock()<<"ms, totalTime = "<<m_audioInput->totalTime()/1000<<"ms";
}

void AudioEngine::audio_callback() {
  vw_out(0) << "\n\n*** CALL TO AUDIO CALLBACK() \n";
  vw_out(0) <<"   bytesReady = "<<m_audioInput->bytesReady() << "\n"
            <<"   clock = "<<m_audioInput->clock()<<"ms\n"
            <<"   totalTime = "<<m_audioInput->totalTime()/1000<<"ms\n";
  if(m_audioInput->state() == QAudio::SuspendState) {
    vw_out(0)<<"  status: Suspended";
  } else if (m_audioInput->state() == QAudio::ActiveState) {
    vw_out(0)<<"  status: Active";
  } else if (m_audioInput->state() == QAudio::StopState) {
    vw_out(0)<<"  status: Stopped";
  } else if (m_audioInput->state() == QAudio::IdleState) {
    vw_out(0)<<"  status: IdleState";
  }

  if(m_audioInput->error() == QAudio::UnderrunError) {
    vw_out(0)<<"  error: UnderrunError";
  } else if (m_audioInput->error() == QAudio::FatalError) {
    vw_out(0)<<"  error: FatalError";
  } else if (m_audioInput->error() == QAudio::IOError) {
    vw_out(0)<<"  error: IOError";
  } else if (m_audioInput->error() == QAudio::OpenError) {
    vw_out(0)<<"  error: OpenError";
  } else if (m_audioInput->error() == QAudio::NoError) {
    vw_out(0)<<"  error: NoError";
  }

  m_input = m_audioInput->start();

  if(!m_audioInput)
    return;
  qint64 len = m_audioInput->bytesReady();
  std::cout << "Reading " << len << " bytes\n";

  // // if(len > 4096)
  // //   len = 4096;
  
  qint64 l = m_input->read(m_buffer,len);
  std::cout << "l = " << l << "\n";
  // if(l > 0) {
  //   m_audioinfo->write(m_buffer,l);
  // }

  // typedef std::list<boost::shared_ptr<AudioListener> >::iterator iter_type;
  // vw::Mutex::Lock lock(m_mutex);

  // // Pass the audio samples along to each of the registered listeners.
  // for (iter_type iter = m_listeners.begin(); iter != m_listeners.end(); ++iter ) {
  //   (*iter)->audio_callback((float*)m_buffer,m_audioInput->bytesReady()/sizeof(float), NUM_CHANNELS);
  // }

}

void AudioEngine::state(QAudio::State state) {
  vw_out(0) <<" state change="<<state;
}

AudioEngine::~AudioEngine() {
  vw::Mutex::Lock lock(m_mutex);

  m_listeners.clear();
  // Terminate audio listening?
}
