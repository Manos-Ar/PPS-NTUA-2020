#include <stdio.h>
#include <stdlib.h> /* rand() */
#include <limits.h>
#include <pthread.h> /* for pthread_spinlock_t */

#include "../common/alloc.h"
#include "ll.h"
#include "lock.h"

typedef struct ll_node {
	int key;
	struct ll_node *next;
	lock_t *lock;	
} ll_node_t;

struct linked_list {
	ll_node_t *head;
	/* other fields here? */
};

/**
 * Create a new linked list node.
 **/
static ll_node_t *ll_node_new(int key)
{
	ll_node_t *ret;

	XMALLOC(ret, 1);
	ret->lock=lock_init(0);
	ret->key = key;
	ret->next = NULL;
	/* Other initializations here? */

	return ret;
}

/**
 * Free a linked list node.
 **/
static void ll_node_free(ll_node_t *ll_node)
{
	lock_free(ll_node->lock);
	XFREE(ll_node);
}

/**
 * Create a new empty linked list.
 **/
ll_t *ll_new()
{
	ll_t *ret;

	XMALLOC(ret, 1);
	ret->head = ll_node_new(-1);
	ret->head->next = ll_node_new(INT_MAX);
	ret->head->next->next = NULL;

	return ret;
}

/**
 * Free a linked list and all its contained nodes.
 **/
void ll_free(ll_t *ll)
{
	ll_node_t *next, *curr = ll->head;
	while (curr) {
		next = curr->next;
		ll_node_free(curr);
		curr = next;
	}
	XFREE(ll);
}

int ll_validate(ll_t *ll, ll_node_t *prev, ll_node_t *curr){
	ll_node_t *node = ll->head;

	while(node->key<=prev->key){
		if(node==prev)
			return prev->next==curr;
		node=node->next;
	}
	return 0;
}

int ll_contains(ll_t *ll, int key)
{
	ll_node_t *prev, *curr;
	while(1)
	{
		prev=ll->head;
		curr=prev->next;

		while(curr->key < key){
			prev=curr;
			curr=curr->next;
		}

		lock_acquire(prev->lock);
		lock_acquire(curr->lock);
		if(ll_validate(ll,prev,curr)){
			if(curr->key==key){
				lock_release(prev->lock);
				lock_release(curr->lock);
				return 1;
			}
			else{
				lock_release(prev->lock);
				lock_release(curr->lock);
				return 0;
			}
		}
		else{
			lock_release(prev->lock);
			lock_release(curr->lock);
			continue;
		}
	}
	return 0;
}

int ll_add(ll_t *ll, int key)
{
	ll_node_t *prev, *curr, *new;
	while(1)
	{
		prev=ll->head;
		curr=prev->next;

		while(curr->key < key){
			prev=curr;
			curr=curr->next;
		}

		lock_acquire(prev->lock);
		lock_acquire(curr->lock);
		if(ll_validate(ll,prev,curr)){
			if(curr->key==key){
				lock_release(prev->lock);
				lock_release(curr->lock);
				return 0;
			}
			else{
				new=ll_node_new(key);
				prev->next=new;
				new->next=curr;
				lock_release(prev->lock);
				lock_release(curr->lock);
				return 1;
			}
		}
		else{
			lock_release(prev->lock);
			lock_release(curr->lock);
			continue;
		}
	}
	return 0;
}



int ll_remove(ll_t *ll, int key)
{
	ll_node_t *prev, *curr;
	while(1)
	{
		prev=ll->head;
		curr=prev->next;

		while(curr->key < key){
			prev=curr;
			curr=curr->next;
		}

		lock_acquire(prev->lock);
		lock_acquire(curr->lock);
		if(ll_validate(ll,prev,curr)){
			if(curr->key==key){
				prev->next=curr->next;
				lock_release(prev->lock);
				lock_release(curr->lock);
				return 1;
			}
			else{
				lock_release(prev->lock);
				lock_release(curr->lock);
				return 0;
			}
		}
		else{
			lock_release(prev->lock);
			lock_release(curr->lock);
			continue;
		}
	}
	return 0;
}

/**
 * Print a linked list.
 **/
void ll_print(ll_t *ll)
{
	ll_node_t *curr = ll->head;
	printf("LIST [");
	while (curr) {
		if (curr->key == INT_MAX)
			printf(" -> MAX");
		else
			printf(" -> %d", curr->key);
		curr = curr->next;
	}
	printf(" ]\n");
}
