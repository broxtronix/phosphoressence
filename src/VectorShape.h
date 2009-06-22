// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file VectorShape.h
///
/// This is the base class for drawing a glowing "phosphor" on the
/// screen.  It takes care of the details of rendering a realistic
/// lines and curves to the screen with the proper fade-out, etc.
#ifndef __VECTOR_SHAPE_H__
#define __VECTOR_SHAPE_H__

#ifdef __APPLE__
#include <OpenGL/OpenGL.h>
#include <OpenGL/glu.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#endif 

#include <PeUtils.h>
#include <ScriptEngine.h>
 
#include <vw/Math/Vector.h>

#define PE_VECTORSHAPE_NULL -32000.0f

class VectorShape : public Drawable {

  double m_last_time;
  double m_timebase;
  vw::Vector2 m_last_point;

protected:

  RingBuffer<vw::Vector2> m_linebuffer;

  /// Subclass must implement this to indicate the sampling rate of
  /// the data we're using in the draw loop.
  virtual int sample_rate() const { return 96000; }

  /// Subclass must implement this method if it wants to provide new
  /// data to the x and y linebuffers.
  virtual int update(float t0, float frame_number) {
    double new_time = double(vw::Stopwatch::microtime()) / 1.0e6;
    float elapsed_time = new_time - m_last_time;
    m_last_time = new_time;

    double time_slice = 1.0/sample_rate();

    float A = 0.5;
    float B = 0.5;
    float omega = pe_script_engine().get_parameter("wave_frequency");
    float ratio_a = 5;//pe_script_engine().get_parameter("bass");
    float ratio_b = 9;//pe_script_engine().get_parameter("treb");
    float phase = 1.01;

    for (unsigned i = 0; i < elapsed_time*this->sample_rate(); ++i) {

      // Lissajous Curve
      vw::Vector2 d(A*cos(omega*phase*ratio_a/ratio_b*m_timebase), 
                    B*cos(omega*m_timebase));

      // Spirograph Curve
      // float t = m_timebase;
      // float p = phase;
      // vw::Vector2 d(0.5*((A+B)*cos(omega_a*m_timebase) + p * cos((A+B)*omega_a*t/B)),
      //               0.5*((A+B)*sin(omega_a*m_timebase) + p * sin((A+B)*omega_a*t/B)));

      // Butterfly Curve
      // ( http://en.wikipedia.org/wiki/Butterfly_curve_(transcendental) )
      // float w = omega_a;
      // float t = m_timebase;
      // vw::Vector2 d( A * sin(w*t) * (exp(cos(w*t))-2*cos(4*w*t)-pow(sin(w*t/12),5)),
      //                B * cos(w*t) * (exp(cos(w*t))-2*cos(4*w*t)-pow(sin(w*t/12),5)) );

      m_linebuffer.append( d );
      m_timebase += time_slice;
    }
  }
  
public:
  VectorShape() : m_last_time(double(vw::Stopwatch::microtime()) / 1.0e6),
                  m_timebase(0), m_last_point(PE_VECTORSHAPE_NULL, PE_VECTORSHAPE_NULL) {}
  
