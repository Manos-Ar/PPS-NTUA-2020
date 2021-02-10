# SSH File Sharing

### Local -> Scirouter (Without Proxy)
From the local machine, this command:
- If the directory on the remote machine does not exists:
  - It creates the directory and transfers all its contents.
- If the directory on the remote machine exists:
  - It transfers all its contents in the existing directory.

From the `dmm-skeleton` directory on local to transfer the `dmm-skeleton` directory on remote:
```
rsync -vr --delete --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" . parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/a4/dmm-skeleton
```

### Scirouter -> Local (Without Proxy)
From the local machine, this command:
- If the directory on the local machine does not exists:
  - It creates the directory and transfers all its contents.
- If the directory on the local machine exists:
  - It transfers all its contents in the existing directory.

From the `4rd_exec` directory on local to transfer the `4rd_exec` directory on remote:
```
rsync -vr --rsh "ssh parlab07@orion.cslab.ece.ntua.gr ssh" parlab07@scirouter.cslab.ece.ntua.gr:/home/parallel/parlab07/a4/ .
```

### Rsync Options

```
--delete = to delete everything old to the remote directory
```
### Compile All
```
qsub -q serial -l nodes=dungani:ppn=1 make_dmm.sh
```

### Run All
```
qsub -q serial -l nodes=dungani:ppn=1 run_dmm.sh
```

# Code Guide
## Changes To Be Made
- Only change `cuda` directory.
- Change files:
  - `dmm_gpu.cu`
  - `dmm_main.cu`
- All changes will be made in code segments with **FILL ME** tags

### Changes `dmm_main.cu`
- Optionally increase appropriately the matrix size here if that helps you with your kernel code, e.g., to avoid divergent warps.
- Set up the block and grid depending on the kernel (`THREAD_BLOCK_X, THREAD_BLOCK_Y, TILE_X, TILE_Y`)
- Set up the thread block and grid dimensions
- Execute and time the kernel (for CUBLAS)

### Changes `dmm_gpu.cu`
- `dmm_gpu_naive()`
- `dmm_gpu_coalesced_A()`
- `dmm_gpu_reduced_global()`
- `dmm_gpu_cublas()`

## Running


## Files Description
- Main Program: `dmm_main.cu`
- CPU Serial implementation: `dmm.cu`
- GPU Parallel implementation: `dmm_gpu.cu`
- GPU Helper files:
  - For 2D Matrixes: `mat_util.c`
  - For GPUs: `gpu_util.c`

## Things to Notice
- `Makefile`
  - Makefile options (DEBUG,...)
  - Optimizations
  - `make DEBUG=0`
- Run `./dmm_main` to see how to use it properly
- Submit code to torque:
  - How to submit to dungani
  - Other GPU options (default: NVIDIA Tesla K40c)
  - `$ qsub -q serial -l nodes=dungani:ppn=1 myjob.sh`

## CUDA Features
### Memory Management
On host code:
```c
float *d_x, *d_y;
/* Allocate device array to GPU */
cudaMalloc(&d_x, N*sizeof(float));
/* Transfer initialized hostarray x to d_x */
cudaMemcpy(d_x, x, N*sizeof(float), cudaMemcpyHostToDevice);
/* Transfer device array d_y to host array y */
cudaMemcpy(y, d_y, N*sizeof(float), cudaMemcpyDeviceToHost);
```

## Launching Kernels
Calling the kernel to run parallel on 256 threads:
```c
add<<<1, 256>>>(N, x, y);
```
The kernel:
```c
__global__
void add(int n, float *x, float *y)
{
  int index = threadIdx.x;
  int stride = blockDim.x;
  for (int i = index; i < n; i += stride)
      y[i] = x[i] + y[i];
}
```

`<<<numBlocks, threadsPerBlock>>>`: execution configuration, tells the CUDA runtime how many parallel threads to use for the launch on the GPU.

`numBlocks`: Number of blocks to use (grid).

`threadsPerBlock`: Number of threads per block, must be a multiple of 32 (a warp). Usuall value is 256.

CUDA GPUs run kernels using blocks of threads that are a multiple of 32 in size.

`threadIdx.x`: contains the index of the current thread within its block

`blockDim.x`: contains the number of threads in the block

```c
saxpy<<<(N+255)/256, 256>>>(N, 2.0, d_x, d_y);
```

### Kernels - Functions
`__global__` tells the CUDA C++ compiler that this is a function that runs on the GPU and can be called from CPU code.
*kernels*: These `__global__` functions. 
```c
/* We define kernels with __global__ specifier */
__global__ void kernel() {}
```

### Device Code
