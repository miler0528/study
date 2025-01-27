import requests
import json

url = 'http://localhost:5000/data'  # サーバのURL

# 送信するデータ
data = {
    'temperature': 25,
    'humidity': 60
}

# JSON形式に変換
json_data = json.dumps(data)

# POSTリクエストを送信
response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json_data)

# レスポンスを確認
if response.status_code == 200:
    print('Data successfully sent')
else:
    print(f'Failed to send data, status code: {response.status_code}')