  /// This implements the abstract method for class Drawable.  It is
  /// called once during each time through the render loop in the
  /// GraphicsEngine, and it gives this shape a chance to render
  /// itself to the screen.
  virtual void draw(float time, float gain) {
  //   std::cout << "Draw! " << time << "\n";
    
    // Give the child class a chance to draw itself.
    this->update(time, 0);

    glLoadIdentity();
    
    // Wave position
    float wave_x = pe_script_engine().get_parameter("wave_x")*2-1;
    float wave_y = pe_script_engine().get_parameter("wave_y")*2-1;
    glTranslatef(wave_x, wave_y, 0);

    // Wave line thickness
    if (pe_script_engine().get_parameter("wave_thick")) {
      glLineWidth(2.0);
      glPointSize(3.0);
    } else {
      glLineWidth(0.25);
      glPointSize(1.0);
    }

    // Wave Color
    float wave_r = pe_script_engine().get_parameter("wave_r");
    float wave_g = pe_script_engine().get_parameter("wave_g");
    float wave_b = pe_script_engine().get_parameter("wave_b");
    float wave_a = pe_script_engine().get_parameter("wave_a");
    vw::Vector3 color(wave_r, wave_g, wave_b);
    vw::Vector3 norm_color = color;
    if (pe_script_engine().get_parameter("wave_brighten")) 
      norm_color = normalize(color);

    // Blend mode
    //
    // Currently the wave is drawn directly on top without and alpha
    // blending.
    glEnable(GL_BLEND);
    glBlendFunc (GL_ONE, GL_ZERO);

    // Wave lines or dots
    if (pe_script_engine().get_parameter("wave_usedots")) 
      glBegin(GL_POINTS);
    else 
      glBegin(GL_LINES);

    // This code computes a "fade factor" to apply to the color so
    // that the waveform "fades away" like a real phosphor as it is
    // drawn to the screen.  It's a little messy and hard to read, bit
    // it gets the job done.
    float dt_draw = 1.0/sample_rate();
    float tau_excite = 3e-5;                   // TODO : Move to parameters.
    float tau_decay = -(1/30.0)/log(pe_script_engine().get_parameter("decay")); 
                                               // TODO: Avoid using fixed frame rate (30.0)!
    float beta = (1-exp(-dt_draw/tau_decay));  // TODO: Move tau_decay to pe_parameters()

    // Read the values into a local cache so that we can draw them
    // below.  We initialize the first point in the buffer to be a
    // NULL point just in case the linebuffer is empty.
    vw::Vector2 linecache[m_linebuffer.size()];
    linecache[0] = vw::Vector2(PE_VECTORSHAPE_NULL, PE_VECTORSHAPE_NULL);
    vw::Vector2 new_last_point(PE_VECTORSHAPE_NULL, PE_VECTORSHAPE_NULL);

    int idx = 0;
    while (!m_linebuffer.empty() && idx < m_linebuffer.size()) {
      linecache[idx] = m_linebuffer.pop();
      new_last_point = linecache[idx];
      idx++;
    }

    // We know that the wave is going to decay by a factor of delta
    // over the course of rendering this frame, so we need to compute
    // that decay factor on a sample by sample basis here.  
    float decay = pe_script_engine().get_parameter("decay");
    double sample_decay = pow(decay,1.0/float(idx));

    // Start by drawing a line that connects from the last point drawn
    // in the previous frame to the first point in this frame.  Note: we
    // only draw the line if it moves from left to right.  (We don't
    // draw the scan return...)
    if (m_last_point[0] != PE_VECTORSHAPE_NULL &&
        linecache[0][0] != PE_VECTORSHAPE_NULL) {
      // Compute the phosphor color (with the proper decay rate applied)
      float beta_factor = pow(sample_decay,idx);
      float r = norm_color[0] * beta_factor;
      float g = norm_color[1] * beta_factor;
      float b = norm_color[2] * beta_factor;
      glColor4f(r, g, b, wave_a );

      glVertex2d(m_last_point[0],  m_last_point[1]);
      glVertex2d(linecache[0][0], linecache[0][1]);
    }
    m_last_point = new_last_point;


    // Now draw the wave by traversing the buffer in reverse
    // order.
    for (int i = 1; i < idx; ++i) {

      // Compute the phosphor color (with the proper decay rate applied)
      float beta_factor = pow(sample_decay,idx-i);
      float r = norm_color[0] * beta_factor;
      float g = norm_color[1] * beta_factor;
      float b = norm_color[2] * beta_factor;
      glColor4f(r, g, b, wave_a );

      // We only draw the line if it moves from left to right.  (We
      // don't draw the scan return...)      
      if (linecache[i-1][0] != PE_VECTORSHAPE_NULL &&
          linecache[i][0] != PE_VECTORSHAPE_NULL) {
        glVertex2d(linecache[i-1][0],  linecache[i-1][1]);
        glVertex2d(linecache[i][0], linecache[i][1]);
      }
    }
    glEnd();
    glDisable(GL_BLEND);
    glBlendFunc (GL_ONE, GL_ZERO);

  }
};

#endif // __VECTOR_SHAPE_H__



