// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file GraphicsEngine.cc
///

#ifdef __linux__
// This is required to get prototypes, according to the opengl linux abi
#define GL_GLEXT_PROTOTYPES 1
#endif

//#include <OpenFrameworks/graphics/ofTexture.h>

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <AGL/agl.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glext.h>
#endif 

#include <QtGui>

#include <GraphicsEngine.h>
#include <GpuProgram.h>
#include <PeParameters.h>
using namespace vw::GPU;

// Vision Workbench
#include <vw/Image.h>
#include <vw/FileIO.h>
//#include <vw/Math.h>
using namespace vw;

#include <fstream>

// ShivaVG
#include <vg/openvg.h>
#include <vg/vgu.h>

// Switch from uin8 to floating point textures
#define PE_GL_FORMAT GL_RGBA16F_ARB
//#define PE_GL_FORMAT GL_RGBA

// --------------------------------------------------------------
//                       GLSL DEBUGGING
// --------------------------------------------------------------

void print_shader_info_log(GLuint obj)
{
  int infologLength = 0;
  int charsWritten  = 0;
  char *infoLog;

  glGetShaderiv(obj, GL_INFO_LOG_LENGTH,&infologLength);

  if (infologLength > 1) {
    infoLog = (char *)malloc(infologLength);
    glGetShaderInfoLog(obj, infologLength, &charsWritten, infoLog);
    std::ostringstream err;
    err << "<h4>An error occured while compiling the GLSL shader:</h4><p><h5><tt>" << infoLog << "</tt></h5>";
    QMessageBox::critical(0, "GLSL Shader Error", 
                            err.str().c_str());
    free(infoLog);
  }
}

void print_program_info_log(GLuint obj)
{
  int infologLength = 0;
  int charsWritten  = 0;
  char *infoLog;
  
  glGetProgramiv(obj, GL_INFO_LOG_LENGTH,&infologLength);
  
  if (infologLength > 1) {
    infoLog = (char *)malloc(infologLength);
    glGetProgramInfoLog(obj, infologLength, &charsWritten, infoLog);
    std::ostringstream err;
    err << "<h4>An error occured while linking the GLSL program:</h4><p><h5><tt>" << infoLog << "</tt></h5>";
    QMessageBox::critical(0, "GLSL Program Error", 
                          err.str().c_str());
    printf("%s\n",infoLog);
    free(infoLog);
  }
}

void check_gl_errors( void ) 
{ 
  GLenum errCode; 
  const GLubyte *errStr; 
  if ( ( errCode = glGetError( ) ) != GL_NO_ERROR ) { 
    errStr = gluErrorString( errCode ); 
    std::cout << "OpenGL ERROR (" << int(errCode) << "): " << errStr << "\n";
  } 
} 
// --------------------------------------------------------------
//               GraphicsEngine Public Methods
// --------------------------------------------------------------

GraphicsEngine::GraphicsEngine(QWidget *parent, QGLFormat const& frmt) : 
  QGLWidget(parent) {

  if (!this->isValid()) {
    vw::vw_out() << "Failed to initialize OpenGL.\nExiting\n\n";
    exit(1);
  }

  if (!QGLFormat::hasOpenGL()) {
    vw::vw_out() << "This system has no OpenGL support.\nExiting\n\n";
    exit(1);
  }

  if (!format().sampleBuffers())
    std::cout << "\n\nCould not activate FSAA; results will be suboptimal\n\n";
  if (!format().doubleBuffer())
    std::cout << "\n\nCould not set double buffering; results will be suboptimal\n\n";

  // Feedback
  m_feedback_texcoords.set_size(HORIZ_MESH_SIZE + 1, VERT_MESH_SIZE + 1);
  m_feedback_screencoords.set_size(HORIZ_MESH_SIZE + 1, VERT_MESH_SIZE + 1);
  m_warped_screencoords.set_size(HORIZ_MESH_SIZE + 1, VERT_MESH_SIZE + 1);

  // Fluid simulation
  //
  // First we check to make sure the mesh size and fluid size are the
  // same (and are both square).  If they aren't then wacky things
  // could happen, including a seg fault.  Someday I'll go through the
  // fluid code and add support for non-square meshes, but for now
  // this prevents future Michael from suffering if he forgets this
  // constraint.
  VW_ASSERT(HORIZ_MESH_SIZE == FLUID_DIMENSION, 
            NoImplErr() << "Mesh size and FLUID_DIMENSION are not equal!");
  VW_ASSERT(VERT_MESH_SIZE == FLUID_DIMENSION, 
            NoImplErr() << "Mesh size and FLUID_DIMENSION are not equal!");

  m_fluid_previous_time = pe_time();
  m_fluid_u.reset(new float[FLUID_SIZE]);
  m_fluid_v.reset(new float[FLUID_SIZE]);
  m_fluid_u_prev.reset(new float[FLUID_SIZE]);
  m_fluid_v_prev.reset(new float[FLUID_SIZE]);
  m_fluid_density.reset(new float[FLUID_SIZE]);
  m_fluid_density_prev.reset(new float[FLUID_SIZE]);

  for (int i=0; i < FLUID_SIZE; ++i) {
    m_fluid_u[i] = 0.0;
    m_fluid_v[i] = 0.0;
    m_fluid_u_prev[i] = 0.0;
    m_fluid_v_prev[i] = 0.0;
    m_fluid_density[i] = 0.0;
    m_fluid_density_prev[i] = 0.0;
  }

  // Other variables
  m_fps_avg = 30.0;
  m_record = false;
  m_record_frame_number = 0;

  // Set mouse tracking
  this->setMouseTracking(true);

  // Set the size policy that the widget can grow or shrink and still
  // be useful.
  this->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
}

