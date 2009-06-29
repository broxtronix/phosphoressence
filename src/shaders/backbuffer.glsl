// Top level uniform variables
uniform sampler2D feedback_texture;                             
uniform float framebuffer_radius;
uniform float decay;
uniform float ifs_mode;
uniform float edge_extend;
uniform float kaleidoscope;
uniform float kaleidoscope_radius;

// Video Echo
uniform float echo_zoom;
uniform float echo_alpha;
uniform float echo_orient;

uniform float zoom;
uniform float zoomexp;
uniform float rot;
uniform float dx;
uniform float dy;

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

// Multiply two complex number together
vec2 cmult(in vec2 a, in vec2 b) {
  return vec2(a.x*b.x-a.y*b.y,  // Real Part
              a.x*b.y+a.y*b.x); // Complex Part
}

vec2 cmult_polar(in vec2 a, in vec2 b) {
  return vec2(a.x*b.x, a.y+b.y);
}

// Divide two complex numbers
vec2 cdiv(in vec2 a, in vec2 b) {
  float numerator = b.x*b.x+b.y*b.y;
  return vec2((a.x*b.x+a.y*b.y) / numerator,  // Real Part
              (a.y*b.x-a.x*b.y) / numerator); // Complex Part
}

vec2 cdiv_polar(in vec2 a, in vec2 b) {
  return vec2(a.x/b.x, a.y-b.y);
}

vec2 polar_to_cartesian(in vec2 a) {
  return vec2(a.x * cos(a.y), a.x * sin(a.y));
}

vec2 mobius_transform(in vec2 z, in vec2 a, in vec2 b, in vec2 c) {
  float z_exp = pow(a.x, -1.0 * pow(zoomexp, 
                                    z.x * 2.0 * framebuffer_radius - framebuffer_radius));

  vec2 aa = vec2(z_exp, a.y);
  vec2 numerator = polar_to_cartesian(cmult_polar(aa,z)) + b;

  // Disabling the d parameter.  Seems to me that it's redundant with
  // the a parameter?
  // 
  //   vec2 denominator =  polar_to_cartesian(cmult_polar(c,z)) + d;

  vec2 denominator = polar_to_cartesian(cmult_polar(c,z)) + vec2(1.0,0.0);
  return cdiv(numerator,denominator);
}

