#include <PeParameters.h>
#include <GraphicsEngine.h>
#include <vw/Math/Vector.h>
#include <vw/Math/Matrix.h>

void GraphicsEngine::drawFeedback() {

  // Copy the pixel data from the pixel buffer object to the feedback texture.
  glEnable( GL_TEXTURE_2D );
  glActiveTexture(GL_TEXTURE0);
  glBindTexture( GL_TEXTURE_2D, m_feedback_texture );

  float aspect = float(m_viewport_width) / m_viewport_height;
  float framebuffer_radius = sqrt(1+pow(aspect,2));

  // Feedback decay, gamma, etc are controlled using a pixel shader.
  m_gpu_backbuffer_program->install();
  m_gpu_backbuffer_program->set_input_int("feedback_texture", 0);
  m_gpu_backbuffer_program->set_input_float("framebuffer_radius", framebuffer_radius);
  m_gpu_backbuffer_program->set_input_float("time", pe_parameters().get_value("time"));
  m_gpu_backbuffer_program->set_input_float("decay", pe_parameters().get_value("decay"));
  m_gpu_backbuffer_program->set_input_float("invert", pe_parameters().get_value("invert"));
  m_gpu_backbuffer_program->set_input_float("gamma", pe_parameters().get_value("gamma"));
  m_gpu_backbuffer_program->set_input_float("ifs_mode", pe_parameters().get_value("ifs_mode"));

  // These are handled by the mobius transform
  m_gpu_backbuffer_program->set_input_float("zoom", pe_parameters().get_value("zoom"));
  m_gpu_backbuffer_program->set_input_float("zoomexp", pe_parameters().get_value("zoomexp"));
  m_gpu_backbuffer_program->set_input_float("rot", pe_parameters().get_value("rot"));
  m_gpu_backbuffer_program->set_input_float("dx", pe_parameters().get_value("dx"));
  m_gpu_backbuffer_program->set_input_float("dy", pe_parameters().get_value("dy"));

  m_gpu_backbuffer_program->set_input_float("q1", pe_parameters().get_value("q1"));
  m_gpu_backbuffer_program->set_input_float("q2", pe_parameters().get_value("q2"));
  m_gpu_backbuffer_program->set_input_float("q3", pe_parameters().get_value("q3"));
  m_gpu_backbuffer_program->set_input_float("q4", pe_parameters().get_value("q4"));
  m_gpu_backbuffer_program->set_input_float("q5", pe_parameters().get_value("q5"));
  m_gpu_backbuffer_program->set_input_float("q6", pe_parameters().get_value("q6"));
  m_gpu_backbuffer_program->set_input_float("q7", pe_parameters().get_value("q7"));
  m_gpu_backbuffer_program->set_input_float("q8", pe_parameters().get_value("q8"));

  // Warp stuff
  float zoom = 1.0;//pe_parameters().get_value("zoom");
  float zoomExp = 1.0;//pe_parameters().get_value("zoomexp");
  float warpAmount = pe_parameters().get_value("warp");
  float warpSpeed = pe_parameters().get_value("warp_speed");
  float warpScale = pe_parameters().get_value("warp_scale");
  float warpTime = pe_parameters().get_value("time") * warpSpeed;
  float warpScaleInv = 1.0f / warpScale;

  float f[4];
  f[0] = 11.68f + 4.0f*cosf(warpTime*1.413f + 10);
  f[1] =  8.77f + 3.0f*cosf(warpTime*1.113f + 7);
  f[2] = 10.54f + 3.0f*cosf(warpTime*1.233f + 3);
  f[3] = 11.49f + 4.0f*cosf(warpTime*0.933f + 5);

  // Affine parameters
  float rot = 0.0; //pe_parameters().get_value("rot");
  float cx = pe_parameters().get_value("cx");
  float cy = pe_parameters().get_value("cy");
  float dx = 0.0; //pe_parameters().get_value("dx");
  float dy = 0.0; //pe_parameters().get_value("dy");
  float sx = pe_parameters().get_value("sx");
  float sy = pe_parameters().get_value("sy");
  // glTranslatef(cx, cy, 0);
  // glRotatef(rot, 0.0f, 0.0f, 1.0f);
  // glScalef(sx, sy, 0.0f);
  // glTranslatef(-1.0f * cx, -1.0f * cy, 0);
  // glTranslatef(dx, dy, 0);
	
  // Iterate through the coordinates in the mesh, applying a coordinate by coordinate
  // mesh distortion.  THIS IS WHERE THE MAGIC HAPPENS, FOLKS
  for (int i = 0; i < HORIZ_MESH_SIZE + 1; i++) { 
    for (int j = 0; j < VERT_MESH_SIZE + 1; j++) {
      float u = m_feedback_screencoords(i,j)[0];
      float v = m_feedback_screencoords(i,j)[1];

      // pe_parameters().set_value("x",u);
      // pe_parameters().set_value("y",v);
      // pe_parameters().set_value("rad",sqrt(u*u+v*v));
      // pe_parameters().set_value("ang",atan2(v,u));

      // Apply the zoom effect 
      float zoomCoefficient = powf(zoom, -1 * powf(zoomExp, 
                                                   sqrtf(u * u + v * v) * 2.0 * framebuffer_radius - framebuffer_radius));
      u = u * zoomCoefficient;
      v = v * zoomCoefficient;

      // Apply the scaling effect
      u = (u - cx)/sx + cx;
      v = (v - cy)/sy + cy;

      // Apply the Milkdrop warp effect (most of these constants were
      // taken from the milkdrop source code)
      u += warpAmount * 0.0035f * sinf(warpTime * 0.333f + warpScaleInv*(m_feedback_screencoords(i,j)[0] * f[0] - m_feedback_screencoords(i,j)[1] * f[3]));
      v += warpAmount * 0.0035f * cosf(warpTime * 0.375f - warpScaleInv*(m_feedback_screencoords(i,j)[0] * f[2] + m_feedback_screencoords(i,j)[1] * f[1]));
      u += warpAmount * 0.0035f * cosf(warpTime * 0.753f - warpScaleInv*(m_feedback_screencoords(i,j)[0] * f[1] - m_feedback_screencoords(i,j)[1] * f[2]));
      v += warpAmount * 0.0035f * sinf(warpTime * 0.825f + warpScaleInv*(m_feedback_screencoords(i,j)[0] * f[0] + m_feedback_screencoords(i,j)[1] * f[3]));

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

      // typedef std::list<boost::shared_ptr<ScriptEngine> >::iterator iter_type;
      // for (iter_type iter = m_script_engines.begin(); iter != m_script_engines.end(); ++iter ) {
      //   (*iter)->execute_js("per_pixel_equations", u, v);
      // }

      m_warped_screencoords(i,j)[0] = u;
      m_warped_screencoords(i,j)[1] = v;
    }
  }
 
  //  glEnable(GL_BLEND);
  glDisable(GL_BLEND);
  //  glBlendFunc (GL_ONE, GL_ZERO);
        
  //  We will draw the image as a texture on this quad.
  qglColor(Qt::white);
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
  glEnd() ;

  //  glDisable(GL_BLEND);

  // Disable texture mapping and GLSL shaders
  glDisable( GL_TEXTURE_2D );
  m_gpu_backbuffer_program->uninstall();
}


