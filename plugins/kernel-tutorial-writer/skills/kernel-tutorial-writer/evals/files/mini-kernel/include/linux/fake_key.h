#ifndef _LINUX_FAKE_KEY_H
#define _LINUX_FAKE_KEY_H

#include <linux/atomic.h>

struct fake_key {
	atomic_t enabled;
};

static inline bool fake_key_enabled(const struct fake_key *key)
{
	return atomic_read(&key->enabled) > 0;
}

void fake_key_init(void);
void fake_key_enable(struct fake_key *key);
void fake_key_disable(struct fake_key *key);

#endif
