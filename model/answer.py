from model.base import Document
from mongoengine import (
                         StringField,
                         SequenceField,
                         DateTimeField,
                         EmbeddedDocument,
                         ReferenceField,
                         ListField,
                         EmbeddedDocumentField,
                         IntField,

)
import datetime
from model.user import User
from model.comment import Comment
from model.question import Question


class Answer(Document):
    star = IntField(default=0)
    content = StringField(default='no content')
    author = ReferenceField(User)
    datetime = DateTimeField(default=datetime.datetime.now())
    comment = ListField(EmbeddedDocumentField(Comment))
    question = ReferenceField(Question)

    @classmethod
    def create_by_userId(cls, author, question, content='answer_content'):
        '''新建回复并更新问题 last_answer '''
        '''author和question都是对象'''
        author = User.objects(id=author).first()
        question = Question.objects(id=question).first()
        if author is not None and question is not None:
            a = Answer(author=author, question=question, content=content)
            a.save()
            a._update_last_answer()
        return None

    def _update_last_answer(self):
        '''更新此问题的最后一个回答'''
        q = Question.objects(id=self.question.id).first()
        q.update_last_answer(str(self.id))

    def inc_star(self):
        '''有人赞了问题就加1'''
        self.star += 1
        self.save()

    @classmethod
    def get_last_answer(cls, question):
        q = question
        if len(q.last_answer) != 0 :
            return cls.objects(id=q.last_answer).first()
        else:
            return None

    def add_comment(self, author, content):
        c = Comment(author=author, content=content)
        self.comment.append(c)
        self.save()
