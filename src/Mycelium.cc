#include "Mycelium.h"
#include <pe/Math/Vector.h>
#include <pe/Core/Random.h>
using namespace pe;

#define PIXEL_SCALE_FACTOR (1.0/400.0)

// ----------------------------------------------------------------------
//                          PLANTSMARTS
// ----------------------------------------------------------------------

PlantSmarts::PlantSmarts(Hyphae* _parent, Vector2 _center, Vector2 _loc) {
  parent = _parent;
  tcenter = _center;
  loc = _loc;
  separateFactor = 1;
}

// Update the nearest hyphae
boost::shared_ptr<Hyphae> PlantSmarts::update_closest_hyphae(hyphae_list_t hypha) {
  m_closest_hyphae.reset();
    
  // Check to see if we are the only hyphae.  If so, we return a null ptr.
  if (hypha.size() != 1) {
    float closestDist = 10000.0;
    hyphae_list_t::iterator h = hypha.begin();
    while (h != hypha.end()) {
      float d = math::norm_2(this->loc - (*h)->center);
      if ((d < closestDist) && ((*h).get() != this->parent)) {
        closestDist = d;
        m_closest_hyphae = *h;
      }
      ++h;
    }
  }
  return m_closest_hyphae;
}


boost::shared_ptr<Tendril> PlantSmarts::update_closest_tendril(hyphae_list_t hypha) {
  m_closest_tendril.reset();

  // We also compute a dispersion vector here
  m_dispersion_vector = Vector2(0,0);
  
  // Check to see if we are the only hyphae.  If so, we return a null ptr.
  if (hypha.size() != 1) {
    float closestDist = 10000.0;

    hyphae_list_t::iterator h = hypha.begin();
    while (h != hypha.end()) {
      float desiredseparation = pe_random().uniform(1,40) * this->separateFactor;

      tendril_list_t::iterator t = (*h)->tendrils.begin();
      while (t != (*h)->tendrils.end()) {
        float distl = math::norm_2(this->loc - (*t)->loc);

        // Update dispersion.  If the distance is greater than 0 and
        // less than an arbitrary amount (0 when you are yourself)
        if ((distl > 1) && (distl < desiredseparation)) {
          Vector2 diff = this->loc - this->loc;
          if (math::norm_2(diff) != 0.0)  // avoid NaN
            diff /= math::norm_2(diff);   // normalize
          
          //  Weight by distance
          m_dispersion_vector += diff;
        }

        // Update closest tendril
        if ((distl < closestDist) && 
            ((*t).get() != this) && 
            ((*t)->parent != this->parent) && 
            ((*t)->connected == false)) {
          closestDist = distl;
          m_closest_tendril = *t;
        }
        ++t;
      }
      ++h;
    }
  }
  return m_closest_tendril;
}

// ----------------------------------------------------------------------
//                             TENDRIL
// ----------------------------------------------------------------------

Tendril::Tendril(Hyphae* _parent, int _tendril_id, Vector2 _loc, Vector2 _center, float _radius) : PlantSmarts(_parent, _center, _loc) {
  tendril_id = _tendril_id;
  vel = Vector2(pe_random().uniform(-0.5,0.5), pe_random().uniform(-0.5,0.5));
  acc = Vector2(0,0);
  radius = _radius;
  maxspeed = 1.0;
  connected = false;
}

void Tendril::render(hyphae_list_t hypha) {
  // Periodically update the closest hyphae and tendril.  The
  // less often you do this, the faster the simulation runs!
  if (pe_random().uniform_int(1,10) == 1) {
    this->update_closest_tendril(hypha);
    this->update_closest_hyphae(hypha);
  }

  if ( !(this->connected) ) {
    this->fungal(hypha);
    this->branch();
    this->update();

    // Draw the shape.
    glLoadIdentity();
    glEnable(GL_BLEND);
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glPointSize(this->radius);

    // Draw the dots at the vertices
    if (this->connected) 
      glColor4f(1.0, 0.0, 0.0, 1.0);
    else
      glColor4f(1.0, 1.0, 1.0, 1.0);
    glBegin(GL_POINTS);
    glVertex2f(this->loc[0]*PIXEL_SCALE_FACTOR, this->loc[1]*PIXEL_SCALE_FACTOR);
    glEnd();
  }
}

void Tendril::fungal(hyphae_list_t hypha) {
  Vector2 disp = this->disperse();    // grow away from own center
  Vector2 wand = this->wander();      // adds randomness
  Vector2 atrc = this->attract();     // grow towards closest hyphae center, check if connected
  Vector2 stic = this->stick();    // connect to other tendril tips, check if connected
  Vector2 sep = m_dispersion_vector;

  // Weight these forces
  disp *= 0.1;
  wand *= 0.15;
  atrc *= 0.05;
  stic *= 1.0;
  sep *= 0.5;

  // Add force vectors to acceleration
  this->acc += disp;
  this->acc += wand;
  this->acc += atrc;
  this->acc += stic;
  this->acc += sep;   // weight differently at dif proximity?
}
 
