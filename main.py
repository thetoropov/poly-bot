from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from google.cloud import firestore
from db import search_or_save_user
from secret import BOT_TOKEN, MANAGERS_IDS

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
database = firestore.Client.from_service_account_json("ebook-febf3-firebase-adminsdk-d86xi-626ba4f23e.json")


def get_books_from_db():
    books_ref = database.collection(u'books').stream()

    books_dict = {}
    for doc in books_ref:
        books_dict[doc.id] = doc.to_dict()
    books_list = []
    for id in books_dict.keys():
        books_list.append(id)

    print(books_list)
    return books_list


books_cb = CallbackData('books', 'name', 'action')


def get_keyboard():
    books = get_books_from_db()
    markup = types.InlineKeyboardMarkup()
    for day in books:
        markup.add(
            types.InlineKeyboardButton(
                day,
                callback_data=books_cb.new(name=day, action='buy')),
        )
    return markup


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    search_or_save_user(database, message.from_user, message)
    await message.reply("Welcome!\nI'm EasyBook bot! Bot for our internet book shop :)")


@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    if len(get_books_from_db()) == 0:
        await message.reply("Sorry, we don't have any books...")
    else:
        await message.reply("Choose book:", reply_markup=get_keyboard())


@dp.callback_query_handler(books_cb.filter(action='buy'))
async def query_predict(query, callback_data):
    book = callback_data['name']
    database.collection(u'books').document(str(book)).delete()

    await query.message.edit_text("You buy a " + str(book))


@dp.message_handler(commands=['add'])
async def add_book(message: types.Message):
    if str(message.from_user.id) in MANAGERS_IDS:
        database.collection(u'books').document(str(message.text[5:])).set({"name": {message.text[5:]}})
        await message.reply("You successfully add a book!")
    else:
        await message.reply("Permission denied.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
