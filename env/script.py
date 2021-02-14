import pytesseract
from PIL import Image
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
import uuid

session = vk_api.VkApi(token='88c94357228fe11170d280783a866ff40d226334bcac34cf5edc8f2563c9aa1fb0f9df566b971f3813cfb')
longpool =  VkBotLongPoll(vk=session, group_id=202597974, wait=1)
vk = session.get_api()

for event in longpool.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        #for i in event.object:
            #print(i)
        #exit()
        image_url = event.object["attachments"][0]["photo"]["sizes"][-1]["url"]
        image = requests.get(image_url)
        random_name = str(uuid.uuid4()) + '.jpg'
        with open('C:\\Users\\cjcbc\Desktop\\projects\\bot_image_translater\\env\\not_translated_images\\' + random_name , 'wb') as f:
            f.write(image.content)
        vk.messages.send(user_id=event.object["from_id"],
                         random_id=get_random_id(),
                         message='kek')
        print('FUCK')

exit()

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

img = Image.open('C:/Users/cjcbc/Desktop/projects/bot_image_translater/env/penis2.jpg')

print(pytesseract.image_to_string(img, lang='eng'))