void Tendril::update() {
  this->vel += this->acc;

  // Limit to maxspeed
  if (math::norm_2(this->vel) > this->maxspeed)
    this->vel /= math::norm_2(this->vel) * this->maxspeed;

  this->loc += this->vel;

  // Reset acceleration to 0 on each cycle
  this->acc = Vector2(0,0);
}

Vector2 Tendril::disperse() {
  Vector2 d(0.0,0.0);
  float cdist = math::norm_2(this->loc - this->tcenter);
  if (cdist < 40) {
    d = this->loc - this->tcenter;
    if (math::norm_2(d) != 0.0)  // avoid NaN
      d /= math::norm_2(d);      // normalize
  }
  return d;
}

Vector2 Tendril::wander() {
  Vector2 w(pe_random().uniform(-0.1,0.1), pe_random().uniform(-0.1,0.1));
  if (math::norm_2(w) != 0.0)   // avoid NaN
    w /= math::norm_2(w);       // normalize
  return w;
}

Vector2 Tendril::attract() {

  Vector2 d(0,0);
  
  // Check to see if we are the only hyphae.  If so, we return zero
  // acceleration (i.e. no attraction)
  if (this->m_closest_hyphae) {
    d = (this->m_closest_hyphae)->center - this->loc;
    float dist = math::norm_2(d);

    // Check to see if we connected to another hyphae center
    if ((dist < 5) && (dist > 0))
      this->connected = true;

    // Normalize
    if (math::norm_2(d) != 0.0) // avoid NaN
      d /= math::norm_2(d);
  }   
  return d;
}

Vector2 Tendril::stick() {
  Vector2 d(0,0);
        
  // Make sure there is a closest tendril we are tracking
  if (this->m_closest_tendril) {
    float distl = math::norm_2(this->loc - (this->m_closest_tendril)->loc);
    if (distl < 3 and distl > 0)   // Check for connection
      this->connected = true;

    if (distl < 31)
      this->separateFactor = 0;

    if (distl < 50) {               // If the other tendril is close, zoom towards it.
      d = (this->m_closest_tendril)->loc - this->loc;
      if (math::norm_2(d) != 0.0)   // avoid NaN
        d /= math::norm_2(d);      // normalize
    }
  }

  return d;
}

void Tendril::branch() {
  float k = math::norm_2(this->loc - this->tcenter);
  float r = pe_random().uniform(0,(100.0/(k+0.5)));
  if ((r <= 0.2) && (this->parent->num_generated_tendrils < 50))
    this->parent->add_tendril( this->loc, this->tcenter, 1.0);
}

// ----------------------------------------------------------------------
//                              HYPHAE
// ----------------------------------------------------------------------

Hyphae::Hyphae(float x, float y) {
  center = Vector2(x,y);
  m_next_id = 0;
  num_generated_tendrils = 0;
  
  for (int i = 0; i < pe_random().uniform_int(5,30); ++i) {
    this->add_tendril(center, center, pe_random().uniform(1.2, 2.0));
  }
}

void Hyphae::render(hyphae_list_t hypha) {
  // Draw the shape.
  glLoadIdentity();
  glEnable(GL_BLEND);
  glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
  glColor4f(0.0, 0.8, 0.2, 1.0);
  
  // Draw the dots at the vertices
  glPointSize(10.0);
  glBegin(GL_POINTS);
  glVertex2f(center[0]*PIXEL_SCALE_FACTOR, center[1]*PIXEL_SCALE_FACTOR);
  glEnd();
  
  tendril_list_t::iterator t = tendrils.begin();
  while (t != tendrils.end()) {
    tendril_list_t::iterator current_tendril = t;
    ++t;
    
    // Remove connected tendrils
    if ((*current_tendril)->connected)
      tendrils.erase(current_tendril);
    else
      (*current_tendril)->render(hypha);
  }
}

void Hyphae::add_tendril(Vector2 loc, Vector2 center, float radius) {
  boost::shared_ptr<Tendril> t( new Tendril(this, m_next_id, loc, center, radius) );
  tendrils.push_back( t );
  m_next_id++;
  num_generated_tendrils++;
}

// ----------------------------------------------------------------------
//                              MYCELIUM
// ----------------------------------------------------------------------

void Mycelium::spawn(float x, float y) {
  boost::shared_ptr<Hyphae> h( new Hyphae(x,y) );
  m_hypha.push_back( h );
}

void Mycelium::render() {
  hyphae_list_t::iterator h = m_hypha.begin();
  while (h != m_hypha.end()) {
    (*h)->render(m_hypha);
    ++h;
  }
}


