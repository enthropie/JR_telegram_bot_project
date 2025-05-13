from typing import Union

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from classes import gpt_client
from classes.resource import Resource, Button
from classes.chat_gpt import GPTMessage
from classes.enums import GPTRole
from keyboards.callback_data import CelebrityData, QuizData, TranslateData
from .handlers_state import CelebrityTalk, Quiz, TranslateState
from .command import com_start, com_quiz

callback_router = Router()




@callback_router.callback_query(CelebrityData.filter(F.button == 'select_celebrity'))
async def celebrity_callbacks(callback: CallbackQuery, callback_data: CelebrityData, bot: Bot, state: FSMContext):
    photo = Resource(callback_data.file_name).photo
    button_name = Button(callback_data.file_name).name
    await callback.answer(
        text=f'С тобой говорит {button_name}',
    )
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption='Задайте свой вопрос:',
    )
    request_message = GPTMessage(callback_data.file_name)
    await state.set_state(CelebrityTalk.wait_for_answer)
    await state.set_data({'messages': request_message, 'photo': photo})

@callback_router.callback_query(TranslateData.filter(F.button == 'select_language'))
async def translate_callbacks(callback: CallbackQuery, callback_data: TranslateData, bot: Bot, state: FSMContext):
    photo = Resource('translate').photo
    await callback.answer(
        text=f'Вы выбрали язык {callback_data.topic_name}!',
    )
    request_message = GPTMessage('translate')
    request_message.update(GPTRole.USER, callback_data.topic_name)
    #response = await gpt_client.request(request_message)
    #await bot.send_photo(
    #    chat_id=callback.from_user.id,
    #    photo=photo,
    #    caption=response,
    #)
    await state.set_state(TranslateState.wait_for_answer)
    await state.set_data({'messages': request_message, 'photo': photo, 'callback': callback_data})


@callback_router.callback_query(QuizData.filter(F.button == 'change_topic'))
async def change_topic_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(topic=None, topic_name=None)
    await callback.answer(
        text=f'Выберите новую тему!',
    )
    await com_quiz(callback.message)


@callback_router.callback_query(QuizData.filter(F.button == 'select_topic'))
async def select_topic_callback(callback: CallbackQuery, callback_data: QuizData, bot: Bot, state: FSMContext):
    photo = Resource('quiz').photo
    await callback.answer(
        text=f'Вы выбрали тему {callback_data.topic_name}!',
    )
    request_message = GPTMessage('quiz')
    request_message.update(GPTRole.USER, callback_data.topic)
    response = await gpt_client.request(request_message)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption=response,
    )
    await state.set_state(Quiz.wait_for_answer)
    await state.set_data({'messages': request_message, 'photo': photo, 'score': 0, 'callback': callback_data})


@callback_router.callback_query(QuizData.filter(F.button == 'next_question'))
async def quiz_next_question(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    data: dict[str, Union[GPTMessage, str, QuizData]] = await state.get_data()
    data['messages'].update(GPTRole.USER, 'quiz_more')
    response = await gpt_client.request(data['messages'])
    data['messages'].update(GPTRole.ASSISTANT, response)
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=data['photo'],
        caption=response,
    )
    await callback.answer(
        text=f"Продолжаем тему {data['callback'].topic_name}"
    )
    await state.update_data(data)






@callback_router.callback_query(lambda c: QuizData.unpack(c.data).button == 'finish_quiz')
async def finish_quiz_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.answer(
        text= "Спасибо за участие в квизе!",
    )


    await com_start(callback.message)

