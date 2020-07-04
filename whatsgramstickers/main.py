# from WhatsGramSticker import WhatsGramSticker
import os, re
from time import sleep
from webwhatsapi import WhatsAPIDriver

chromedriver = os.path.join(os.path.dirname(__file__), "chromedriver")
profile_path = os.path.join(os.path.dirname(__file__), "chromeprofile")

driver = WhatsAPIDriver(username="API", client="chrome", profile=profile_path, executable_path=chromedriver)

print(driver.get_all_chats())
# driver.send_message_to_id("553189429782@c.us", "This is a text test message sent from Python. kkkk")


def response(msg: str):
    if re.search(r'(oi|ola|olá|hi|hello)', msg, re.IGNORECASE):
        return "Olá!! Tudo bem?"
    elif 'te amo' in msg:
        return "Eu também amo você!"
    elif 'fofinho' in msg:
        return "Você também é muito fofx!"
    elif 'tchau' in msg:
        return "Que pena que você já vai :(. Tchauzinho. Bom conversar com você."
    else:
        return "Ehr... Bruh... Pi pi pi... Ainda não aprendi o que você disse..."


while True:
    unread = driver.get_unread()
    for msg_group in unread:
        print(msg_group)
        print(f'Message from <{msg_group.chat.id}>.')
        for message in msg_group.messages:
            print("--------------------------------------------------------------")
            print(f"{message.type} from {message.sender}.")
            if message.type == 'chat':
                print(f"[{message.timestamp}]: {message.content}")
                driver.send_message_to_id(message.chat_id, response(message.content))
            elif message.type == 'sticker':
                print(f'[       Size]: {message.size}')
                print(f'[       MIME]: {message.mime}')
                print(f'[    Caption]: {message.caption}')
                print(f'[  Media Key]: {message.media_key}')
                print(f'[ Client URL]: {message.client_url}')
                print(f'[   Filename]: {message.filename}')
                message.save_media(os.path.dirname(__file__), True)
            print(f'Chat id: {message.chat_id}')
            print("--------------------------------------------------------------")


    sleep(5)





# WGS = WhatsGramSticker()