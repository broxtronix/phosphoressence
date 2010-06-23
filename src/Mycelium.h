// __BEGIN_LICENSE__
// Copyright (C) 2009 Mary Franck and Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__
#ifndef __MYCELIUM_H__
#define __MYCELIUM_H__

#include <GraphicsEngine.h>
#include <pe/Math/Vector.h>

// Forward Declarations
class Hyphae;
class Tendril;

// Typedefs
typedef std::list<boost::shared_ptr<Hyphae> > hyphae_list_t;
typedef std::list<boost::shared_ptr<Tendril> > tendril_list_t;

// ----------------------------------------------------------------------
//                          PLANTSMARTS
// ----------------------------------------------------------------------

class PlantSmarts {
  
protected:
  boost::shared_ptr<Hyphae> m_closest_hyphae;
  boost::shared_ptr<Tendril> m_closest_tendril;
  float separateFactor;
  pe::Vector2 m_dispersion_vector;
  
public:

  // Public variables
  Hyphae* parent;
  pe::Vector2 tcenter;
  pe::Vector2 loc;

  PlantSmarts(Hyphae* _parent, pe::Vector2 _center, pe::Vector2 _loc);

  // Update the nearest hyphae
  boost::shared_ptr<Hyphae> update_closest_hyphae(hyphae_list_t hypha);
  boost::shared_ptr<Tendril> update_closest_tendril(hyphae_list_t hypha);
};

// ----------------------------------------------------------------------
//                             TENDRIL
// ----------------------------------------------------------------------

class Tendril : public PlantSmarts {

  void fungal(hyphae_list_t hypha);
  void update();

  void branch();
  pe::Vector2 disperse();
  pe::Vector2 wander();
  pe::Vector2 attract();
  pe::Vector2 stick();
  pe::Vector2 separate(hyphae_list_t hypha);
  
public:
  // Public variables
  int tendril_id;
  pe::Vector2 vel;
  pe::Vector2 acc;
  float radius;
  float maxspeed;
  bool connected;

  Tendril(Hyphae* _parent, int _tendril_id, pe::Vector2 _loc, pe::Vector2 _center, float _radius);
  void render(hyphae_list_t hypha);
};

// ----------------------------------------------------------------------
//                              HYPHAE
// ----------------------------------------------------------------------

class Hyphae {
  int m_next_id;

public:

  // Public variables
  pe::Vector2 center;
  tendril_list_t tendrils;
  int num_generated_tendrils;
  int id;
  int num_frames_since_last_movement;

  // Initialize a hyphae with the specified center location.
  Hyphae(float x, float y, int id);

  // Update the position of this hyphae
  void move(float x, float y);

  // We pass in the complete list of hypha so that hyphae children
  // can access those center loctaions.
  void render(hyphae_list_t hypha);

  // Add a new tendril
  void add_tendril(pe::Vector2 loc, pe::Vector2 center, float radius);
};

// ----------------------------------------------------------------------
//                              MYCELIUM
// ----------------------------------------------------------------------

class Mycelium {
  hyphae_list_t m_hypha;

public:
  Mycelium();
  void spawn(float x, float y);
  void render();
};

#endif