GraphicsEngine::~GraphicsEngine() {

  // De-allocate feedback texture and video texture
  glDeleteTextures(1, &m_feedback_texture);
  glDeleteTextures(1, &m_ground_texture);

  // De-allocate any previously allocated textures or framebuffers
  glDeleteFramebuffersEXT(1, &m_framebuffer0);
  glDeleteTextures(1, &m_framebuffer_texture0);
  glDeleteTextures(1, &m_framebuffer_stencil0);

  glDeleteFramebuffersEXT(1, &m_framebuffer1);
  glDeleteTextures(1, &m_framebuffer_texture1);
  glDeleteTextures(1, &m_framebuffer_stencil1);
}

void GraphicsEngine::setup_mesh() {

  float aspect = float(m_viewport_width) / m_viewport_height;
  float framebuffer_radius = sqrt(1+pow(aspect,2));

  double texture_w = 1.0;
  double texture_h = 1.0;
  double screen_w = 2.0*framebuffer_radius;  
  double screen_h = 2.0*framebuffer_radius;
  
  for (int i = 0 ; i < HORIZ_MESH_SIZE + 1 ; i++) {
    for (int j = 0 ; j < VERT_MESH_SIZE + 1 ; j++) {
      m_feedback_texcoords(i,j)[0] = i * texture_w / HORIZ_MESH_SIZE;
      m_feedback_texcoords(i,j)[1] = j * texture_h / VERT_MESH_SIZE;

      m_feedback_screencoords(i,j)[0] = -framebuffer_radius + (i * screen_w) / HORIZ_MESH_SIZE;
      m_feedback_screencoords(i,j)[1] = -framebuffer_radius + (j * screen_h) / VERT_MESH_SIZE;
    }
  }
}

void GraphicsEngine::initializeGL() {  

  // Set up the GLSL fragment shader.
  std::string resources_dir = pe_resources_directory();
  m_gpu_frontbuffer_program = create_gpu_program(resources_dir + "/shaders/frontbuffer.glsl");
  m_gpu_backbuffer_program = create_gpu_program(resources_dir + "/shaders/backbuffer.glsl");
//                                                 std::vector<int>(),
//                                                 resources_dir + "/shaders/backbuffer_vertex.glsl",
//                                                 std::vector<int>());

  // Generate the ground texture & load the image
  glGenTextures(1, &m_ground_texture);
  glBindTexture(GL_TEXTURE_2D, m_ground_texture);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT );
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT );
  
  // Load the ground image
  std::string ground_image_filename = pe_resources_directory() + "/images/ground.jpg";
  std::cout << "\t--> Loading ground image: " << ground_image_filename << "\n";
  ImageView<PixelRGB<uint8> > ground_image;
  vw::read_image(ground_image, ground_image_filename);
  glBindTexture(GL_TEXTURE_2D, m_ground_texture);
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
               ground_image.cols(), 
               ground_image.rows(),
               0, GL_RGB, GL_UNSIGNED_BYTE, 
               ground_image.data());
  glBindTexture(GL_TEXTURE_2D, 0);
  
  // Generate the feedback texture
  glGenTextures(1, &m_feedback_texture);
  glBindTexture(GL_TEXTURE_2D, m_feedback_texture);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT );
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT );
  // glTexParameterf(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE );

  glBindTexture(GL_TEXTURE_2D, 0);

  // Crank up the anisotropic filtering.  Not totally sure what this
  // does, but it might produce crisper images for filters that really
  // stretch the texture.
  GLfloat largest_supported_anisotropy;
  glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT, &largest_supported_anisotropy);

  // Create the framebuffer & framebuffer texture
  glGenFramebuffersEXT(1, &m_framebuffer0);

  // Create the main framebuffer texture
  glGenTextures(1, &m_framebuffer_texture0);
  glBindTexture(GL_TEXTURE_2D, m_framebuffer_texture0);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, largest_supported_anisotropy);
  glBindTexture(GL_TEXTURE_2D, 0);

  // Create the main stencil texture
  glGenRenderbuffersEXT(1, &m_framebuffer_stencil0);

  // Uncomment to get rid of the tearing (i.e. tearing)!
