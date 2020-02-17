from fakeredis import FakeStrictRedis

MockRedis = FakeStrictRedis


async def create_redis(address, *, db=None, password=None, ssl=None,
                       encoding=None, commands_factory=MockRedis,
                       loop=None):
    '''Create a fake high-level MockRedis interface

    This function is a coroutine
    '''
    return FakeStrictRedis(address, db, password, ssl, encoding)

