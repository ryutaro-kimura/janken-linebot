from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage
)
import os
import random

app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def judge(userhand, bothand):
    if userhand == -1:
        message = "グー、チョキ、パーのどれかを入力してね"
    else:
        status = (userhand - bothand + 3) % 3

        if status == 0:
            message = "まさこです。"
        elif status == 1:
            message = "お前の負け。"
        elif status == 2:
            message = "あなたの勝ち！"
    return message



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
def handle_message(event):
    bot_hand = random.randint(0,2)
    if event.message.text == "グー":
        user_hand = 0
        #message = "グーが入力されました。"
    elif event.message.text == "チョキ":
        user_hand = 1
        #message = "チョキが入力されました。"
    elif event.message.text == "パー":
        user_hand = 2
        #message = "パーが入力されました。"
    else:
        user_hand = -1

    if bot_hand == 0:
        message = "botはグーを出しました。\n"
    elif bot_hand == 1:
        message = "botはチョキを出しました。\n"
    elif bot_hand == 2:
        message = "botはパーを出しました。\n"

    message += judge(user_hand, bot_hand)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
