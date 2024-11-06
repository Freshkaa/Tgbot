import telebot
from Config import keys, TOKEN
from utils import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)






@bot.message_handler(commands=['start'])
def start(message):
    text = 'Чтобы начать работать, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quota, base, amount = values
        total_base = CryptoConverter.convert(quota, base, float(amount))
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать командду.\n{e}')
    else:
        text = f'Цена {amount} {quota} в {base} -  {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling()
