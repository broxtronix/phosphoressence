#ifdef __linux__
// This is required to get prototypes, according to the opengl linux abi
#define GL_GLEXT_PROTOTYPES 1
#endif

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <AGL/agl.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glext.h>
#endif 

#include <PeParameters.h>
#include <GraphicsEngine.h>
#include <pe/Graphics/GpuProgram.h>
#include <pe/Math/Vector.h>
#include <pe/Math/Matrix.h>
#include <pe/Core/FundamentalTypes.h>
#include <pe/Simulation/FluidDynamics.h>
using namespace pe;

// -------------------------------------------------------------------

void GraphicsEngine::drawFeedback() {

  // Copy the pixel data from the pixel buffer object to the feedback texture.
  glEnable( GL_TEXTURE_2D );
  glActiveTexture(GL_TEXTURE1);
  glBindTexture( GL_TEXTURE_2D, m_framebuffer_texture0 );
  glActiveTexture(GL_TEXTURE0);
  glBindTexture( GL_TEXTURE_2D, m_feedback_texture );

  // glEnable(GL_BLEND);
  // glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

  // Fragment Shader
  m_gpu_backbuffer_program->install();

  // Feedback decay, gamma, etc are controlled using a fragment shader.
  m_gpu_backbuffer_program->set_input_int("feedback_texture", 0);
  m_gpu_backbuffer_program->set_input_int("framebuffer_texture", 1);
  m_gpu_backbuffer_program->set_input_float("framebuffer_radius", m_framebuffer_radius);
  m_gpu_backbuffer_program->set_input_float("decay", pe_script_engine().get_parameter("decay"));
  m_gpu_backbuffer_program->set_input_float("ifs_mode", pe_script_engine().get_parameter("ifs_mode"));
  m_gpu_backbuffer_program->set_input_float("invert", pe_script_engine().get_parameter("invert"));
  m_gpu_backbuffer_program->set_input_float("edge_extend", pe_script_engine().get_parameter("wrap"));
  m_gpu_backbuffer_program->set_input_float("kaleidoscope", pe_script_engine().get_parameter("kaleidoscope"));
  m_gpu_backbuffer_program->set_input_float("kaleidoscope_radius", pe_script_engine().get_parameter("kaleidoscope_radius"));
  m_gpu_backbuffer_program->set_input_float("kaleidoscope_x", pe_script_engine().get_parameter("kaleidoscope_x"));
  m_gpu_backbuffer_program->set_input_float("kaleidoscope_y", pe_script_engine().get_parameter("kaleidoscope_y"));
  m_gpu_backbuffer_program->set_input_float("echo_zoom", pe_script_engine().get_parameter("echo_zoom"));
  m_gpu_backbuffer_program->set_input_float("echo_alpha", pe_script_engine().get_parameter("echo_alpha"));
  m_gpu_backbuffer_program->set_input_float("echo_orient", pe_script_engine().get_parameter("echo_orient"));

  // These are handled by the mobius transform
  m_gpu_backbuffer_program->set_input_float("zoom", pe_script_engine().get_parameter("zoom"));
  m_gpu_backbuffer_program->set_input_float("zoomexp", pe_script_engine().get_parameter("zoomexp"));
  m_gpu_backbuffer_program->set_input_float("rot", pe_script_engine().get_parameter("rot"));
  m_gpu_backbuffer_program->set_input_float("dx", pe_script_engine().get_parameter("dx"));
  m_gpu_backbuffer_program->set_input_float("dy", pe_script_engine().get_parameter("dy"));

  m_gpu_backbuffer_program->set_input_float("q1", pe_script_engine().get_parameter("q1"));
  m_gpu_backbuffer_program->set_input_float("q2", pe_script_engine().get_parameter("q2"));
  m_gpu_backbuffer_program->set_input_float("q3", pe_script_engine().get_parameter("q3"));
  m_gpu_backbuffer_program->set_input_float("q4", pe_script_engine().get_parameter("q4"));
  m_gpu_backbuffer_program->set_input_float("q5", pe_script_engine().get_parameter("q5"));
  m_gpu_backbuffer_program->set_input_float("q6", pe_script_engine().get_parameter("q6"));
  m_gpu_backbuffer_program->set_input_float("q7", pe_script_engine().get_parameter("q7"));
  m_gpu_backbuffer_program->set_input_float("q8", pe_script_engine().get_parameter("q8"));
  
  float warpSpeed = pe_script_engine().get_parameter("warp_speed");
  float warpScale = pe_script_engine().get_parameter("warp_scale")+0.0001;
  float warpTime = pe_time() * warpSpeed;
  float warpScaleInv = 1.0f / warpScale;

  float f[4];
  f[0] = 11.68f + 4.0f*cosf(warpTime*1.413f + 10);
  f[1] =  8.77f + 3.0f*cosf(warpTime*1.113f + 7);
  f[2] = 10.54f + 3.0f*cosf(warpTime*1.233f + 3);
  f[3] = 11.49f + 4.0f*cosf(warpTime*0.933f + 5);

  // Extract the per-pixel parameters.  Some of these are disable here
  // because they are now handled by the pixel shader (above).  The
  // effect is similar, except that you can get nice texture wrapping
  // effects when using the pixel shader.
  float zoom = 1.0;//pe_script_engine().get_parameter("zoom");
  float zoom_rate = pe_script_engine().get_parameter("zoom_rate");
  float zoomExp = 1.0;//pe_script_engine().get_parameter("zoomexp");
  float warpAmount = pe_script_engine().get_parameter("warp");
      
  float rot = 0.0;//pe_script_engine().get_parameter("rot");
  float rot_rate = pe_script_engine().get_parameter("rot_rate");
  float cx = pe_script_engine().get_parameter("cx");
  float cy = pe_script_engine().get_parameter("cy");
  float dx = 0.0;//pe_script_engine().get_parameter("dx");
  float dy = 0.0;//pe_script_engine().get_parameter("dy");
  float sx = pe_script_engine().get_parameter("sx")+0.00001;
  float sy = pe_script_engine().get_parameter("sy")+0.00001;

  // Update the fluid simulation
  m_fluid_sim->update();

  // Iterate through the coordinates in the mesh, applying a coordinate by coordinate
  // mesh distortion.  THIS IS WHERE THE MAGIC HAPPENS, FOLKS
  for (int i = 0; i < HORIZ_MESH_SIZE + 1; i++) { 
    for (int j = 0; j < VERT_MESH_SIZE + 1; j++) {
      float u = m_feedback_screencoords(i,j)[0];
      float v = m_feedback_screencoords(i,j)[1];
      float radius = sqrt(u*u+v*v);
      // float angle = atan2(v,u);

      // Apply the zoom effect 
      float zoomCoefficient = powf(zoom, powf(zoomExp, 
                                              sqrtf(u * u + v * v) * 2.0 * 
                                              m_framebuffer_radius - m_framebuffer_radius));

      // Apply the zoom effect (disabled for now... see backbuffer.glsl...)
      u = u * zoomCoefficient;
      v = v * zoomCoefficient;

      // Apply the scaling effect (disabled for now... see backbuffer.glsl...)
      u = (u - cx)/sx + cx;
      v = (v - cy)/sy + cy;

      // Apply the Milkdrop warp effect (most of these constants were
      // taken from the milkdrop source code)
      m_fluid_sim->add_velocity(i,j,Vector2(warpAmount * 0.0035f * sinf(warpTime * 0.333f + warpScaleInv*(m_feedback_screencoords(i,j)[0] * f[0] - m_feedback_screencoords(i,j)[1] * f[3])),
                                            warpAmount * 0.0035f * cosf(warpTime * 0.375f - warpScaleInv*(m_feedback_screencoords(i,j)[0] * f[2] + m_feedback_screencoords(i,j)[1] * f[1])) ));
      m_fluid_sim->add_velocity(i,j,Vector2(warpAmount * 0.0035f * cosf(warpTime * 0.753f - warpScaleInv*(m_feedback_screencoords(i,j)[0] * f[1] - m_feedback_screencoords(i,j)[1] * f[2])),
                                            warpAmount * 0.0035f * sinf(warpTime * 0.825f + warpScaleInv*(m_feedback_screencoords(i,j)[0] * f[0] + m_feedback_screencoords(i,j)[1] * f[3])) ));

      // Apply the fluid rotation effect
      //      if (radius != 0) {
      if (radius > 0.8 && radius < 1.2) {
        float direction_u = (v/radius);
        float direction_v = (-u/radius);
        m_fluid_sim->add_velocity(i,j, Vector2(rot_rate*direction_u, rot_rate * direction_v));
      }

      // Apply the fluid zoom effect
      if (radius != 0) {
        float direction_u = (-u/radius);
        float direction_v = (-v/radius);
        m_fluid_sim->add_velocity(i,j, Vector2(zoom_rate*direction_u, zoom_rate * direction_v));
      }

      // Add in the fluid simulation effect
      Vector2 fluid_velocity = m_fluid_sim->get_velocity(i,j);
      u += fluid_velocity[0];
      v += fluid_velocity[1];

      // Apply the rotation effect
      float u2 = u - cx;
      float v2 = v - cy;
      
      float cos_rot = cosf(rot);
      float sin_rot = sinf(rot);
      u = u2*cos_rot - v2*sin_rot + cx;
      v = u2*sin_rot + v2*cos_rot + cy;

      // Apply the translation effect
      u -= dx;
      v -= dy;

      m_warped_screencoords(i,j)[0] = u;
      m_warped_screencoords(i,j)[1] = v;
    }
  }

  //  We will draw the image as a texture on this quad.
  glColor4f(1.0,1.0,1.0,1.0);
  glBegin(GL_QUADS);
  for (int i = 0 ; i < HORIZ_MESH_SIZE ; ++i) {
    for (int j = 0 ; j < VERT_MESH_SIZE ; ++j) {
      glTexCoord2f( m_feedback_texcoords(i,j)[0], m_feedback_texcoords(i,j)[1] ); 
      glVertex2f(   m_warped_screencoords(i,j)[0] , m_warped_screencoords(i,j)[1] );
      glTexCoord2f( m_feedback_texcoords(i,j+1)[0], m_feedback_texcoords(i,j+1)[1] ); 
      glVertex2f(   m_warped_screencoords(i,j+1)[0], m_warped_screencoords(i,j+1)[1] );
      glTexCoord2f( m_feedback_texcoords(i+1,j+1)[0],  m_feedback_texcoords(i+1,j+1)[1] ); 
      glVertex2f(   m_warped_screencoords(i+1,j+1)[0], m_warped_screencoords(i+1,j+1)[1] );
      glTexCoord2f(  m_feedback_texcoords(i+1,j)[0],  m_feedback_texcoords(i+1,j)[1] ); 
      glVertex2f(   m_warped_screencoords(i+1,j)[0], m_warped_screencoords(i+1,j)[1] );
    }		
  }
  glEnd();

  glDisable( GL_TEXTURE_2D );
  //  glDisable(GL_BLEND);
  m_gpu_backbuffer_program->uninstall();
}


