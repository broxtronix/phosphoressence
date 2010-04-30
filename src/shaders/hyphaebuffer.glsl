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

  gl_FragColor = gain * texture2D(hyphae_texture, gl_TexCoord[0].st);
  return;

}
