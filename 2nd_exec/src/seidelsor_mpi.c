#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include "mpi.h"
#include "utils.h"
#include <string.h>

int j_converge(double ** u_previous, double ** u_current, int X_min, int X_max, int Y_min, int Y_max) {
	int i,j;
	for (i=X_min;i<X_max;i++)
		for (j=X_max;j<Y_max;j++)
			if (fabs(u_current[i][j]-u_previous[i][j])>e) return 0;
	return 1;
}


void GaussSeidel(double ** u_previous, double ** u_current, int X_min, int X_max, int Y_min, int Y_max, double omega) {
	int i,j;
	for (i=X_min;i<X_max;i++)
		for (j=Y_min;j<Y_max;j++)
			u_current[i][j]=u_previous[i][j]+(u_current[i-1][j]+u_previous[i+1][j]+u_current[i][j-1]+u_previous[i][j+1]-4*u_previous[i][j])*omega/4.0;
}


int main(int argc, char ** argv) {
    int rank,size;
    int global[2],local[2]; //global matrix dimensions and local matrix dimensions (2D-domain, 2D-subdomain)
    int global_padded[2];   //padded global matrix dimensions (if padding is not needed, global_padded=global)
    int grid[2];            //processor grid dimensions
    int i,j,t;
    int global_converged=0,converged=0; //flags for convergence, global and per process
    MPI_Datatype dummy;     //dummy datatype used to align user-defined datatypes in memory
    double omega; 			//relaxation factor - useless for Jacobi

    struct timeval tts,ttf,tcs,tcf,tcvs,tcvf;   //Timers: total-> tts,ttf, computation -> tcs,tcf, converged -> tcvs,tcvf
    double ttotal=0,tcomp=0,tconv=0,total_time,comp_time,conv_time;

    double ** U, ** u_current, ** u_previous, ** swap; //Global matrix, local current and previous matrices, pointer to swap between current and previous


    MPI_Init(&argc,&argv);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);

    //----Read 2D-domain dimensions and process grid dimensions from stdin----//

    if (argc!=5) {
        fprintf(stderr,"Usage: mpirun .... ./exec X Y Px Py");
        exit(-1);
    }
    else {
        global[0]=atoi(argv[1]);
        global[1]=atoi(argv[2]);
        grid[0]=atoi(argv[3]);
        grid[1]=atoi(argv[4]);
    }

    //----Create 2D-cartesian communicator----//
	//----Usage of the cartesian communicator is optional----//

    MPI_Comm CART_COMM;         //CART_COMM: the new 2D-cartesian communicator
    int periods[2]={0,0};       //periods={0,0}: the 2D-grid is non-periodic
    int rank_grid[2];           //rank_grid: the position of each process on the new communicator

    MPI_Cart_create(MPI_COMM_WORLD,2,grid,periods,0,&CART_COMM);    //communicator creation
    MPI_Cart_coords(CART_COMM,rank,2,rank_grid);	                //rank mapping on the new communicator


    //----Compute local 2D-subdomain dimensions----//
    //----Test if the 2D-domain can be equally distributed to all processes----//
    //----If not, pad 2D-domain----//

    for (i=0;i<2;i++) {
        if (global[i]%grid[i]==0) {
            local[i]=global[i]/grid[i];
            global_padded[i]=global[i];
        }
        else {
            local[i]=(global[i]/grid[i])+1;
            global_padded[i]=local[i]*grid[i];
        }
    }

	//Initialization of omega
    omega=2.0/(1+sin(3.14/global[0]));

    //----Allocate global 2D-domain and initialize boundary values----//
    //----Rank 0 holds the global 2D-domain----//
    if (rank==0) {
        U=allocate2d(global_padded[0],global_padded[1]);
        init2d(U,global[0],global[1]);
    }

    //----Allocate local 2D-subdomains u_current, u_previous----//
    //----Add a row/column on each size for ghost cells----//

    u_previous=allocate2d(local[0]+2,local[1]+2);
    u_current=allocate2d(local[0]+2,local[1]+2);

    //----Distribute global 2D-domain from rank 0 to all processes----//

 	//----Appropriate datatypes are defined here----//
	/*****The usage of datatypes is optional*****/

    //----Datatype definition for the 2D-subdomain on the global matrix----//

    MPI_Datatype global_block;
    MPI_Type_vector(local[0],local[1],global_padded[1],MPI_DOUBLE,&dummy);
    MPI_Type_create_resized(dummy,0,sizeof(double),&global_block);
    MPI_Type_commit(&global_block);

    //----Datatype definition for the 2D-subdomain on the local matrix----//

    MPI_Datatype local_block;
    MPI_Type_vector(local[0],local[1],local[1]+2,MPI_DOUBLE,&dummy);
    MPI_Type_create_resized(dummy,0,sizeof(double),&local_block);
    MPI_Type_commit(&local_block);

    //----Rank 0 defines positions and counts of local blocks (2D-subdomains) on global matrix----//
    int * scatteroffset, * scattercounts;
    double *u = NULL;
    if (rank==0) {
        u= &U[0][0];
        scatteroffset=(int*)malloc(size*sizeof(int));
        scattercounts=(int*)malloc(size*sizeof(int));
        for (i=0;i<grid[0];i++)
            for (j=0;j<grid[1];j++) {
                scattercounts[i*grid[1]+j]=1;
                scatteroffset[i*grid[1]+j]=(local[0]*local[1]*grid[1]*i+local[1]*j);
            }
    }

	/*Fill your code here*/

    MPI_Scatterv(u, scattercounts, scatteroffset, global_block, &u_previous[1][1], 1, local_block, 0, MPI_COMM_WORLD);
    // memcpy(u_current,u_previous,(local[0]+2)*(local[1]+2));

	/*Make sure u_current and u_previous are
		both initialized*/

		for(i=0; i<local[0]+2; i++)
        for(j=0; j<local[1]+2; j++)
            u_current[i][j]=u_previous[i][j];

     //************************************//

	//----Define datatypes or allocate buffers for message passing----//

	//*************TODO*******************//

	/*Fill your code here*/

    MPI_Datatype column;
    MPI_Type_vector(local[0],1,local[1]+2,MPI_DOUBLE,&column);
    MPI_Type_commit(&column);

    MPI_Datatype row;
    MPI_Type_contiguous (local[1],MPI_DOUBLE,&row);
    MPI_Type_commit(&row);

	//************************************//

  //----Find the 4 neighbors with which a process exchanges messages----//

	//*************TODO*******************//

    int north, south, east, west;

    MPI_Cart_shift(CART_COMM, 0, 1, &north, &south);
    MPI_Cart_shift(CART_COMM, 1, 1, &west, &east);

    // printf("rank: %d\n", rank);
    // printf("%d %d %d %d \n", north, south, west, east);

	/*Fill your code here*/

	/*Make sure you handle non-existing
		neighbors appropriately*/

	//************************************//


    //---Define the iteration ranges per process-----//
	//*************TODO*******************//

    int i_min,i_max,j_min,j_max;
	/*Fill your code here*/

    if(north > -1)
        i_min = 1;
    else
        i_min = 2;

    if(south > -1)
        i_max = local[0] +1;
    else
        i_max = local[0];

    if(west > -1)
        j_min = 1;
    else
        j_min = 2;

    if(east > -1)
        j_max = local[1] + 1;
    else
        j_max = local[1];


	/*Three types of ranges:
		-internal processes
		-boundary processes
		-boundary processes and padded global array
	*/


	//************************************//


 	//----Computational core----//
    int pre_counts, post_counts;
    MPI_Request pre_requests[6];
    MPI_Request posts_requests[2];

	gettimeofday(&tts, NULL);
    #ifdef TEST_CONV
    for (t=0;t<T && !global_converged;t++) {
    #endif
    #ifndef TEST_CONV
    #undef T
    #define T 256
    for (t=0;t<T;t++) {
    #endif

	 	//*************TODO*******************//

		/*Fill your code here*/
		/*Compute and Communicate*/

        swap=u_previous;
		u_previous=u_current;
		u_current=swap;

        pre_counts=0;
        post_counts=0;
        if(north >= 0){
            MPI_Isend(&u_previous[1][1], 1, row, north, rank, CART_COMM, &pre_requests[pre_counts++]);
            MPI_Irecv(&u_current[0][1], 1, row, north, north, CART_COMM, &pre_requests[pre_counts++]);
        }

        if(west >=0){
            MPI_Isend(&u_previous[1][1], 1, column, west, rank, CART_COMM, &pre_requests[pre_counts++]);
            MPI_Irecv(&u_current[1][0], 1, column, west, west, CART_COMM, &pre_requests[pre_counts++]);
        }

        // MPI_Waitall(counts, requests, MPI_STATUSES_IGNORE);

        if(south >= 0){
            // MPI_Isend(&u_previous[local[0]][1], 1, row, south, rank, CART_COMM, &requests[counts++]);
            MPI_Irecv(&u_previous[local[0]+1][1], 1, row, south, south, CART_COMM, &pre_requests[pre_counts++]);
        }

        if(east >=0){
            // MPI_Isend(&u_previous[1][local[1]], 1, column, east, rank, CART_COMM, &requests[counts++]);
            MPI_Irecv(&u_previous[1][local[1]+1], 1, column, east, east, CART_COMM, &pre_requests[pre_counts++]);
        }

        MPI_Waitall(pre_counts, pre_requests, MPI_STATUSES_IGNORE);

        gettimeofday(&tcs,NULL);

        GaussSeidel(u_previous, u_current, i_min, i_max, j_min, j_max, omega);

        gettimeofday(&tcf,NULL);

        // printf("rank : %d\n", rank);

        tcomp+=(tcf.tv_sec-tcs.tv_sec)+(tcf.tv_usec-tcs.tv_usec)*0.000001;

        if(south >= 0){
            MPI_Isend(&u_current[local[0]][1], 1, row, south, rank, CART_COMM, &posts_requests[post_counts++]);
            // MPI_Irecv(&u_previous[local[0]+1][1], 1, row, south, south, CART_COMM, &requests[counts++]);
        }

        if(east >=0){
            MPI_Isend(&u_current[1][local[1]], 1, column, east, rank, CART_COMM, &posts_requests[post_counts++]);
            // MPI_Irecv(&u_previous[1][local[1]+1], 1, column, east, east, CART_COMM, &requests[counts++]);
        }    

        MPI_Waitall(post_counts, posts_requests, MPI_STATUSES_IGNORE);
        


		/*Add appropriate timers for computation*/

		#ifdef TEST_CONV
        if (t%C==0) {
			//*************TODO**************//
			gettimeofday(&tcvs,NULL);
			converged=j_converge(u_previous,u_current,i_min, i_max, j_min, j_max);
			gettimeofday(&tcvf,NULL);
			// converged=converge(u_previous,u_current,local[0]+2, local[1]+2);
      MPI_Allreduce(&converged, &global_converged, 1, MPI_INT, MPI_LAND, MPI_COMM_WORLD);
			tconv+=(tcvf.tv_sec-tcvs.tv_sec)+(tcvf.tv_usec-tcvs.tv_usec)*0.000001;
		}
		#endif

		//************************************//

    }
    gettimeofday(&ttf,NULL);
    // printf("rank: %d t: %d %d \n", rank, t, global_converged);

    ttotal=(ttf.tv_sec-tts.tv_sec)+(ttf.tv_usec-tts.tv_usec)*0.000001;

    MPI_Reduce(&ttotal,&total_time,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);
    MPI_Reduce(&tcomp,&comp_time,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);
    MPI_Reduce(&tconv,&conv_time,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);

    //----Rank 0 gathers local matrices back to the global matrix----//

	//*************TODO*******************//

    MPI_Gatherv(&u_previous[1][1], 1, local_block, u, scattercounts, scatteroffset, global_block, 0, MPI_COMM_WORLD);

	//----Printing results----//

	//**************TODO: Change "Jacobi" to "GaussSeidelSOR" or "RedBlackSOR" for appropriate printing****************//
    if (rank==0) {

            #ifdef TEST_CONV
	        printf("GaussSeidelSOR X %d Y %d Jobs %d Px %d Py %d Iter %d ComputationTime %lf ConvergedTime %lf TotalTime %lf midpoint %lf\n",global[0],global[1],size,grid[0],grid[1],t,comp_time,conv_time,total_time,U[global[0]/2][global[1]/2]);
		    #endif
		    #ifndef TEST_CONV
	        printf("GaussSeidelSOR X %d Y %d Jobs %d Px %d Py %d Iter %d ComputationTime %lf TotalTime %lf midpoint %lf\n",global[0],global[1],size,grid[0],grid[1],t,comp_time,total_time,U[global[0]/2][global[1]/2]);
		    #endif

        #ifdef PRINT_RESULTS
        char * s=malloc(50*sizeof(char));
        sprintf(s,"resGaussSeidelSORMPI_%dx%d_%dx%d",global[0],global[1],grid[0],grid[1]);
        fprint2d(s,U,global[0],global[1]);
        free(s);
        #endif

				free2d(U);

    }
    MPI_Finalize();
    return 0;
}
