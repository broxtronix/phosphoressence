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
#include <pe/Graphics/Texture.h>
#include <pe/Vision/ContourFinder.h>
#include <VideoEngine.h>
#include <iostream>

#include "highgui.h"
using namespace cv;


// ---------------------------------------------------------------------------
//                              Video Thread
// ---------------------------------------------------------------------------

class VideoTask {
  pe::Mutex m_mutex;
  bool m_terminate;
  boost::shared_ptr<cv::VideoCapture> m_video_capture;
  cv::Mat m_current_frame, m_prev_frame;
  pe::graphics::Texture m_video_texture;
  pe::vision::ContourFinder m_contour_finder;

public:
  VideoTask(std::string url) : m_terminate(false) {

    // Plays a file on disk.
    if (url.size() != 0) {
      m_video_capture.reset(new cv::VideoCapture(url));

      // check if we succeeded  
      if(!m_video_capture->isOpened()) {
        std::cout << "Could not open video file: " << url << "\n";
        exit(1);
    }

    // Opens the webcam.
    } else {
      m_video_capture.reset(new cv::VideoCapture(0));

      // check if we succeeded  
      if(!m_video_capture->isOpened()) {
        std::cout << "Could not open video camera 0.  Exiting.\n";
        exit(1);
      }
    }

    // Seed the first frame
    cv::Mat frame;
    (*m_video_capture) >> frame;
    cvtColor(frame, m_current_frame, CV_BGR2GRAY);

    // Allocate texture memory
    m_video_texture.allocate(frame.size().width, frame.size().height, GL_RGB);
  }

  void operator()() {
    cv::Mat frame;
    while (!m_terminate) {
      pe::Mutex::Lock lock(m_mutex);

      // Store the previous frame
      m_prev_frame = m_current_frame;
      
      // Get a new frame from camera
      (*m_video_capture) >> frame; 
      cvtColor(frame, m_current_frame, CV_BGR2GRAY);
      
      // Todo: add background subtraction.

      // Blur a bit
      GaussianBlur(m_current_frame, m_current_frame, cv::Size(7,7), 1.5, 1.5);

      
      // Compute the threhold image.
      float thresh = pe_script_engine().get_parameter("vision_threshold");
      cv::threshold(m_current_frame, m_current_frame, 255*thresh, 255, cv::THRESH_BINARY);

      imshow("test", m_current_frame);

      // Find Contours
      m_contour_finder.findContours(m_current_frame,
                                    100,      // Min area
                                    640*480, // Max area
                                    pe_script_engine().get_parameter("vision_num_blobs"),      // nConsidered
                                    false,   // find holes
                                    true);  // Use approximation

      // Record frame at 60 Hz, tops!
      pe::Thread::sleep_ms(16);
    } 
  }

  void draw(int x, int y, int width, int height) {
    pe::Mutex::Lock lock(m_mutex);
    m_video_texture.loadData(m_current_frame.ptr(), 
                             m_current_frame.size().width, 
                             m_current_frame.size().height, 
                             GL_LUMINANCE, GL_UNSIGNED_BYTE);

    //    m_video_texture.draw(-1.0, -1.0, 1.0, 1.0);
    m_contour_finder.draw(x, y, width, height);
  }

  void terminate() { m_terminate = true; }
};



// ---------------------------------------------------------------------------
//                              Video Engine
// ---------------------------------------------------------------------------

VideoEngine::VideoEngine(std::string url) {
  m_task.reset(new VideoTask(url));
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


