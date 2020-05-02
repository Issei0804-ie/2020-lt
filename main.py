import slackweb
import urllib.error
import requests

# webhook には Mattermostから発行されたアドレスを入れる
# アドレスが直接入ったまま GitHub などにアップロードしないこと
webhook = ""

# livedoor天気情報さんのAPIを叩く
url = "http://weather.livedoor.com/forecast/webservice/json/v1"

# クエリパラメータの設定
payload = {"city": "471010"}

# エンドポイントにアクセスする
weather_data = requests.get(url, params=payload).json()

print("***************************")
print(weather_data["title"])
# 今日の日付
print(weather_data["forecasts"][0]["date"])
# 今日の天気
print(weather_data["forecasts"][0]["telop"])
print("***************************")

# Mattermostに送信したい内容を代入
content = weather_data["title"] + "\n" + weather_data["forecasts"][0]["date"] + "\n" + weather_data["forecasts"][0]["telop"]


try:
    # アクセス先を引数として渡す
    mattermost = slackweb.Slack(url=webhook)
# URLが間違ってた時のエラー処理
except urllib.error.HTTPError as e:
    print("Slackweb.Slack" + e)
    exit(1)

try:
    # Mattermost に引数の内容を投稿する
    response = mattermost.notify(text=content)
# URLが不正の場合のエラー処理
except (ValueError, urllib.error.HTTPError) as e:
    print(e)
    print("mattermost.notify: 正しいURLを入力してください")
    exit(1)


if response == "ok":
    print("上手に送信できました!!!!")
else:
    print("上手く送信できませんでした。" + response)