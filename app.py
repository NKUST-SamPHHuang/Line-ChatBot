from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('ldupQY1gKd9ca1aDm+aUwd4orpihn1tA4t6TWQnZuVnpGEY6g/UDfjerRmMK4lwyJCvL4YN5K6tACZFa8FYVd7Yf/A/zMU7d2hz92tOHMNTzm+aZUlxQzbY8Kr/Ngfe1t2aznY8PSBKtZKcPWsHtbwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('28c2b52a2baaad892093d05f5aac9f01')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()