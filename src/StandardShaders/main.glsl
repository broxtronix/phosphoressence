// Top level uniform variables
uniform sampler2D feedback_texture;                             
uniform float framebuffer_width;
uniform float framebuffer_height;
uniform float gain;
uniform float invert;
uniform float gamma;

uniform float width;
uniform float D_g;
uniform float D_b;
uniform float s;
uniform float beta;
uniform float rd_blur;

vec4 laplace_4() {
  vec4 laplacian = vec4(-4.0,-4.0,-4.0,1.0) * texture2D(feedback_texture, gl_TexCoord[0].st);
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(-width/framebuffer_width,0.0) );
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2( width/framebuffer_width,0.0) );
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(0.0,-width/framebuffer_height) );
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(0.0, width/framebuffer_height) );
  return laplacian;
}

vec4 laplace_8() {
  vec4 laplacian = vec4(-8.0,-8.0,-8.0,1.0) * texture2D(feedback_texture, gl_TexCoord[0].st);
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(-width/framebuffer_width, -width/framebuffer_height) );
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(-width/framebuffer_width, 0.0) );
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(-width/framebuffer_width, width/framebuffer_height) );
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2( 0.0                    , -width/framebuffer_height) );
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2( 0.0                    , width/framebuffer_height) );
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2( width/framebuffer_width, -width/framebuffer_height) );
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2( width/framebuffer_width, 0.0) );
  laplacian += texture2D(feedback_texture, gl_TexCoord[0].st + vec2( width/framebuffer_width, width/framebuffer_height) );
  return laplacian;
}

vec4 myblur(float kernel_size) {
  vec4 total;
  float N = floor(kernel_size+1.0)*floor(kernel_size+1.0);
  for (float j= -kernel_size/2.0; j <= kernel_size/2.0; j += 1.0 ) {
    for (float i=-kernel_size/2.0; i <= kernel_size/2.0; i += 1.0) {
      total += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(i/framebuffer_width,j/framebuffer_height) );
    }
  }
  vec4 result = total / vec4(N,N,N,N);
  result.a = 1.0;
  return result;
}

