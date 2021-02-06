CC = gcc
CFLAGS = -Wall -Wextra -pthread

## Remove some warnings.
CFLAGS += -Wno-unused-parameter -Wno-unused-variable -Wno-unused-function

all: serial fine_grain optimistic 

## Which linked list implementation to use?
LL_FILE = ll_serial.c

## Additional source files
SRC_FILES = ../common/aff.c pthread_lock.c


serial: main.c ll_serial.c ${SRC_FILES}
	$(CC) $(CFLAGS) $^ -o $@.out

fine_grain: main.c ll_fgl.c ${SRC_FILES}
	$(CC) $(CFLAGS) $^ -o $@.out

optimistic: main.c ll_opt.c ${SRC_FILES}
	$(CC) $(CFLAGS) $^ -o $@.out

clean:
	rm -f *.out
