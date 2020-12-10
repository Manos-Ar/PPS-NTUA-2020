CC=gcc
MPICC=mpicc
CFLAGS=-O3 -lm -Wall
# RES=-DPRINT_RESULTS
# CONV=-DTEST_CONV

all: jacobi jacobi_mpi jacobi_mpi_conv
# seidelsor redblacksor

jacobi: jacobi_serial.c utils.c
	$(CC) $(CFLAGS) $(RES) $(CONV) jacobi_serial.c utils.c -o jacobi.out

jacobi_mpi: jacobi_mpi.c utils.c
	$(MPICC) $(CFLAGS) $(RES) jacobi_mpi.c utils.c -o jacobi_mpi.out

jacobi_mpi_conv: jacobi_mpi.c utils.c
	$(MPICC) $(CFLAGS) $(RES) -DTEST_CONV jacobi_mpi.c utils.c -o jacobi_mpi_conv.out

# seidelsor: GaussSeidelSOR_serial.c utils.c
# 	$(CC) $(CFLAGS) $(RES) $(CONV) GaussSeidelSOR_serial.c utils.c -o seidelsor

# redblacksor: RedBlackSOR_serial.c utils.c
# 	$(CC) $(CFLAGS) $(RES) $(CONV) RedBlackSOR_serial.c utils.c -o redblacksor

clean:
	rm -f  *.out res*
