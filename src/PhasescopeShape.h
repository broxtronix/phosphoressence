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

#include <pe/Math/Vector.h>

class PhasescopeShape : public AudioListener, public Drawable {
  float m_time;
  float m_time_slice;
  float m_ending_x;
  float m_ending_y;
  
  boost::shared_array<float> m_left_cache;
  boost::shared_array<float> m_right_cache;

public:
  PhasescopeShape() : AudioListener(false, 5.0), m_time(0) {
    m_time_slice = 1.0f / this->sample_rate();
    m_ending_x = 0;
    m_ending_y = 0;

    m_left_cache.reset(new float[this->sample_rate()]);
    m_right_cache.reset(new float[this->sample_rate()]);
  }

  virtual void draw(float time, float gain) {

    float dt_draw = 1.0/float(this->sample_rate());
    float tau_excite = 3e-5;   // TODO : Move to parameters
    float tau_decay = -(1/30.0)/log(pe_script_engine().get_parameter("decay")); // TODO: Avoid using fixed frame rate!
    float beta = (1-exp(-dt_draw/tau_decay)); // TODO: Move tau_decay to pe_parameters()

    // Read the values into a local audio cache
    int idx = 0;
    {
      pe::Mutex::Lock lock(m_mutex);

      while ( m_circular_buffer.size() >= 2 && idx < this->sample_rate() ) {
        m_left_cache[idx] = m_circular_buffer[0] * 1.5;
        m_circular_buffer.pop_front();
        m_right_cache[idx] = m_circular_buffer[0] * 1.5;
        m_circular_buffer.pop_front();

        // Go to next frame
        ++idx;
        m_time += m_time_slice;
      }
    }

    // Set up the GL parameters for drawing
    glLoadIdentity();
    float wave_x = pe_script_engine().get_parameter("wave_x")*2-1;
    float wave_y = pe_script_engine().get_parameter("wave_y")*2-1;
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
    pe::Vector3 color(wave_r, wave_g, wave_b);
    pe::Vector3 norm_color = color;
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

    // Draw the line connecting the last sample in the previous frame
    // to the first sample in this frame.
    float r = norm_color[0] * gain;
    float g = norm_color[1] * gain;
    float b = norm_color[2] * gain;
    glColor4f(r, g, b, wave_a );
      
    glVertex2d(m_ending_x,  m_ending_y);
    glVertex2d(m_left_cache[0], m_right_cache[0]);

    m_ending_x = m_left_cache[idx-1];
    m_ending_y = m_right_cache[idx-1];

    // Now draw the wave by traversing the buffer in reverse
    // order.
    for (int i = 1; i < idx; ++i) {

      // Compute the phosphor color
      float d = sqrt(pow(m_left_cache[i]-m_left_cache[i-1],2) + 
                     pow(m_right_cache[i]-m_right_cache[i-1],2));
      float dt_phosphor = dt_draw/d;
      float alpha = 1-exp(-dt_phosphor/tau_excite);
      float beta_factor = pow(1-beta,idx-1-i);
      float r = norm_color[0] * alpha * beta_factor;
      float g = norm_color[1] * alpha * beta_factor;
      float b = norm_color[2] * alpha * beta_factor;
      glColor4f(r, g, b, alpha );

      // We only draw the line if it moves from left to right.  (We
      // don't draw the scan return...)
      glVertex2d(m_left_cache[i-1],  m_right_cache[i-1]);
      glVertex2d(m_left_cache[i], m_right_cache[i]);
    }
    glEnd();
    glDisable(GL_BLEND);
  }
};

#endif // __OSCOPE_SHAPE_H__
