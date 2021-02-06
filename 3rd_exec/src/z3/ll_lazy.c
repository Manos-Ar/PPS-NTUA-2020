#include <stdio.h>
#include <stdlib.h> /* rand() */
#include <limits.h>
#include <pthread.h> /* for pthread_spinlock_t */

#include "../common/alloc.h"
#include "ll.h"
#include <stdbool.h>

typedef struct ll_node {
	int key;
	struct ll_node *next;
	pthread_spinlock_t lock;
	bool mark;
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
	pthread_spin_init(&ret->lock,PTHREAD_PROCESS_PRIVATE);
	ret->key = key;
	ret->next = NULL;
	ret->mark = false;
	return ret;
}

/**
 * Free a linked list node.
 **/
static void ll_node_free(ll_node_t *ll_node)
{
	pthread_spin_destroy(&ll_node->lock);
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

int ll_validate(ll_node_t *prev, ll_node_t *curr){
	return (!prev->mark && !curr->mark && prev->next==curr);
}

int ll_contains(ll_t *ll, int key)
{
	ll_node_t *curr;
	curr=ll->head;
	while(curr->key < key){
		curr=curr->next;
	}
	return (!curr->mark && curr->key==key);
}

int ll_add(ll_t *ll, int key)
{
	// printf("add in\n");
	ll_node_t *prev, *curr, *new;
	int flag=-1;
	while(1)
	{
		prev=ll->head;
		curr=prev->next;

		while(curr->key < key){
			prev=curr;
			curr=curr->next;
		}
		pthread_spin_lock(&prev->lock);
		pthread_spin_lock(&curr->lock);
		if(ll_validate(prev,curr)){
			if(curr->key==key)
				flag=0;
			else{
				new=ll_node_new(key);
				new->next=curr;
				prev->next=new;
				flag=1;
			}
		}
		pthread_spin_unlock(&prev->lock);
		pthread_spin_unlock(&curr->lock);
		if (flag==0 || flag==1)
			break;
	}
	// printf("add out\n");
	return flag;
}

int ll_remove(ll_t *ll, int key)
{
	ll_node_t *prev, *curr;
	int flag=-1;
	while(1)
	{
		prev=ll->head;
		curr=prev->next;

		while(curr->key < key){
			prev=curr;
			curr=curr->next;
		}

		pthread_spin_lock(&prev->lock);
		pthread_spin_lock(&curr->lock);
		if(ll_validate(prev,curr)){
			if(curr->key==key){
				curr->mark=true;
				prev->next=curr->next;
				flag=1;
			}
			else{
				flag=0;
			}
		}
		pthread_spin_unlock(&prev->lock);
		pthread_spin_unlock(&curr->lock);
		if(flag==1 || flag==0)
			break;
	}
	return flag;
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