#ifdef __APPLE__
  // AGLContext aglContext;
  // aglContext = aglGetCurrentContext();
  // GLint swapInt = 1;
  // aglSetInteger(aglContext, AGL_SWAP_INTERVAL, &swapInt);
  this->setAutoBufferSwap(false);
#endif

  // Enable hardware anti-aliasing
  glEnable(GL_MULTISAMPLE);

  // Set the grid size
  pe_script_engine().set_parameter("meshx", HORIZ_MESH_SIZE);
  pe_script_engine().set_parameter("meshy", VERT_MESH_SIZE);

  // Now that GL is setup, we can start the Qt Timer that drives our
  // rendering.
  m_timer = new QTimer(this);
  connect(m_timer, SIGNAL(timeout()), this, SLOT(timer_callback()));
  m_timer->start(33.0); // Limit frame rate to ~30 fps
}

void GraphicsEngine::resizeGL(int width, int height) {
  makeCurrent();

  // Set the current viewport width/height
  m_viewport_width = width;
  m_viewport_height = height;

  m_aspect = float(m_viewport_width) / m_viewport_height;
  m_framebuffer_radius = sqrt(1+pow(m_aspect,2));
  pe_parameters().set_value("aspect", m_aspect);

  // Set the framebuffer dimensions.  
  m_framebuffer_width = FRAMEBUFFER_SIZE;
  m_framebuffer_height = FRAMEBUFFER_SIZE;

  //------------------------------------
  // Setup the OpenVG rendering engine
  //------------------------------------
  vgCreateContextSH(m_framebuffer_width, m_framebuffer_height);
  
  //------------------------------------
  // Set up the framebuffer and textures
  //------------------------------------

  // Create the framebuffer texture (for rendering...)
  glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, m_framebuffer0);

  // Bind the main texture to the framebuffer
  glBindTexture(GL_TEXTURE_2D, m_framebuffer_texture0);
  glTexImage2D(GL_TEXTURE_2D, 0, PE_GL_FORMAT, 
               m_framebuffer_width, m_framebuffer_height, 
               0, GL_BGRA, GL_UNSIGNED_BYTE, NULL);
  glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT,
                            GL_TEXTURE_2D, m_framebuffer_texture0, 0);

  // Bind the stencil buffer to the framebuffer
  glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, m_framebuffer_stencil0);
  glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT, GL_DEPTH_STENCIL_EXT, 
                           m_framebuffer_width, m_framebuffer_height);
  glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT,GL_DEPTH_ATTACHMENT_EXT,
                               GL_RENDERBUFFER_EXT, m_framebuffer_stencil0);
  glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT,GL_STENCIL_ATTACHMENT_EXT,
                               GL_RENDERBUFFER_EXT, m_framebuffer_stencil0);

  // Make sure that the framebuffer is correctly configured.
  GLenum status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT);
  if (status != GL_FRAMEBUFFER_COMPLETE_EXT)
    vw_throw(vw::LogicErr() << "GraphicsEngine::initializeGl() - could not initialize framebuffer.\n");
  glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0);

  // Setup the feedback texture buffer
  glBindTexture(GL_TEXTURE_2D, m_feedback_texture);
  glTexImage2D(GL_TEXTURE_2D, 0, PE_GL_FORMAT, 
               m_framebuffer_width, m_framebuffer_height,
               0, GL_BGRA, GL_UNSIGNED_BYTE, NULL);
  glBindTexture(GL_TEXTURE_2D, 0);

  //------------------------------------
  // Set up the warp mesh
  //------------------------------------
  setup_mesh();
}

