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
  - `run_dmm.sh`
- All changes will be made in code segments with **FILL ME** tags

### Changes `dmm_main.cu`
- Optionally increase appropriately the matrix size here if that helps you with your kernel code, e.g., to avoid divergent warps.
- Set up the block and grid depending on the kernel (`THREAD_BLOCK_X, THREAD_BLOCK_Y, TILE_X, TILE_Y`)
  - Set block size from script
- Set up the thread block and grid dimensions
- Execute and time the kernel (for CUBLAS)

### Changes `dmm_gpu.cu`
- `dmm_gpu_naive()`
- `dmm_gpu_coalesced_A()`
- `dmm_gpu_reduced_global()`
- `dmm_gpu_cublas()`

### Changes `run_dmm.sh`
Two runnning scenarios:
#### 1st Scenario
- For (naive, coalesced, shmem)
- For all block dimensions between `16-512`:
  - `16 32 48 64 80 96 112 128 144 160 176 192 208 224 240 256 272 288 304 320 336 352 368 384 400 416 432 448 464 480 496 512`
- For `M=N=K=2048`
#### 2nd Scenario
- For (naive, coalesced, shmem, cuBLAS)
- For best block dimensions for each kernel
- For `M, N, K ∈ [256, 512, 1024, 2048]`

## Running
- Current Usage: `[GPU_KERNEL=<kernel_no>] <M> <N> <K>`

- Changed Usage: `[GPU_KERNEL=<kernel_no>] [GPU_BLOCK_SIZE=<block_dim>] <M> <N> <K>
`

What the program expects:
```
./dmm_main

Usage: [GPU_KERNEL=<kernel_no>] ./dmm_main <M> <N> <K>
KERNEL defaults to 0
Available kernels [id:name]:
	0:naive
	1:coalesced_A
	2:reduced_global
	3:cublas
```

## Files Description
- Main Program: `dmm_main.cu`
- CPU Serial implementation: `dmm.cu`
- GPU Parallel implementation: `dmm_gpu.cu`
- GPU Helper files:
  - For 2D Matrixes: `mat_util.c`
  - For GPUs: `gpu_util.c`

## Things to Notice
- `Makefile`
  - Makefile options
  - Optimizations
  - `make DEBUG=0`
- Submit code to torque:
  - Other GPU options (default: NVIDIA Tesla K40c)

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

# VS Code Settings for CUDA
## Install extensions
- Install `C/C++` extension from marketplace
- Install `vscode-cudacpp` extension from marketplace

## Set Google Formatter
- Open settings with <kbd>Ctrl</kbd> + <kbd>,</kbd>
- Go to *Extensions* tab.
- Go to *C/C++* section.
- Find `C_Cpp: Clang_format_fallback Style` option.
- Type `Google` to the text field.

## Set Format on Save
- Open settings with <kbd>Ctrl</kbd> + <kbd>,</kbd>
- Go to *Text Editor* tab.
- Go to *Formatting* section.
- Find `Format on Save` option.
- Check the check-box

## Add file assocations
Open `settings.json`:
- <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>
- Type: *Open Settings (JSON)*
- Press Enter

And add the following:
```
"files.associations": {
        "*.cu": "cpp",
        "*.cuh": "cpp"
    },
```

