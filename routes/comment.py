from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
    flash,
)

from model.user import User
from model.question import Question
from model.answer import Answer


comment_page = Blueprint('comment', __name__)


@comment_page.route('/<string:id>')
def add_star(id):
    if session.get('user') is not None:
        a = Answer.objects(id=id).first()
        a.inc_star()
        return redirect(url_for('index.index'))
    flash('请先登录')
    return redirect(url_for('user.login'))

