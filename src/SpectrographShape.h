// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__
#ifndef __SPECTROGRAPH_SHAPE_H__
#define __SPECTROGRAPH_SHAPE_H__

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#endif 

#include <QTimer>
#include <QWidget>

#include <AudioEngine.h>
#include <PeParameters.h>
#include <ScriptEngine.h>
#include <GraphicsEngine.h>
#include <FFT.h>

#include <vw/Math/Vector.h>

#define NUM_FFT_SAMPLES 2048

class SpectrographShape : public AudioListener, public Drawable {
  FFT m_fft;
  float left_samples[NUM_FFT_SAMPLES];
  float left_spectrum[NUM_FFT_SAMPLES];
  float right_samples[NUM_FFT_SAMPLES];
  float right_spectrum[NUM_FFT_SAMPLES];
  int m_sample_index;
public:
  SpectrographShape() : AudioListener(false, 5.0), m_sample_index(0) {
    m_fft.Init(NUM_FFT_SAMPLES, NUM_FFT_SAMPLES, 
               0,     // Do not equalize to de-emphasize low frequencies
               0.0);  // Use a small amount of envelope (smoothing)
  }


  virtual void draw(float time,float gain) {

    // Compute the FFT
    {
      vw::Mutex::Lock lock(m_mutex);
      while ( m_circular_buffer.size() >= 2 ) {

        left_samples[m_sample_index] = m_circular_buffer[0];
        m_circular_buffer.pop_front();
        right_samples[m_sample_index] = m_circular_buffer[0];
        m_circular_buffer.pop_front();
        ++m_sample_index;
        
        // Draw the waveshape
        if (m_sample_index == NUM_FFT_SAMPLES) {
          m_sample_index = 0;
          m_fft.time_to_frequency_domain(left_samples, left_spectrum);
          m_fft.time_to_frequency_domain(right_samples, right_spectrum);

          // Set up the GL parameters for drawing
          glLoadIdentity();
          float wave_x = 0; //pe_script_engine().get_parameter("wave_x")*2-1;
          float wave_y = 0; //pe_script_engine().get_parameter("wave_y")*2-1;
          glTranslatef(wave_x, wave_y, 0);
          
          if (pe_script_engine().get_parameter("wave_thick")) {
            glLineWidth(2.0);
            glPointSize(3.0);
          } else {
            glLineWidth(0.25);
            glPointSize(1.0);
          }

          float wave_r = pe_script_engine().get_parameter("wave_r");
          float wave_g = pe_script_engine().get_parameter("wave_g");
          float wave_b = pe_script_engine().get_parameter("wave_b");
          float wave_a = pe_script_engine().get_parameter("wave_a");
          vw::Vector3 color(wave_r, wave_g, wave_b);
          vw::Vector3 norm_color = color;
          if (pe_script_engine().get_parameter("wave_brighten")) 
            norm_color = normalize(color);
          
          glEnable(GL_BLEND);
          if (pe_script_engine().get_parameter("wave_additive"))
            glBlendFunc (GL_SRC_ALPHA, GL_ONE);
          else
            glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
                    
          if (pe_script_engine().get_parameter("wave_usedots")) 
            glBegin(GL_POINTS);
          else 
            glBegin(GL_LINES);
          
          float horiz_pos = 0.0;
          float T = float(NUM_FFT_SAMPLES)/this->sample_rate(); // FFT length
          float log_lo = log10f(1/T);
          float log_hi = log10f(float(NUM_FFT_SAMPLES/2)/T);
          float aspect = pe_script_engine().get_parameter("aspect");
          for (unsigned i=1; i < NUM_FFT_SAMPLES/2; ++i) {

            // This bit of math sets up a position between [-aspec +aspect]
            // on a log scale.
            float f = float(i)/T;        // FFT frequency
            horiz_pos = ( (log10f(f)-log_lo)/(log_hi-log_lo) )*2*aspect-aspect;
            
            // Draw the bar as more red as the volume increases
            //            std::cout << spectrum[i] << "\n";
            glColor4f(norm_color[0], norm_color[1], norm_color[2], wave_a );

            // Taking the square root of the averaged spectrum values
            // seems to be a good way to attenuate large spectrum
            // values relative to smaller ones, making for a more
            // aesthetically pleasing spectrum.
            float spectrum_value = sqrt((left_spectrum[i]+right_spectrum[i])/2);

            // Here we choose between drawing the scope vertically
            // (orientation = 1.0) or horizonatally (orientation = 0.0).
            if (pe_parameters().get_value("orientation") == 1.0) {
              glVertex2d(1.0, horiz_pos/aspect);
              glVertex2d(1.0-spectrum_value*0.06, horiz_pos/aspect);
            } else {
              glVertex2d(horiz_pos, -1.0);
              glVertex2d(horiz_pos, spectrum_value*0.1-1.0);
            }

            // // Right
            // glVertex2d(horiz_pos, 1.0);
            // glVertex2d(horiz_pos, -(right_spectrum[i]*80-1.0));
          }
          glEnd();
          glDisable(GL_BLEND);
          
        }
        
      }
    }
  }
};

