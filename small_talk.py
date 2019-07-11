import apiai
import json
import jelios
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from my_data import MyVkData
from jelios import send_message

def send_message_dialoge(message):
    request = apiai.ApiAI(MyVkData.client_token).text_request()
    request.lang = "en"
    request.session_id = "session_1"
    request.query = message
    response = json.loads(request.getresponse().read().decode("utf-8"))
    print(response['result']['fulfillment']['speech'])
    return response['result']['action']

def dialoge():
    send_message(jelios.vk_session, jelios.id_type, jelios.id, message='для выхода из диалога напишите !выход')
    while True:
        try:
            for event in jelios.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    message = event.text.lower()
                    print(message)
                    if message != '!выход':
                        send_message_dialoge(message)
                    else:
                        return 0


        except BaseException:
            print('Упс! Что-то пошло не так')