void main() { 

  // For debugging.  Uncomment to disable the rest of the shader.
  //
  // gl_FragColor = texture2D(feedback_texture, gl_TexCoord[0].st);
  // return;

  // Compute the source texture coordinates
  //
  // gl_TexCoord ranges from [0..1, 0..1]
  // normalized coordinates range from [-1..1, -1..1] * framebuffer_radius
  float x = (gl_TexCoord[0].x-0.5) * 2.0 * framebuffer_radius;
  float y = (gl_TexCoord[0].y-0.5) * 2.0 * framebuffer_radius;
  float r = sqrt(x*x+y*y);
  float r_sqr = r*r;
  float theta = atan(y,x);
  float phi = atan(x,y);
  
  // Linear
  vec2 remapped_coords = vec2(x,y);

  if (ifs_mode == 1.0) {

    // 1. Sinusoidal
    remapped_coords = vec2(sin(x),
                           sin(y));

  } else if (ifs_mode == 2.0) {

    // 2. Spherical
     remapped_coords = vec2(x/(0.26*r_sqr),
                            y/(0.26*r_sqr));

  } else if (ifs_mode == 3.0) {

    // 3. Swirl (variation 3)
    remapped_coords = vec2(x*sin(r_sqr)-y*cos(r_sqr),
                           x*cos(r_sqr)+y*sin(r_sqr));

  } else if (ifs_mode == 4.0) {

    // 4. Horsehoe 
    remapped_coords = vec2(1.0/r * (x-y)*(x+y), 
                           1.0/r * 2.0*x*y);
    
  } 

  // Mobius Transform
  float xx = remapped_coords.x;
  float yy = remapped_coords.y;
  float rr = sqrt(xx*xx+yy*yy);
  float theta2 = atan(yy,xx);
  
  remapped_coords = mobius_transform(vec2(rr,theta2), 
                                     vec2(zoom,rot), // polar      : zoom & rotation
                                     vec2(dx,dy),    // cartesian  : x & y translation 
                                     vec2(0,0));     // polar      : rotation & orientation of 3D sphere

  // Kaleidoscope mode
  if (kaleidoscope == 1.0) {

    vec2 p = vec2(remapped_coords.x, remapped_coords.y-kaleidoscope_radius);

    // Top right mirror
    if (1.7320 * p.x + p.y > 0.0) {
      mat2 m = mat2(-0.5, -0.866025, -0.866025, 0.5);
      remapped_coords = m*p;
      remapped_coords.y += kaleidoscope_radius;
    }

    // Top left mirror
    if (-1.7320 * p.x + p.y > 0.0) {
      mat2 m = mat2(-0.5, 0.866025, 0.866025, 0.5);
      remapped_coords = m*p;
      remapped_coords.y += kaleidoscope_radius;
    }

    // Bottom mirror
    float bottom = -kaleidoscope_radius / 2.0;
    if (remapped_coords.y < bottom)
      remapped_coords.y = -(remapped_coords.y-bottom)+bottom;
  }

  // Remap the coordinates back into texture coordinate space: [0.0,1.0]
  vec2 unnormalized_coords = vec2(remapped_coords.x / 
                                  (2.0*framebuffer_radius) + 0.5, 
                                  remapped_coords.y / 
                                  (2.0*framebuffer_radius) + 0.5);

  // Texture Flip
  // float xmodval = mod(unnormalized_coords.x,2.0);
  // float ymodval = mod(unnormalized_coords.x,2.0);
  // if (xmodval > 1.0)
  //   unnormalized_coords.x = 2.0 - xmodval;
  // if (ymodval > 1.0)
  //   unnormalized_coords.y = 2.0 - ymodval;

  // Texture Wrap
  if (edge_extend == 1.0) {
    unnormalized_coords.x = mod(unnormalized_coords.x,1.0);
    unnormalized_coords.y = mod(unnormalized_coords.y,1.0);
  } else {
    unnormalized_coords.x = clamp(unnormalized_coords.x,0.0,1.0);
    unnormalized_coords.y = clamp(unnormalized_coords.y,0.0,1.0);
  } 
  
  vec4 src = texture2D(feedback_texture, unnormalized_coords);
  
  // Apply gain.  This is done in the HSV color space so that the hue
  // can cycle when the image becomes saturated.
  vec4 g = vec4(decay, decay, decay, 1.0);
  vec4 hsv_texel = g * rgb_to_hsv(src);
  hsv_texel.r = mod(hsv_texel.r,1.0)+0.0004; // Wrap hue
  hsv_texel = clamp(hsv_texel,0.0,1.0);      // Clamp saturation & luminance
  vec4 final_texel = hsv_to_rgb(hsv_texel);

  // NaNs are the bane of our existence here!  We replace them with
  // null values.
  if (final_texel.r != final_texel.r ||
      final_texel.g != final_texel.g ||
      final_texel.b != final_texel.b ||
      final_texel.a != final_texel.a)
    final_texel = vec4(0.0,0.0,0.0,1.0);

  // Video echo
  vec2 prev_coords = gl_TexCoord[0].st;
  vec2 echo_coords = vec2((prev_coords.x-0.5) * echo_zoom + 0.5, 
                          (prev_coords.y-0.5) * echo_zoom + 0.5);
  // if (echo_orient == 1.0 || echo_orient == 3.0)
  //   echo_coords.x *= -1.0;
  // if (echo_orient >= 1.0)
  //   echo_coords.y *= -1.0;
  vec4 src_prev = texture2D(feedback_texture, echo_coords);

  // Return the final value
  gl_FragColor = mix(final_texel, src_prev, echo_alpha);
}
