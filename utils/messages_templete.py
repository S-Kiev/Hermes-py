def text_message(text: str, number: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "to": "59897464651",
        "type": "text",
        "text": {
            "body": text
        }
    }
    
    
def image_message(number: str, url: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "image",
        "image": {
            "link": url
        }
    }
    
    
def AudioMessage(number: str, url: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "audio",
        "audio": {
            "link": url
        }
    }
    

def VideoMessage(number: str, url: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "video",
        "video": {
            "link": url
        }
    }
    
def DocumentMessage(number: str, url: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "document",
        "document": {
            "link": url
        }
    }
    
    
def LocationMessage(number: str, localization: dict)-> dict:
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "location",
        "location": {
            "latitude": localization["latitude"],
            "longitude": localization["longitude"],
            "name": localization["name"],
            "address": localization["address"]
        }
    }
    return data




