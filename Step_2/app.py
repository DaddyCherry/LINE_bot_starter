import os
import azure_table_handler as abh

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!!'

# if __name__ == '__main__':
#     app.run()

YOUR_CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
YOUR_CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info(body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.reply_token)

    if event.message.text == '出勤':
        abh.write_entity_to_shift_table(event.source.user_id, 'IN')

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='出勤記録しました。今日も一日頑張りましょう！')
        )
    
    elif event.message.text == '退勤':
        abh.write_entity_to_shift_table(event.source.user_id, 'OUT')

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='退勤記録しました。お疲れ様でした！')
        )
    
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    


if __name__ == "__main__":
   app.run()
