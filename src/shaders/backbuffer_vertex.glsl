uniform float time;
uniform float warp;
uniform float warp_scale;
uniform float warp_speed;
uniform float sx;
uniform float sy;
uniform float cx;
uniform float cy;

void main() {

  //  vec4 pos = gl_ModelViewProjectionMatrix * gl_Vertex;

//   // Apply the Milkdrop warp effect (most of these constants were
//   // adapted from the milkdrop source code)
//   float warp_time = time * warp_speed;
//   float warp_scale_inv = 1.0 / warp_scale;

//   float f[4];
//   f[0] = 11.68f + 4.0f*cos(warp_time*1.413f + 10);
//   f[1] =  8.77f + 3.0f*cos(warp_time*1.113f + 7);
//   f[2] = 10.54f + 3.0f*cos(warp_time*1.233f + 3);
//   f[3] = 11.49f + 4.0f*cos(warp_time*0.933f + 5);


//   // Apply the scaling effect
//   u = (u - cx)/sx + cx;
//   v = (v - cy)/sy + cy;

//   u += warpAmount * 0.0035f * sin(warp_time * 0.333f + warp_scale_inv*(initial_pos.u * f[0] - initial_pos.v * f[3]));
//   v += warpAmount * 0.0035f * cos(warp_time * 0.375f - warp_scale_inv*(initial_pos.u * f[2] + initial_pos.v * f[1]));
//   u += warpAmount * 0.0035f * cos(warp_time * 0.753f - warp_scale_inv*(initial_pos.u * f[1] - initial_pos.v * f[2]));
//   v += warpAmount * 0.0035f * sin(warp_time * 0.825f + warp_scale_inv*(initial_pos.u * f[0] + initial_pos.v * f[3]));

  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
