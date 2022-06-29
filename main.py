import re
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
    await message.reply("Welcome!\nI'm EasyBook bot! Bot for our internet book shop :)\n"
                        "Let's start with /start command.\n"
                        "Add info(address) about you via /info command.\n"
                        "To start shopping write /buy and you can see a full list of books.\n"
                        "Click on any book to buy it\n"
                        "Enjoy our simple service :)")


@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    user = {
        "address": message.text[6:]
    }
    database.collection(u'users').document(str(message.from_user.id)).update(user)
    await message.reply("Successfully update your info!")


@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    if len(get_books_from_db()) == 0:
        await message.reply("Sorry, we don't have any books...")
    else:
        await message.reply("Choose book:", reply_markup=get_keyboard())


@dp.callback_query_handler(books_cb.filter(action='buy'))
async def query_predict(query, callback_data):
    book = callback_data['name']
    doc = database.collection(u'books').document(book).get()
    database.collection(u'books').document(str(book)).delete()
    print(book)

    print(doc.to_dict())
    await query.message.edit_text("You buy a " + str(book) + '\n' + 'Price: ' + str(
        doc.to_dict()["price"][0]) + "\nCheck your address after two days!")


@dp.message_handler(commands=['add'])
async def add_book(message: types.Message):
    if str(message.from_user.id) in MANAGERS_IDS:
        name = re.sub(r'[^\w\s]+|[\d]+', r'', message.text[5:]).strip()
        price = [int(i) for i in re.findall(r'\d+', message.text[5:])]
        database.collection(u'books').document(str(name)).set({"name": {str(name)}, "price": {int(price[0])}})
        await message.reply("You successfully add a book!")
    else:
        await message.reply("Permission denied.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
