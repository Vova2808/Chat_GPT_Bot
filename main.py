from VortexGPT import Client
from gtts import gTTS
import telebot
from telebot import types


bot = telebot.TeleBot('YOUR_TOKEN')
print("Bot Запущен")

@bot.message_handler(commands=['start', 'help'])
def start(message):
    text_start = '''Привет'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    ChatGPT = types.KeyboardButton("ChatGPT")
    markup.add(ChatGPT)
    bot.send_message(message.chat.id, text_start, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def chatgpt(message):
    if message.text == 'ChatGPT':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        raspisan_call = types.KeyboardButton("выход")
        markup.add(raspisan_call)
        bot.send_message(message.chat.id, "Пожалуйсто отправте сообщение:", reply_markup=markup)

        bot.register_next_step_handler(message, handle_user_message)

    else:
        bot.send_message(message.chat.id, "Я вас не понимаю напишите /help")

def handle_user_message(message):
    if message.text == "выход":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        chat_gpt = types.KeyboardButton("ChatGPT")
        markup.add(chat_gpt)
        bot.send_message(message.chat.id, "Выход", reply_markup=markup)

    else:
        bot.register_next_step_handler(message, handle_user_message)
        prompt = message.text

        try:
            bot.send_chat_action(message.chat.id, 'typing')
            resp = Client.create_completion("gpt3", prompt)


            bot.send_message(message.chat.id, f"GPT: {resp}")

            language = 'ru'
            obj = gTTS(text=resp, lang=language, slow=False)
            obj.save("gpt.mp3")

            audio = open('gpt.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)
            audio.close()


        except Exception as e:
            bot.send_message(message.chat.id, f"GPT: {e}")




bot.polling(none_stop=True)