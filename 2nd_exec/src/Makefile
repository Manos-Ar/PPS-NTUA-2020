CC=gcc
MPICC=mpicc
CFLAGS=-O3 -lm -Wall
RES=-DPRINT_RESULTS
CONV=-DTEST_CONV

all: jacobi jacobi_mpi
# seidelsor redblacksor

jacobi: Jacobi_serial.c utils.c
	$(CC) $(CFLAGS) $(RES) $(CONV) Jacobi_serial.c utils.c -o jacobi.out

jacobi_mpi: Jacobi_mpi.c utils.c
	$(MPICC) $(CFLAGS) $(RES) $(CONV) Jacobi_mpi.c utils.c -o jacobi_mpi.out

# seidelsor: GaussSeidelSOR_serial.c utils.c
# 	$(CC) $(CFLAGS) $(RES) $(CONV) GaussSeidelSOR_serial.c utils.c -o seidelsor

# redblacksor: RedBlackSOR_serial.c utils.c
# 	$(CC) $(CFLAGS) $(RES) $(CONV) RedBlackSOR_serial.c utils.c -o redblacksor

clean:
	rm -f  *.out res*
