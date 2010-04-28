// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <pe/core/Time.h>
#include <pe/Core/Exception.h>
#include <pe/Core/FundamentalTypes.h>
#include <pe/simulation/FluidDynamics.h>

#include <string>
#include <iostream>

using namespace pe;

// -------------------------------------------------------------------

void print_hasnan(int N, std::string variable, float *x) {
  bool hasNaN = false;

  int i, size=(N+2)*(N+2); 
  for ( i=0 ; i<size ; i++ ) {
    if (x[i] != x[i])
      hasNaN = true;
  }
  
  if (hasNaN)
    std::cout << "The " << variable << " variable has NaNs!\n";
  else
    std::cout << "The " << variable << " variable is all clear!\n";

}

void print_stats(std::string variable, float *x, int fluid_size) {
  
  float lo = pe::ScalarTypeLimits<float>::highest(), hi = pe::ScalarTypeLimits<float>::lowest();
  float avg_sum = 0;
  
  for (int j = 1; j <= fluid_size; ++j) {
    for (int i = 1; i <= fluid_size; ++i) {
      avg_sum += x[i];
      if (x[i] < lo) lo = x[i];
      if (x[i] > hi) hi = x[i];
    }
  }
  std::cout << "[" << variable << "] - Mean: " << (avg_sum / fluid_size) 
            << "  Min: " << lo <<  "  Max: " << hi << "\n"; 
}

// --------------------------------------------------------------------

void pe::simulation::FluidSimulation::set_bnd ( int N, int b, float * x ) {
  
  for ( int i=1 ; i<=N ; ++i ) { 
    x[IX(0  ,i)] = b==1 ? -x[IX(1,i)] : x[IX(1,i)];
    x[IX(N+1,i)] = b==1 ? -x[IX(N,i)] : x[IX(N,i)];
    x[IX(i  ,0)] = b==2 ? -x[IX(i,1)] : x[IX(i,1)];
    x[IX(i,N+1)] = b==2 ? -x[IX(i,N)] : x[IX(i,N)];
  }
  x[IX(0,  0  )] = 0.5*(x[IX(1,0 )]+x[IX(0 ,1)]);
  x[IX(0,  N+1)] = 0.5*(x[IX(1,N+1)]+x[IX(0,N)]); 
  x[IX(N+1,0  )] = 0.5*(x[IX(N,0 )]+x[IX(N+1,1)]); 
  x[IX(N+1,N+1)] = 0.5*(x[IX(N,N+1)]+x[IX(N+1,N)]);
}


void pe::simulation::FluidSimulation::add_source ( int N, float * x, float * s, float dt ) {
  int i, size=(N+2)*(N+2); 
  for ( i=0 ; i<size ; i++ ) {
    x[i] += dt*s[i];
  }
}


void pe::simulation::FluidSimulation::diffuse ( int N, int b, float * x, 
                                           float * x0, float diff, float dt ) {
  float a=dt*diff*N*N;

  for ( int k=0 ; k<20 ; k++ ) { 
    for ( int i=1 ; i<=N ; i++ ) {
      for ( int j=1 ; j<=N ; j++ ) {
        //        float x_prev = x[IX(i,j)];
        x[IX(i,j)] = (x0[IX(i,j)] + a*(x[IX(i-1,j)]+x[IX(i+1,j)] + 
                                       x[IX(i,j-1)]+x[IX(i,j+1)]))/(1+4*a);
        // if (x[IX(i,j)] != x[IX(i,j)]) {
        //   std::cout << "processing (" << i << " " << j << ")...\n";
        //   std::cout << "diffuse (" << x_prev << "  " << x0[IX(i,j)] << "...\n";
        // }

      }
    }
    set_bnd ( N, b, x );
  }
}


