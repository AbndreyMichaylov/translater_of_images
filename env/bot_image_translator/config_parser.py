import toml

config = toml.load('settings/bot_config.toml')

TOKEN = config['vk_bot_data']['TOKEN']
GROUP_ID = config['vk_bot_data']['GROUP_ID']
SAVE_PATH = config['save_files_data']['SAVE_PATH']
TESSERACT_OCR_PATH = config['tesseract']['TESSERACT_OCR_PATH']