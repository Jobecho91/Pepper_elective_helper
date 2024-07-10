import requests

def get_rasa_response(message):
    url = "http://localhost:5005/webhooks/rest/webhook"  # Usa la dirección que has visto
    payload = {"sender": "test_user", "message": message}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        messages = response.json()
        if messages:
            return messages[0].get("text")
    return "No response from Rasa."

if __name__ == "__main__":
    test_message = "Hello"
    response = get_rasa_response(test_message)
    print(f"Rasa response: {response}")