void pe::simulation::FluidSimulation::advect ( int N, int b, float * d, 
                                          float * d0, float * u, float * v, float dt ) {
  int i0, i1, j0, j1;
  float x, y, s0, t0, s1, t1;

  //  std::cout << "Call to advect...\n";

  float dt0 = dt*N; 
  for ( int j=1 ; j<=N ; j++ ) {
    for ( int i=1 ; i<=N ; i++ ) {
      x = i-dt0*u[IX(i,j)]; 
      y = j-dt0*v[IX(i,j)]; 

      if (x<0.5) x=0.5; if (x>N+0.5) x=N+0.5; 
      i0=(int)x; i1=i0+1; 

      if (y<0.5) y=0.5; if (y>N+0.5) y=N+0.5; 
      j0=(int)y; j1=j0+1; 
      
      s1 = x-i0; s0 = 1-s1; 
      t1 = y-j0; t0 = 1-t1; 

      PE_ASSERT(i0 >=0 || i0 <= N+1, LogicErr() << "Out of bounds memory access: i0 in advect().");
      PE_ASSERT(j0 >=0 || j0 <= N+1, LogicErr() << "Out of bounds memory access: j0 in advect().");
      PE_ASSERT(i1 >=0 || i1 <= N+1, LogicErr() << "Out of bounds memory access: i1 in advect().");
      PE_ASSERT(j1 >=0 || j1 <= N+1, LogicErr() << "Out of bounds memory access: j1 in advect().");

      d[IX(i,j)] = (s0*(t0*d0[IX(i0,j0)]+t1*d0[IX(i0,j1)]) +
                    s1*(t0*d0[IX(i1,j0)]+t1*d0[IX(i1,j1)]));
    } 
  }
  set_bnd ( N, b, d );
}

void pe::simulation::FluidSimulation::project ( int N, float * u, float * v, 
                                           float * p, float * div ) {
  float h = 1.0/N; 
  
  for ( int i=1 ; i<=N ; i++ ) {
    for ( int j=1 ; j<=N ; j++ ) { 
      div[IX(i,j)] = -0.5*h*(u[IX(i+1,j)]-u[IX(i-1,j)]+
                             v[IX(i,j+1)]-v[IX(i,j-1)]);
      p[IX(i,j)] = 0;
    }
  }
  set_bnd ( N, 0, div ); set_bnd ( N, 0, p );

  for ( int k=0 ; k<20 ; k++ ) {
    for ( int i=1 ; i<=N ; i++ ) { 
      for ( int j=1 ; j<=N ; j++ ) {
        p[IX(i,j)] = (div[IX(i,j)]+p[IX(i-1,j)]+p[IX(i+1,j)]+ 
                      p[IX(i,j-1)]+p[IX(i,j+1)])/4;
      }
    }
    set_bnd ( N, 0, p );
  }

  for ( int i=1 ; i<=N ; i++ ) { 
    for ( int j=1 ; j<=N ; j++ ) {
      u[IX(i,j)] -= 0.5*(p[IX(i+1,j)]-p[IX(i-1,j)])/h; 
      v[IX(i,j)] -= 0.5*(p[IX(i,j+1)]-p[IX(i,j-1)])/h;
    }
  }
  set_bnd ( N, 1, u ); set_bnd ( N, 2, v );
}

void pe::simulation::FluidSimulation::dens_step ( int N, float * x, float * x0, 
                                             float * u, float * v, float diff, float dt ) {
  add_source ( N, x, x0, dt ); 
  SWAP ( x0, x ); diffuse ( N, 0, x, x0, diff, dt ); 
  SWAP ( x0, x ); advect ( N, 0, x, x0, u, v, dt );
}

void pe::simulation::FluidSimulation::vel_step ( int N, float * u, float * v, 
                                            float * u0, float * v0, float visc, float dt ) {
  add_source ( N, u, u0, dt ); add_source ( N, v, v0, dt ); 
  SWAP ( u0, u ); diffuse ( N, 1, u, u0, visc, dt ); 
  SWAP ( v0, v ); diffuse ( N, 2, v, v0, visc, dt ); 
  project ( N, u, v, u0, v0 );
  SWAP ( u0, u ); SWAP ( v0, v ); 
  advect ( N, 1, u, u0, u0, v0, dt ); advect ( N, 2, v, v0, u0, v0, dt ); 
  project ( N, u, v, u0, v0 );
}


