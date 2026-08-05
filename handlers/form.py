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

@router.message(AppealForm.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AppealForm.waiting_for_direction)

    await message.answer(
        "Jónelisińizdi saylań👇",
        reply_markup=direction_keyboard
    )

@router.message(AppealForm.waiting_for_direction)
async def get_direction(message: Message, state: FSMContext):
    await state.update_data(direction=message.text)
    await state.set_state(AppealForm.waiting_for_group)

    await message.answer(
        "Toparıńızdı saylań👇",
        reply_markup=group_keyboard
    )

@router.message(AppealForm.waiting_for_group)
async def get_group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(AppealForm.waiting_for_course)

    await message.answer(
        "Kursıńızdı saylań👇",
        reply_markup=course_keyboard
    )

@router.message(AppealForm.waiting_for_course)
async def get_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await state.set_state(AppealForm.waiting_for_appeal)

    await message.answer(
        "Tariyx fakultetine baylanıslı bolǵan mashqala yáki usınısıńızdı tolıq jazıp qaldırıń😊",
        reply_markup=appeal_keyboard
    )

@router.message(AppealForm.waiting_for_appeal)
async def get_appeal(message: Message, state: FSMContext):
    await state.update_data(appeal=message.text)
    data = await state.get_data()
    user_id = message.from_user.id

    # Paydalanıwshı maǵlıwmatların keyingi safar ushın saqlap qoyamyz
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