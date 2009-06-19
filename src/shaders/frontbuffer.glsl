// Top level uniform variables
uniform sampler2D backbuffer_texture;                             
uniform float framebuffer_radius;
uniform float gamma;
uniform float time;

#define EPS 0.00001
#define PI 3.14159


vec4 blur(float kernel_size) {
  vec4 total;
  float N = floor(kernel_size+1.0)*floor(kernel_size+1.0);
  for (float i= -kernel_size/2.0; i <= kernel_size/2.0; i += 1.0 ) {
    for (float j= -kernel_size/2.0; j <= kernel_size/2.0; j += 1.0 ) {
      total += texture2D(backbuffer_texture, gl_TexCoord[0].st + vec2(i/framebuffer_radius,
                                                                      j/framebuffer_radius));
    }
  }
  vec4 result = total / vec4(N,N,N,N);
  result.a = 1.0;
  return result;
}

void main() { 

  // For debugging.  Uncomment to disable the rest of the shader.
  //vec4 src = blur(2.0);
  vec4 src = texture2D(backbuffer_texture, gl_TexCoord[0].st);

  // Map the colors
  vec4 final_texel = src;
    
  // Apply Gamma
  final_texel.r = pow(final_texel.r, gamma);
  final_texel.g = pow(final_texel.g, gamma);
  final_texel.b = pow(final_texel.b, gamma);
  gl_FragColor = final_texel;
}
