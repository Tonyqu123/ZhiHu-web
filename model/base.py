from mongoengine import (Document as BaseDocument,
                         QuerySet,
                         DoesNotExist,
                         ValidationError,
                         )
from flask import abort
import redis

class BaseQuerySet(QuerySet):
    '''
    自定义查询，方便修改查询不到时候的返回值
    '''

    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except (DoesNotExist, ValidationError):
            abort(404)


class Document(BaseDocument):
    meta = {
        'abstract': True,
        'queryset_class': BaseQuerySet,
    }


class Cache(object):

    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def __repr__(self):
        return '{}-->dict-->{}'.format(self.__class__.__name__,
                                       self.cache.values()
                                       )


class RedisCache(Cache):
    import redis
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)

    def get(self, key):
        return RedisCache.redis_db.get(key)