// <<MILKDROP>> This code was adapted from Milkdrop's milkdropfs.cpp.
// See the milkdrop license in COPYING for more details.
bool ReversePropagatePoint(float fx, float fy, float *fx2, float *fy2, 
                           int size_x, int size_y, float framebuffer_radius,
                           vw::Matrix<vw::Vector2>& screencoords) {

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


// <<MILKDROP>> This code was adapted from Milkdrop's milkdropfs.cpp.
// See the milkdrop license in COPYING for more details.

void GraphicsEngine::drawVectorField() {
  
  if (pe_parameters().get_value("mv_a") >= 0.001f) {
    
    glLoadIdentity();
    glLineWidth(1.0);
    glPointSize(2.0);

    glColor4f(pe_parameters().get_value("mv_r"),
              pe_parameters().get_value("mv_g"),
              pe_parameters().get_value("mv_b"),
              pe_parameters().get_value("mv_a"));              


    glEnable(GL_BLEND);
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    float aspect = float(m_viewport_width) / m_viewport_height;
    float framebuffer_radius = sqrt(1+pow(aspect,2));

    int nX = int(pe_parameters().get_value("mv_x"));
    int nY = int(pe_parameters().get_value("mv_y"));
    float dx = pe_parameters().get_value("mv_x") - nX;
    float dy = pe_parameters().get_value("mv_y") - nY;
    if (nX > 64) { nX = 64; dx = 0; }
    if (nY > 48) { nY = 48; dy = 0; }
    
    if (nX > 0 && nY > 0) {

      float len_mult = pe_parameters().get_value("mv_l");
      if (dx < 0) dx = 0;
      if (dy < 0) dy = 0;
      if (dx > 1) dx = 1;
      if (dy > 1) dy = 1;
      float min_len = 1.0f/m_viewport_width; // Is this correct?  

      for (int y=0; y<nY; y++) { 
        float fy = (y + 0.25f)/(float)(nY + dy + 0.25f - 1.0f) * 2.0f - 1.0f ;

        // now move by offset
        fy -= pe_parameters().get_value("mv_dy");

        if (fy > -1.0f && fy < 1.0f) {
          for (int x=0; x<nX; x++) {
            float fx = (x + 0.25f)/(float)(nX + dx + 0.25f - 1.0f) * 2.0f * aspect - aspect;

            // now move by offset
            fx += pe_parameters().get_value("mv_dx");
            
            if (fx > -aspect && fx < aspect) {

              float fx2, fy2;
              ReversePropagatePoint(fx, fy, &fx2, &fy2, 
                                    HORIZ_MESH_SIZE, VERT_MESH_SIZE, 
                                    framebuffer_radius,
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
