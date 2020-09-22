from linebot.models import *
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot import (
    LineBotApi, WebhookHandler
)
from sss import *
import requests
import traceback
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, request, abort
import sys
import os
sys.path.append(os.path.abspath("/"))


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'uKVOAb1Bn3EeGsMBjCdRYkYXqrZFIv/ukCFc/SPBYIRsBKTcR92ktaKyY1JKgqW0k00uIyY0uHscO0rJaxMfS+6QBLv3zjMsPgem76rTCrw1NaHvOvDlPBU6sX43W0utxaP9pYCAQeoJNyhvpwUlSAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('066c395ef7192ab55179e5595dd47bf7')


@app.route('/')
def index():
    return 'OK'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    try:
        text = event.message.text

        user_profile = None
        if isinstance(event.source, SourceUser):
            user_profile = line_bot_api.get_profile(event.source.user_id)

        if text == '#โปร':
            if isinstance(event.source, SourceUser):
                profile = line_bot_api.get_profile(event.source.user_id)
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text='Display name: ' +
                                        profile.display_name),
                        TextSendMessage(text='Status message: ' +
                                        str(profile.status_message))
                    ]
                )

            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="Bot can't use profile API without user ID"))
        elif text.startswith('#เลข '):  # broadcast 20190505
            idnum = text.split(' ')[1]
            pdcfind(idnum)
            line_msg = pdcfind(idnum)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=line_msg),
                ]
            )
            if user_profile:
                line_send("{}\n{}".format(user_profile.display_name, line_msg))

        elif text.startswith('#ชื่อ '):  # broadcast 20190505
            xa = text.split(' ')[1]
            xb = text.split(' ')[2]
            xname = xa+' '+xb
            pdcfindname(xname)
            line_msg = pdcfindname(xname)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=line_msg),
                ]
            )
            if user_profile:
                line_send("{}\n{}".format(user_profile.display_name, line_msg))
        else:
            line_msg = "ไม่มีคำสั่งนี้ในระบบ"
            line_bot_api.reply_message(
                event.reply_token, [
                    FlexSendMessage(
                            alt_text='hello',
                            contents={
                                'type': 'bubble',
                                'body': {
                                'type': 'box',
                                'layout': 'vertical',
                                'contents': [
                                    {
                                        'type': 'text',
                                        'text': 'ข้อมูล',
                                        'weight': 'bold',
                                        'size': 'xl',
                                        'margin': 'none',
                                        'align': 'center',
                                        'color': '#1d23e2'
                                    },
                                    {
                                        'type': 'separator'
                                    },
                                    {
                                        'type': 'text',
                                        'text': line_msg,
                                        'align': 'center',
                                        'color': '#03fa03'
                                    }
                                ]
                                }
                            }
                    )
                ]
            )
    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1230))
    app.run(debug=True, host='0.0.0.0', port=port)