// --------------------------------------------------------------
//             GraphicsEngine Private Methods
// --------------------------------------------------------------
void GraphicsEngine::timer_callback() {
  update();
}


void GraphicsEngine::drawImage() {
  if (pe_parameters().get_value("exit")) 
    emit pe_quit();

  if (!pe_script_engine().get_parameter("initialized")) 
    return;

  // ------------------------ <Scripts> -------------------------

  // Call out to any PhosphorScripts that are running on the
  // JavaScript VM, allowing them to update parameters if they would
  // like.
  pe_script_engine().execute("pe_animate()");
  if (pe_parameters().get_value("orientation") == 1)  // vertical 
    pe_parameters().set_readonly("aspect", 1.0/m_aspect);
  else                                                // horizontal
    pe_parameters().set_readonly("aspect", m_aspect);
    

  // Make this context current, and store the current OpenGL state
  // before we start to modify it. (This is a QT function)
  makeCurrent();
  
  // ------------------------ <FrameBuffer> -------------------------
 
  // Activate the framebuffer.  All of the following drawing is done
  // in the framebuffer so that we have a larger area available to
  // draw in.
  glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, m_framebuffer0);
  glDrawBuffer(GL_COLOR_ATTACHMENT0_EXT);
  glReadBuffer(GL_COLOR_ATTACHMENT0_EXT);

  // -----------------------
  // FEEDBACK TEXTURE 
  // ----------------------
  drawFeedback();

  // -----------------------
  // Darken Center
  // -----------------------
  drawDarkenCenter();

  // -----------------------
  // Motion Vectors
  // ----------------------
  drawVectorField();

  // -----------------------
  // Call out to python environment
  // -----------------------
  
  // Call the python environment and allow it to render whatever it wants using PyOpenGL
  pe_script_engine().execute("pe_render()");

  // Run through the list of drawables, giving them each a chance to
  // render into the display.
  glDisable(GL_BLEND);
  if (pe_script_engine().get_parameter("wave_enabled") ) {
    std::list<boost::shared_ptr<Drawable> >::iterator iter = m_drawables.begin();
    for (int i = 0; iter != m_drawables.end(); ++i, ++iter) {
      if ( i == pe_script_engine().get_parameter("wave_mode") ) {
        (*iter)->draw(pe_time(), pe_script_engine().get_parameter("decay"));
         break;
      }
    }
  }

  // Make the real screen the OpenGL target
  glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0);

  // -------------- <Render to Screen> -----------------

  qglClearColor(QColor(0, 0, 0)); // Black Background
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glViewport(0,0,m_viewport_width,m_viewport_height);
  
  // Set up the orthographic view of the scene.  The exact extent of
  // the view onto the scene depends on the current panning and zoom
  // in the UI.
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glOrtho(-m_aspect, m_aspect, -1.0, 1.0, -1.0, 1.0);

  // Set up the modelview matrix, and bind the image as the texture we
  // are about to use.
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  // Let the script draw a background (that won't become part of the feedback)
  pe_script_engine().execute("pe_render_bg()");
  glLoadIdentity();

  // Draw the ground texture
  glEnable( GL_TEXTURE_2D );
  glBindTexture( GL_TEXTURE_2D, m_ground_texture );
  qglColor(Qt::white);
  glBegin(GL_QUADS);
  glTexCoord2f( 0, 1.0 );
  glVertex2d( -m_aspect, -1);
  glTexCoord2f( 1.0, 1.0 );
  glVertex2d( m_aspect, -1);
  glTexCoord2f( 1.0, 0.0 );
  glVertex2d( m_aspect, 1);
  glTexCoord2f( 0.0, 0.0 );
  glVertex2d( -m_aspect, 1);
  glEnd();
  glBindTexture( GL_TEXTURE_2D, 0 );
  glDisable( GL_TEXTURE_2D );

  // Draw the framebuffer to the real screen.
  glEnable(GL_BLEND);
  glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
  glEnable( GL_TEXTURE_2D );
  glBindTexture( GL_TEXTURE_2D, m_framebuffer_texture0 );

  m_gpu_frontbuffer_program->install();
  m_gpu_frontbuffer_program->set_input_int("backbuffer_texture", 0);
  m_gpu_frontbuffer_program->set_input_float("framebuffer_radius", float(m_framebuffer_width));
  m_gpu_frontbuffer_program->set_input_float("time", pe_time());
  m_gpu_frontbuffer_program->set_input_float("gamma", pe_script_engine().get_parameter("gamma"));
  m_gpu_frontbuffer_program->set_input_float("invert", pe_script_engine().get_parameter("invert"));
  m_gpu_frontbuffer_program->set_input_float("brighten", pe_script_engine().get_parameter("brighten"));
  m_gpu_frontbuffer_program->set_input_float("darken", pe_script_engine().get_parameter("darken"));
  m_gpu_frontbuffer_program->set_input_float("solarize", pe_script_engine().get_parameter("solarize"));
  m_gpu_frontbuffer_program->set_input_float("edge_filter", pe_script_engine().get_parameter("edge_filter"));
    
  // Determine the dimensions of the sub-window for drawing from the
  // framebuffer texture.
  float w_texture = 0.5 * m_aspect/m_framebuffer_radius; // r_texture * ( w_object / r_object )
  float h_texture = 0.5 * 1.0/m_framebuffer_radius;      // r_texture * ( h_object / r_object )

  //  We will draw the image as a texture on this quad.
  qglColor(Qt::blue);
  glBegin(GL_QUADS);
  glTexCoord2f( 0.5-w_texture, 0.5-h_texture );
  glVertex2d( -m_aspect, -1.0);
  glTexCoord2f( 0.5+w_texture, 0.5-h_texture ); 
  glVertex2d( m_aspect, -1.0);
  glTexCoord2f( 0.5+w_texture, 0.5+h_texture );
  glVertex2d( m_aspect, 1.0);
  glTexCoord2f( 0.5-w_texture, 0.5+h_texture );
  glVertex2d( -m_aspect, 1.0);
  glEnd() ;

  glBindTexture( GL_TEXTURE_2D, 0 );
  glDisable( GL_TEXTURE_2D );
  glDisable(GL_BLEND);
  m_gpu_frontbuffer_program->uninstall();

  if (pe_script_engine().get_parameter("show_fps") != 0) {
    char fps_cstr[255];
    sprintf(fps_cstr, "FPS: %0.2f", m_fps_avg);
    QString fps_str(fps_cstr);
    this->renderText(20,20,fps_str);
  }

  // Swap the buffer and render to the screen.
  this->recordFrame();

  // Note: this seems to be necessary on QT4.6 preview on OSX 10.6
