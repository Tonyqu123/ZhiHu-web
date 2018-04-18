from flask import (
    Blueprint,
    render_template,
    redirect,
    g,
    session,
)
from model.user import User
from model.question import Question
from model.answer import Answer


index_page = Blueprint('index', __name__)


@index_page.route('/')
def index():
    # num 表示想要显示问题的数量
    print(Question._should_update)
    questions = Question.cache_all()
    q = Question.has_answer_first(questions)
    current_num = session['currnet_q_num'] = 3

    q_answer = {q: Answer.get_last_answer(q) for q in questions}
    given_question_list = q[:current_num]
    #q_answer 格式 {question: answer}
    return render_template('index.html',
                           article_list=given_question_list,
                           answer=q_answer,
                           )