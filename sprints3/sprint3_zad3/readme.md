������������������� ��������-���.
������ ��� ������ ����� �������� � ������������ � ������ ASCII-���.

�������� �����������:

1)������� � ���������:
- telebot ������������ ��� �������������� � Telegram API.
- PIL (Python Imaging Library), ��������� ��� Pillow, ������������� ����������� ��� ������ � �������������.
- TOKEN � ��� ��������� ����������, ���� �� ������ ��������� ����� ������ ����, ���������� �� @BotFather � Telegram.
- bot = telebot.TeleBot(TOKEN) ������� ��������� ���� ��� �������������� � Telegram.

2)�������� ��������� �������������:
- user_states ������������ ��� ������������ �������� ��� ��������� �������������. ��������, ����� ����������� ���� ����������.

3)������������:
-pixelate_image(image, pixel_size):
- ��������� ����������� � ������ �������. ��������� ����������� �� �������, ��� ���� ������� ������������ ������� �������, ����� ����������� �������, �������� ���������� ������.

4)�������������� � ASCII-���:
���������� �����������:
- resize_image(image, new_width=100): �������� ������ ����������� � ����������� ���������.
- grayify(image): ����������� ������� ����������� � ������� ������.
- image_to_ascii(image_stream, new_width=40): �������� ������� ��� �������������� ����������� � ASCII-���. �������� ������, ����������� � �������� ������ � ����� � ������ ASCII-��������.
pixels_to_ascii(image): ������������ ������� ����������� � ��������� ������ � ������ ASCII-��������, ��������� ���������������� ������ ASCII_CHARS.

5)�������������� � �������������:
����������� ���������:
- @bot.message_handler(commands=['start', 'help']): ��������� �� ������� /start � /help, ��������� �������������� ���������.
- @bot.message_handler(content_types=['photo']): ��������� �� �����������, ������������ �������������, � ���������� �������� ���������.
���������� ��� ��������������:
- get_options_keyboard(): ������� ���������� � �������� ��� ������ �������������, ��� ���������� �����������: ����� ������������ ��� �������������� � ASCII-���.

6)��������� ��������
��������� ��������:
- @bot.callback_query_handler(func=lambda call: True): ���������� �������� � ����� �� ����� ������������ (��������, ������������ ��� ASCII-���) � �������� ��������������� ������� ���������.
�������� �����������
������� ��������:
- pixelate_and_send(message): ������������� ����������� � ���������� ��� ������� ������������.
- ascii_and_send(message): ����������� ����������� � ASCII-��� � ���������� ��������� � ���� ���������� ���������.

7)�������� ����������: ������������ ����� �������� ���� ����� �������� ��� �������� ASCII-���� �� ������������� �����������.
����� ��������� �����������, ��� ����������� � ������������ ����� ��������, ������� ����� �������������� ��� �������������� ����������� � ASCII-���.
��� ��������� ������������� ����������������� �������� ���������.

8)�������� ����������:������ ����� ����������� �� ���������������, ��� ����� �������� "�������" �����������.
������������ ������� invert_colors, ������� ��������� ImageOps.invert �� PIL (Python Imaging Library) � �����������.

9)�������� ����������:���������� �������� ���������� ����� �����������(����������� ���� � ���������) �� ����������� ��� ���������.
������� mirror_image ��������� ����� transpose �� PIL � ����������� Image.FLIP_LEFT_RIGHT ��� Image.FLIP_TOP_BOTTOM ��� ���������������
��� ������������� ��������� ��������������. ��� ��������� ��������� �������  ������  � ���� reflect. �� ������ ������ ��������� ���
�������� ����� ��������������� � ����� ������������� ��������� c �������������� ���������: V-reflect � G-reflect 