// <<MILKDROP>> This code was adapted from Milkdrop's milkdropfs.cpp.
// See the milkdrop license in COPYING for more details.
bool ReversePropagatePoint(float fx, float fy, float *fx2, float *fy2, 
                           int size_x, int size_y, float framebuffer_radius,
                           pe::Matrix<pe::Vector2>& screencoords) {

  float screen_w = 2.0*framebuffer_radius;  
  float screen_h = 2.0*framebuffer_radius;

  float Y = (fy + framebuffer_radius) / screen_h * (size_y);
  float X = (fx + framebuffer_radius) / screen_w * (size_x);

  int   y0 = int(Y);
  float dy = Y - y0;

  int   x0 = int(X);
  float dx = X - x0;

  int x1 = x0 + 1;
  int y1 = y0 + 1;
  
  if (x0 < 0) return false;
  if (y0 < 0) return false;
  if (x1 > size_x) return false;
  if (y1 > size_y) return false;

  float tu, tv;
  tu  = screencoords(x0,y0)[0] * (1-dx)*(1-dy);
  tv  = screencoords(x0,y0)[1] * (1-dx)*(1-dy);
  tu += screencoords(x0,y1)[0] * (dx)*(1-dy);
  tv += screencoords(x0,y1)[1] * (dx)*(1-dy);
  tu += screencoords(x1,y0)[0] * (1-dx)*(dy);
  tv += screencoords(x1,y0)[1] * (1-dx)*(dy);
  tu += screencoords(x1,y1)[0] * (dx)*(dy);
  tv += screencoords(x1,y1)[1] * (dx)*(dy);
  
  *fx2 = tu;
  *fy2 = tv;
  return true;
}