// --------------------------------------------------------------

pe::simulation::FluidSimulation::FluidSimulation(int width, int height, float viscosity, float diffusion) {

  // First we check to make sure the mesh size and fluid size are the
  // same (and are both square).  If they aren't then wacky things
  // could happen, including a seg fault.  Someday I'll go through the
  // fluid code and add support for non-square meshes, but for now
  // this prevents future Michael from suffering if he forgets this
  // constraint.
  PE_ASSERT(width == height, 
            NoImplErr() << "Fluid mesh size must be square!");

  PE_ASSERT(width > 1,
            NoImplErr() << "Fluid mesh size must be non-zero");

  m_fluid_dimension = width;
  m_fluid_size = (m_fluid_dimension+2)*(m_fluid_dimension+2);

  m_fluid_viscosity = viscosity;
  m_fluid_diffusion = diffusion;
  m_framebuffer_radius = 1.0;

  m_fluid_previous_time = pe::pe_time();
  m_fluid_u.reset(new float[m_fluid_size]);
  m_fluid_v.reset(new float[m_fluid_size]);
  m_fluid_u_prev.reset(new float[m_fluid_size]);
  m_fluid_v_prev.reset(new float[m_fluid_size]);
  m_fluid_density.reset(new float[m_fluid_size]);
  m_fluid_density_prev.reset(new float[m_fluid_size]);

  for (int i=0; i < m_fluid_size; ++i) {
    m_fluid_u[i] = 0.0;
    m_fluid_v[i] = 0.0;
    m_fluid_u_prev[i] = 0.0;
    m_fluid_v_prev[i] = 0.0;
    m_fluid_density[i] = 0.0;
    m_fluid_density_prev[i] = 0.0;
  }
}

void pe::simulation::FluidSimulation::update() {
  float fluid_dt = pe::pe_time() - m_fluid_previous_time;
  m_fluid_previous_time = pe::pe_time();
  vel_step ( m_fluid_dimension, m_fluid_u.get(), m_fluid_v.get(), 
             m_fluid_u_prev.get(), m_fluid_v_prev.get(), m_fluid_viscosity, fluid_dt ); 
  dens_step ( m_fluid_dimension, m_fluid_density.get(), m_fluid_density_prev.get(), 
              m_fluid_u.get(), m_fluid_v.get(), m_fluid_diffusion, fluid_dt ); 
}

void pe::simulation::FluidSimulation::add_velocity(int i, int j, pe::Vector2 vel) {
  if (i >= 0 || i < m_fluid_dimension || j >= 0 || j < m_fluid_dimension) {
    m_fluid_u_prev[IX(i+1,j+1)] += vel[0];
    m_fluid_v_prev[IX(i+1,j+1)] += vel[1];
  }
}

  // Add Velocity in simulation space: [-aspect aspect][-1.0 1.0]
  void pe::simulation::FluidSimulation::add_velocity_worldcoords(float x, float y, 
                                                                 pe::Vector2 vel) {
    int i = m_fluid_dimension * (x + m_framebuffer_radius) / (2.0 * m_framebuffer_radius);
    int j = m_fluid_dimension * (y + m_framebuffer_radius) / (2.0 * m_framebuffer_radius);
    if (i >= 0 || i < m_fluid_dimension || j >= 0 || j < m_fluid_dimension) {
        m_fluid_u_prev[IX(i+1,j+1)] += vel[0];
        m_fluid_v_prev[IX(i+1,j+1)] += vel[1];
      }
}

Vector2 pe::simulation::FluidSimulation::get_velocity(int i, int j) const {
  return Vector2(m_fluid_u[IX(i+1,j+1)], m_fluid_v[IX(i+1,j+1)]);
}
