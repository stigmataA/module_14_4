from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

api = "****"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True) # инициализация клавиатуры
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button3 = KeyboardButton(text='Купить')
kb.row(button)
kb.row(button2)
kb.row(button3)

ikb = InlineKeyboardMarkup(resize_keyboard=True)
in_button1=InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
ikb.add(in_button1)
ikb.add(in_button2)

ilb = InlineKeyboardMarkup(resize_keyboard=True)
ilb_button1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
ilb_button2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
ilb_button3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
ilb_button4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
ilb.add(ilb_button1)
ilb.add(ilb_button2)
ilb.add(ilb_button3)
ilb.add(ilb_button4)

initiale_db()
products = get_all_products()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for number in products:
        await message.answer(f'Название: {number[1]} | Описание: {number[2]} | Цена: {number[3]} р')
        try:
            with open('files/' + str(number[0]) + '.png', 'rb') as img:
                await message.answer_photo(img, f'Название: {number[1]} | Описание: {number[2]} | Цена: {number[3]} р')
        except: FileNotFoundError
        await message.answer('Нет изображения для этого продукта')

    await message.answer(f'Выберите продукт для покупки', reply_markup=ilb)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий Вашему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=ikb)


@dp.callback_query_handler(text='formulas')
async def get_formula(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.callback_query_handler(text= 'calories')
async def set_age(call):
    await call.message.answer(f"Введите свой возраст")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f"Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f"Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result_m = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    result_w = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f"Ваша норма калорий составляет: \n для мужчин{result_m} ккал в сутки \n для женщин {result_w} ккал в сутки")
    await UserState.weight.set()
    await state.finish()


@dp.message_handler(text=['Информация'])
async def info(message):
    await message.answer(f'Данный бот помогает Вам расcчитать норму потребления калорий для мужчин по'
                         'упрощенной формуле Миффлина-Сан Жерома')


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer(f'Вы успешно выбрали продукт!')
    await call.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
