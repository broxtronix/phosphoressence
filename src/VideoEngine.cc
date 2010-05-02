// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

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

#include <Mycelium.h>

#include <ScriptEngine.h>
#include <pe/Math/Matrix.h>
#include <pe/Graphics/Texture.h>
#include <pe/Vision/ContourFinder.h>
#include <pe/Vision/BlobTracker.h>
#include <pe/Vision/Blob.h>
#include <pe/Core/Time.h>
#include <VideoEngine.h>
#include <iostream>

#include "highgui.h"
using namespace cv;

// ---------------------------------------------------------------------------
//                              HyphaeListener
// ---------------------------------------------------------------------------

class HyphaeListener : public pe::vision::BlobListener {
  std::list<boost::shared_ptr<Hyphae> > m_hypha;
  std::map<int, int> m_timeouts;            // [ id, timeout ]
  std::map<int, pe::Vector2> m_positions;   // [ id, position ]

public:
  virtual void blobOn( float x, float y, int id, int order) { 
    // Create new timeout counter
    m_timeouts[id] = 0;
    m_positions[id] = pe::Vector2(x,y);
  }

  virtual void blobMoved( float x, float y, int id, int order ) {     
    // Reset the timeout counter to zero
    m_timeouts[id] = 0;
    m_positions[id] = pe::Vector2(x,y);
  }

  virtual void blobOff( float x, float y, int id, int order ) {
    // Erase this timeout counter
    m_timeouts.erase(id);
    m_positions.erase(id);
  }

  void render() {
    // Step 1: Update Timeouts
    std::map<int,int>::iterator t = m_timeouts.begin();
    while (t != m_timeouts.end()) {

      // Increment all timeouts by one.
      (t->second)++;

      // If the timeout threshold has been reached for this blob id,
      // we launch a new hyphae!
      if (t->second == pe_script_engine().get_parameter("vision_blob_movement_delay")) {
        pe::Vector2 pos = m_positions[t->first];
        boost::shared_ptr<Hyphae> hyphae(new Hyphae(pos.x(), pos.y(), t->first));
        std::cout << "Creating hyphae at " << pos << "\n";
        m_hypha.push_back(hyphae);
      }
      ++t;
    }

    // Step 2: Clean up "finished" hyphae and render the rest
    std::list<boost::shared_ptr<Hyphae> >::iterator h = m_hypha.begin();
    while (h != m_hypha.end()) {
      std::list<boost::shared_ptr<Hyphae> >::iterator current_hyphae = h;
      ++h;
      if ((*current_hyphae)->tendrils.size() == 0) {
        m_hypha.erase(current_hyphae);
      } else {
        (*current_hyphae)->render(m_hypha);
      }
    }
  }
};

// ---------------------------------------------------------------------------
//                              Video Thread
// ---------------------------------------------------------------------------

class VideoTask {
  pe::Mutex m_mutex;
  bool m_initialized, m_terminate, m_needs_background_captured;
  float m_aspect_ratio;
  boost::shared_ptr<cv::VideoCapture> m_video_capture;
  cv::Mat m_raw_frame, m_background_frame, m_working_frame, m_render_frame;
  pe::graphics::Texture m_video_texture;
  pe::vision::ContourFinder m_contour_finder;
  boost::shared_ptr<pe::vision::BlobTracker> m_blob_tracker;
  HyphaeListener m_hyphae_listener;
  boost::shared_ptr<pe::simulation::FluidSimulation> m_fluid_sim;
  boost::shared_ptr<Mycelium> m_mycelium;
  pe::Vector2 m_resolution;

public:
  VideoTask(pe::Vector2 resolution,
            boost::shared_ptr<pe::simulation::FluidSimulation> fluid_sim) : m_terminate(false), m_needs_background_captured(false), m_fluid_sim(fluid_sim), m_resolution(resolution) {

    m_video_capture.reset(new cv::VideoCapture(1));
    
    // check if we succeeded  
    if(!m_video_capture->isOpened()) {
      std::cout << "WARNING: Could not open video camera.\n";
      m_initialized = false;
      m_terminate = true;
      return;
    } else {
      m_initialized = true;
    }

    // Set capture size
    m_video_capture->set(CV_CAP_PROP_FRAME_WIDTH, resolution[0]);
    m_video_capture->set(CV_CAP_PROP_FRAME_WIDTH, resolution[1]);

    // Seed the first frame
    cv::Mat frame;
    (*m_video_capture) >> frame;
    cvtColor(frame, m_raw_frame, CV_BGR2GRAY);

    // Save the background image & set the intial previous frame.
    m_background_frame = m_raw_frame.clone();
    m_working_frame = m_raw_frame.clone();
    m_render_frame = m_raw_frame.clone();

    // Allocate texture memory
    m_video_texture.allocate(frame.size().width, frame.size().height, GL_RGB);

    this->set_aspect_ratio(resolution.x()/resolution.y());

    m_mycelium.reset(new Mycelium());
    // m_mycelium->spawn(0,250);
    // m_mycelium->spawn(180,0);
    // m_mycelium->spawn(199,32);
    // m_mycelium->spawn(-132,323);
    // m_mycelium->spawn(-233,-22);

    // Initialize blob tracker
    m_blob_tracker.reset( new pe::vision::BlobTracker() );
    m_blob_tracker->setListener(&m_hyphae_listener);
  }

