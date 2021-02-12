/*
 *  dmm_gpu.cu -- Template for DMM GPU kernels
 *
 *  Copyright (C) 2020, Computing Systems Laboratory (CSLab)
 *  Copyright (C) 2020, Athena Elafrou/Petros Anastasiadis
 */

#include <stdio.h>

#include "cublas_v2.h"
#include "dmm.h"

/*
 *  Naive kernel
 */
__global__ void dmm_gpu_naive(const value_t *A, const value_t *B, value_t *C,
                              const size_t M, const size_t N, const size_t K) {
  // Compute the row and the column of the current thread
  int row = blockIdx.y * blockDim.y + threadIdx.y;
  int col = blockIdx.x * blockDim.x + threadIdx.x;

  value_t Cvalue = 0;

  // If the threads positions is out of array bounds, exit
  if (row >= M || col >= N) return;

  // Each thread computes one element of C by accumulating results into Cvalue
  for (int e = 0; e < K; e++) {
    Cvalue += A[row * K + e] * B[e * N + col];
  }

  C[row * N + col] = Cvalue;
}

/*
 *  Coalesced memory acceses of A.
 */
__global__ void dmm_gpu_coalesced_A(const value_t *A, const value_t *B,
                                    value_t *C, const size_t M, const size_t N,
                                    const size_t K) {
  // Shared memory between threads of the same block, for Tiled sub-matrix of A
  __shared__ value_t A_shared[TILE_X][TILE_Y];

  // Compute the row and column of each thread in a Tile
  int tid_y = threadIdx.y;
  int tid_x = threadIdx.x;
  int row = blockIdx.y * TILE_Y + tid_y;
  int col = blockIdx.x * TILE_X + tid_x;

  // Each thread computes one element of C by accumulating results into Cvalue
  value_t Cvalue = 0;

  // Calculate the ceiling for number of Tiles needed for A
  int tile_x_ceil = (K + TILE_X - 1) / TILE_X;

  // Loop over all the sub-matrices of A (on x-axis, for all columns) that are
  // required to compute Csub.
  for (int m = 0; m < tile_x_ceil; m++) {
    // Load sub-matrix of A from device memory to shared memory
    A_shared[tid_y][tid_x] = A[row * K + m * TILE_X + tid_x];
    // Explanation: Find from which row to start, from which tile, from which
    // thread inside the tile

    // Synchronize to make sure the sub-matrix is loaded
    // before starting the computation
    __syncthreads();

    // Multiply the A sub-matrix with B and accumulate the results.
    for (int e = 0; e < TILE_X; e++) {
      Cvalue += A_shared[tid_y][e] * B[(m * TILE_X + e) * N + col];
    }
    // Synchronize to make sure that the preceding computation is done
    // before loading new sub-matrix of A and in the next iteration
    __syncthreads();
  }
  // Write Csub to device memory
  C[row * N + col] = Cvalue;
}

/*
 *  Reduced memory accesses.
 */
__global__ void dmm_gpu_reduced_global(const value_t *A, const value_t *B,
                                       value_t *C, const size_t M,
                                       const size_t N, const size_t K) {
  // Shared memory between threads of the same block, for Tiled sub-matrices A,B
  __shared__ value_t A_shared[TILE_X][TILE_Y];
  __shared__ value_t B_shared[TILE_X][TILE_Y];

  // Compute the row and column of each thread in a Tile
  int tid_y = threadIdx.y;
  int tid_x = threadIdx.x;
  int row = blockIdx.y * TILE_Y + tid_y;
  int col = blockIdx.x * TILE_X + tid_x;

  // Each thread computes one element of C by accumulating results into Cvalue
  value_t Cvalue = 0;

  // Calculate the ceiling for number of Tiles needed for A
  int tile_x_ceil = (K + TILE_X - 1) / TILE_X;

  // Loop over all the sub-matrices of A (on x-axis, for all columns) and
  // B (on y-axis, for all rows) that are required to compute Csub.
  for (int m = 0; m < tile_x_ceil; m++) {
    // Load sub-matrices of A,B from device memory to shared memory
    A_shared[tid_y][tid_x] = A[row * K + m * TILE_X + tid_x];
    B_shared[tid_y][tid_x] = B[col + (m * TILE_Y + tid_y) * N];
    // Explanation A: Find from which row to start, from which tile, from which
    // thread inside the tile
    // Explanation B: Find from which col to start, from which tile, from which
    // thread inside the tile

    // Synchronize to make sure the sub-matrix is loaded
    // before starting the computation
    __syncthreads();

    // Multiply the sub-matrices together and accumulate the results.
    for (int e = 0; e < TILE_X; e++) {
      Cvalue += A_shared[tid_y][e] * B_shared[e][tid_x];
    }
    // Synchronize to make sure that the preceding computation is done
    // before loading new sub-matrix of A and in the next iteration
    __syncthreads();
  }
  // Write Csub to device memory
  C[row * N + col] = Cvalue;
}

/*
 *  Use of cuBLAS
 */
void dmm_gpu_cublas(const value_t *A, const value_t *B, value_t *C,
                    const size_t M, const size_t N, const size_t K) {
  // Define variables for cuBLAS status and handle
  cublasStatus_t stat;
  cublasHandle_t handle;

  // Define leading dimensions of A,B,C matrices for cublasSgemm
  int lda = N;
  int ldb = K;
  int ldc = N;

  // Define alpha, beta values for GEMM calculation
  // C = alpha*A*B + beta*C
  const value_t alpha_val = 1;
  const value_t beta_val = 0;
  const value_t *alpha = &alpha_val;
  const value_t *beta = &beta_val;

  // Create a handle for cuBLAS
  stat = cublasCreate(&handle);
  if (stat != CUBLAS_STATUS_SUCCESS) {
    printf("CUBLAS initialization failed\n");
  }

  // Call cublasSgemm to calculate the DMM (for floats)
  stat = cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N, N, M, K, alpha, A, lda,
                     B, ldb, beta, C, ldc);
  if (stat != CUBLAS_STATUS_SUCCESS) {
    printf("cublasSgemm failed");
  }

  // Destroy the handle
  cublasDestroy(handle);
}
