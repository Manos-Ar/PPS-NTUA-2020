#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>

/*
 * This example is to demonstrate that the recvcnt and sendcnt 
 * parameters in collective communication APIs such as
 * MPI_Scatter, MPI_Gather and MPI_Allgather need not be similar.
 *
 * It will be different only if the datatype are different at both
 * sender and receivers. The following example demonstrate this by using
 * user defined datatypes in MPI. Note that we did not cover user defined 
 * datatypes in MPI. This example just to answer the queries raised in the
 * class.
 */

int main(int argc, char** argv) {
  MPI_Init(&argc, &argv);
  
  int i, rank, size;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
 
  int* sendbuf;
  // Only root initializes the sendbuf. Root is scattering an array of length=num_procs * 4
  // to each rank in MPI_COMM_WORLD. Hence, each rank will receive 4 integers after MPI_Scatter call.
  if(rank ==0) {
    sendbuf = (int*) malloc(sizeof(int) * size * 4);
    for(i=0; i<size * 4; i++) {
        sendbuf[i] = i;
        if(i%size==0 && i!=0)
            printf("\n"); 
        printf("%d ",sendbuf[i]);
        
    }
    printf("\n");
  }
  // Note that although the recvbuf at each rank is of size = 4, the recvcnt in MPI_Scatter 
  // is 1 instead of 4. This is possible by creating a user defined datatype "my_own_datatype"
  // that is effectively an structure containing 4 integers (contiguous).
  int recvbuf[4];
  MPI_Datatype my_own_datatype,tmp; // Declaring the user defined datatype
//   MPI_Type_vector(4, 2, 4, MPI_INT, &my_own_datatype); // specifying to runtime that this datatype is contiguous
  MPI_Type_vector(2, 2, 4, MPI_INT, &my_own_datatype); // specifying to runtime that this datatype is contiguous

//   MPI_Type_create_resized(&tmp)
  MPI_Type_contiguous(4, MPI_INT, &tmp); // specifying to runtime that this datatype is contiguous
  MPI_Type_commit(&my_own_datatype); // A datatype can only be communicated once its committed (saved).
  MPI_Type_commit(&tmp); // A datatype can only be communicated once its committed (saved).
  
  // Although the sendcnt and recvcnt is different, its important to note that total bytes
  // sent by the root is equal to the sum of total bytes recevied at all processes in MPI_COMM_WORLD.
//   int sendcnt = 4;
//   int recvcnt = 1; 
//   MPI_Scatter(sendbuf, sendcnt, MPI_INT, recvbuf, recvcnt, my_own_datatype, 0, MPI_COMM_WORLD);
  
    // MPI_
    int k=0;
  if(rank==0){
    for(int i=0; i<size ; i+=2){
        for(int j=0; j<size ; j+=2){
            MPI_Send(&sendbuf[i*size+j],1,my_own_datatype, k,0,MPI_COMM_WORLD);
            printf("send ok %d\n",k);
            k++;
            }
        }        
    }
    // for(int i=0; i<size ; i++)
    
    MPI_Recv(recvbuf,4,MPI_DOUBLE, 0,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
    
  
//   MPI_Scatter(sendbuf, 1, my_own_datatype, recvbuf, 4, MPI_INT, 0, MPI_COMM_WORLD);

  // Print the message received at each rank
  char msg[100];
  sprintf(msg,"Rank %d: ", rank);
  for(i=0; i<4; i++){
    sprintf(msg + strlen(msg),"%d ", recvbuf[i]);
  }
  sprintf(msg + strlen(msg),"\n");
  printf("%s",msg);
  fflush(stdout);
 
  MPI_Finalize();
  return 0;
}