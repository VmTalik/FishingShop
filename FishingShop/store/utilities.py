from django.template.loader import render_to_string
from django.core.signing import Signer
from FishingShop.settings import ALLOWED_HOSTS
from os.path import splitext
from datetime import datetime

signer = Signer()


def send_activation_notification(user):
    """Функция для рассылки электронных писем"""
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)


def get_timestamp_path(instance, filename):
    "Функция, генерирующая имена сохраняемых в модели выгруженных файлов"
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])