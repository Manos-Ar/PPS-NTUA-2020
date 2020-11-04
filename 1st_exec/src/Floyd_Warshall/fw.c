/*
 Standard implementation of the Floyd-Warshall Algorithm
*/

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include "util.h"
#include <omp.h>

inline int min(int a, int b);

int main(int argc, char **argv)
{
     int **A;
     int i,j,k;
     struct timeval t1, t2;
     double time;
     int N=1024;

     if (argc != 2) {
        fprintf(stdout,"Usage: %s N\n", argv[0]);
        exit(0);
     }

     N=atoi(argv[1]);

     A = (int **) malloc(N*sizeof(int *));
     for(i=0; i<N; i++) A[i] = (int *) malloc(N*sizeof(int));

     graph_init_random(A,-1,N,128*N);

     gettimeofday(&t1,0);
     for(k=0;k<N;k++)
     #pragma omp parallel
     {
       // printf("Num of threads: %d \n", omp_get_num_threads() );
        #pragma omp for schedule(static)
          for(j=0; j<N; j++)
            A[k][j] = min(A[k][j], A[k][k] + A[k][j]);

        #pragma omp for schedule(static)
          for(i=0; i<N; i++)
            A[i][k] = min(A[i][k], A[i][k] + A[k][k]);

        #pragma omp barrier


        #pragma omp for schedule(static) private(j)
          for(i=0; i<N; i++){
              if(i != k){
                for(j=0; j<N; j++){
                  if (j != k)
                    A[i][j]=min(A[i][j], A[i][k] + A[k][j]);
                }
              }
          }
      }
     gettimeofday(&t2,0);

     time=(double)((t2.tv_sec-t1.tv_sec)*1000000+t2.tv_usec-t1.tv_usec)/1000000;
     printf("FW,%d,%.4f\n", N, time);

     // /*
     // for(i=0; i<N; i++){
     //    for(j=0; j<N; j++)
     //      fprintf(stdout,"%d ", A[i][j]);
     //    fprintf(stdout,"\n");
     //  }
     // */

     return 0;
}

inline int min(int a, int b)
{
     if(a<=b)return a;
     else return b;
}
