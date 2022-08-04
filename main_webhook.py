import logging
import flask
import telebot
import socket
import sys
import re
import json
import decorator
from subprocess import Popen, PIPE

import settings


def externalIP():
    #return Popen('wget http://ipinfo.io/ip -qO -', shell=True, stdout=PIPE).stdout.read()[:-1]
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr


TELEBOT_TOKEN = settings.TOKEN
WEBHOOK_HOST = externalIP()
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = '0.0.0.0'
# WEBHOOK_SSL_CERT = 'server.crt'
# WEBHOOK_SSL_PRIV = 'server.key'
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TELEBOT_TOKEN)
bot = telebot.TeleBot(TELEBOT_TOKEN)
app = flask.Flask(__name__)


@decorator.decorator
def errLog(func, *args, **kwargs):
    result = None
    try:
        result = func(*args, **kwargs)
    except Exception as e:
        print(e.__repr__())
    return result


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'Hello world!'


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data()
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_messages([update.message])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)


@errLog
def processPhotoMessage(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file = bot.get_file(fileID)
    print('file.file_path =', file.file_path)


@bot.message_handler(content_types=['photo'])
def photo(message):
    processPhotoMessage(message)


def main():
    global data
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    # certificate=open(WEBHOOK_SSL_CERT, 'r')
                    )
    app.run(host=WEBHOOK_LISTEN,
            port=8443,
            # ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=False)


if __name__ == '__main__':
    main()