#ifdef __APPLE__
  this->swapBuffers();
#endif

  // Recompute FPS
  double new_time = double(vw::Stopwatch::microtime()) / 1.0e6;
  float fps = 1.0/(new_time - m_fps_last_time);
  m_fps_avg = 0.01 * fps + 0.99 * m_fps_avg;
  pe_script_engine().set_parameter("fps", fps);
  // For debugging:
  //  std::cout << "FPS: " << fps << "\n";

  m_fps_last_time = new_time;
  pe_script_engine().set_parameter("frame", pe_script_engine().get_parameter("frame") + 1.0);

  // ----------------- <Feedback> ----------------------

  // Feedback-only rendering
  glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, m_framebuffer0);
  glViewport(0,0,m_framebuffer_width,m_framebuffer_height);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();

  glOrtho(-m_framebuffer_radius, m_framebuffer_radius, 
          -m_framebuffer_radius, m_framebuffer_radius, 
          -1.0, 1.0);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  pe_script_engine().execute("pe_render_back()");

  // Save the feedback texture 
  saveFeedback();
}

void GraphicsEngine::updateCurrentMousePosition() {
  float x_loc = m_current_viewport.min().x() + m_current_viewport.width() * float(lastPos.x()) / m_viewport_width;
  float y_loc = m_current_viewport.min().y() + m_current_viewport.height() * float(lastPos.y()) / m_viewport_height;
  currentImagePos = QPoint(x_loc,y_loc);
}


