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
#include <pe/Math/Vector.h>
#include <pe/Simulation/FluidDynamics.h>
#include <pe/Core/FundamentalTypes.h>
#include <boost/circular_buffer.hpp>

// ---------------------------------------------------------------------------
//                              Video Engine
// ---------------------------------------------------------------------------

class VideoTask;

class VideoEngine {
  boost::shared_ptr<VideoTask> m_task;
  boost::shared_ptr<pe::Thread> m_thread;

public:

  // An empty URL string causes us to open the default camera
  VideoEngine(pe::Vector2 resolution, 
              boost::shared_ptr<pe::simulation::FluidSimulation> fluid_sim);
  ~VideoEngine();

  void operator()();
  void set_aspect_ratio(float aspect_ratio);
  void draw();
  void drawDebug();
  void drawMycelium();
  void capture_background_frame();

};

#endif // __VIDEO_ENGINE_H__
