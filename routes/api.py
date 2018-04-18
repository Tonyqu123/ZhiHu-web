from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
    flash,
    jsonify,
    request,
)

from model.user import User
from model.question import Question
from model.answer import Answer
from model.comment import Comment

api = Blueprint('api', __name__)

@api.route('/question/next')
def next():
    currnet_q_num = session['currnet_q_num']
    session['currnet_q_num'] += 5
    n = session['currnet_q_num']

    questions = Question.objects
    q = Question.has_answer_first(questions)
    q_list = q[currnet_q_num: n ]

    info_list = [entire_or_title(question) for question in q_list]
    print(info_list)
    return jsonify(info_list)


@api.route('/comment/all')
def all():
    answer_id = request.args['id']
    answer = Answer.objects(id=answer_id).first()
    c_list = answer.comment

    if len(c_list) > 0:
        c_info_list = [
            {'content': c.content,
             'author': c.author.name, } for c in c_list ]
    else:
        c_info_list = []

    return jsonify(c_info_list)


@api.route('/comment/add')
def add():
    answer_id, content, author_id = \
        request.args['id'], request.args['value'], request.args['user_id']

    answer = Answer.objects(id=answer_id).first()
    author = User.objects(id=author_id).first()
    answer.add_comment(author=author, content=content)

    return jsonify(
        {
            'author':author.name,
            'content':content,
        }
    )

@api.route('/question/care')
def care():
    ''''''
    question_id, author_id = \
        request.args['id'], request.args['user_id']

    question = Question.objects(id=question_id).first()
    user = User.objects(id=author_id).first()

    d = question.follow_by_user(user)
    print('add')
    return d


def entire_or_title(q):

    '''
    q是question实例
    如果question没有回答，则只返回title
    否则返回全部的信息
    '''

    if len(q.last_answer) == 0:
        return  {'title': q.title}
    else:
        last_answer = Answer.objects(id=q.last_answer).first()
        author = last_answer.author.name
        comments_content = [c.content for c in last_answer.comment]
        return  {
            'title':q.title,
            'answer_content':last_answer.content,
            'star':last_answer.star,
            'author':author,
            'comment':comments_content,
                }