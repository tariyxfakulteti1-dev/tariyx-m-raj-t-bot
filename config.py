import os
from dotenv import load_dotenv

# .env faylidagi o'zgaruvchilarni yuklash
load_dotenv()

# Bot token va Kanal ID sozlamalari
BOT_TOKEN = os.getenv("BOT_TOKEN", "8857810164:AAHYnXSc7_QpJ4B9MIgoXzEaBJ60hWO6dKI")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1003999534099"))