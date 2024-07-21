import requests
import json
import os
from dotenv import load_dotenv
from whisper_service import get_transcription
from vision_service import gpt_vision_service


load_dotenv()

def get_text_user(message):
    text = ""
    typeMessage = message["type"]

    if typeMessage == "text":
        text = (message["text"])["body"]
    elif typeMessage == "audio":
        
        # Llamar a whisper
        id_audio = message['audio']['id']
        url = get_url_media(id_audio)
        binary_audio = get_binary_media(url)
        transcription = get_transcription(binary_audio);
        text = transcription
        
    elif typeMessage == "document":
        # ver carga RAG
        pass
    elif typeMessage == "image":
        # Llamar a Vision
        id_image = message['image']['id']
        url = get_url_media(id_image)
        binary_image = get_binary_media(url)
        textUser = message['image']['caption']
        image_description = gpt_vision_service(binary_image, 'jpeg', textUser)
        text = image_description
        
    elif typeMessage == "video":
        # Llamar a Vision
        id_video = message['video']['id']
        url = get_url_media(id_video)
        binary_video = get_binary_media(url)
        textUser = message['video']['caption']
        video_description = gpt_vision_service(binary_video, 'mp4', textUser)
        #text = video_description
        
    elif typeMessage == "interactive":
        pass
    else:
        print("sin mensaje")

    return text

def send_message_whatsapp(data):
    try:
        token = os.getenv('WHATSAPP_TOKEN')
        print(token)
        api_url = os.getenv('META_API_MESSAGE')
        print(api_url)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        print(response)

        if response.status_code == 200:
            return True
        
        print(f"Error en el envío: {response.status_code} - {response.text}")

        return False
    except Exception as exception:
        print(exception)
        return False
    


def get_url_media(id_media):
    print(f"Llego a Meta API Media: {id_media}")
    url = f"https://graph.facebook.com/v18.0/{id_media}/"
    headers = {
        'Authorization': f'Bearer {os.getenv("WHATSAPP_CLOUD_API_KEY")}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        print(f"Llego BIEN Meta API Media: {response.json()['url']}")
        return response.json()['url']
    except requests.exceptions.RequestException as error:
        print("Di error en la API Media")
        raise error

def get_binary_media(url):
    headers = {
        'Authorization': f'Bearer {os.getenv("WHATSAPP_CLOUD_API_KEY")}'
    }

    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as error:
        print(error)
        raise error

def get_url_median8n(id_media, token):
    print(f"Llego a Meta API Media: {id_media}")
    url = f"https://graph.facebook.com/v18.0/{id_media}/"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        print(f"Llego BIEN Meta API Media: {response.json()['url']}")
        return response.json()['url']
    except requests.exceptions.RequestException as error:
        print("Di error en la API Media")
        raise error



