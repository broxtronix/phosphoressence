// Top level uniform variables
uniform sampler2D backbuffer_texture;                             
uniform float gamma;
uniform float time;

#define EPS 0.00001
#define PI 3.14159


void main() { 

  // For debugging.  Uncomment to disable the rest of the shader.
  vec4 src = texture2D(backbuffer_texture, gl_TexCoord[0].st);

  // Map the colors
  vec4 final_texel;
  // if (src.r > 1.0 || src.g > 1.0 || src.b > 1.0) {
  //   final_texel.r = log(src.r+1.0)/10.0;
  //   final_texel.g = log(src.g+1.0)/10.0;
  //   final_texel.b = log(src.b+1.0)/10.0;
  //   // final_texel.r = sin(log(src.r+EPS))*0.5+0.5;
  //   // final_texel.g = sin(log(src.g+EPS))*0.5+0.5;
  //   // final_texel.b = sin(log(src.b+EPS))*0.5+0.5;
  //   final_texel.a = src.a;
  // } else {
  final_texel = src;
  //    final_texel = vec4(0.0,0.0,1.0,1.0);
    //  }
    
  // Apply Gamma
  final_texel.r = pow(final_texel.r, gamma);
  final_texel.g = pow(final_texel.g, gamma);
  final_texel.b = pow(final_texel.b, gamma);

  // Apply gain
  gl_FragColor = final_texel;
}
