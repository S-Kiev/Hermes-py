import os
import tempfile
import base64
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def gpt_vision_service(binary_media, media_type='jpeg', text_user=None):
    try:
        openai = OpenAI(os.getenv("OPENAI_API_KEY"))

        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{media_type}') as temp_file:
            temp_file.write(binary_media)
            temp_file_path = temp_file.name

        with open(temp_file_path, 'rb') as media_file:
            base64_image = base64.b64encode(media_file.read()).decode('utf-8')

        text_user = text_user if text_user else "Describe la imagen"
    
        response = openai.Completion.create(
            model='gpt-4-vision-preview',
            messages=[
                { 
                    "role": "system", 
                    "content": [
                        {
                            "type": "text",
                            "text": "Eres un asistente de facturación que recibe imagenes de facturas. Si la imagen es una factura quiero que inicies tu respuesta explicitamnte como: 'quiero facturar'. En tu respuesta debes identificar los siguientes datos: el número de la consulta/factura, el número de cliente, el costo total. Ademas debes inferir en base al costo y a cuanto fue abonado el estatus de la factura, cuyos valores posibles pueden ser:\n 1- total (cuando se ha pagado el total de la cuenta)\n 2- partial (cuando es pacial y no se ha abonado el 100%)\n 3- pending (cuando esta pendiente porque el cliente ha abonado 0)\n\n caso no sea una factura solo describe lo que ves \n\n  nombra cada elemento para identifiacarlo, ejemplo: 'N° Consulta: 1', 'N° Cliente: 1', 'Pago: 1000', 'Abono: 500', 'Estatus: partial'"
                        }
                    ] 
                },
                { 
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": text_user
                        },
                        {
                            "type": "image_url",
                            "image_url":  f"data:image/{media_type};base64,{base64_image}",
                        }
                    ] 
                }
            ]
        )

        # Borra el archivo temporal después de usarlo
        os.remove(temp_file_path)

        return response.choices[0].message.content

    except Exception as error:
        # Borrar el archivo temporal en caso de error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        print(error)
        raise error
