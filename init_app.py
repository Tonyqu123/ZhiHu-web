from flask import Flask
from flask_mail import Mail
from celery import Celery


app = Flask(__name__)
app.config.update(dict(
    MAIL_SERVER='smtp.qq.com',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_PASSWORD='xeaujznlyyzhbefa',
    MAIL_USERNAME='654361635@qq.com',
))
mail = Mail(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

celery.conf.update(app.config)