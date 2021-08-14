"""Python OPS client wrapper"""

import os

import epo_ops
from epo_ops.middlewares.throttle.storages import SQLite
from dogpile.cache import make_region


CACHE_DIR = os.path.expanduser("~/.python-epo-ops-client")


def region():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    return make_region().configure(
        "dogpile.cache.dbm",
        expiration_time=60 * 60 * 24,  # 1 day in seconds
        arguments={
            "filename": os.path.join(CACHE_DIR, "cache.dbm"),
            "rw_lockfile": False,  # disable locking, because it doesn't work out of the box on windows
            "dogpile_lockfile": False,
        },
    )


def throttle_storage():
    return SQLite(
        db_path=os.path.join(CACHE_DIR, "throttle_history.db"),
    )


def middlewares():
    return [
        epo_ops.middlewares.Dogpile(region=region()),
        epo_ops.middlewares.Throttler(history_storage=throttle_storage()),
    ]


def ops_client():
    ops_key = os.getenv("OPS_KEY")
    if not ops_key:
        raise RuntimeError("'OPS_KEY' environment variable does not exist or is empty.")
    ops_secret = os.getenv("OPS_SECRET")
    if not ops_secret:
        raise RuntimeError(
            "'OPS_SECRET' environment variable does not exist or is empty."
        )
    return epo_ops.Client(
        key=ops_key,
        secret=ops_secret,
        middlewares=middlewares(),
    )


if __name__ == "__main__":
    """Test"""
    client = ops_client()
    response = client.register(
        reference_type="publication",
        input=epo_ops.models.Epodoc(number="EP1000000"),
    )
    print(response.text)