  void operator()() {
    cv::Mat frame;
    while (!m_terminate) {
      pe::Mutex::Lock lock(m_mutex);
      
      // Get a new frame from camera
      (*m_video_capture) >> frame; 

      // Normalize
      // cv::Mat norm_frame;
      // cv::normalize(frame, norm_frame);

      // Convert to grayscale
      cvtColor(frame, m_raw_frame, CV_BGR2GRAY);

      // Reset background image if requested
      if (m_needs_background_captured) {
        m_background_frame = m_raw_frame.clone();
        m_needs_background_captured = false;
      }
      
      // Background subtraction
      cv::absdiff(m_raw_frame, m_background_frame, m_working_frame);
      
      // Uncomment to disable background subtraction
      //m_working_frame = m_raw_frame.clone();

      // Flip video left/right
      cv::flip(m_working_frame, m_working_frame, 1);

      m_render_frame = m_working_frame.clone();

      // Blur a bit
      float sigma = pe_script_engine().get_parameter("vision_blur_sigma");
      GaussianBlur(m_working_frame, m_working_frame, cv::Size(7,7), sigma, sigma);
      
      // Compute the threhold image.
      float thresh = pe_script_engine().get_parameter("vision_threshold");
      cv::threshold(m_working_frame, m_working_frame, 255*thresh, 255, cv::THRESH_BINARY);
      //      imshow("test", m_working_frame);

      // Find Contours
      m_contour_finder.findContours(m_working_frame,
                                    pe_script_engine().get_parameter("vision_blob_minsize"), 
                                    pe_script_engine().get_parameter("vision_blob_maxsize"), 
                                    pe_script_engine().get_parameter("vision_num_blobs"), 
                                    pe_script_engine().get_parameter("vision_blob_findholes"), 
                                    pe_script_engine().get_parameter("vision_blob_approximate"));

      // Track blobs
      m_blob_tracker->trackBlobs(m_contour_finder.blobs());

      // Record frames at 30 Hz, tops!
      pe::Thread::sleep_ms(33);
    } 
  }

  void set_aspect_ratio(float aspect_ratio) { 
    pe::Mutex::Lock lock(m_mutex);
    m_aspect_ratio = aspect_ratio; 

    // Set up the camera calibration matrix
    pe::Matrix3x3 camera_calibration;
    camera_calibration.set_identity();
    camera_calibration(0,0) = -2.0*m_aspect_ratio/m_resolution[0];
    camera_calibration(1,1) = -2.0/m_resolution[1];
    camera_calibration(0,2) = m_aspect_ratio;
    camera_calibration(1,2) = 1.0;
    m_contour_finder.setCalibration(camera_calibration);
  }

  void drawMycelium() {
    pe::Mutex::Lock lock(m_mutex);

    m_blob_tracker->minimumDisplacementThreshold = pe_script_engine().get_parameter("vision_blob_movement_threshold");
    m_hyphae_listener.render();
    m_mycelium->render();
  }

  void drawPhosphorEssence() {
    pe::Mutex::Lock lock(m_mutex);

    // Add in perturbations to the fluid layer.
    for (unsigned i = 0; i < m_blob_tracker->blobs.size(); ++i) {
      float x = m_blob_tracker->blobs[i].smoothedCentroid.x();
      float y = m_blob_tracker->blobs[i].smoothedCentroid.y();

      glEnable(GL_BLEND);
      glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
      glColor4f(1.0,1.0,1.0,0.1);
      glBegin(GL_QUADS);
      glVertex2d( x-0.25, y-0.25);
      glVertex2d( x+0.25, y-0.25);
      glVertex2d( x+0.25, y+0.25);
      glVertex2d( x-0.25, y+0.25);
      glEnd();
      glDisable(GL_BLEND);

      // Add in perturbations to the fluid layer.
      // m_fluid_sim->add_velocity_worldcoords(m_blob_tracker->blobs[i].smoothedCentroid.x(),
      //                                       m_blob_tracker->blobs[i].smoothedCentroid.y(), 
      //                                       10.0*m_blob_tracker->blobs[i].deltaLoc);

    }
  }

  void draw() {
    pe::Mutex::Lock lock(m_mutex);
    m_contour_finder.draw();
    m_blob_tracker->draw();
  }

  void drawDebug() {
    if (!m_initialized)
      return;

    pe::Mutex::Lock lock(m_mutex);

    m_video_texture.loadData(m_render_frame.ptr(), 
                             m_render_frame.size().width, 
                             m_render_frame.size().height, 
                             GL_LUMINANCE, GL_UNSIGNED_BYTE);
    m_video_texture.draw(m_aspect_ratio, -1.0, -2*m_aspect_ratio, 2.0);
  }
  
  void capture_background_frame() {
    m_needs_background_captured = true;
  }

  void terminate() { m_terminate = true; }
};



// ---------------------------------------------------------------------------
//                              Video Engine
// ---------------------------------------------------------------------------

VideoEngine::VideoEngine(pe::Vector2 resolution,
                         boost::shared_ptr<pe::simulation::FluidSimulation> fluid_sim) {
  m_task.reset(new VideoTask(resolution, fluid_sim));
  m_thread.reset(new pe::Thread( m_task ));
}

VideoEngine::~VideoEngine() {
  if (m_task) {
    m_task->terminate();
    m_thread->join();
  }
}

void VideoEngine::set_aspect_ratio(float aspect_ratio) {
  m_task->set_aspect_ratio(aspect_ratio);
}

void VideoEngine::draw() {
  m_task->draw();
}

void VideoEngine::drawDebug() {
  m_task->drawDebug();
}

void VideoEngine::drawMycelium() {
  m_task->drawMycelium();
}

void VideoEngine::drawPhosphorEssence() {
  m_task->drawPhosphorEssence();
}

void VideoEngine::capture_background_frame() {
  m_task->capture_background_frame();
}