void main() { 
  //  gl_FragColor = texture2D(feedback_texture, gl_TexCoord[0].st);

  // Compute the source texture coordinates
  vec2 texture_coords = gl_TexCoord[0].st;                               // Ranges from [0..1, 0..1]
  vec2 normalized_coords = vec2((texture_coords.x-0.5)*2.0,
                                (texture_coords.y-0.5)*2.0);             // Ranges from [-1..1, -1..1]
  float x = normalized_coords.x;
  float y = -normalized_coords.y * framebuffer_width / framebuffer_height;
  float r = sqrt(x*x+y*y);
  float theta = atan(x,y)-3.14159;
  float phi = atan(y,x);

  // Linear
  //  vec2 remapped_coords = vec2(x,y);

  // 1. Sinusoidal
  //  vec2 remapped_coords = vec2(sin(x),sin(y));

  // 2. Spherical
  //   vec2 remapped_coords = vec2(1.0/(r*r)*x,
  //                               1.0/(r*r)*y);

  // 3. Swirl (variation 3)
  // vec2 remapped_coords = vec2(x*sin(r*r)-y*cos(r*r),
  //                             x*cos(r*r)+y*sin(r*r));

  // 4. Horsehoe 
  // vec2 remapped_coords = vec2(1.0/r * (x-y)*(x+y), 
  //                             1.0/r * 2.0*x*y);

  //  5. Polar (*)
  //  vec2 remapped_coords = vec2(theta/3.14159, r-1.0);

  // 6. Handkerchief
  // vec2 remapped_coords = vec2(r*sin(theta+r), 
  //                             r*cos(theta-r));

  // 7. Heart (*)
  // vec2 remapped_coords = vec2(r*sin(theta*r), 
  //                             -r*cos(theta*r));

  // 8. Disc
  // vec2 remapped_coords = vec2(theta/3.14159*sin(theta*r), 
  //                             theta/3.14159*cos(theta*r));

  // Test
  vec2 remapped_coords = vec2(theta, y);
  
  




  vec2 unnormalized_coords = vec2(remapped_coords.x / 2.0 + 0.5, remapped_coords.y / 2.0 + 0.5);

  // Extract the old and new texel
  vec4 dest = texture2D(feedback_texture, texture_coords);
  vec4 src = texture2D(feedback_texture, unnormalized_coords);

  // Apply invert
  if (invert == 1.0) {
    src.r = src.r * -1.0 + 1.0;
    src.g = src.g * -1.0 + 1.0;
    src.b = src.b * -1.0 + 1.0;
  }

  // Apply Gamma
  src.r = pow(src.r, gamma);
  src.g = pow(src.g, gamma);
  src.b = pow(src.b, gamma);

  // Apply gain
  vec4 g = vec4(gain, gain, gain, 1.0);
  vec4 final_texel = g * src;

  // final_texel.r = ((final_texel.r + dest.r)+0.001) / 2.0;
  // final_texel.g = ((final_texel.g + dest.g)+0.001) / 2.0;
  // final_texel.b = ((final_texel.b + dest.b)+0.001) / 2.0;

  // final_texel.r = log(1.0+final_texel.r);
  // final_texel.g = log(1.0+final_texel.g);
  // final_texel.b = log(1.0+final_texel.b);
  // final_texel.a = 1.0;
  // if (final_texel.r > 10.0) {
  //   final_texel.r = 1.0;
  //   final_texel.g = 0.0;
  // } else {
  //   final_texel.r = 0.0;
  //   final_texel.g = 1.0;
  // }
  // final_texel.b = 0.0;

  // NaNs are the bane of our existence here!  We replace them with
  // null values.
  if (final_texel.r != final_texel.r ||
      final_texel.g != final_texel.g ||
      final_texel.b != final_texel.b ||
      final_texel.a != final_texel.a)
    final_texel = vec4(1.0,0,0,0);

  // Return the final value
  gl_FragColor = final_texel;

  




  // Current center texture
    //  vec4 f = texture2D(feedback_texture, gl_TexCoord[0].st);

  // float laplacian_g = -4.0 * texture2D(feedback_texture, gl_TexCoord[0].st).g;
  // laplacian_g += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(-width/framebuffer_width,0.0) ).g;
  // laplacian_g += texture2D(feedback_texture, gl_TexCoord[0].st + vec2( width/framebuffer_width,0.0) ).g;
  // laplacian_g += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(0.0,-width/framebuffer_height) ).g;
  // laplacian_g += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(0.0, width/framebuffer_height) ).g;

  // float laplacian_b = -4.0 * texture2D(feedback_texture, gl_TexCoord[0].st).b;
  // laplacian_b += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(-width/framebuffer_width,0.0) ).b;
  // laplacian_b += texture2D(feedback_texture, gl_TexCoord[0].st + vec2( width/framebuffer_width,0.0) ).b;
  // laplacian_b += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(0.0,-width/framebuffer_height) ).b;
  // laplacian_b += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(0.0, width/framebuffer_height) ).b;

  // gl_FragColor = f;
  // vec4 l8 = laplace_8();
  // gl_FragColor.r -= s * (f.r * f.b) + D_g * l8.r;
  // gl_FragColor.g -= s * (16.0 - f.g * f.b) + D_g * l8.g;
  // gl_FragColor.b -= s * (f.g * f.b - f.b - beta) + D_b * l8.b;
  // gl_FragColor -= D_g * laplace_8();
  // gl_FragColor.a = 1.0;

  // gl_FragColor.a = 1.0;
  //  texture2D(test, gl_TexCoord[0].st) = g * blur(5.0);
  //  gl_FragColor = g * blur(5.0);
}
