void rest_init(void);
void fake_key_enable(struct fake_key *key);

static struct fake_key early_key;

void early_boot_setup(void)
{
	fake_key_enable(&early_key);
}

void start_kernel(void)
{
	early_boot_setup();
	rest_init();
}
