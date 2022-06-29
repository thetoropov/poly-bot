# Easy Book Bot
**Telegram bot to automate manager interaction with publishers and resellers, and shopping.**
## Commands
* `/start` Get info about user
* `/add <book_info>` Add book to database if you are manager
* `/buy` Show books and buy it
* `/info` Add address


## Get started
1) Install dependencies:

```pip install aiogram google-cloud-firestore```

2) Go to google console and generate and save credentials file.
3) Go to telegram and copy bot token
4) Use `secret.py` to save secret data and manage managers.


## User guide
* Let's start with `/start` command.
* Add info(address) about you via `/info` command.
* To start shopping write `/buy` and you can see a full list of books.
* Click on any book to buy it
* Enjoy our simple service :)

If you are manager you need to add books to the database via `/add` command.