// AveragingListener
//
// Listens to the audio stream and computes aggregate statistics.
#define FFT_SAMPLES 512

class SoundStatsListener : public QObject, public AudioListener {
  Q_OBJECT

  QTimer* m_timer;
  FFT m_fft;
  int m_sample_index;
  float left_samples[FFT_SAMPLES];
  float right_samples[FFT_SAMPLES];
  float left_spectrum[FFT_SAMPLES];
  float right_spectrum[FFT_SAMPLES];
  int m_nFrames;

  float left_imm[3];			// bass, mids, treble (absolute)
  float	left_imm_rel[3];		// bass, mids, treble (relative to song; 1=avg, 0.9~below, 1.1~above)
  float	left_avg[3];			// bass, mids, treble (absolute)
  float	left_avg_rel[3];		// bass, mids, treble (relative to song; 1=avg, 0.9~below, 1.1~above)
  float	left_long_avg[3];	        // bass, mids, treble (absolute)

  float right_imm[3];			// bass, mids, treble (absolute)
  float	right_imm_rel[3];		// bass, mids, treble (relative to song; 1=avg, 0.9~below, 1.1~above)
  float	right_avg[3];			// bass, mids, treble (absolute)
  float	right_avg_rel[3];		// bass, mids, treble (relative to song; 1=avg, 0.9~below, 1.1~above)
  float	right_long_avg[3];	        // bass, mids, treble (absolute)

public:
  SoundStatsListener() : AudioListener(false, 5.0), m_sample_index(0) {
    m_fft.Init(FFT_SAMPLES, FFT_SAMPLES,
               0,      // Do not equalize to de-emphasize low frequencies
               10.0);  // Use a small amount of envelope (smoothing)
    m_nFrames		= 0;
    
    memset(left_imm      , 0, sizeof(float)*3);
    memset(left_imm_rel  , 0, sizeof(float)*3);
    memset(left_avg      , 0, sizeof(float)*3);
    memset(left_avg_rel  , 0, sizeof(float)*3);
    memset(left_long_avg , 0, sizeof(float)*3);

    memset(right_imm      , 0, sizeof(float)*3);
    memset(right_imm_rel  , 0, sizeof(float)*3);
    memset(right_avg      , 0, sizeof(float)*3);
    memset(right_avg_rel  , 0, sizeof(float)*3);
    memset(right_long_avg , 0, sizeof(float)*3);

    m_timer = new QTimer(this);
    connect(m_timer, SIGNAL(timeout()), this, SLOT(update()));
    m_timer->start(5); // The statistics are reprocessed 200 times a second
  }

public slots:
  // Compute the FFT & update statistics.  
  void update() {
    vw::Mutex::Lock lock(m_mutex);

    while ( m_circular_buffer.size() >= 2 ) {
      
      left_samples[m_sample_index] = m_circular_buffer[0];
      m_circular_buffer.pop_front();
      if ( this->mono() ) {
        right_samples[m_sample_index] = left_samples[m_sample_index];
      } else {
        right_samples[m_sample_index] = m_circular_buffer[1];
        m_circular_buffer.pop_front();
      }
      ++m_sample_index;

      // If we have collected a full window of data, we process it!
      if (m_sample_index == FFT_SAMPLES) {
        m_sample_index = 0;
	m_fft.time_to_frequency_domain(left_samples, left_spectrum);
	m_fft.time_to_frequency_domain(right_samples, right_spectrum);

	// sum spectrum up into 3 bands
	for (unsigned i=0; i<3; i++) {
          // note: only look at bottom half of spectrum!  (hence divide by 6 instead of 3)
          int start = FFT_SAMPLES*i/6;
          int end   = FFT_SAMPLES*(i+1)/6;
          
          left_imm[i] = 0;
          right_imm[i] = 0;
          
          for (unsigned j=start; j<end; j++) {
            left_imm[i] += left_spectrum[j];
            right_imm[i] += right_spectrum[j];
          }
	}
        
	// do temporal blending to create attenuated and super-attenuated versions
	for (unsigned i=0; i<3; i++) {
          if (left_imm[i] > left_avg[i])
            left_avg[i] = left_avg[i]*0.2f + left_imm[i]*0.8f;
          else
            left_avg[i] = left_avg[i]*0.5f + left_imm[i]*0.5f;

          if (right_imm[i] > right_avg[i])
            right_avg[i] = right_avg[i]*0.2f + right_imm[i]*0.8f;
          else
            right_avg[i] = right_avg[i]*0.5f + right_imm[i]*0.5f;

          if (m_nFrames < 50) {
            left_long_avg[i] = left_long_avg[i]*0.900f + left_imm[i]*0.100f;
            right_long_avg[i] = right_long_avg[i]*0.900f + right_imm[i]*0.100f;
          } else {
            left_long_avg[i] = left_long_avg[i]*0.992f + left_imm[i]*0.008f;
            right_long_avg[i] = right_long_avg[i]*0.992f + right_imm[i]*0.008f;
          }

          // also get bass/mid/treble levels *relative to the past*
          if (fabsf(left_long_avg[i]) < 0.001f)
            left_imm_rel[i] = 1.0f;
          else
            left_imm_rel[i]  = left_imm[i] / left_long_avg[i];

          if (fabsf(right_long_avg[i]) < 0.001f)
            right_imm_rel[i] = 1.0f;
          else
            right_imm_rel[i]  = right_imm[i] / right_long_avg[i];
          
          if (fabsf(left_long_avg[i]) < 0.001f)
            left_avg_rel[i]  = 1.0f;
          else
            left_avg_rel[i]  = left_avg[i] / left_long_avg[i];

          if (fabsf(right_long_avg[i]) < 0.001f)
            right_avg_rel[i]  = 1.0f;
          else
            right_avg_rel[i]  = right_avg[i] / right_long_avg[i];
	}

        m_nFrames++;

        
      }
    }

    
    // Update the various PE Parameters
    pe_script_engine().set_parameter("bass", left_avg[0]);
    pe_script_engine().set_parameter("mid", left_avg[1]);
    pe_script_engine().set_parameter("treb", left_avg[2]);
    pe_script_engine().set_parameter("bass_att",left_avg_rel[0]);
    pe_script_engine().set_parameter("mid_att", left_avg_rel[1]);
    pe_script_engine().set_parameter("treb_att", left_avg_rel[2]);

    pe_script_engine().set_parameter("bass_r", right_avg[0]);
    pe_script_engine().set_parameter("mid_r", right_avg[1]);
    pe_script_engine().set_parameter("treb_r", right_avg[2]);
    pe_script_engine().set_parameter("bass_att_r",right_avg_rel[0]);
    pe_script_engine().set_parameter("mid_att_r", right_avg_rel[1]);
    pe_script_engine().set_parameter("treb_att_r", right_avg_rel[2]);
  }
};



#endif // __SPECTROGRAPH_SHAPE_H__
