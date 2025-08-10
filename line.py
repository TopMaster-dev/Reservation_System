from linebot.v3.messaging import MessagingApi, PushMessageRequest, TextMessage
from linebot.v3.messaging import Configuration, ApiClient
from linebot.exceptions import LineBotApiError

CHANNEL_ACCESS_TOKEN = '6Tqs0gH5irqefUnJEPimcJbpJSvLwA/sKkdvo3UDocCxkQ8LDqyJy99CnBfcoRQA3j2pKVthvjtkD0vytUcLNYmqk1XYXEEKifTHopJu89YBrWTpBUwnhS2L6yex1h7ToJnIiQS5qC24H3jH5wdEXwdB04t89/1O/w1cDnyilFU='
USER_ID = "U2b729a9c0f5b435b6e81807a21ba908f"

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

def line_bot():
    try:
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            messaging_api.push_message(
                PushMessageRequest(
                    to=USER_ID,
                    messages=[TextMessage(text="予約いたしました。ご確認いただけますと幸いです。")]
                )
            )
        return True
    except LineBotApiError as e:
        print(f"Failed to send message: {e.status} {e.body}")
        return False