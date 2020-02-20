import asyncio
from collections import defaultdict

from mockredis import MockRedis as _MockRedis

from .generic import GenericCommandsMixin
from .hash import HashCommandsMixin
from .list import ListCommandsMixin
from .pubsub import PubSubCommandsMixin
from .set import SetCommandsMixin

__all__ = ['MockRedis']


class WrappedMockRedis(_MockRedis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apubsub = defaultdict(asyncio.Queue)

    def publish(self, channel, message):
        super().publish(channel, message)
        self._apubsub[channel].put_nowait(message)

    def subscribe(self, channel, *channels):
        return [self._apubsub[channel].get()] + [self._apubsub[ch].get() for ch in channels]

    def unsubscribe(self, *channels):
        for e in channels:
            while True:
                try:
                    self._apubsub[e].task_done()
                except:
                    break


class MockRedis(GenericCommandsMixin, HashCommandsMixin, ListCommandsMixin, SetCommandsMixin, PubSubCommandsMixin):
    """Fake high-level aioredis.Redis interface"""

    def __init__(self, connection=None, encoding=None, **kwargs):

        # Just for API compatibility
        self._conn = connection
        self._redis = WrappedMockRedis(**kwargs)

        self._encoding = encoding


async def create_redis(address, *, db=None, password=None, ssl=None,
                       encoding=None, commands_factory=MockRedis,
                       loop=None):
    '''Create a fake high-level MockRedis interface

    This function is a coroutine
    '''
    return commands_factory(None, encoding=encoding)
