CC=gcc
MPICC=mpicc
CFLAGS=-O3 -lm -Wall
# RES=-DPRINT_RESULTS
# CONV=-DTEST_CONV

all: jacobi jacobi_mpi jacobi_mpi_conv seidelsor seidelsor_mpi seidelsor_mpi_conv redblacksor redblacksor_mpi redblacksor_mpi_conv

jacobi: jacobi_serial.c utils.c
	$(CC) $(CFLAGS) $(RES) $(CONV) jacobi_serial.c utils.c -o jacobi.out

jacobi_mpi: jacobi_mpi.c utils.c
	$(MPICC) $(CFLAGS) $(RES) jacobi_mpi.c utils.c -o jacobi_mpi.out

jacobi_mpi_conv: jacobi_mpi.c utils.c
	$(MPICC) $(CFLAGS) $(RES) -DTEST_CONV jacobi_mpi.c utils.c -o jacobi_mpi_conv.out

seidelsor: seidelsor_serial.c utils.c
	$(CC) $(RES) $(CONV) seidelsor_serial.c utils.c -o seidelsor.out $(CFLAGS)

seidelsor_mpi: seidelsor_mpi.c utils.c
	$(MPICC) $(RES) seidelsor_mpi.c utils.c -o seidelsor_mpi.out $(CFLAGS)

seidelsor_mpi_conv: seidelsor_mpi.c utils.c
	$(MPICC) $(RES) -DTEST_CONV seidelsor_mpi.c utils.c -o seidelsor_mpi_conv.out $(CFLAGS)

redblacksor: redblacksor_serial.c utils.c
	$(CC) $(RES) $(CONV) redblacksor_serial.c utils.c -o redblacksor.out $(CFLAGS)

redblacksor_mpi: redblacksor_mpi.c utils.c
	$(MPICC) $(RES) redblacksor_mpi.c utils.c -o redblacksor_mpi.out $(CFLAGS)

redblacksor_mpi_conv: redblacksor_mpi.c utils.c
	$(MPICC) $(RES) -DTEST_CONV redblacksor_mpi.c utils.c -o redblacksor_mpi_conv.out $(CFLAGS)


clean:
	rm -f  *.out res*
