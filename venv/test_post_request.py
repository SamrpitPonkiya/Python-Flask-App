import requests

url = 'http://localhost:5000/whatsapp-webhook'
headers = {
    'Content-Type': 'application/json'
}
data = {
    "entry": [
        {
            "changes": [
                {
                    "value": {
                        "messages": [
                            {
                                "timestamp": "1654038530",
                                "from": "user_id",
                                "id": "message_id_1",
                                "type": "text",
                                "text": {
                                    "body": "Hello!"
                                },
                                "context": {
                                    "group_id": "123456@group.whatsapp.com",
                                    "participant": "participant_id"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
}


response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.text)
