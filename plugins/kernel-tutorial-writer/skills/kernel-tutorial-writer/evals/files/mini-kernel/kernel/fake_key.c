#include <linux/fake_key.h>

static bool fake_key_ready;
static void fake_key_update(struct fake_key *key, bool on);

void fake_key_init(void)
{
	fake_key_ready = true;
}

void fake_key_enable(struct fake_key *key)
{
	int count = atomic_inc_return(&key->enabled);

	if (count == 1 && fake_key_ready)
		fake_key_update(key, true);
}

void fake_key_disable(struct fake_key *key)
{
	int count = atomic_dec_return(&key->enabled);

	if (count == 0 && fake_key_ready)
		fake_key_update(key, false);
}

static void fake_key_update(struct fake_key *key, bool on)
{
	/* Walk sites and patch nop <-> jmp. Fixture body omitted. */
	(void)key;
	(void)on;
}
