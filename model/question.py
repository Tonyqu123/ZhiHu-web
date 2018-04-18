from mongoengine import (
    StringField,
    SequenceField,
    DateTimeField,
    ReferenceField,
    ListField,
    EmbeddedDocumentField,
    IntField,
    queryset_manager,
)
import datetime
from model.base import Document
from model.user import User
from flask import jsonify
from .base import Cache, RedisCache


class Question(Document):
    followers = IntField(default=0)
    title = StringField(max_length=100, required=True)
    content = StringField(default='no content')
    date_modified = DateTimeField(default=datetime.datetime.now())
    author = ReferenceField(User, dbref=False, required=True)
    _last_answer_id = StringField(default='')

    _should_update = False
    cache = Cache() # MemoryCache
    redis_cache = RedisCache() # 与Cache接口一致


    def save(self, force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, signal_kwargs=None, **kwargs):
        '''调用save后缓存失效'''
        self.__class__._should_update = True
        super(Question, self).save()

    @queryset_manager
    def objects(doc_cls, queryset):
        '''使查询按日期倒序排列'''
        return queryset.order_by('-date_modified')

    @property
    def last_answer(self):
        if self._last_answer_id is not None:
            return self._last_answer_id
        return None

    def update_last_answer(self, answer_id):
        '''把最后一个回答的id保存'''
        # print(self)
        self._last_answer_id = answer_id
        self.save()

    @classmethod
    def new(cls, form, id):
        '''
        :param form: flask 模块中的 request.form变量
        :param id: user _ id
        :return: 创建新的question 并保存，不return 值
        '''
        t = form.get('title')
        c = form.get('content')
        user = User.objects(id=id).first()
        cls(title=t, content=c, author=user).save()

    @classmethod
    def _test(cls, title='test'):
        author = User.objects(name='qu').first()
        cls(title=title, author=author).save()

    @classmethod
    def has_answer_first(cls, questions):
        '''questions 是需要进行排列的列表'''
        answer_first = [q for q in questions if q.last_answer]
        for q in questions:
            if q not in answer_first:
                answer_first.append(q)
        return answer_first

    def follow_by_user(self, user):
        if str(self.id) not in user.following:
            self.followers += 1
            self.save()
            user.following.append(str(self.id))
            user.save()
            d = jsonify({'span': '成功添加关注'})
        else:
            d = jsonify({'span': '您已添加关乎，不要重复点击'})
        return d

    @classmethod
    def get_all_following(self, user_id):
        u = User.objects(id=user_id).first()
        follow = [Question.objects(id=q).first() for q in u.following]
        return follow

    @classmethod
    def cache_all(cls):
        if cls._should_update == True:
            cls.cache.set('all_questions', cls.objects())
            cls._should_update = False
        return cls.cache.get('all_questions')
