// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file Fluids.h
///
/// Fluid simulation code.  Taken pretty much verbatim from Jos Stam's
/// paper entitled: "Real-Time Fluid Dynamics Simulations for Games."
///
#ifndef __PE_SIMULATION_FLUID_H__
#define __PE_SIMULATION_FLUID_H__

#include <boost/shared_array.hpp>
#include <pe/Math/Vector.h>

namespace pe {
namespace simulation {

  class FluidSimulation {

    // Physical parameters
    float m_fluid_viscosity;
    float m_fluid_diffusion;
    float m_framebuffer_radius;

    // Internal Parameters
    int m_fluid_dimension;
    int m_fluid_size;

    boost::shared_array<float> m_fluid_u, m_fluid_v;
    boost::shared_array<float> m_fluid_u_prev, m_fluid_v_prev; 
    boost::shared_array<float> m_fluid_density, m_fluid_density_prev;
    float m_fluid_previous_time;  
  
    // Private methods
    void set_bnd ( int N, int b, float * x );
    void add_source ( int N, float * x, float * s, float dt );
    void diffuse ( int N, int b, float * x, float * x0, float diff, float dt );
    void advect ( int N, int b, float * d, float * d0, float * u, float * v, float dt );
    void project ( int N, float * u, float * v, float * p, float * div );
    void dens_step ( int N, float * x, float * x0, float * u, float * v, float diff, float dt );
    void vel_step ( int N, float * u, float * v, float * u0, float * v0, float visc, float dt );

    inline int IX(int i,int j) const { return (i)+(m_fluid_dimension+2)*(j); }
    inline void SWAP(float* &x0,float* &x) { float *tmp=x0; x0=x; x=tmp; }


  public:

    FluidSimulation(int width, int height, float viscosity = 0.0005, float diffusion = 1.0);

    // Run the simulation forward one time step.
    void update();

    void add_velocity(int i, int j, Vector2 vel);
    void add_velocity_worldcoords(float x, float y, pe::Vector2 vel);
    Vector2 get_velocity(int i, int j) const;

    // Read the current values of physical constants.
    float viscosity() const { return m_fluid_viscosity; }
    float diffusion() const { return m_fluid_diffusion; }

    // Set the current values of physical constants.
    void set_viscosity(float v) { m_fluid_viscosity = v; }
    void set_diffusion(float d) { m_fluid_diffusion = d; }

    void set_framebuffer_radius(float radius) { m_framebuffer_radius = radius; }
  };

}} // namespace pe::simulation

#endif // __PE_SIMULATION_FLUID_H__
