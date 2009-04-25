// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__
#ifndef __PHASESCOPE_SHAPE_H__
#define __PHASESCOPE_SHAPE_H__

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#endif 

#include <AudioEngine.h>
#include <PeParameters.h>

#include <vw/Math/Vector.h>

class PhasescopeShape : public AudioListener, public Drawable {
  float m_time;
  float m_time_slice;
  float m_ending_x;
  float m_ending_y;
  
public:
  PhasescopeShape() : AudioListener(5.0), m_time(0) {
    m_time_slice = 1.0f / this->sample_rate();
    m_ending_x = 0;
    m_ending_y = 0;
  }

  virtual void draw(float time, float gain) {

    float dt_draw = 1/AUDIO_SAMPLE_RATE; // TODO : Replace with call to sample_rate()
    float tau_excite = 3e-5;   // TODO : Move to parameters
    float tau_decay = -(1/30.0)/log(pe_parameters().get_value("decay")); // TODO: Avoid using fixed frame rate!
    float beta = (1-exp(-dt_draw/tau_decay)); // TODO: Move tau_decay to pe_parameters()

    // Read the values into a local audio cache
    float left_cache[int(AUDIO_SAMPLE_RATE)];
    float right_cache[int(AUDIO_SAMPLE_RATE)];
    int idx = 0;
    {
      vw::Mutex::Lock lock(m_mutex);

      float *data_ptr = &(m_data.samples[m_data.read_index * NUM_CHANNELS]);
      while (m_data.read_index != m_data.write_index) {
        if (idx < AUDIO_SAMPLE_RATE) {
          left_cache[idx] = *data_ptr++*2.0;
          right_cache[idx] = *data_ptr++*2.0;
          ++idx;
        } 

        // Go to next frame
        m_time += m_time_slice;
        if ( (m_data.read_index)++ >= m_data.max_frame_index ) {
          m_data.read_index = 0;
          data_ptr = &(m_data.samples[0]);
        }
      }
    }

    // Set up the GL parameters for drawing
    glLoadIdentity();
    float wave_x = pe_parameters().get_value("wave_x")*2-1;
    float wave_y = pe_parameters().get_value("wave_y")*2-1;
    glTranslatef(wave_x, wave_y, 0);

    if (pe_parameters().get_value("wave_thick")) {
      glLineWidth(2.0);
      glPointSize(3.0);
    } else {
      glLineWidth(0.25);
      glPointSize(1.0);
    }

    float wave_r = pe_parameters().get_value("wave_r");
    float wave_g = pe_parameters().get_value("wave_g");
    float wave_b = pe_parameters().get_value("wave_b");
    float wave_a = pe_parameters().get_value("wave_a");
    vw::Vector3 color(wave_r, wave_g, wave_b);
    vw::Vector3 norm_color = color;
    if (pe_parameters().get_value("wave_brighten")) 
      norm_color = normalize(color);

    glEnable(GL_BLEND);
    glBlendFunc (GL_ONE, GL_ZERO);

    if (pe_parameters().get_value("wave_usedots")) 
      glBegin(GL_POINTS);
    else 
      glBegin(GL_LINES);

    // Draw the line connecting the last sample in the previous frame
    // to the first sample in this frame.
    float r = norm_color[0] * gain;
    float g = norm_color[1] * gain;
    float b = norm_color[2] * gain;
    glColor4f(r, g, b, wave_a );
      
    glVertex2d(m_ending_x,  m_ending_y);
    glVertex2d(left_cache[0], right_cache[0]);

    m_ending_x = left_cache[idx-1];
    m_ending_y = right_cache[idx-1];

    // Now draw the wave by traversing the buffer in reverse
    // order.
    float one_minus_beta_accum = 1.0;
    for (int i = 1; i < idx; ++i) {

      // Compute the phosphor color
      float d = sqrt(pow(left_cache[i]-left_cache[i-1],2) + 
                     pow(right_cache[i]-right_cache[i-1],2));
      float dt_phosphor = dt_draw/d;
      float alpha = 1-exp(-dt_phosphor/tau_excite);
      float beta_factor = pow(1-beta,idx-1-i);
      float r = norm_color[0] * alpha * beta_factor;
      float g = norm_color[1] * alpha * beta_factor;
      float b = norm_color[2] * alpha * beta_factor;
      glColor4f(r, g, b, wave_a );

      //      one_minus_beta_accum *= (1-beta);
      
      // We only draw the line if it moves from left to right.  (We
      // don't draw the scan return...)
      glVertex2d(left_cache[i-1],  right_cache[i-1]);
      glVertex2d(left_cache[i], right_cache[i]);
    }
    glEnd();
    glDisable(GL_BLEND);
  }
};

#endif // __OSCOPE_SHAPE_H__
