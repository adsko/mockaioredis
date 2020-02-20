from aioredis.commands import PubSubCommandsMixin as PubSubCommandsMixin_


class PubSubCommandsMixin(PubSubCommandsMixin_):
    async def publish(self, channel, message):
        self._redis.publish(channel, message)

    async def subscribe(self, channel, *channels):
        return self._redis.subscribe(channel, *channels)

    async def unsubscribe(self, channel, *channels):
        return self._redis.unsubscribe(channels, *channels)
