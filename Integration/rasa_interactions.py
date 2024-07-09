

import requests

def get_rasa_response(message):
    url = "http://localhost:5005/webhooks/rest/webhook"  # Cambia esto si tu servidor Rasa está en otra dirección
    payload = {"sender": "pepper", "message": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Esto arrojará una excepción para errores HTTP
        messages = response.json()
        if messages:
            texts = [msg.get("text") for msg in messages if msg.get("text")]
            entities = [msg.get("entities", []) for msg in messages if msg.get("entities")]
            return texts, entities
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Rasa server: {e}")
    return ["Sorry, I didn't understand that."], []