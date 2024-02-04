import os
import azure_blob_handler as abh

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

    if event.message.text == '新規登録':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='新規登録します。\n名前（カタカナ）を入力してください。\n\n例:ヤマダタロウです')
        )
    
    elif 'です' in event.message.text:
        msg = event.message.text
        abh.write_entity_to_patient_table(event.source.user_id, msg.replace('です', '').replace('。', ''))
        pat_name = abh.get_name_from_patient_table(event.source.user_id)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pat_name+'さんですね。\n新規登録が完了しました。')
        )



if __name__ == "__main__":
   app.run()
