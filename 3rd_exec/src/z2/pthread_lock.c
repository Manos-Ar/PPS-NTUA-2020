#include "lock.h"
#include "../common/alloc.h"
#include <pthread.h>
#include <errno.h>


struct lock_struct {
	pthread_spinlock_t *spin_lock;
};

lock_t *lock_init(int nthreads)
{
	lock_t *lock;
	// int pshared=0;
	XMALLOC(lock, 1);

	while(pthread_spin_init(lock->spin_lock,0)){}; //success  == 0
	return lock;
}

void lock_free(lock_t *lock)
{
	pthread_spin_destroy(lock->spin_lock);
	XFREE(lock);
}

void lock_acquire(lock_t *lock)
{
	int ret;
	while(1){
		ret = pthread_spin_lock(lock->spin_lock);
		if(ret==0) break;
		else if(ret==EDEADLK) break;
		else if(ret==EINVAL){
			fprintf(stderr, "Undefined spinlock: %s:%d\n", __FILE__, __LINE__);
			exit(1);
		}
	};
}

void lock_release(lock_t *lock)
{
	int ret;
	ret=pthread_spin_lock(lock->spin_lock);
	if(ret==0) return;
	else if(ret==EPERM){
		fprintf(stderr, "Thread does not hold the spinlock: %s:%d\n", __FILE__, __LINE__);
			exit(1);
	}
	else if(ret==EINVAL){
			fprintf(stderr, "Undefined spinlock: %s:%d\n", __FILE__, __LINE__);
			exit(1);
		}
	
}
