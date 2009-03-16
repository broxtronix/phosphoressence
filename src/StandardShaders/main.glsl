uniform sampler2D feedback_texture;                             
uniform float gain;
uniform float invert;
uniform float gamma;
uniform float color_shift;
uniform float framebuffer_width;
uniform float framebuffer_height;

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
  vec4 g = vec4(gain, gain, gain, 1.0);
  vec4 src = texture2D(feedback_texture, gl_TexCoord[0].st);

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

  gl_FragColor = g * src;

  if (invert == 1.0) {
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
}
