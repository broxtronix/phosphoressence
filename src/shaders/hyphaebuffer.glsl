// Top level uniform variables
uniform sampler2D hyphae_texture;
uniform float framebuffer_radius;
uniform float hyphae_decay;

// -------------------------------------------------------------------
//                              MAIN
// -------------------------------------------------------------------

void main() { 

  // Perform a simple fade-out
  vec4 gain = vec4(hyphae_decay, hyphae_decay, hyphae_decay, hyphae_decay);
  vec4 sample_loc = gl_TexCoord[0];

  // This gives the tendrils a little antialiasing (or "fuzz"), which
  // makes them look nice.
  sample_loc.s = sample_loc.s*1.000001;
  sample_loc.t = sample_loc.t*1.000001;

  gl_FragColor = gain * texture2D(hyphae_texture, sample_loc.st);
  return;

}
