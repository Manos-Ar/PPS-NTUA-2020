CC = gcc
CFLAGS = -Wall -Wextra -pthread -O0

## Remove some warnings.
CFLAGS += -Wno-unused-parameter -Wno-unused-variable -Wno-unused-function

all: ttas tas pthread nosync array clh test

LOCK_FILE=nosync_lock.c

## Additional source files
SRC_FILES = ../common/aff.c

ttas: main.c ttas_lock.c $(SRC_FILES) 
	$(CC) $(CFLAGS) $^ -o $@.out
tas: main.c tas_lock.c $(SRC_FILES) 
	$(CC) $(CFLAGS) $^ -o $@.out
pthread: main.c pthread_lock.c $(SRC_FILES) 
	$(CC) $(CFLAGS) $^ -o $@.out
nosync: main.c nosync_lock.c $(SRC_FILES) 
	$(CC) $(CFLAGS) $^ -o $@.out
array: main.c array_lock.c $(SRC_FILES) 
	$(CC) $(CFLAGS) $^ -o $@.out
clh: main.c clh_lock.c $(SRC_FILES) 
	$(CC) $(CFLAGS) $^ -o $@.out

test: test.c $(LOCK_FILE) $(SRC_FILES)
	$(CC) $(CFLAGS) $^ -o $@.out

clean:
	rm -f *.out
