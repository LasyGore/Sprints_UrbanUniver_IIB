import telebot
from PIL import Image
import io
from telebot import types
from PIL import ImageOps


TOKEN = '___===___'  # Замените на ваш токен
""" telebot используется для взаимодействия с Telegram API - это ключик к боту"""
bot = telebot.TeleBot(TOKEN)
""" экземпляр бота для взаимодействия с Telegram."""

user_states = {}  # Здесь будем хранить информацию о действиях пользователя
"""используется для отслеживания действий или состояний"""

# Стандартный набор символов
DEFAULT_ASCII_CHARS = '@%#*+=-:. '


def resize_image(image, new_width=100):
    """Изменяет размер изображения с сохранением пропорций."""
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))


def grayify(image):
    """Преобразует цветное изображение в оттенки серого."""
    return image.convert("L")


def image_to_ascii(image_stream, new_width=40, ascii_chars=DEFAULT_ASCII_CHARS):
    """Основная функция для преобразования изображения в ASCII-арт.
    Изменяет размер, преобразует в градации серого и затем в строку ASCII-символов.
    """
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
    """
    Конвертирует пиксели изображения в градациях серого
    в строку ASCII-символов, используя предопределенную
    строку ASCII_CHARS
    """
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ascii_chars[pixel * len(ascii_chars) // 256]
    return characters


def pixelate_image(image, pixel_size):
    """
    Принимает изображение и размер пикселя.
    Уменьшает изображение до размера, где один
    пиксель представляет большую область, затем
    увеличивает обратно, создавая пиксельный
    эффект. Применяем Image.BOX вместо Image.NEAREST.
    Качество значительно увеличилось.
    """
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.BOX
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.BOX
    )
    return image


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Реагирует на команды /start и /help, отправляя приветственное сообщение."""
    bot.reply_to(message, "Send me an image, and I'll provide options for you!")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """
    Реагирует на изображения, отправляемые пользователем, и предлагает варианты обработки.
    Бот получил фото! Просит ввести символы для кодировки
    """
    bot.reply_to(message, "I got your photo! Please enter a set of 10 characters for ASCII art:")
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id, 'ascii_chars': DEFAULT_ASCII_CHARS}


@bot.message_handler(func=lambda message: message.chat.id in user_states and len(message.text) == 10)
def set_ascii_chars(message):
    """Вносим требуемые символы вместо константы DEFAULT_ASCII_CHARS"""
    ascii_input = message.text  # Ввод остается без изменений
    user_states[message.chat.id]['ascii_chars'] = ascii_input
    bot.reply_to(message, "Thanks! Now choose an option:", reply_markup=get_options_keyboard())


def get_options_keyboard():
    """
    Создает клавиатуру с кнопками для выбора пользователем, как обработать изображение:
    через пикселизацию, преобразование в ASCII-арт, или преобразование в негатив.
    """
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Pixelate", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII Art", callback_data="ascii")
    invert_btn = types.InlineKeyboardButton("Invert Colors", callback_data="invert")
    reflect_btn = types.InlineKeyboardButton("Reflect", callback_data="reflect")  # Новая кнопка
    keyboard.add(pixelate_btn, ascii_btn, invert_btn, reflect_btn)
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Определяет действия в ответ на выбор пользователя
    (например, пикселизация или ASCII-арт) и вызывает
    соответствующую функцию обработки.
    """
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Pixelating your image...")
        pixelate_and_send(call.message)
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Converting your image to ASCII art...")
        ascii_and_send(call.message)
    elif call.data == "invert":  # Новая обработка
        bot.answer_callback_query(call.id, "Inverting your image colors...")
        invert_and_send(call.message)
    elif call.data == "reflect":
        bot.answer_callback_query(call.id, "Reflecting your image...")
        reflect_image(call)

@bot.callback_query_handler(func=lambda call: call.data == "reflect")
def reflect_image(call):
    """
        Реализует горизонтальное и вертикальное зеркальные отражения
        предоставленного фото или картинки.
    """
    photo_id = user_states[call.message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)

    # Создаем отраженные изображения
    horizontal_reflect = mirror_image(image, 'horizontal')
    vertical_reflect = mirror_image(image, 'vertical')

    # Сохраняем их в поток
    horizontal_output = io.BytesIO()
    vertical_output = io.BytesIO()

    horizontal_reflect.save(horizontal_output, format='JPEG')
    vertical_reflect.save(vertical_output, format='JPEG')

    horizontal_output.seek(0)
    vertical_output.seek(0)

    # Отправляем обе картинки с подписями
    bot.send_photo(call.message.chat.id, horizontal_output, caption=".V-reflect")
    bot.send_photo(call.message.chat.id, vertical_output, caption="G-reflect")


def invert_colors(image):
    """Инвертируем."""
    return ImageOps.invert(image)


def invert_and_send(message):
    """Конвертируем (при необходимости), инвертируем, отправляем пользователю."""
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)

    # Убедимся, что изображение в правильном формате
    if image.mode in ["RGBA", "P"]:
        image = image.convert("RGB")  # Конвертируем в RGB, если это необходимо

    # Инвертируем цвета
    print("Inverting colors of the image...")
    inverted_image = invert_colors(image)
    print("Inversion completed.")

    # Сохраняем инвертированное изображение в поток
    output_stream = io.BytesIO()
    inverted_image.save(output_stream, format="JPEG")
    output_stream.seek(0)

    # Отправляем инвертированное изображение обратно пользователю
    bot.send_photo(message.chat.id, output_stream, caption="Here is your inverted image!")
    print("Inverted image sent!")


def pixelate_and_send(message):
    """Конвертируем в пиксели и отсылаем пользователю."""
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
    """Преобразует изображение в ASCII-арт и отправляет результат в виде текстового сообщения."""
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


def mirror_image(image, direction):
    if direction == 'horizontal':
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == 'vertical':
        return image.transpose(Image.FLIP_TOP_BOTTOM)


bot.polling(none_stop=True)