def errorHandler(bot, message, type):
    if type == 'except':
        return bot.reply_to(message, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /reset')