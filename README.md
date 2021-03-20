# Python OPS client wrapper

A thin wrapper around `python_epo_ops_client`. The wrapper disables
file locking for dogpile cache and sets a default directory for the
cache and the throttle db file inside the user home directory. The
client assumes that OPS_KEY and OPS_SECRET are set as environment
variables.

