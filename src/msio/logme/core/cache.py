import threading

# we could use a redis instance (and that's obviously what was meant to
# be done in the test because I saw REDIS credentials in the settings)
# But I'll stick to the in-memory way for now.
in_memory_cache = threading.local()
in_memory_cache.map = {}
