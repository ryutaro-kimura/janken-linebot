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



#返答を決める変数
def judge(userhand, bothand):
    if userhand == -1:
        message = "なるほど！"
    else:
        status = (userhand - bothand + 3) % 3

        if status == 0:
            message = "今"
        elif status == 1:
            message = "お前の負け。"
        elif status == 2:
            message = "あなたの勝ち！"

    return message


#呪文
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

#入力値に応じてuser_handを変更
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #bot_hand = random.randint(0,2)
    if event.message.text == "進捗どう？":
        user_hand = 0
        progress_response = random.randint(0,2)
        #message = "グーが入力されました。"
    elif event.message.text == "元気？":
        user_hand = 1
        #message = "チョキが入力されました。"
    elif event.message.text == "ありがとう":
        user_hand = 2
        #message = "パーが入力されました。"
    else:
        user_hand = -1


    if progress_response == 0:
        message = "いい感じ！\n"
    elif progress_response == 1:
        num = random.randint(1,100)
        message = "今" + str() + "％くらい！\n"
    elif progress_response == 2:
        message = "ピエンなう！\n"

    message += judge(user_hand, bot_hand)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