// --------------------------------------------------------------
//             GraphicsEngine Setup Methods
// --------------------------------------------------------------
void GraphicsEngine::saveFeedback() {

  // Activate the framebuffer.  All of the following steps pull data
  // from the framebuffer rather than the main screen.
  glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, m_framebuffer0);

  // Copy the contents of the framebuffer into the feedback texture.
  glBindTexture(GL_TEXTURE_2D, m_feedback_texture);
  glCopyTexImage2D(GL_TEXTURE_2D, 0, PE_GL_FORMAT, 0, 0, 
                   m_framebuffer_width, m_framebuffer_height, 0);
  glBindTexture(GL_TEXTURE_2D, 0);
}

void GraphicsEngine::recordFrame() {
  if (m_record) {
    std::ostringstream ostr;    
    ostr << "/tmp/pe_frame_";
    for (int i = 1; i < 5; ++i) {
      if (int(m_record_frame_number / powf(10,i)) == 0) {
        ostr << "0";
      }
    }
    ostr << m_record_frame_number << ".jpg";
    std::cout << "Recording frame: " << ostr.str() << "\n";
    
    // Deactivate the framebuffer.  Make sure we are reading pixels from
    // the screen.
    glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0);

    ImageView<PixelRGB<uint8> > image(m_viewport_width, m_viewport_height);
    glReadPixels(0,0,m_viewport_width,m_viewport_height,
                 GL_RGB, GL_UNSIGNED_BYTE,&(image(0,0)));
    write_image(ostr.str(), image);


    m_record_frame_number++;
  }
  
}

// --------------------------------------------------------------
//             GraphicsEngine Event Handlers
// --------------------------------------------------------------

void GraphicsEngine::paintEvent(QPaintEvent * /* event */) { 
  QPainter painter(this);
  drawImage();
}

void GraphicsEngine::mousePressEvent(QMouseEvent *event) { 
  grabKeyboard();
  lastPos = event->pos();
  updateCurrentMousePosition();
}

void GraphicsEngine::mouseMoveEvent(QMouseEvent *event) {
  // Left mouse button moves the image around
  if (event->buttons() & Qt::LeftButton) {
    // float x_diff = float(event->x() - lastPos.x()) / m_viewport_width;
    // float y_diff = float(event->y() - lastPos.y()) / m_viewport_height;
    // float ticks;

    // std::ostringstream s; 

    // do something here?
  }
  // Regardless, we store the current position for the text legend.
  lastPos = event->pos();
  updateCurrentMousePosition();
  //  update();
}

void GraphicsEngine::mouseDoubleClickEvent(QMouseEvent * /*event*/) {
  //  update();
}

void GraphicsEngine::wheelEvent(QWheelEvent *event) {
  // int num_degrees = event->delta() / 8;
  // float num_ticks = num_degrees / 15;

  // float scale = pow(2,num_ticks/5);

  // if (m_gain * scale >= 0.0 && m_gain * scale <= 1.0)
  //   m_gain *= scale;
  
  // //  zoom(scale);

  // m_show_legend = true;
  grabKeyboard();
  lastPos = event->pos();
  updateCurrentMousePosition();
}


void GraphicsEngine::enterEvent(QEvent */*event*/) {
  //  m_show_legend = true;
  grabKeyboard();
  //  update();
}

void GraphicsEngine::leaveEvent(QEvent */*event*/) {
  //  m_show_legend = false;
  releaseKeyboard();
  //  update();
}

void GraphicsEngine::keyPressEvent(QKeyEvent *event) {

  std::ostringstream s; 
  
  switch (event->key()) {
  case Qt::Key_Left: 
    pe_script_engine().execute("PePreset.prev_preset();");
    break;
  case Qt::Key_Right:  
    pe_script_engine().execute("PePreset.next_preset();");
    break;

  case Qt::Key_R:  
    m_record = !m_record;
    if (m_record) 
      std::cout << "Starting screen capture.\n";
    else
      std::cout << "Stopping screen capture.  Results can be found in /tmp\n";
    break;

  case Qt::Key_Up:  
    pe_script_engine().set_parameter("ifs_mode", pe_script_engine().get_parameter("ifs_mode") + 1.0);
    break;
  case Qt::Key_Down:  
    pe_script_engine().set_parameter("ifs_mode", pe_script_engine().get_parameter("ifs_mode") - 1.0);
    break;
  case Qt::Key_I:  
    pe_script_engine().set_parameter("invert", 1.0-pe_script_engine().get_parameter("invert"));
    break;
  default: 
    QWidget::keyPressEvent(event);
  }
}

