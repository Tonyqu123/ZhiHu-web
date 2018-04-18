from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
    request,
    flash,
)

from model.user import User
from model.question import Question
from model.answer import Answer

question_page = Blueprint('question', __name__)


@question_page.route('/<string:id>')
def article(id):
    question = Question.objects(id=id).first()
    answer_list = Answer.objects(question=question)
    return render_template('article.html',
                           artcile=question,
                           answer_list=answer_list,
                           )





@question_page.route('/new_answer/<id>', methods=['POST','GET'])
def add_answer(id):
    user_id = session.get('user')
    if user_id is not None:
        if request.method == 'POST':
            content = request.form['content']
            Answer.create_by_userId(
                author=user_id,
                question=id,
                content=content,
            )
            return redirect(url_for('index.index'))

        q = Question.objects(id=id).first()
        return render_template('new_answer.html', question=q)

    flash('请先登录')
    return redirect(url_for('index.index'))




@question_page.route('/new', methods=['POST','GET'])
def new():
    user_id = session.get('user')
    if user_id is not None:
        if request.method == 'POST':
            form = request.form
            Question.new(form, user_id)
            return redirect(url_for('index.index'))
        return render_template('new_question.html')
    flash('请先登录')
    return redirect(url_for('index.index'))