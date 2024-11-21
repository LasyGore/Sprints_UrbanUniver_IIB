import telebot
from PIL import Image
import io
from telebot import types
from PIL import ImageOps
import random

TOKEN = '222-333'  # Замените на ваш токен
bot = telebot.TeleBot(TOKEN)

user_states = {}  # Здесь будем хранить информацию о действиях пользователя
DEFAULT_ASCII_CHARS = '@%#*+=-:. '  # Стандартный набор символов для ASCII


JOKES = [
    "Девушка становится женщиной, когда впервые говорит: «Это хороший пакет, не выбрасывай».",
    "В мире 80% мужчин не знают, из-за чего злится жена. Оставшиеся 20% даже не знают, что жена злится.",
    "— Мадемуазель, можно вашу ручку? Какая изящная. А достанешь дяде огурчик из банки?",
    "Если женщина — это шкатулка с секретом, то мужчина — сундук со сказками.",
    "Какая разница между мужчиной и ребенком? В принципе никакой, но ребенка можно оставить одного с няней.",
    "Лучше всего поднимает мужчину с дивана сработавшая за окном сигнализация."
]


def resize_image(image, new_width=100):
    """Изменяет размер изображения с сохранением пропорций."""
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))


def resize_for_sticker(image, max_size=512):
    """Изменяет размер изображения для использования в качестве стикера без изменения пропорций."""
    width, height = image.size
    if width > height:
        ratio = max_size / width
    else:
        ratio = max_size / height

    new_width = int(width * ratio)
    new_height = int(height * ratio)

    return image.resize((new_width, new_height), Image.LANCZOS)  # Замените Image.ANTIALIAS на Image.LANCZOS


def grayify(image):
    """Преобразует цветное изображение в оттенки серого."""
    return image.convert("L")


def invert_colors(image):
    """Инвертирует цвета изображения."""
    return ImageOps.invert(image)


def create_heatmap(image):
    """Создает тепловую карту из изображения."""
    gray_image = grayify(image)
    heatmap = ImageOps.colorize(gray_image, black="blue", white="red")  # Цвета для тепловой карты
    return heatmap


def pixelate_image(image, pixel_size):
    """Пикселизирует изображение."""
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    return image


def image_to_ascii(image_stream, new_width=40, ascii_chars=DEFAULT_ASCII_CHARS):
    """Преобразует изображение в ASCII-арт."""
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
    """Конвертирует пиксели изображения в градациях серого в строку ASCII. """
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ascii_chars[pixel * len(ascii_chars) // 256]
    return characters


def get_options_keyboard():
    """Создает клавиатуру с кнопками для выбора пользователем, как обработать изображение."""
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Pixelate", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII Art", callback_data="ascii")
    invert_btn = types.InlineKeyboardButton("Invert Colors", callback_data="invert")
    reflect_btn = types.InlineKeyboardButton("Reflect", callback_data="reflect")
    heatmap_btn = types.InlineKeyboardButton("Heatmap", callback_data="heatmap")  # Новая кнопка
    resize_btn = types.InlineKeyboardButton("Resize for Sticker", callback_data="resize_for_sticker")  # Новая кнопка
    joke_btn = types.InlineKeyboardButton("Joke!", callback_data="random_joke")  # Новая кнопка для шутки
    keyboard.add(pixelate_btn, ascii_btn, invert_btn, reflect_btn, heatmap_btn, resize_btn, joke_btn)
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Отправляет приветственное сообщение пользователю."""
    print("send_welcome function called")  # Отладочное сообщение
    bot.reply_to(message, "Welcome! Send me a photo to get started.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """Обрабатывает фотографию, отправленную пользователем."""
    bot.reply_to(message, "I got your photo! Please enter a set of 10 characters for ASCII art:")
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id, 'ascii_chars': DEFAULT_ASCII_CHARS}


@bot.message_handler(func=lambda message: message.chat.id in user_states and len(message.text) == 10)
def set_ascii_chars(message):
    """Сохраняет набор символов для ASCII-арта."""
    ascii_input = message.text
    user_states[message.chat.id]['ascii_chars'] = ascii_input
    bot.reply_to(message, "Thanks! Now choose an option:", reply_markup=get_options_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Обрабатывает выбор пользователя из клавиатуры."""
    photo_id = user_states[call.message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)

    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Pixelating your image...")
        pixelated_image = pixelate_image(image, 10)  # Измените уровень пикселизации по мере необходимости
        output_stream = io.BytesIO()
        pixelated_image.save(output_stream, format='JPEG')
        output_stream.seek(0)
        bot.send_photo(call.message.chat.id, output_stream, caption="Here is your pixelated image!")
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Converting your image to ASCII art...")
        ascii_art = image_to_ascii(image_stream)
        bot.send_message(call.message.chat.id, f"```\n{ascii_art}\n```", parse_mode="MarkdownV2")
    elif call.data == "invert":
        bot.answer_callback_query(call.id, "Inverting your image colors...")
        inverted_image = invert_colors(image)
        output_stream = io.BytesIO()
        inverted_image.save(output_stream, format='JPEG')
        output_stream.seek(0)
        bot.send_photo(call.message.chat.id, output_stream, caption="Here is your inverted image!")
    elif call.data == "heatmap":
        bot.answer_callback_query(call.id, "Creating heatmap of your image...")
        heatmap_image = create_heatmap(image)
        heatmap_bytes = io.BytesIO()
        heatmap_image.save(heatmap_bytes, format='PNG')
        heatmap_bytes.seek(0)
        bot.send_photo(call.message.chat.id, heatmap_bytes, caption="Here is your heatmap!")
    elif call.data == "reflect":
        bot.answer_callback_query(call.id, "Reflecting your image...")
        reflect_image(call)
    elif call.data == "resize_for_sticker":
        bot.answer_callback_query(call.id, "Resizing your image for Telegram sticker...")
        resized_image = resize_for_sticker(image, max_size=512)
        output_stream = io.BytesIO()
        resized_image.save(output_stream, format='PNG')  # Сохраняем в формате PNG
        output_stream.seek(0)
        bot.send_photo(call.message.chat.id, output_stream, caption="Here is your resized image for use as a sticker!")
    elif call.data == "random_joke":
        joke = random.choice(JOKES)  # Выбираем случайную шутку
        bot.answer_callback_query(call.id, "Here's a joke for you!")
        bot.send_message(call.message.chat.id, joke)  # Отправляем шутку пользователю

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


def mirror_image(image, direction):
    """Создаем отражение."""
    if direction == 'horizontal':
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == 'vertical':
        return image.transpose(Image.FLIP_TOP_BOTTOM)


# Запуск бота
bot.polling(none_stop=True)
