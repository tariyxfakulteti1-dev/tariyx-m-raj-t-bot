import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import CHANNEL_ID
from states.form import AppealForm
from keyboards.reply import (
    start_keyboard,
    phone_keyboard,
    direction_keyboard,
    group_keyboard,
    course_keyboard,
    appeal_keyboard,
    finish_keyboard
)

# start.py faylındaǵı saqlawshı lug'atty import etemiz
from handlers.start import user_data_store

router = Router()

# ==================== ANIQ KNOPKA MAǴLIWMATLAR DIZIMI ====================
VALID_DIRECTIONS = [
    "Tariyx", 
    "Sociologiya", 
    "Arxeologiya", 
    "Filosofiya"
]

VALID_GROUPS = [
    "A topar", 
    "B topar", 
    "C topar", 
    "G topar", 
    "V topar"
]

VALID_COURSES = [
    "1-kurs", "2-kurs", "3-kurs", "4-kurs"
]


# ==================== ARTQA QAYTIW LOGIKASI ====================
@router.message(F.text == "⬅️ Artqa qaytıw")
async def go_back(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AppealForm.waiting_for_phone.state:
        await state.set_state(AppealForm.waiting_for_name)
        await message.answer(
            "Atı familiyańızdı qaytadan jazıp qaldırıń 😊",
            reply_markup=start_keyboard
        )

    elif current_state == AppealForm.waiting_for_direction.state:
        await state.set_state(AppealForm.waiting_for_phone)
        await message.answer(
            "📱 Telefon nomerińizdi jiberiń yamasa jazıp qaldırıń👇",
            reply_markup=phone_keyboard
        )

    elif current_state == AppealForm.waiting_for_group.state:
        await state.set_state(AppealForm.waiting_for_direction)
        await message.answer(
            "Jónelisińizdi saylań👇",
            reply_markup=direction_keyboard
        )

    elif current_state == AppealForm.waiting_for_course.state:
        await state.set_state(AppealForm.waiting_for_group)
        await message.answer(
            "Toparıńızdı saylań👇",
            reply_markup=group_keyboard
        )

    elif current_state == AppealForm.waiting_for_appeal.state:
        await state.set_state(AppealForm.waiting_for_course)
        await message.answer(
            "Kursıńızdı saylań👇",
            reply_markup=course_keyboard
        )

    else:
        await state.set_state(AppealForm.waiting_for_name)
        await message.answer(
            "Atı familiyańızdı jazıp qaldırıń 😊",
            reply_markup=start_keyboard
        )


# ==================== BASQISHPAN-BASQISH FORMA ====================

# 1. AT-FAMILIYA QABIL ETIW HÁM VALIDATSIYA
@router.message(AppealForm.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    text = message.text.strip() if message.text else ""
    words = text.split()

    # Keminde 2 sóz hám tek háriplerden turıwı kerek
    pattern = r"^[a-zA-Zʻ’'`А-Яа-яӨөÓóÚúÁáǴǵŃńÍíƵƶ\s-]+$"
    if len(words) < 2 or not all(re.match(pattern, w) for w in words):
        await message.answer(
            "⚠️ Atıńız hám familiyańızdı jazıń!\n"
            "<i>Mısalı: Boranbaev Allayar</i>",
            parse_mode="HTML",
            reply_markup=start_keyboard
        )
        return

    await state.update_data(name=text)
    await state.set_state(AppealForm.waiting_for_phone)

    await message.answer(
        "📱 Telefon nomerińizdi jiberiw ushın tómendegi túymeni basıń yamasa nomerińizdi jazıp jiberiń👇",
        reply_markup=phone_keyboard
    )


# 1.5. TELEFON NOMERIN QABIL ETIW HÁM TEKSERIW (VALIDATION)
@router.message(AppealForm.waiting_for_phone)
async def get_phone(message: Message, state: FSMContext):
    phone_number = None

    if message.contact:
        phone_number = message.contact.phone_number
        if not phone_number.startswith("+"):
            phone_number = f"+{phone_number}"
            
    elif message.text and message.text != "⬅️ Artqa qaytıw":
        raw_text = message.text.strip()
        # Nomerdi tekseriw: basında optional +, keyin 9 yaki 12 dana cifr
        # Mısalı: 901234567, 998901234567, +998901234567
        phone_pattern = r"^\+?\d{9,12}$"
        
        if re.match(phone_pattern, raw_text):
            phone_number = raw_text if raw_text.startswith("+") else f"+{raw_text}"
        else:
            await message.answer(
                "⚠️ Nadurıs telefon nomer kiritildi!\n"
                "Tekserip qaytadan kiritiń!",
                parse_mode="HTML",
                reply_markup=phone_keyboard
            )
            return
    else:
        await message.answer(
            "⚠️ Ótinish, telefon nomerińizdi knopkanı basıw arqalı jiberiń yamasa tekst túrinde jazıń!",
            reply_markup=phone_keyboard
        )
        return

    await state.update_data(phone=phone_number)
    await state.set_state(AppealForm.waiting_for_direction)

    await message.answer(
        "Jónelisińizdi saylań👇",
        reply_markup=direction_keyboard
    )


# 2. JÓNELIS SAYLAW (Tek durıs túyme basılǵanda)
@router.message(AppealForm.waiting_for_direction, F.text.in_(VALID_DIRECTIONS))
async def get_direction(message: Message, state: FSMContext):
    await state.update_data(direction=message.text)
    await state.set_state(AppealForm.waiting_for_group)

    await message.answer(
        "Toparıńızdı saylań👇",
        reply_markup=group_keyboard
    )

# Jónelis durıs saylanbaǵanda:
@router.message(AppealForm.waiting_for_direction)
async def invalid_direction(message: Message):
    await message.answer(
        "⚠️ Ótinish, tómendegi túymelerden jónelisińizdi saylań👇",
        reply_markup=direction_keyboard
    )


# 3. TOPAR SAYLAW (Tek durıs túyme basılǵanda)
@router.message(AppealForm.waiting_for_group, F.text.in_(VALID_GROUPS))
async def get_group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(AppealForm.waiting_for_course)

    await message.answer(
        "Kursıńızdı saylań👇",
        reply_markup=course_keyboard
    )

# Topar durıs saylanbaǵanda:
@router.message(AppealForm.waiting_for_group)
async def invalid_group(message: Message):
    await message.answer(
        "⚠️ Ótinish, tómendegi túymelerden toparıńızdı saylań👇",
        reply_markup=group_keyboard
    )


# 4. KURS SAYLAW (Tek durıs túyme basılǵanda)
@router.message(AppealForm.waiting_for_course, F.text.in_(VALID_COURSES))
async def get_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await state.set_state(AppealForm.waiting_for_appeal)

    await message.answer(
        "Tariyx fakultetine baylanıslı bolǵan mashqala yáki usınısıńızdı tolıq jazıp qaldırıń😊",
        reply_markup=appeal_keyboard
    )

# Kurs durıs saylanbaǵanda:
@router.message(AppealForm.waiting_for_course)
async def invalid_course(message: Message):
    await message.answer(
        "⚠️ Ótinish, tómendegi túymelerden kursıńızdı saylań👇",
        reply_markup=course_keyboard
    )


# 5. MÚRAJÁÁT TEKSTIN QABIL ETIW (3 sóz hám 10 hárip shárti menen)
@router.message(AppealForm.waiting_for_appeal)
async def get_appeal(message: Message, state: FSMContext):
    text_content = message.text.strip() if message.text else ""

    # Teksttegi sózler dizimin alamız
    words = text_content.split()
    
    # Teksttegi tek háripler sanın esaplaymız (bos orınlar hám simvollarsız)
    letters_only = re.sub(r'[^a-zA-ZáóúıǵńÁÓÚİǴŃа-яА-ЯөөӨӨ]', '', text_content)

    # 1. Keminde 3 sóz hám keminde 10 hárip shártin tekseremiz
    if len(words) < 3 or len(letters_only) < 10:
        await message.answer(
            "⚠️ Múrajáátıńızdı anıq hám túsinikli etip jazıp qaldırıń!",
            reply_markup=appeal_keyboard
        )
        return
        
    # Shártler orınlansa, saqlaw hám jiberiw:
    await state.update_data(appeal=text_content)
    data = await state.get_data()
    user_id = message.from_user.id

    # Paydalanıwshı maǵlıwmatların saqlaw
    user_data_store[user_id] = {
        'name': data.get('name'),
        'phone': data.get('phone'),
        'direction': data.get('direction'),
        'group': data.get('group'),
        'course': data.get('course')
    }

    # Kanalǵa jiberiw
    text = (
        "📨 <b>JAŃA MÚRAJÁÁT</b>\n\n"
        f"👤 <b>Atı-familiyası:</b> {data.get('name')}\n"
        f"📱 <b>Telefon nomeri:</b> {data.get('phone')}\n"
        f"🏛 <b>Jónelisi:</b> {data.get('direction')}\n"
        f"👥 <b>Toparı:</b> {data.get('group')}\n"
        f"🎓 <b>Kursı:</b> {data.get('course')}\n\n"
        f"📝 <b>Múrajáátı:</b>\n{data.get('appeal')}"
    )

    await message.bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        parse_mode="HTML"
    )

    await message.answer(
        "✅ Múrajáátıńızdı tez arada kórip shıǵamız😊",
        reply_markup=finish_keyboard
    )

    await state.clear()
