import yfinance as yf
from datetime import datetime


def fetch_stock_data(ticker, start_date=None, end_date=None, period=None):
    """
    Описание: Эта функция получает исторические данные о ценах акций для
    указанного тикера за заданный временной период или между конкретными датами.

    Параметры:
    ticker (str): тикер акций, для которых необходимо получить данные.
    start_date (datetime): дата начала анализа (если указано).
    end_date (datetime): дата окончания анализа (если указано).
    period (str): временной период для данных (например, '1d', '5d', '1mo' и т.д., если не указаны даты).

    Возвращает: DataFrame с историческими данными акций.
    """
    stock = yf.Ticker(ticker)
    if start_date and end_date:
        data = stock.history(start=start_date, end=end_date)
    else:
        data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    """
    Описание: Эта функция добавляет в DataFrame колонку со скользящим средним
    для цен закрытия акций. Она вычисляет среднее значение цен закрытия за
    заданное окно (по умолчанию 5), что помогает видеть тенденции в движении цен.
    Параметры:
    data (DataFrame): DataFrame, содержащий данные акций с колонкой 'Close'.
    Window_size (int): Количество периодов, по которым вычисляется скользящее среднее (по умолчанию 5).
    Возвращает: Модифицированный DataFrame, который включает дополнительную колонку 'Moving_Average'.
    :param data:
    :param window_size:
    :return:
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    """
    Описание: Эта функция вычисляет среднюю цену закрытия акций за указанный период и отображает
    её в консоли. Если колонка 'Close' отсутствует в DataFrame, функция выводит сообщение об ошибке.
    Параметры:
    data (DataFrame): DataFrame, содержащий данные акций с колонкой 'Close'.
    Возвращает: Ничего не возвращает, но выводит среднюю цену закрытия в консоль или сообщение об ошибке,
    если данные некорректны.
    :param data:
    :return:
    """
    if 'Close' in data.columns:
        average_price = data['Close'].mean()
        print(f"Средняя цена закрытия за выбранный период: {average_price:.2f}")
    else:
        print("Ошибочная дата: отсутствует колонка 'Close'")


def notify_if_strong_fluctuations(data, threshold):
    """
    Вычисляет и выводит среднюю цену закрытия акций за заданный период.
    Описание: Эта функция анализирует данные о ценах акций и уведомляет пользователей о наличии значительных
    колебаний цен за указанный период. Она вычисляет максимальное и минимальное значения цен закрытия и определяет,
    колебалась ли цена более чем на заданный процент (порог). Если колебания превышают порог, в консоли выводится
    соответствующее уведомление.
    Параметры:
    data (DataFrame): DataFrame, содержащий данные акций, включая колонку 'Close',
    с которой будут проводиться вычисления.
    Threshold (float): Процентный порог колебаний, который используется для сравнения.
    Возвращает: Ничего не возвращает, но выводит уведомления о колебаниях цен в консоль или сообщение об ошибке,
    если данные некорректны.
    :param data:
    :param threshold:
    :return:
    """
    if 'Close' in data.columns:
        max_price = data['Close'].max()
        min_price = data['Close'].min()
        fluctuation = ((max_price - min_price) / min_price) * 100

        if fluctuation > threshold:
            print(f"Уведомление: Цена акций колебалась более чем на {threshold}% за этот период!")
        else:
            print(f"Цена акций не колебалась более чем на {threshold}% за этот период.")
    else:
        print("Ошибка: отсутствует колонка 'Close'")


def export_data_to_csv(data, ticker, period):
    """
    Функция формирует имя файла, открывает его в текущем каталоге, принимает дату, тикер и период, делает
    выборку из данных и выводит в файл.
    :param data:
    :param ticker:
    :param period:
    :return:
    """
    # Формируем имя файла
    current_time = datetime.now().strftime("%H_%M_%d_%m_%Y")
    filename = f"{ticker}_{period}_{current_time}.csv"

    # Сохраняем данные в CSV с разделителем ";"
    data.to_csv(filename, sep=';', index=True)  # index=True, чтобы сохранить индекс (например, даты)
    print(f"Данные экспортированы в {filename}")


def calculate_rsi(data, window=14):
    """Calculate Relative Strength Index (RSI)"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data


def calculate_macd(data):
    """Calculate MACD"""
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    return data
