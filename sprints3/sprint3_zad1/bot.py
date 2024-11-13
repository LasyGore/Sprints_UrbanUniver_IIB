import telebot
from PIL import Image
import io
from telebot import types

TOKEN = '< ;) >'  # Замените на ваш токен
bot = telebot.TeleBot(TOKEN)

user_states = {}  # Здесь будем хранить информацию о действиях пользователя

# Стандартный набор символов
DEFAULT_ASCII_CHARS = '@%#*+=-:. '

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def image_to_ascii(image_stream, new_width=40, ascii_chars=DEFAULT_ASCII_CHARS):
    image = Image.open(image_stream).convert('L')  # Переводим в оттенки серого
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(aspect_ratio * new_width * 0.55)
    img_resized = image.resize((new_width, new_height))
    img_str = pixels_to_ascii(img_resized, ascii_chars)
    img_width = img_resized.width

    max_characters = 4000 - (new_width + 1)
    max_rows = max_characters // (new_width + 1)

    ascii_art = ""
    for i in range(0, min(max_rows * img_width, len(img_str)), img_width):
        ascii_art += img_str[i:i + img_width] + "\n"

    return ascii_art

def pixels_to_ascii(image, ascii_chars):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ascii_chars[pixel * len(ascii_chars) // 256]
    return characters

def pixelate_image(image, pixel_size):
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    return image

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me an image, and I'll provide options for you!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "I got your photo! Please enter a set of 10 characters for ASCII art:")
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id, 'ascii_chars': DEFAULT_ASCII_CHARS}

@bot.message_handler(func=lambda message: message.chat.id in user_states and len(message.text) == 10)
def set_ascii_chars(message):
    ascii_input = message.text  # Ввод остается без изменений
    user_states[message.chat.id]['ascii_chars'] = message.text
    bot.reply_to(message, "Thanks! Now choose an option:", reply_markup=get_options_keyboard())

def get_options_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Pixelate", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII Art", callback_data="ascii")
    keyboard.add(pixelate_btn, ascii_btn)
    return keyboard

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Pixelating your image...")
        pixelate_and_send(call.message)
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Converting your image to ASCII art...")
        ascii_and_send(call.message)

def pixelate_and_send(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    pixelated = pixelate_image(image, 20)

    output_stream = io.BytesIO()
    pixelated.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)

def ascii_and_send(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    ascii_chars = user_states[message.chat.id]['ascii_chars']
    ascii_art = image_to_ascii(image_stream, ascii_chars=ascii_chars)

    # Добавим отладочное сообщение, чтобы проверить, был ли сгенерирован ASCII арт
    if ascii_art.strip():
        bot.send_message(message.chat.id, f"```\n{ascii_art}\n```", parse_mode="MarkdownV2")
    else:
        bot.send_message(message.chat.id, "Sorry, I couldn't generate ASCII art from this image.")

bot.polling(none_stop=True)