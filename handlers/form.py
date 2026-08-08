import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import CHANNEL_ID
from states.form import AppealForm
from keyboards.reply import (
    start_keyboard,
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

    if current_state == AppealForm.waiting_for_direction.state:
        await state.set_state(AppealForm.waiting_for_name)
        await message.answer(
            "Atı familiyańızdı qaytadan jazıp qaldırıń 😊",
            reply_markup=start_keyboard
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


# 5. MÚRAJÁÁT TEKSTIN QABIL ETIW
@router.message(AppealForm.waiting_for_appeal)
async def get_appeal(message: Message, state: FSMContext):
    text_content = message.text.strip() if message.text else ""
    words = text_content.split()

    # Múrájat tekseriwı: eń keminde 15 simvol, keminde 2 so'z hám bir árip 5-ten artıq qaytalanbawı kerek
    if len(text_content) < 15 or len(words) < 2 or re.search(r"(.)\1{5,}", text_content):
        await message.answer(
            "⚠️ Múrájáátıńız júdá qısqa!\n"
            "Iltimas, mashqala yamasa usınısıńızdı tolıǵıraq etip jazıp qaldırıń😊",
            reply_markup=appeal_keyboard
        )
        return

    await state.update_data(appeal=text_content)
    data = await state.get_data()
    user_id = message.from_user.id

    # Paydalanıwshı maǵlıwmatların saqlaw
    user_data_store[user_id] = {
        'name': data.get('name'),
        'direction': data.get('direction'),
        'group': data.get('group'),
        'course': data.get('course')
    }

    # Terminalǵa shıǵarıw
    print("===== JAŃA MÚRAJÁÁT =====")
    print(f"Atı-familiyası: {data.get('name')}")
    print(f"Jónelisi: {data.get('direction')}")
    print(f"Toparı: {data.get('group')}")
    print(f"Kursı: {data.get('course')}")
    print(f"Múrajáátı: {data.get('appeal')}")
    print("=========================")

    # Kanalǵa jiberiw
    text = (
        "📨 <b>JAŃA MÚRAJÁÁT</b>\n\n"
        f"👤 <b>Atı-familiyası:</b> {data.get('name')}\n"
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
