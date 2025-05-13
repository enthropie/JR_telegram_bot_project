from aiogram.utils.keyboard import InlineKeyboardBuilder

import os
from collections import namedtuple
from classes.enums import ResourcePath

from .callback_data import CelebrityData, QuizData, TranslateData

Button = namedtuple('Button', ['button_text', 'button_callback'])


def ikb_celebrity():
    keyboard = InlineKeyboardBuilder()
    path_celebrity = ResourcePath.PROMPTS.value
    celebrity_list = [file for file in os.listdir(path_celebrity) if file.startswith('talk_')]
    buttons = []
    for file in celebrity_list:
        with open(os.path.join(path_celebrity, file), 'r', encoding='UTF-8') as txt_file:
            buttons.append((txt_file.readline().split(', ')[0][5:], file.split('.')[0]))
    for button_name, file_name in buttons:
        keyboard.button(
            text=button_name,
            callback_data=CelebrityData(
                button='select_celebrity',
                file_name=file_name,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_quiz_select_topic():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Язык Python', 'quiz_prog'),
        Button('Математика', 'quiz_math'),
        Button('Биология', 'quiz_biology'),

    ]
    for button in buttons:
        keyboard.button(
            text=button.button_text,
            callback_data=QuizData(
                button='select_topic',
                topic=button.button_callback,
                topic_name=button.button_text,
            )

        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_quiz_next(current_topic: QuizData):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Дальше', 'next_question'),
        Button('Сменить тему', 'change_topic'),
        Button('Закончить', 'finish_quiz'),

    ]
    for button in buttons:
        keyboard.button(
            text=button.button_text,
            callback_data=QuizData(
                button=button.button_callback,
                topic=current_topic.topic,
                topic_name=current_topic.topic_name
            )
        )
    keyboard.adjust(2, 1)
    return keyboard.as_markup()


def ikb_translate():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Английский', 'tr_eng'),
        Button('Французский', 'tr_fra'),
        Button('Немецкий', 'tr_deu'),

    ]
    for button in buttons:
        keyboard.button(
            text=button.button_text,
            callback_data=TranslateData(
                button='select_language',
                topic=button.button_callback,
                topic_name=button.button_text,
            )

        )
    keyboard.adjust(1)
    return keyboard.as_markup()