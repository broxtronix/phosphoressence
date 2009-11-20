#include <cuda.h>
#include <cuda_gl_interop.h>
#include <iostream>

/* --------------------------- target code ------------------------------*/  

// cudaArray* array;
// texture<float,2,cudaReadModeNormalizedFloat> texRef;
 
__global__ void copy_image_impl (uint8_t* in_data, int width, int height) 
{ 
  //  cudaBindTextureToArray(texRef, array);

  int i = blockIdx.x * blockDim.x + threadIdx.x;
  int j = blockIdx.y * blockDim.y + threadIdx.y;

  if (i < width && j < height) {
    int base_index = 4 * (j * width + i);
    // out_data[base_index] = in_data[base_index];
    // out_data[base_index+1] = in_data[base_index+1];
    // out_data[base_index+2] = in_data[base_index+2];
    // out_data[base_index+3] = in_data[base_index+3];
    in_data[base_index] = 0;//in_data[base_index];
    in_data[base_index+1] = 0;
    in_data[base_index+2] = in_data[base_index+2];
    in_data[base_index+3] = 255;
  }
} 
 
/* --------------------------- host code ------------------------------*/ 

void copy_image (int pbo_in, int width, int height) {

  uint8_t* in_data;
  cudaGLMapBufferObject( (void**)&in_data, pbo_in );

  // cudaChannelFormatDesc channelDesc = cudaCreateChannelDesc(8, 8, 8, 8, cudaChannelFormatKindUnsigned);
  // cudaGLMapBufferObject( (void**)&array, pbo_in );
  // cudaBindTextureToArray(texRef, array, channelDesc);

  std::cout << "grid size: " << width << "  " << height << "\n";
  dim3 block(16,16);
  dim3 grid((width + block.x - 1)  / block.x,
            (height + block.y - 1) / block.y);
  std::cout << "grid size: " << grid.x << "  " << grid.y << "\n";
  copy_image_impl<<<grid,block>>>(in_data, width, height); 
  
  cudaGLUnmapBufferObject( pbo_in );
} 

void pboRegister(int pbo) {
  // register this buffer object with CUDA
  cudaGLRegisterBufferObject(pbo);
}
void pboUnregister(int pbo) {
  // unregister this buffer object with CUDA
  cudaGLUnregisterBufferObject(pbo);
}
