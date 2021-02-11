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
  //   // Compute the Block row and column of each thread
  //     int blockRow = blockIdx.y;
  //   int blockCol = blockIdx.x;

  //   // Each thread block computes one sub-matrix Csub of C

  //   // Each thread computes one element of C by accumulating results into
  //   Cvalue value_t Cvalue;

  //   // Thread row and column within Csub
  //   int row = threadIdx.y;
  //   int col = threadIdx.x;

  //   // If the threads positions is out of array bounds, exit
  //   if (row >= M || col >= N) return;

  //   // Loop over all the sub-matrices of A and B that are required to compute
  //   Csub
  //   // Multiply each pair of sub-matrices together and accumulate the results
  //   for (int m = 0; m < (K / BLOCK_SIZE); ++m) {
  //     // Get sub-matrix Asub of A

  //     // Get sub-matrix Bsub of B

  //     // Shared memory used to store Asub and Bsub respectively
  //     __shared__ value_t As[BLOCK_SIZE][BLOCK_SIZE];
  //     __shared__ value_t As[BLOCK_SIZE][BLOCK_SIZE];
  //   }

  //   // Each thread computes one element of C by accumulating results into
  //   Cvalue for (int e = 0; e < K; e++) {
  //     Cvalue += A[row * K + e] * B[e * N + col];
  //   }

  //   C[row * N + col] = Cvalue;
}

/*
 *  Reduced memory accesses.
 */
__global__ void dmm_gpu_reduced_global(const value_t *A, const value_t *B,
                                       value_t *C, const size_t M,
                                       const size_t N, const size_t K) {
  /*
   * FILLME: fill the code.
   */
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

  // Call cublasSgemm to calculate the DMM (for doubles)
  // stat = cublasDgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N, N, M, K, alpha, A,
  //   lda, B, ldb, beta, C, ldc);

  if (stat != CUBLAS_STATUS_SUCCESS) {
    printf("cublasSgemm failed");
  }

  // Destroy the handle
  cublasDestroy(handle);
}
