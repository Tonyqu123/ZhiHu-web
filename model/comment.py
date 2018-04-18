from model.base import Document
from mongoengine import (
                         StringField,
                         SequenceField,
                         DateTimeField,
                         EmbeddedDocument,
                         ReferenceField,
                         ListField,
)
import datetime
from model.user import User


class Comment(EmbeddedDocument):
    content = StringField(default='')
    author = ReferenceField(User)
    datetime = DateTimeField(default=datetime.datetime.now())

