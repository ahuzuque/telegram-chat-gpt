from typing import Concatenate, Text
from g4f import Completion
from g4f.client import Client
import telebot
from telebot import types, TeleBot

token = 'token'

client = Client()
bot = TeleBot(token)

models_text = {
    'mixtral': 'mixtral-8x7b'
}
models_image = {
    'stable-diffusion': 'stable-diffusion-3',
    'sdxl-lightning': 'sdxl-lightning',
    'playground-v2.5': 'playground-v2.5'
}
kb_models_text = types.ReplyKeyboardMarkup()
for x in models_text:
    kb_models_text.add(types.KeyboardButton(x))

kb_models_image = types.ReplyKeyboardMarkup()
for x in models_image:
    kb_models_image.add(types.KeyboardButton(x))

kb_mode = types.ReplyKeyboardMarkup()
kb_mode.add(types.KeyboardButton('text'), types.KeyboardButton('image'))


@bot.message_handler(commands=['start'])
def welcome_func(message):
    bot.send_message(message.chat.id, 'Привет! Я gpt-bot, выбери режим работы!', reply_markup=kb_mode)


@bot.message_handler(func=lambda message: message.text in ['text', 'image'])
def choice_mode(message):
    if message.text == 'text':
        bot.send_message(message.chat.id, 'Выбери модель!', reply_markup=kb_models_text)
    elif message.text == 'image':
        bot.send_message(message.chat.id, 'Выбери модель!', reply_markup=kb_models_image)


@bot.message_handler(func=lambda message: message.text in models_text.keys())
def choice_model_text(message):
    model = models_text[message.text]
    bot.send_message(message.chat.id, f'Вы выбрали модель {model}! Теперь напиши свой вопрос!')
    bot.register_next_step_handler(message, qw_function, model)


def qw_function(message, model):
    user_message = message.text
    response = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': user_message}],
    )
    answer_response = response.choices[0].message.content
    bot.send_message(message.chat.id, answer_response)


@bot.message_handler(func=lambda message: message.text in models_image.keys())
def choice_model_image(message):
    model = models_image[message.text]
    bot.send_message(message.chat.id, f'Вы выбрали модель {model}! Теперь напиши свой запрос на генерацию')
    bot.register_next_step_handler(message, qw_function_image, model)


def qw_function_image(message, model):
    user_message = message.text
    response = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': user_message}],
    )
    answer_response = response.choices[0].message.content
    bot.send_message(message.chat.id, answer_response)


bot.infinity_polling()
