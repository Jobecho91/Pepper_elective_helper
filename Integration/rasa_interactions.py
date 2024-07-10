import requests

def get_rasa_response(message):
    url = "http://localhost:5005/webhooks/rest/webhook"  # URL of the Rasa server
    payload = {"sender": "pepper", "message": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # raise an exception in case of an error
        messages = response.json()
        if messages:
            #print("MESSEEE:", messages)
            texts = [msg.get("text") for msg in messages if msg.get("text")]
            entities = [msg.get("entities", []) for msg in messages if msg.get("entities")] # Get the entities but it doesnt work as expected
            return texts, entities
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Rasa server: {e}")
    return ["Sorry, I didn't understand that."], []