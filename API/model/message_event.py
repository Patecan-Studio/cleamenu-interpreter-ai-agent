import datetime as dt

from marshmallow import Schema, fields


class MessageEvent(object):
    def __init__(self, msg_id, text):
        self.msg_id = msg_id
        self.text = text


class MessageEventSchema(Schema):
    msg_id = fields.Str(required=True)
    text = fields.Str(required=True)
