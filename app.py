import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from dotenv import load_dotenv
from flask import Flask, request
from services.whatsapp_service import send_message_whatsapp, get_text_user
from utils.messages_templete import text_message

from utils.welcome import welcome 
from services.vision_service import gpt_vision_service
from services.whisper_service import get_transcription
from services.whatsapp_service import get_binary_media, get_url_media

app = Flask(__name__)

load_dotenv()

@app.route("/welcome", methods=["GET"])
def index(): return welcome()



@app.route('/whatsapp', methods=['GET'])
def verify_token():
    try:
        accessToken = os.getenv('ACCESS_TOKEN')
        print(accessToken)
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token is not None and challenge is not None and token == accessToken:
            return challenge
        else:
            return "", 400
    except Exception as e:
        return "", 400

@app.route('/whatsapp', methods=['POST'])
def received_message():
    try:
        body = request.get_json()
        entry = (body["entry"])[0]
        changes = (entry["changes"])[0]
        value = changes["value"]
        message = (value["messages"])[0]
        number = message["from"]
        text = get_text_user(message)
          
       # Enviar el text a GPT para procesar la respuesta   
          
       # Aqui se usa el modelo de mensaje de texto pero pueden usarse otros   
        data = text_message(text, number)
        
        if send_message_whatsapp(data):
            print("Mensaje enviado exitosamente")
        else:
            print("Error al enviar el mensaje")
        
        print(text)
    

        return "EVENT_RECEIVED"
    except Exception as e:
        return "EVENT_RECEIVED"
    
    
    
@app.route('/vision', methods=['POST'])
def received_vision():
    try:
        body = request.get_json()
        
        if body is None:
            return "Solicitud de JSON vacío", 400
        
        id_media = body["id_media"]
        media_type = body["media_type"]
        user_message = body["user_message"]
        if id_media is None or media_type is None or user_message is None:
            return "Falta el id o el tipo de la imagen", 400
        
        url = get_url_media(id_media)
        binary = get_binary_media(url)
        image_description = gpt_vision_service(binary, media_type, user_message)
        
        return {'desciption': image_description}, 200
        
    except Exception as e:
        return e
    
    
@app.route('/audio', methods=['POST'])
def received_audio():
    try:
        body = request.get_json()
        
        if body is None:
            return "Solicitud de JSON vacío", 400
        
        id_media = body["id_media"]
        if id_media is None:
            return "Falta el id del audio", 400
        
        url = get_url_media(id_media)
        binary = get_binary_media(url)
        audio_transcription = get_transcription(binary)
        
        return {'desciption': audio_transcription}, 200
        
    except Exception as e:
        return e

if __name__ == '__main__':
    app.run(debug=True)