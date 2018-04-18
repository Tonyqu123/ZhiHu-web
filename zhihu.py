from mongoengine import connect
from routes.index import index_page
from routes.question import question_page
from routes.user import user_page
from routes.comment import comment_page
from routes.api import api
from init_app import app

import logging

app.register_blueprint(index_page)
app.register_blueprint(question_page, url_prefix='/question')
app.register_blueprint(user_page, url_prefix='/user')
app.register_blueprint(comment_page, url_prefix='/comment')
app.register_blueprint(api, url_prefix='/api')

app.debug = True
app.secret_key = 's123'

handler = logging.FileHandler('app.log', encoding='UTF-8')
app.logger.addHandler(handler)

if __name__ == '__main__':
    connect('test2')
    app.run()
