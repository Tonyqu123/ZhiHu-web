from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    flash,
    url_for,
    session,
    make_response,
)
from model.user import User
from model.question import Question
from flask_mail import Message
from init_app import mail, celery, app


user_page = Blueprint('user', __name__)


@user_page.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        form = request.form
        message = User.register(form)
        flash(message)
        msg = form.get('email')
        send_async_email.apply_async(args=[msg], countdown=10)
        return redirect(url_for('index.index'))
    return render_template('register.html')


@user_page.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        form = request.form
        message = User.login(form)
        flash(message)
        resp = redirect(url_for('index.index'))
        # 增加cookie一个字段 [user_id]
        resp.set_cookie('u_id', value=session['user'])
        return resp
    return render_template('login.html')


@user_page.route('/logout')
def logout():
    session.pop('user')
    flash('登出')
    return redirect(url_for('index.index'))


@user_page.route('/following')
def following():
    user_id = session['user']
    print(type(user_id))
    q_list = Question.get_all_following(user_id)
    return render_template('user_follow.html', questions=q_list)

#
# @celery.task
# def send_email(email):
#     with app.app_context():
#         msg = Message("test delay",
#                       sender="654361635@qq.com",
#                       recipients=[email])
#         mail.send(msg)

@celery.task
def send_async_email(email):
    with app.app_context():
        msg = Message("test delay dddd",
                      sender="654361635@qq.com",
                      recipients=[email])
        mail.send(msg)
        print('sadadadada')