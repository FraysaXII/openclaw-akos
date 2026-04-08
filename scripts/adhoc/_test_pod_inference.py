import json, urllib.request
url = 'https://y7hdyssezt8h6j-8080.proxy.runpod.net/v1/chat/completions'
payload = json.dumps({
    'model': 'deepseek-r1-70b',
    'messages': [{'role': 'user', 'content': 'Reply with exactly one word: READY'}],
    'max_tokens': 20,
    'temperature': 0
}).encode()
req = urllib.request.Request(url, data=payload, headers={'Content-Type':'application/json'})
with urllib.request.urlopen(req, timeout=180) as resp:
    body = resp.read().decode()
print(body[:1000])
