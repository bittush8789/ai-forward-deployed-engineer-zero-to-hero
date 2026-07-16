#include <iostream>
#include <cuda_runtime.h>

// CUDA Kernel definition to print thread index mapping
__global__ void verifyIndices() {
    int threadId = threadIdx.x;
    int blockId = blockIdx.x;
    int globalId = blockIdx.x * blockDim.x + threadIdx.x;
    
    printf("Block: %d | Thread: %d | Global Index: %d\n", blockId, threadId, globalId);
}

int main() {
    std::cout << "=== Running CUDA Thread Index Verification Kernel ===" << std::endl;
    
    // Launch kernel with 2 blocks of 4 threads each
    verifyIndices<<<2, 4>>>();
    
    // Wait for GPU threads to complete execution
    cudaDeviceSynchronize();
    
    std::cout << "Kernel execution completed." << std::endl;
    return 0;
}
