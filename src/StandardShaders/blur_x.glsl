uniform sampler2D feedback_texture;                             
uniform float framebuffer_width;
uniform float framebuffer_height;
uniform float blur_amount;

vec4 myblur(float kernel_size) {
  vec4 total;
  float N = floor(kernel_size+1.0)*floor(kernel_size+1.0);
  for (float i= -kernel_size/2.0; i <= kernel_size/2.0; i += 1.0 ) {
    for (float j= -kernel_size/2.0; j <= kernel_size/2.0; j += 1.0 ) {
      total += texture2D(feedback_texture, gl_TexCoord[0].st + vec2(i/framebuffer_width,j/framebuffer_height) );
    }
  }
  vec4 result = total / vec4(N,N,N,N);
  result.a = 1.0;
  return result;
}

void main() { 
  gl_FragColor = myblur(blur_amount*2.0);
}
