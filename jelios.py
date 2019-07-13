from vk_api.longpoll import VkLongPoll, VkEventType, VkMessageFlag
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
import apiai
import json
import random
import small_talk
from my_data import MyVkData
from datetime import datetime

group_token = MyVkData.group_token
vk_session = vk_api.VkApi(token=group_token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

print("develop branch")

def create_keyboard(response):
    keyboard = VkKeyboard(one_time=True)

    if response == '!тык':
        keyboard.add_button('!оскорбиться', color=VkKeyboardColor.DEFAULT)

        keyboard.add_line()
        keyboard.add_button('!тык', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('!small talk', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()  # Переход на вторую строку
        keyboard.add_button('!ботопроверка', color=VkKeyboardColor.NEGATIVE)

    elif response == 'привет':
        keyboard.add_button('Тест', color=VkKeyboardColor.POSITIVE)

    keyboard = keyboard.get_keyboard()
    return keyboard



def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',
                      {id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648),
                       "attachment": attachment, 'keyboard': keyboard})


def send_message_dialoge(message):
    request = apiai.ApiAI(MyVkData.client_token).text_request()
    request.lang = "ru"
    request.session_id = "session_1"
    request.query = message
    response = json.loads(request.getresponse().read().decode("utf-8"))

    return response['result']


def dialoge():
    action = None

    try:
         for dialoge_event in longpoll.listen():
              if dialoge_event.type == VkEventType.MESSAGE_NEW:
                  if dialoge_event.from_user & dialoge_event.to_me:
                        message = dialoge_event.text.lower()
                        print(message)
                        new_message = send_message_dialoge(message)
                        action = new_message['action']

                        send_it_user = new_message['fulfillment']['speech']
                        send_message(vk_session, id_type, id, message = send_it_user)

                        if action == 'smalltalk.greetings.bye':
                            return 0

    except Exception as ex:
        print(ex)

while True:
    try:
        for event in longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW:
                print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                print('Текст сообщения: ' + str(event.text))
                response = event.text.lower()
                keyboard = create_keyboard(response)
                if event.from_user:
                    id_type = 'user_id'
                    id = event.user_id
                elif event.from_chat:
                    id_type = 'chat_id'
                    id = event.chat_id

                if response == "!ботопроверка":
                    send_message(vk_session, id_type, id, message='Внимание! Работает бот')
                elif response == "!small talk":
                    dialoge()
                elif response == "!оскорбиться":
                    send_message(vk_session, id_type, id, message='бот (оскорбился)')
                elif response == "!тык":
                    send_message(vk_session, id_type, id, message='Открываю клавиатуру', keyboard=keyboard)

            elif event.type == VkEventType.MESSAGE_EDIT:

                print("Пользователь отредактировал сообщение")
                response = event.text.lower()
                if event.from_user:
                    id_type = 'user_id'
                    id = event.user_id
                elif event.from_chat:
                    id_type = 'chat_id'
                    id = event.chat_id

                send_message(vk_session, id_type, id, message='Было отредактировано сообщение')


    except Exception as ex:
        print(ex)
