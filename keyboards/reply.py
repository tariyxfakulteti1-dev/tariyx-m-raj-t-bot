from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Doimiy (namunaviy) túymeler
nav_buttons = [
    [KeyboardButton(text="⬅️ Artqa qaytıw"), KeyboardButton(text="🏠 Bas menyu")],
    [KeyboardButton(text="📝 Jańa múrajáát")]
]

# 1-basqısh: Ism-familiya basqıshındaǵı klawiatura
start_keyboard = ReplyKeyboardMarkup(
    keyboard=nav_buttons,
    resize_keyboard=True
)

# 2-basqısh: Jónelis klaviaturası (Tariyx, Sociologiya, Arxeologiya, Filosofiya)
direction_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Tariyx"), KeyboardButton(text="Sociologiya")],
        [KeyboardButton(text="Arxeologiya"), KeyboardButton(text="Filosofiya")],
        *nav_buttons
    ],
    resize_keyboard=True
)

# 3-basqısh: Topar klaviaturası
group_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="A topar"), KeyboardButton(text="B topar")],
        [KeyboardButton(text="C topar"), KeyboardButton(text="G topar")],
        [KeyboardButton(text="V topar")],
        *nav_buttons
    ],
    resize_keyboard=True
)

# 4-basqısh: Kurs klaviaturası
course_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1-kurs"), KeyboardButton(text="2-kurs")],
        [KeyboardButton(text="3-kurs"), KeyboardButton(text="4-kurs")],
        *nav_buttons
    ],
    resize_keyboard=True
)

# 5-basqısh: Múrajáát jazıw basqıshındaǵı klawiatura
appeal_keyboard = ReplyKeyboardMarkup(
    keyboard=nav_buttons,
    resize_keyboard=True
)

# 6-basqısh: Juwmaqlawshı klawiatura
finish_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏠 Bas menyu"), KeyboardButton(text="📝 Jańa múrajáát")]
    ],
    resize_keyboard=True
)