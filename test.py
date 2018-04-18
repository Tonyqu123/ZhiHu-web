from mongoengine import connect
from model.question import Question
# from model.user import User
# from model.answer import Answer
#
connect('test2')
# #
# for i in range(5):
#     print(Question._should_update)
#     t = 'test{}'.format(i)
#     a = Question._test(title=t)


# a = Artcile(title='hahaha')
# # # print(a.date_modified)
# # # # a.save()
# # #
# # b = User.objects(name='qu').first()
# # b.update_img('../static/img/touxiang/t.jpg')
# # # # b.save()
# # # # print(b.artcile)
# # #
# # # a = Artcile(title='x', author=b)
# # # # a.save()
# # #
# # # a.new_reply('q')
# # # # a.save()
# # # c = Artcile.objects(title='x').first()
# # # print([r.author.name for r in c.replies])
# #
# u = User.objects(name='qu').first()
# Question(title='test', author=u).save()
# # q = Question.objects(title='test').first()
# # print(q)
#
# # Answer.create_by_user(author=u.id, question=q.id)
# # q.add_new_answer(content='回答了一堆东西', author=b)
# # q.save()
from collections import namedtuple, OrderedDict, deque
from array import array