void GraphicsEngine::drawDarkenCenter() {

  if (pe_script_engine().get_parameter("darken_center")) {

       glEnable(GL_BLEND);
       glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

       float fHalfSize = 0.005f;
       glBegin(GL_TRIANGLE_FAN);
       
       // Center point
       glColor4f(0.0, 0.0, 0.0, 3.0f/32.0f);
       glVertex2f(0.0,0.0);
       
       // Perimeter
       glColor4f(0.0, 0.0, 0.0, 0.0);
       glVertex2f(0.0f - fHalfSize*m_aspect, 0.0);
       glVertex2f(0.0f, 0.0f - fHalfSize);
       glVertex2f(0.0f + fHalfSize*m_aspect, 0.0);
       glVertex2f(0.0f, 0.0f + fHalfSize);
       glVertex2f(0.0f - fHalfSize*m_aspect, 0.0);
       
       glEnd();
       glDisable( GL_BLEND ); 
     }
}



// <<MILKDROP>> This code was adapted from Milkdrop's milkdropfs.cpp.
// See the milkdrop license in COPYING for more details.

void GraphicsEngine::drawVectorField() {
  
  if (pe_script_engine().get_parameter("mv_a") >= 0.001f) {
    
    glLoadIdentity();
    glLineWidth(1.0);
    glPointSize(2.0);

    glEnable(GL_POINT_SMOOTH);

    glColor4f(pe_script_engine().get_parameter("mv_r"),
              pe_script_engine().get_parameter("mv_g"),
              pe_script_engine().get_parameter("mv_b"),
              pe_script_engine().get_parameter("mv_a"));              


    glEnable(GL_BLEND);
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);


    int nX = int(pe_script_engine().get_parameter("mv_x"));
    int nY = int(pe_script_engine().get_parameter("mv_y"));
    float dx = pe_script_engine().get_parameter("mv_x") - nX;
    float dy = pe_script_engine().get_parameter("mv_y") - nY;
    if (nX > 64) { nX = 64; dx = 0; }
    if (nY > 48) { nY = 48; dy = 0; }
    
    if (nX > 0 && nY > 0) {

      float len_mult = pe_script_engine().get_parameter("mv_l");
      if (dx < 0) dx = 0;
      if (dy < 0) dy = 0;
      if (dx > 1) dx = 1;
      if (dy > 1) dy = 1;
      //      float min_len = 1.0f/m_viewport_width; // Is this correct?  

      for (int y=0; y<nY; y++) { 
        float fy = (y + 0.25f)/(float)(nY + dy + 0.25f - 1.0f) * 2.0f - 1.0f ;

        // now move by offset
        fy -= pe_script_engine().get_parameter("mv_dy");

        if (fy > -1.0f && fy < 1.0f) {
          for (int x=0; x<nX; x++) {
            float fx = (x + 0.25f)/(float)(nX + dx + 0.25f - 1.0f) * 2.0f * m_aspect - m_aspect;

            // now move by offset
            fx += pe_script_engine().get_parameter("mv_dx");
            
            if (fx > -m_aspect && fx < m_aspect) {

              float fx2, fy2;
              ReversePropagatePoint(fx, fy, &fx2, &fy2, 
                                    HORIZ_MESH_SIZE, VERT_MESH_SIZE, 
                                    m_framebuffer_radius,
                                    m_warped_screencoords);	
              float dx = (fx2 - fx);
              float dy = (fy2 - fy);
              fx2 = fx + len_mult * dx;
              fy2 = fy + len_mult * dy;

              glBegin(GL_LINES);
              glVertex2d( fx, fy );
              glVertex2d( fx2, fy2);
              glEnd();
              glBegin(GL_POINTS);
              glVertex2d( fx2, fy2 );
              glEnd();
            }
          }
        }
      }
    }
    glDisable(GL_BLEND);
  }
  
}


