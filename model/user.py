from flask import session, request
from mongoengine import (
                         StringField,
                         SequenceField,
                         DateTimeField,
                         ListField,
                         )
import datetime
from model.base import Document


class User(Document):
    name = StringField()
    password = StringField(default='')
    ct = DateTimeField(default=datetime.datetime.now())
    img_url = StringField(default='')
    following = ListField(StringField(default=None))
    like_answer = ListField(StringField(default=None))

    def like_comment(self, id):
        self.like_answer.append(id)

    def update_img(self, url):
        self.img_url = url
        self.save()

    @classmethod
    def register(cls, form):
        username = form.get('username', None)
        password = form.get('password', None)
        if username is None or password is None:
            return 'failed'
        u = cls(name=username, password=password)
        u.save()
        return '{}注册成功'.format(u.name)

    @classmethod
    def login(cls, form):
        username = form.get('username', None)
        password = form.get('password', None)
        u = cls.objects(name=username).first()
        if u is None:
            return 'no such user'
        elif u.password != password:
            return 'wrong password'
        else:
            session['user'] = str(u.id)
            return '{}登录成功'.format(u.name)