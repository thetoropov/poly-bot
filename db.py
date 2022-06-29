def search_or_save_user(database, effective_user, message):
    users_ref = database.collection(u'users')
    manager_flag = False
    user_found = False
    for doc in users_ref.stream():
        if effective_user.id == doc.id:
            user_found = True

    if user_found is False:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "chat_id": message.chat.id
        }
        database.collection(u'users').document(str(user["user_id"])).set(user)
    return user
