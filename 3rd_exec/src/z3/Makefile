CC = gcc
CFLAGS = -Wall -Wextra -pthread

## Remove some warnings.
CFLAGS += -Wno-unused-parameter -Wno-unused-variable -Wno-unused-function

all: fine_grain

## Which linked list implementation to use?
LL_FILE = ll_serial.c

## Additional source files
SRC_FILES = ../common/aff.c pthread_lock.c


fine_grain: main.c ${LL_FILE} ${SRC_FILES}
	$(CC) $(CFLAGS) $^ -o $@.out

clean:
	rm -f *.out
