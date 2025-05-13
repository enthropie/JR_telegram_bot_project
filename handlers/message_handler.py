from aiogram import Bot, Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

import aiohttp
import base64

from .handlers_state import CelebrityTalk, ChatGPTRequests, ImageRequests, Quiz, TranslateState
from typing import Union, Dict
from classes import gpt_client
from classes.resource import Resource
from classes.chat_gpt import GPTMessage, GPTRole
from keyboards import kb_end_talk, ikb_quiz_next
from keyboards.callback_data import QuizData
from .command import com_start
from misc import bot_thinking

message_router = Router()


@message_router.message(CelebrityTalk.wait_for_answer, F.text == 'Попрощаться!')
@message_router.message(TranslateState.wait_for_answer, F.text == 'Попрощаться!')
async def end_talk_handler(message: Message, state: FSMContext):
    await state.clear()
    await com_start(message)


@message_router.message(ChatGPTRequests.wait_for_request)
async def wait_for_gpt_handler(message: Message, state: FSMContext):
    await bot_thinking(message)
    gpt_message = GPTMessage('gpt')
    gpt_message.update(GPTRole.USER, message.text)
    gpt_response = await gpt_client.request(gpt_message)
    photo = Resource('gpt').photo
    await message.answer_photo(
        photo=photo,
        caption=gpt_response,
    )
    await state.clear()


@message_router.message(CelebrityTalk.wait_for_answer)
async def talk_handler(message: Message, state: FSMContext):
    await bot_thinking(message)
    data: Dict[str, Union[FSInputFile, str]] = await state.get_data()
    data['messages'].update(GPTRole.USER, message.text)
    response = await gpt_client.request(data['messages'])
    await message.answer_photo(
        photo=data['photo'],
        caption=response,
        reply_markup=kb_end_talk(),
    )
    data['messages'].update(GPTRole.ASSISTANT, response)
    await state.update_data(data)


@message_router.message(TranslateState.wait_for_answer)
async def translate_handler(message: Message, state: FSMContext):
    await bot_thinking(message)
    data: Dict[str, Union[FSInputFile, str]] = await state.get_data()
    data['messages'].update(GPTRole.USER, message.text)
    response = await gpt_client.request(data['messages'])
    await message.answer_photo(
        photo=data['photo'],
        caption=response,
        reply_markup=kb_end_talk(),
    )
    data['messages'].update(GPTRole.ASSISTANT, response)
    await state.update_data(data)


@message_router.message(Quiz.wait_for_answer)
async def quiz_answer(message: Message, state: FSMContext):
    data: dict[str, Union[GPTMessage, str, QuizData]] = await state.get_data()
    data['messages'].update(GPTRole.USER, message.text)
    response = await gpt_client.request(data['messages'])
    if response == 'Правильно!':
        data['score'] += 1
    data['messages'].update(GPTRole.ASSISTANT, response)
    await message.answer_photo(
        photo=data['photo'],
        caption=f"Ваш счет: {data['score']}\n{response}",
        reply_markup=ikb_quiz_next(data['callback']),
    )
    await state.update_data(data)


async def get_image_bytes(file_id, bot: Bot):
    file_info = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            if resp.status != 200:
                return None
            return await resp.read()


@message_router.message(ImageRequests.wait_for_request)
async def wait_for_image_handler(message: Message, bot: Bot, state: FSMContext):
    await bot_thinking(message)
    if message.photo:
        file_id = message.photo[-1].file_id  # Наибольшее по размеру фото
    else:
        file_id = message.document.file_id  # Изображение как документ

    img_bytes = await get_image_bytes(file_id, bot)

    if not img_bytes:
        await message.answer("Ошибка при загрузке изображения 😢")
        return

    try:
        # Преобразуем в base64
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        gpt_response = await gpt_client.photo_request(img_base64)
        description = gpt_response.choices[0].message.content
        await message.answer(f"🖼 Описание изображения:\n\n{description}")

    except Exception as e:
        await message.answer(f"Произошла ошибка при распознавании: {e}")
    finally:
        await state.clear()
