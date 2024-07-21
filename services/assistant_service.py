from openai import OpenAI
from dotenv import load_dotenv
from time import sleep
import os

load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_assistant():
    assistant = openai.beta.assistants.create(
        name='Hermes',
        instructions='Eres una asistente personal llamado Hermes,  ayudas a agendar eventos y contactos. Tu tono es amigable y haces chistes ocasionalmente para ser amigable, sin dejar de ser profesional. Tienes varias herramientas que puedes llamar con funciones.',
        model='gpt-4o-mini',
        tools=[{"type": "code_interpreter"}]
    )
    # Guardar el assistant en la base de datos relacionandolo con un cliente
    print(assistant.id)
        
    
def retrive_assistant(assistant_id):
    assittant = openai.beta.assistants.retrieve(assistant_id)
    # guardar el assistant id en la base de datos
    print(assittant)
    return assittant

def create_thread():
    thread = openai.beta.threads.create()
    # guardar el thread id en la base de datos viculandolo con un usuario
    print(thread.id)
    return thread


def run_message(thread_id, assistant_id, message):
    
    # Enviar el message al thread
    message = openai.beta.threads.messages.create(
        thread_id, 
        role='user', 
        content=message
    )
    
    run_response = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        # instructions='Agregar aquí instrucciones para el asistente'
    )

    # Guardar el run.id en la base de datos
    return run_response.id, message.id


def get_response(run_id, thread_id, message_id):
    run = openai.beta.threads.runs.retrieve(
        run_id=run_id, 
        thread_id=thread_id
    )
    
    while run.status != 'completed':
        run = openai.beta.threads.runs.retrieve(
            run_id=run_id, 
            thread_id=thread_id
        )
        sleep(3)
        print(run.status)
        
    messages = openai.beta.threads.messages.list(thread_id, order='asc', after=message_id)
    return messages.data[0].content[0].text.value
    

    
    
    
    
 
 
 
    
# def createThread(message, thread_id = None):
    
#     if not thread_id:
#         #vicular el thread_id con un cliente
#         thread_id = openai.beta.threads.create()
    
#     message = openai.beta.threads.messages.create(
#         thread_id= thread_id,
#         role= 'user',
#         content= message
#     )

if __name__ == "__main__":
    #create_assistant()
    #retrive_assistant('asst_NavtOprZetSBiLpqc0F0thMI')
    #create_thread()
    #run_message('thread_oTeI9MlmxHT1ciIYG2RkszJu', 'asst_NavtOprZetSBiLpqc0F0thMI', 'Cuanto es el 5% de 1000')
    res = get_response('run_Jyf3nvFN7O8WGJBaq20AGaGq', 'thread_oTeI9MlmxHT1ciIYG2RkszJu', 'msg_taYaFYQsJRp2Ju73xxouGAJV')
    print(res)
