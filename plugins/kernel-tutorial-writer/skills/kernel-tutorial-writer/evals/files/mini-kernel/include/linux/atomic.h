#ifndef _LINUX_ATOMIC_H
#define _LINUX_ATOMIC_H

typedef struct {
	int counter;
} atomic_t;

static inline int atomic_read(const atomic_t *v)
{
	return v->counter;
}

static inline int atomic_inc_return(atomic_t *v)
{
	return ++v->counter;
}

static inline int atomic_dec_return(atomic_t *v)
{
	return --v->counter;
}

#endif
