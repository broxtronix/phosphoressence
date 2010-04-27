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

#include <ScriptEngine.h>
#include <pe/Math/Matrix.h>
#include <pe/Graphics/Texture.h>
#include <pe/Vision/ContourFinder.h>
#include <pe/Vision/BlobTracker.h>
#include <VideoEngine.h>
#include <iostream>

#include "highgui.h"
using namespace cv;


// ---------------------------------------------------------------------------
//                              Video Thread
// ---------------------------------------------------------------------------

class VideoTask {
  pe::Mutex m_mutex;
  bool m_terminate, m_needs_background_captured;
  float m_aspect_ratio;
  boost::shared_ptr<cv::VideoCapture> m_video_capture;
  cv::Mat m_raw_frame, m_prev_frame, m_background_frame, m_working_frame, m_render_frame;
  pe::graphics::Texture m_video_texture;
  pe::vision::ContourFinder m_contour_finder;
  pe::vision::BlobTracker m_blob_tracker;

public:
  VideoTask(pe::Vector2 resolution) : m_terminate(false), m_needs_background_captured(false) {

    m_video_capture.reset(new cv::VideoCapture(0));
    
    // check if we succeeded  
    if(!m_video_capture->isOpened()) {
      std::cout << "Could not open video camera 0.  Exiting.\n";
      exit(1);
    }

    // Set capture size
    m_video_capture->set(CV_CAP_PROP_FRAME_WIDTH, resolution[0]);
    m_video_capture->set(CV_CAP_PROP_FRAME_WIDTH, resolution[1]);

    // Seed the first frame
    cv::Mat frame;
    (*m_video_capture) >> frame;
    cvtColor(frame, m_raw_frame, CV_BGR2GRAY);

    // Save the background image & set the intial previous frame.
    m_prev_frame = m_raw_frame;
    m_background_frame = m_raw_frame.clone();
    m_working_frame = m_raw_frame.clone();
    m_render_frame = m_raw_frame;

    // Allocate texture memory
    m_video_texture.allocate(frame.size().width, frame.size().height, GL_RGB);

    // Set up the camera calibration matrix
    m_aspect_ratio = resolution.x()/resolution.y();
    pe::Matrix3x3 camera_calibration;
    camera_calibration.set_identity();
    camera_calibration(0,0) = -2.0*m_aspect_ratio/resolution[0];
    camera_calibration(1,1) = -2.0/resolution[1];
    camera_calibration(0,2) = m_aspect_ratio;
    camera_calibration(1,2) = 1.0;
    m_contour_finder.setCalibration(camera_calibration);
  }

  void operator()() {
    cv::Mat frame;
    while (!m_terminate) {
      pe::Mutex::Lock lock(m_mutex);

      // Store the previous frame
      m_prev_frame = m_raw_frame;
      
      // Get a new frame from camera
      (*m_video_capture) >> frame; 
      cvtColor(frame, m_raw_frame, CV_BGR2GRAY);

      // Reset background image if requested
      if (m_needs_background_captured) {
        m_background_frame = m_raw_frame.clone();
        m_needs_background_captured = false;
      }
      
      // Background subtraction
      cv::absdiff(m_raw_frame, m_background_frame, m_working_frame);
      m_render_frame = m_working_frame.clone();

      // Blur a bit
      GaussianBlur(m_working_frame, m_working_frame, cv::Size(7,7), 1.5, 1.5);
      
      // Compute the threhold image.
      //float thresh = pe_script_engine().get_parameter("vision_threshold");
      float thresh = 0.2;
      cv::threshold(m_working_frame, m_working_frame, 255*thresh, 255, cv::THRESH_BINARY);

      //      imshow("test", m_working_frame);

      // Find Contours
      m_contour_finder.findContours(m_working_frame,
                                    100,     // Min area
                                    640*480, // Max area
                                    10,
                                    //pe_script_engine().get_parameter("vision_num_blobs"),      // nConsidered
                                    false,   // find holes
                                    true);  // Use approximation

      // Track blobs
      m_blob_tracker.trackBlobs(m_contour_finder.blobs());

      // Record frames at 60 Hz, tops!
      pe::Thread::sleep_ms(16);
    } 
  }

  void draw(int x, int y, int width, int height) {
    pe::Mutex::Lock lock(m_mutex);
    m_video_texture.loadData(m_render_frame.ptr(), 
                             m_render_frame.size().width, 
                             m_render_frame.size().height, 
                             GL_LUMINANCE, GL_UNSIGNED_BYTE);

    m_video_texture.draw(m_aspect_ratio, -1.0, -2*m_aspect_ratio, 2.0);
    m_contour_finder.draw();
    m_blob_tracker.draw();
  }
  
  void capture_background_frame() {
    m_needs_background_captured = true;
  }

  void terminate() { m_terminate = true; }
};



// ---------------------------------------------------------------------------
//                              Video Engine
// ---------------------------------------------------------------------------

VideoEngine::VideoEngine(pe::Vector2 resolution) {
  m_task.reset(new VideoTask(resolution));
  m_thread.reset(new pe::Thread( m_task ));
}

VideoEngine::~VideoEngine() {
  if (m_task) {
    m_task->terminate();
    m_thread->join();
  }
}

void VideoEngine::draw(int x, int y, int width, int height) {
  m_task->draw(x,y,width,height);
}

void VideoEngine::capture_background_frame() {
  m_task->capture_background_frame();
}
