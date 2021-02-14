import pytesseract
from PIL import Image
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

session = vk_api.VkApi(token='88c94357228fe11170d280783a866ff40d226334bcac34cf5edc8f2563c9aa1fb0f9df566b971f3813cfb')
longpool =  VkBotLongPoll(vk=session, group_id=202597974, wait=1)

for eventt in longpool.listen():
    if eventt.type == VkBotEventType.MESSAGE_NEW:
        print('FUCK')

exit()

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

img = Image.open('C:/Users/cjcbc/Desktop/projects/bot_image_translater/env/penis2.jpg')

print(pytesseract.image_to_string(img, lang='eng'))