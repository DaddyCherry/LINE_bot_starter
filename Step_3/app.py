import os
import azure_blob_handler as abh

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from dateutil.parser import parse
from dateutil.parser._parser import ParserError

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


def parse_datetime_string(s):
    try:
        return parse(s), True
    except ParserError:
        return None, False


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
        abh.register_patient(event.source.user_id, msg.replace('です', '').replace('。', ''))
        pat_name = abh.get_patient_name(event.source.user_id)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pat_name+'さんですね。\n新規登録が完了しました。')
        )

    elif event.message.text == '予約':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='新規予約します。\n日時を入力してください。\n\n例:2024/2/5 12:25')
        )

    elif '/' in event.message.text and ':' in event.message.text:
        msg = event.message.text
        dt, is_valid = parse_datetime_string(msg)

        if is_valid:
            abh.register_reservation(event.source.user_id, dt.strftime("%Y/%m/%d %H:%M"))
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='予約完了しました。')
            )

        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='無効な入力フォーマットです。\n日時を入力してください。\n\n例:2024/2/5 12:25')
            )

    elif event.message.text == '予約確認':
        pat_name = abh.get_patient_name(event.source.user_id)
        reserve_datetime = abh.get_reservation(event.source.user_id)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pat_name+'さんの次回のご予約は次のとおりです。\n\n'+reserve_datetime)
        )

    elif event.message.text == '予約削除':
        pat_name = abh.get_patient_name(event.source.user_id)
        reserve_datetime = abh.get_reservation(event.source.user_id)
        abh.delete_reservation(event.source.user_id)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pat_name+'さんの次のご予約を削除しました。\n\n'+reserve_datetime)
        )
    
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )



if __name__ == "__main__":
   app.run()
