from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

#from utils.chatgpt import ask_chatgpt
from keyboards.inline import random_fact_kb

router = Router()

RANDOM_FACT_PROMPT = "Расскажи интересный и неожиданный научный факт."

"""
@router.callback_query(F.data == "random_again")
async def random_again(callback: CallbackQuery, state: FSMContext):
    await send_random_fact(callback.message, state)

@router.callback_query(F.data == "end")
async def end_conversation(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Диалог завершён. Используй /start чтобы начать заново.")
"""