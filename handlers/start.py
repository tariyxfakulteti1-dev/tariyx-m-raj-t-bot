from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.form import AppealForm
from keyboards.reply import start_keyboard, appeal_keyboard

router = Router()

# Paydalanıwshılardıń dáslepki maǵlıwmatların saqlaw ushın lug'at
user_data_store = {}

@router.message(CommandStart())
@router.message(F.text == "🏠 Bas menyu")
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AppealForm.waiting_for_name)

    await message.answer(
        "👋 Assalawma aleykum!\n\n"
        "Tariyx fakulteti múrajáátlar botına xosh kelipsiz.\n\n"
        "Atı familiyańızdı jazıp qaldırıń 😊",
        reply_markup=start_keyboard
    )

@router.message(F.text == "📝 Jańa múrajáát")
async def new_appeal_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # Eger paydalanıwshı maǵlıwmatları aldın kiritilgen bolsa
    if user_id in user_data_store:
        saved_data = user_data_store[user_id]
        await state.clear()
        
        # Aldınǵı maǵlıwmatlardı FSM memory-ǵa qayta júkleymiz (telefon nomeri qosıldı)
        await state.update_data(
            name=saved_data['name'],
            phone=saved_data.get('phone'),
            direction=saved_data['direction'],
            group=saved_data['group'],
            course=saved_data['course']
        )
        await state.set_state(AppealForm.waiting_for_appeal)

        await message.answer(
            f"👤 <b>{saved_data['name']}</b>\n"
            f"📱 {saved_data.get('phone', 'Nomer joq')}\n"
            f"🏛 {saved_data['direction']} | {saved_data['group']} | {saved_data['course']}\n\n"
            "Tariyx fakultetine baylanıslı bolǵan jańa múrajáátıńızdı tolıq jazıp qaldırıń😊",
            reply_markup=appeal_keyboard,
            parse_mode="HTML"
        )
    else:
        # Eger birinshi ret kiritip atırǵan bolsa, basınan baslaydı
        await start_handler(message, state)
