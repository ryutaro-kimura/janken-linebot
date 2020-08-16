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
def judge(A):
    if A == 0:
        num = random.randint(1,101)
        message = "今" + str(num) + "％だよ！"
    elif A == 1:
        message = "完全に理解した！"
    elif A == 2:
        message = "ピエンなう！"
    elif A == 3:
        message = "元気！！"
    elif A == 4:
        message = "元気100倍アンパンマン！"
    elif A == 5:
        message = "うん！"
    elif A == 6:
        message = "気にすんな！"
    elif A == 7:
        message = "困った時はお互い様だろ？？"
    elif A == 8:
        message = "どいたま！"
    elif A == 9:
        message = "なるほど！"
    elif A == 10:
        message = "わかるわ〜"
    if A == 11:
        message = "ほうほう"

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    b = random.randint(0,2)
    #文字が入力された時、数字を代入
    if event.message.text == "進捗どう？":
        a = random.randint(0,2)
    #文字が入力された時、数字を代入
    elif event.message.text == "元気？":
        a = random.randint(3,5)
    #文字が入力された時、数字を代入
    elif event.message.text == "ありがとう":
        a = random.randint(6,8)
    #文字が入力された時、数字を代入
    else:
        a = random.randint(9,11)

    if b == 0:
        message = "佐藤くん:"
    elif b == 1:
        message = "田中くん:"
    elif b == 2:
        message = "山田さん:"

    message += judge(a)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))



if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
