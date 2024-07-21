import requests
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

def get_transcription(binary_audio):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_file:
            temp_file.write(binary_audio)
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, 'rb') as audio_file:
                files = {
                    'file': (os.path.basename(temp_file_path), audio_file, 'audio/ogg')
                }
                data = {
                    'model': 'whisper-1'
                }
                headers = {
                    'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}'
                }

                response = requests.post(
                    'https://api.openai.com/v1/audio/transcriptions',
                    headers=headers,
                    files=files,
                    data=data
                )

                response.raise_for_status()
                transcription_text = response.json().get('text', '')

            # Borra el archivo temporal después de usarlo
            os.remove(temp_file_path)

            return transcription_text
        except Exception as err:
            # Si algo sale mal, borrar el archivo temporal de todas formas
            os.remove(temp_file_path)
            print(err)
            raise err
    except Exception as error:
        print(error)
        raise error
