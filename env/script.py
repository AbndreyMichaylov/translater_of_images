import queue
import os
import pytesseract
from PIL import Image
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
import uuid
import path
#from google.cloud import translate
import requests
import json



SAVE_PATH = 'C:/Users/cjcbc/Desktop/projects/bot_image_translater/not_translated_images/'
TOKEN = '88c94357228fe11170d280783a866ff40d226334bcac34cf5edc8f2563c9aa1fb0f9df566b971f3813cfb'
GROUP_ID = 202597974
IMAGES_QUEUE = queue.Queue()
#CLIENT = Translator('af21c496f83c408db87b24912897b860')

END_POINT = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
PARAM = '&from=en&to=ru'
REQUEST_URL = END_POINT + PARAM


session = vk_api.VkApi(token=TOKEN)
longpool =  VkBotLongPoll(vk=session, group_id=GROUP_ID, wait=1)
vk = session.get_api()

#Парсит пришедший json
def get_image_url(event_object):
    return event.object["attachments"][0]["photo"]["sizes"][-1]["url"]

#Сохраняет изображение по урлу в папку по указанному пути
def save_image_to_path(save_path, img_url):
    image = requests.get(img_url)
    random_name = str(uuid.uuid4()) + '.jpg'
    with open(save_path + random_name , 'wb') as f:
        f.write(image.content)

#Создаёт список для очереди
def make_queue_of_process_images(save_path):
    list_of_not_translated_images = os.listdir(save_path)
    return [path.Path('not_translated_images/' + i).abspath() for i in list_of_not_translated_images]

for event in longpool.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        image_url = get_image_url(event)

        save_image_to_path(SAVE_PATH, image_url)

        list_of_not_translated_images = os.listdir(SAVE_PATH)

        list_of_full_paths_of_files = make_queue_of_process_images(SAVE_PATH)

        #print(list_of_full_paths_of_files)
        #Заполняет очередь обработки изображений
        for image in list_of_full_paths_of_files:
            IMAGES_QUEUE.put(image)

        while not IMAGES_QUEUE.empty():
            image_to_process = IMAGES_QUEUE.get()
            
            pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

            img = Image.open(image_to_process)

            result = pytesseract.image_to_string(img, lang='eng')
            print(result)
            
            HEADER = {
                'Ocp-Apim-Subscription-Key': 'b4dd1f60dd00432fb552c9bbb1ce90b7',
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4()),
                'Ocp-Apim-Subscription-Region' : 'eastus',
            }

            body = [{
                'text' : result
            }]

            #exit()
            try: 
                #translated = CLIENT.translate(result, to='rus')
                request = requests.post(REQUEST_URL, headers=HEADER, json=body)
                response = request.json()[0]['translations'][0]['text']
                print(response)
                #exit()
                vk.messages.send(user_id=event.object["from_id"],
                                 random_id=get_random_id(),
                                 message=response)
            except vk_api.exceptions.ApiError:
                vk.messages.send(user_id=event.object["from_id"],
                                 random_id=get_random_id(),
                                 message='Не могу обработать фото')
            finally:
                os.remove(image_to_process)
        print('FUCK')
