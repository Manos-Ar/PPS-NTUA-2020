#include "lock.h"
#include "../common/alloc.h"
#include <stdbool.h>
#include <threads.h>

struct lock_struct {
	bool *flag;
	int tail;
	int size;
};

thread_local int thread_slot;

lock_t *lock_init(int nthreads)
{
	lock_t *lock;
	XMALLOC(lock,1);
	XMALLOC(lock->flag,nthreads);
	lock->size=nthreads;
	lock->tail=0;
	lock->flag[0]=true;
	return lock;
}

void lock_free(lock_t *lock)
{	
	XFREE(lock->flag);
	XFREE(lock);
}

void lock_acquire(lock_t *lock)
{
	int slot=__sync_fetch_and_add(&lock->tail,1)%lock->size;
	thread_slot=slot;
	while(!lock->flag[slot]);
}

void lock_release(lock_t *lock)
{
	lock->flag[thread_slot]=false;
	lock->flag[(thread_slot+1)%lock->size]=false;
}
