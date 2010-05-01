// Top level uniform variables
uniform sampler2D ground_texture;
uniform sampler2D feedback_texture;
uniform float aspect_ratio;
uniform float framebuffer_radius;

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


// -------------------------------------------------------------------
//                              MAIN
// -------------------------------------------------------------------

void main() { 

  // First we must compute the location to sample from in the feedback
  // texture.  The feedback texture is [2 * m_framebuffer_radius x 2 *
  // m_framebuffer_radius ] pixels in size, whereas the ground image
  // is only [ 2 * m_aspect x 2 ] in size.
  vec4 ground_sample_loc = gl_TexCoord[0];
  vec4 feedback_sample_loc = gl_TexCoord[1];
  feedback_sample_loc.t = (feedback_sample_loc.t + 0.3) / aspect_ratio;
  feedback_sample_loc.s *= aspect_ratio / framebuffer_radius;
  feedback_sample_loc.t *= aspect_ratio / framebuffer_radius;
  feedback_sample_loc.s += 0.076; // FIXME: How do I compute these numbers?
  feedback_sample_loc.t += 0.076;

  // Perform a simple fade-out
  vec4 ground_texel = texture2D(ground_texture, ground_sample_loc.st);
  vec4 feedback_texel = texture2D(feedback_texture, feedback_sample_loc.st);
  vec4 hsv_ground_texel = rgb_to_hsv(ground_texel);
  vec4 hsv_feedback_texel = rgb_to_hsv(feedback_texel);
  hsv_ground_texel.g *= (0.3 + (hsv_feedback_texel.b*0.7));  // mute the saturation
  gl_FragColor = hsv_to_rgb(hsv_ground_texel);
}
