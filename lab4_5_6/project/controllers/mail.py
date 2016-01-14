# -*- coding: utf-8 -*-
import json

from bottle import request, response

from lab4_5_6.project import app
from lab4_5_6.project.models.fields.EmailField import EmailField
from lab4_5_6.project.models.fields.IdField import IdField
from lab4_5_6.project.models.fields.MessageField import MessageField
from lab4_5_6.project.models.fields.ThemeField import ThemeField
from lab4_5_6.project.models.mail import Mail


@app.route('/mail.:act', method=['GET', 'POST'])
def get(act):
    response.content_type = 'application/json'
    if act == 'get':
        return get()
    elif act == 'save':
        return save()
    elif act == 'count':
        return count()


def get():
    mail = Mail()
    try:
        if request.query.offset != '':
            offset = int(request.query.offset)
            if mail.findByOffset(offset):
                return json.dumps(
                    {"id": str(mail.id), "to": str(mail.to), "from": str(mail.from_), "theme": str(mail.theme),
                     "message": str(mail.message)})
            return "not row"
    except:
        return json.dumps({"status": "error", "error_message": "error"})
    return json.dumps({"status": "error", "error_message": "offset not passed"})


def save():
    # try:
    #     mail = findByID()
    # except NoSuchID
    #     try:
    #         mail = Mail(theme = aaa,message = nnn,c)
    #     except NotValidTheme
    #         pass
    #     except NotValidMessage
    #         pass

    mail = Mail()
    try:
        mail.findById(int(request.query.id))
        mail.id = IdField(int(request.query.id))
        if request.query.to != '':
            mail.to = EmailField(request.query.to)
        # if (request.query['from'] != ''):
        #     mail.from_ = request.query['from']
        if request.query.theme != '':
            mail.theme = ThemeField(request.query.message)
        if request.query.message != '':
            mail.message = MessageField(request.query.message)
        mail.save()
        return json.dumps({"status": "response", "data": "OK"})
    except:
        raise
        return json.dumps({"status": "error", "error_message": "error"})


def count():
    return str(0)