// <<MILKDROP>> This code was adapted from Milkdrop's milkdropfs.cpp.
// See the milkdrop license in COPYING for more details.

// void GraphicsEngine::draw_milkdrop_waves() {
//     glEnable(GL_BLEND);
//     if (pe_script_engine().get_parameter("wave_additive"))
//       glBlendFunc (GL_SRC_ALPHA, GL_ONE);
//     else
//       glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

//     float wave_r = pe_script_engine().get_parameter("wave_r");
//     float wave_g = pe_script_engine().get_parameter("wave_g");
//     float wave_b = pe_script_engine().get_parameter("wave_b");
//     float wave_a = pe_script_engine().get_parameter("wave_a");
//     float wave_mystery = pe_script_engine().get_parameter("wave_mystery");
    
//     if (pe_script_engine().get_parameter("wave_brighten")) {
//       float max = wave_r;
//       if (max < wave_g) max = wave_g;
//       if (max < wave_b) max = wave_b;
//       if (max > 0.01f) {
//         wave_r = wave_r/max;
//         wave_g = wave_g/max;
//         wave_b = wave_b/max;
//       }

//     }

//     // Compute wave position, adjusting from the parameter range
//     // [0..1] to the window range [-1..1] for x and [-aspect..aspect]
//     // for y.
//     float x = pe_script_engine().get_parameter("wave_x")*2.0*m_aspect - m_aspect;
//     float y = pe_script_engine().get_parameter("wave_y")*2.0 - 1.0;


//     float bass_rel   = pe_script_engine().get_parameter("bass_att");
//     float mid_rel    = pe_script_engine().get_parameter("mid_att");
//     float treble_rel = pe_script_engine().get_parameter("treb_att");

//     glDisable(GL_BLEND);
// }
