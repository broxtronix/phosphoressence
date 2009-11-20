// Top level uniform variables
uniform sampler2D backbuffer_texture;                             
uniform float framebuffer_radius;
uniform float gamma;
uniform float invert;
uniform float brighten;
uniform float darken;
uniform float solarize;
uniform float edge_filter;
uniform float time;

#define EPS 0.00001
#define PI 3.14159

/// RGB->HSV conversion
vec4 rgb_to_hsv(in vec4 rgb) {
  float hue;
  float saturation;
  float luminance;
  
  if( rgb.r==rgb.g && rgb.r==rgb.b ) {                 // S = 0
    hue = 0.0;
    saturation = 0.0;
    luminance = rgb.r;
  } else if( rgb.r<=rgb.g && rgb.r<=rgb.b ) {          // H=[1/3,2/3)
    luminance = max(rgb.g,rgb.b);
    hue = (3.0 - (rgb.g-rgb.b)/(luminance-rgb.r))/6.0;
    saturation = (luminance-rgb.r)/(luminance+EPS);
  } else if( rgb.g <= rgb.r && rgb.g < rgb.b ) {       // H=[2/3,1)
    luminance = max(rgb.r,rgb.b);
    hue = (5.0 - (rgb.b-rgb.r)/(luminance-rgb.g))/6.0;
    saturation = (luminance-rgb.g)/(luminance+EPS);
  } else {                                             // H=[0,1/3)
    luminance = max(rgb.r,rgb.g);
    hue = (1.0 - (rgb.r-rgb.g)/(luminance-rgb.b))/6.0;
    saturation = (luminance-rgb.b)/(luminance+EPS);
  }
  return vec4(hue, saturation, luminance, rgb.a);
}

/// HSV->RGB conversion
vec4 hsv_to_rgb(in vec4 hsv) {
  float h = hsv.r;
  float s = hsv.g;
  float v = hsv.b;

  int i = int(floor(6.0*h));
  float f = 6.0*h - float(i);

  float p = v * (1.0 - s);
  float q = v * (1.0 - s*f);
  float t = v * (1.0 - (1.0-f) * s);

  float r,g,b;
  if (i==1) {
    r=q; g=v; b=p; 
  } else if (i==2) {
    r=p; g=v; b=t; 
  } else if (i==3) {
    r=p; g=q; b=v; 
  } else if (i==4) {
    r=t; g=p; b=v;
  } else if (i==5) {
    r=v; g=p; b=q; 
  } else {  // i == 0 || i == 6
    r=v; g=t; b=p; 
  }
  return vec4(r,g,b,hsv.a);
}

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
  vec4 ones = vec4(1.0, 1.0, 1.0, 1.0);
  vec4 neg_ones = vec4(-1.0, -1.0, -1.0, -1.0);

  // For debugging.  Uncomment to disable the rest of the shader.
  //vec4 src = blur(2.0);
  vec4 src = texture2D(backbuffer_texture, gl_TexCoord[0].st);

  // Apply edge filter
  if (edge_filter == 1.0) {
    vec4 src1 = texture2D(backbuffer_texture, gl_TexCoord[0].st + vec2(1.0/framebuffer_radius,
                                                                       0.0/framebuffer_radius));
    vec4 src2 = texture2D(backbuffer_texture, gl_TexCoord[0].st + vec2(0.0/framebuffer_radius,
                                                                       1.0/framebuffer_radius));
    vec4 x_deriv = src - src1;
    vec4 y_deriv = src2 - src;
    src = sqrt(x_deriv * x_deriv + y_deriv * y_deriv);
    src.a = 1.0;
  }

  // Map the colors
  vec4 final_texel = src;

  // Apply Gamma
  final_texel.r = pow(final_texel.r, 1.0/gamma);
  final_texel.g = pow(final_texel.g, 1.0/gamma);
  final_texel.b = pow(final_texel.b, 1.0/gamma);

  // Apply invert
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
  if (solarize == 1.0) {
    final_texel = final_texel - (final_texel * neg_ones + ones);
    final_texel.a = 1.0;
  }
    
  gl_FragColor = final_texel;
}
