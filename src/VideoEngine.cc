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

#include <VideoEngine.h>
#include <iostream>
using namespace cv;

Video::Video(std::string url): m_url(url), m_terminate(false) {
  std::cout << "Attempting to open " << url << "\n";

  // Plays a file on disk.
  if (url.size() != 0) {
    m_video_capture.open(url);

    // check if we succeeded  
    if(!m_video_capture.isOpened()) {
      std::cout << "Could not open video file: " << url << "\n";
      exit(1);
    }

  // Opens the webcam.
  } else {
    m_video_capture.open(0);

    // check if we succeeded  
    if(!m_video_capture.isOpened()) {
      std::cout << "Could not open video camera 0.  Exiting.\n";
      exit(1);
    }
  }
}

Video::~Video() {}

void Video::copy_to_texture(vw::uint32 texture) {
  vw::Mutex::Lock lock(m_mutex);

  //  cv::Mat frame;
  if (m_video_capture.grab()) {}
  //    m_video_capture.retrieve(m_last_frame); // get a new frame from camera

  //  cv::cvtColor(frame, m_last_frame, CV_BGR2GRAY);
  cv::GaussianBlur(m_last_frame, m_last_frame, cv::Size(7,7), 1.5, 1.5);
  //  cv::Canny(m_last_frame, m_last_frame, 0, 30, 3);

  glBindTexture(GL_TEXTURE_2D, texture);
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
               m_last_frame.size().width, 
               m_last_frame.size().height, 
               0, GL_BGR, GL_UNSIGNED_BYTE, 
               m_last_frame.ptr());
  glBindTexture(GL_TEXTURE_2D, 0);
}

