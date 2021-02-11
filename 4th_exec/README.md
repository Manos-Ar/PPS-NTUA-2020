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
qsub -q serial -l nodes=dungani:ppn=8 run_dmm.sh
```

# Code Guide
## Changes To Be Made
- Only change `cuda` directory.
- All changes will be made in code segments with **FILL ME** tags

Changed files:
- Implementation files:
  - `dmm_gpu.cu`
  - `dmm_main.cu`

- Other changed files:
  - `Makefile`
  - `make_dmm.sh`
  - `run_dmm.sh`

- Temp Changes:
  - `common.h` (`float` VS `double`) ??
  - `dmm_gpu.cu` (`Sgemm` VS `Dgemm`) ??
  - Make `float`, `double` choise at compile time


### Changes `dmm_main.cu`
- [ ] `cudaSetDevice()`, set device to be NVIDIA Tesla K40c (Device 2)
- [ ] Optionally increase appropriately the matrix size here if that helps you with your kernel code, e.g., to avoid divergent warps.
- [x] Set up the block and grid depending on the kernel (`THREAD_BLOCK_X, THREAD_BLOCK_Y, TILE_X, TILE_Y`)
  - [x] Set `gpu_block`
  - [x] Set `gpu_grid`
    ```c
    dim3 gpu_block(THREAD_BLOCK_Y, THREAD_BLOCK_X);
    dim3 gpu_grid((N + THREAD_BLOCK_Y - 1) / THREAD_BLOCK_Y,
                (M + THREAD_BLOCK_X - 1) / THREAD_BLOCK_X);
    ```
    C output matrix is MxN, so we need at least `⌈N/THREAD_BLOCK_Y⌉` number of blocks in X dimension
    and at least `⌈M/THREAD_BLOCK_X⌉` number of blocks in Y dimension.
- [x] CUBLAS arguments
    ```c
    gpu_kernels[kernel].fn(gpu_B, gpu_A, gpu_C, M, N, K);
    ```

### Changes `dmm_gpu.cu`
#### `dmm_gpu_naive()`

#### `dmm_gpu_coalesced_A()`

#### `dmm_gpu_reduced_global()`

#### `dmm_gpu_cublas()`
- [x] `alpha`, `beta`
- [x] `lda`, `ldb`, `ldc`
- [x] `transa`, `transb`
- [x] indexing by row-stored matrixes
- [x] Change A,B arguments


### Changes `Makefile`
Make `EPS` error value a compile time parameter:
```makefile
EPS ?= 1e-5
MAKE_CPPFLAGS = -D__FLOAT_VALUES -DEPS=$(EPS) -I../common
```

### Changes `make_dmm.sh`
Clean directory and set `EPS` values at compile time:
```sh
make clean
make DEBUG=0 EPS=1e-5
```

### Changes `run_dmm.sh`
For the GPU we are using:
```
Maximum number of threads per block:           1024
Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
```
So there is no point in checking block sizes over `32x32=1024`.

We also want: `THREAD_BLOCK_*=TILE_*`, because:
- `THREAD_BLOCK_*`: is the number of threads per block
- `TILE_*`: is the number of elements to compute in the C submatrix
and we want the elements to compute to be equal to the number of threads.

Two runnning scenarios:
#### 1st Scenario
- For (naive, coalesced, shmem)
- For all block-tile dimensions between `4-32`:
  - `4 8 16 32`
  - Find block sizes to test
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

### CuBLAS
[cuBLAS - API Reference Guide](https://docs.nvidia.com/cuda/cublas/index.html)
For natively written C and C++ code, one would most likely choose **0-based indexing**, in which case the array index of a matrix element in row “i” and column “j” can be computed via the following macro:
```c
#define IDX2C(i,j,ld) (((j)*(ld))+(i))
```
Also, for C and C++ the **transpose operation** should be selected, because the cuBLAS library uses column-major storage, and 1-based indexing.

The **leading dimension** always refers to the length of the first dimension of the array. If we are using **row-major** representation then the number of "columns" will be leading dimension.

##### 2.1.2. cuBLAS context
The application must initialize the handle to the cuBLAS library context by calling the `cublasCreate()` function.
Then, the handle is explicitly passed to every subsequent library function call. 
Once the application finishes using the library, it must call the function `cublasDestroy()` to release the resources associated with the cuBLAS library context.

##### 2.1.5. A.5. Scalar Parameters
The functions that take `alpha` and/or `beta` parameters by reference on the host or the device as scaling factors, such as `gemm`:
- When the pointer mode is set to `CUBLAS_POINTER_MODE_HOST`, the scalar parameters `alpha` and/or `beta` can be on the stack or allocated on the heap, shouldn't be placed in managed memory.
- When the pointer mode is set to `CUBLAS_POINTER_MODE_DEVICE`, `alpha` and/or `beta` must be accessible on the device and their values should not be modified until the kernel is done.

##### 2.7.1. cublas<t>gemm()
```c
cublasStatus_t cublasSgemm(cublasHandle_t handle,
                           cublasOperation_t transa, cublasOperation_t transb,
                           int m, int n, int k,
                           const float           *alpha,
                           const float           *A, int lda,
                           const float           *B, int ldb,
                           const float           *beta,
                           float           *C, int ldc)
```

This function performs the matrix-matrix multiplication:
$C = α op ( A ) op ( B ) + β C$
where $α$ and $β$ are scalars, and $A$ , $B$ and $C$ are matrices stored in column-major format with dimensions:
- $op ( A )$: $m × k$
- $op ( B )$: $k × n$
- $C$: $m × n$ 

Also, for matrix A:
- $op ( A ) = A$   if  `transa == CUBLAS_OP_N` 
- $op ( A ) = A^T$ if  `transa == CUBLAS_OP_T` 
- $op ( A ) = A^H$ if  `transa == CUBLAS_OP_C` 
and $op ( B )$ is defined similarly for matrix B.

**Parameters for exercise 4:**
We change the arguments, for the matrices and give $A$ as $B$, and $B$ as $A$. We do this because we store them in a row-major format, but cuBLAS assumes its column-major. Insteaded of transposing the $A$, $B$ matrices and needing to also transpose back $C$ matrix, we change the matrix arguments in order to have the correct format for $C$:
- `handle`: *handle to the cuBLAS library context*
- `transa` = `CUBLAS_OP_N` *($op ( A ) = A$, the non-transpose operation is selected*
- `transb` = `CUBLAS_OP_N` *($op ( B ) = B$, the non-transpose operation is selected*
- `m` = `N` *(number of rows of matrix $A$ and $C$)*
- `n` = `M` *(number of columns of matrix $B$ and $C$)*
- `k` = `K` *(number of columns of matrix $A$ and rows of $B$)*
- `alpha`: `<type>` scalar used for multiplication.
- `A` = `A` *(`<type>` array of dimensions `m k`)*
- `lda` = `N` *(leading dimension of two-dimensional array used to store the matrix $A$ = column size of $A$, for row-major matrix)*
- `B` = `B` *(`<type>` array of dimensions `k n`)*
- `ldb` = `K` *(leading dimension of two-dimensional array used to store the matrix $B$ = column size of $B$, for row-major matrix)*
- `beta`: `<type>` scalar used for multiplication.
- `C` = `C` *(`<type>` array of dimensions `m n`)*
- `ldc` = `N` *(leading dimension of two-dimensional array used to store the matrix $C$ = column size of $C$, for row-major matrix)*


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

