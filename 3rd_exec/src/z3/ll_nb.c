#include <stdio.h>
#include <stdlib.h> /* rand() */
#include <limits.h>

#include "../common/alloc.h"
#include "ll.h"
#include <stdbool.h>

typedef struct ll_node {
	int key;
	struct ll_node *next;
} ll_node_t;

struct linked_list {
	ll_node_t *head;
};

typedef struct window{
	ll_node_t *prev;
	ll_node_t *curr;	
}window_t;

/**
 * Create a new linked list node.
 **/
static ll_node_t *ll_node_new(int key)
{
	ll_node_t *ret;

	XMALLOC(ret, 1);
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

ll_node_t *getReference(ll_node_t *node)
{
	ll_node_t *next_ref;
	next_ref = (ll_node_t *) ((unsigned long long)node & -1);
	return next_ref;
}

ll_node_t *get(ll_node_t *node, bool *mark)
{
	ll_node_t *next_ref;
	*mark = (bool) ((unsigned long long) node & 1);
	next_ref = (ll_node_t *) ((unsigned long long) node & -1);
	return next_ref;
}


bool compareAndset(ll_node_t *node, ll_node_t *expectedRef, ll_node_t *updateRef, bool expectedMark, bool updateMark)
{
	ll_node_t *expected, *update;
	bool ret;
	expected = (ll_node_t *) ((unsigned long long) expectedRef & expectedMark);
	update = (ll_node_t *) ((unsigned long long) updateRef & updateMark);
	ret=__sync_bool_compare_and_swap(&node,expected,update);
	return ret;
}

window_t find(ll_t *ll, int key){
	ll_node_t *prev=NULL, *curr=NULL, *succ=NULL;
	window_t ret;
	bool mark=false, snip;
retry:
	while(true){
		prev=ll->head;
		curr=getReference(prev->next);
		while(true){
			succ = get(curr->next,&mark);
			while(mark){
				snip = compareAndset(prev->next,curr,succ,false,false);
				if(!snip) goto retry;
				curr = succ;
				succ = get(curr->next,&mark);
			}
			if(curr->key >= key){
				ret.prev=prev;
				ret.curr=curr;
				return ret;
			}
			prev = curr;
			curr = succ;
		}
	}
}

int ll_contains(ll_t *ll, int key)
{
	bool mark;
	ll_node_t *curr;
	curr = ll->head;
	while(curr->key<key)
		curr=curr->next;
	get(curr,&mark);
	return (curr->key==key && !mark);
}

int ll_add(ll_t *ll, int key)
{
	bool slice;
	ll_node_t *prev=NULL, *curr=NULL, *node=NULL;	
	window_t ret;
	// XMALLOC(ret,1);
	while(true){
		ret = find(ll,key);	
		prev = ret.prev;
		curr = ret.curr;
		
		if (curr->key==key){
				// XFREE(ret);
				return false;
			}
		else{
			node = ll_node_new(key);
			node->next = curr;
			if(compareAndset(prev->next,curr,node,false,false)){
				// XFREE(ret);	
				return true;
			}
		}
	}
	return 0;
}

int ll_remove(ll_t *ll, int key)
{
	ll_node_t *prev=NULL, *curr=NULL, *succ=NULL;	
	window_t ret;
	bool snip;
	while(true){
		// XMALLOC(ret,1);
		ret=find(ll,key);	
		prev = ret.prev;
		curr = ret.curr;
		// XFREE(ret);
		if (curr->key!=key)
			return false;
		else{
			succ = getReference(curr->next);
			snip = compareAndset(curr->next,succ,succ,false,true);
			if(!snip)
				continue;
			compareAndset(prev->next,curr,succ,false,false);
			return true;
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
