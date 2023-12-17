import requests

url = 'https://api.matgim.ai/54edkvw2hn/api-keyword-slang'
headers = {
    'content-type': 'application/json',
    'x-auth-token': '5ea265fc-0070-4e8b-a0e3-f0ca42451ea4'
}
data = {
    'document': '안녕하세요 존나 시끄럽네 '
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

response_data = result.get('result', {}).get('data', [])
if response_data:
    print("욕설이 포함되어 있습니다.")
    for item in response_data:
        if item['category'] == 'vulgarism':
            print(f"텍스트: {item['text']}")
else:
    print("욕설이 포함되어 있지 않습니다.")
