// Top level uniform variables
uniform sampler2D backbuffer_texture;                             
uniform float framebuffer_radius;
uniform float gamma;
uniform float invert;
uniform float brighten;
uniform float darken;
uniform float solarize;
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
  final_texel.r = pow(final_texel.r, 1.0/gamma);
  final_texel.g = pow(final_texel.g, 1.0/gamma);
  final_texel.b = pow(final_texel.b, 1.0/gamma);

  // Apply invert
  vec4 ones = vec4(1.0, 1.0, 1.0, 1.0);
  vec4 neg_ones = vec4(-1.0, -1.0, -1.0, -1.0);
  // if (invert == 1.0) 
  //   final_texel = final_texel * neg_ones + ones;

  // Brighten
  if (brighten == 1.0) 
    final_texel = sqrt(final_texel); 

  // Darken
  if (darken == 1.0) {
    vec4 e = vec4(2.0,2.0,2.0,1.0);
    final_texel = pow(final_texel,e);
  }

  // Solarize
  if (solarize == 1.0) 
    final_texel = final_texel - (final_texel * neg_ones + ones);
  final_texel.a = 1.0;
    
  gl_FragColor = final_texel;
}
