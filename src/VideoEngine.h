// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#ifndef __VIDEO_ENGINE_H__
#define __VIDEO_ENGINE_H__

// OpenCV
#include "cv.h"
#include "highgui.h"

#include <pe/Core/Thread.h>
#include <pe/Core/FundamentalTypes.h>
#include <boost/circular_buffer.hpp>

// ---------------------------------------------------------------------------
//                              Video Thread
// ---------------------------------------------------------------------------

/// Video
///
class Video {
  pe::Mutex m_mutex;
  std::string m_url;
  bool m_terminate;
  cv::VideoCapture m_video_capture;
  cv::Mat m_last_frame;

public:

  Video(std::string url);
  ~Video();

  void operator()();
  void terminate() { m_terminate = true; }

  void copy_to_texture(pe::uint32);
};

#endif // __VIDEO_ENGINE_H__
