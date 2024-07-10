import requests

def get_rasa_response(message):
    url = "http://localhost:5005/webhooks/rest/webhook"  # Cambia esto si tu servidor Rasa está en otra dirección
    payload = {"sender": "tester", "message": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Esto arrojará una excepción para errores HTTP
        messages = response.json()
        
        # Depuración: imprimir la respuesta completa del servidor
        print("Full Rasa response:")
        print(messages)
        
        texts = [message.get("text") for message in messages if "text" in message]
        entities = []
        for message in messages:
            if 'entities' in message:
                entities.extend(message['entities'])
            elif 'parse_data' in message and 'entities' in message['parse_data']:
                entities.extend(message['parse_data']['entities'])
        return texts, entities
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Rasa server: {e}")
    return [], []

def main():
    print("Type 'exit' to quit")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit', 'q']:
            break
        texts, entities = get_rasa_response(user_input)
        print("Rasa response:")
        for text in texts:
            print(text)
        print("Entities found:")
        if entities:
            for entity in entities:
                print(entity)
        else:
            print("No entities found")

if __name__ == "__main__":
    main()
