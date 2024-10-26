import data_download as dd
import data_plotting as dplt
from datetime import datetime


def main():
    """
    Основная функция программы.
    """

    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")

    # Выбор способа ввода периода
    period_choice = input(
        "Вы хотите ввести предустановленный период или конкретные даты? (укажите 'период' или 'даты'): ")

    if period_choice.lower() == 'период':
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        ticker = input("Введите тикер акции (например, 'AAPL' для Apple Inc): ")
        stock_data = dd.fetch_stock_data(ticker, period=period)

    elif period_choice.lower() == 'даты':
        ticker = input("Введите тикер акции (например, 'AAPL' для Apple Inc): ")

        # Запрос даты начала
        while True:
            start_date = input("Введите дату начала в формате 'дд-мм-гггг': ")
            try:
                start_date_obj = datetime.strptime(start_date, '%d-%m-%Y')
                break
            except ValueError:
                print("Некорректный формат даты. Пожалуйста, попробуйте еще раз.")

        # Запрос даты окончания
        while True:
            end_date = input("Введите дату окончания в формате 'дд-мм-гггг': ")
            try:
                end_date_obj = datetime.strptime(end_date, '%d-%m-%Y')
                if end_date_obj < start_date_obj:
                    print("Дата окончания должна быть позже даты начала.")
                else:
                    break
            except ValueError:
                print("Некорректный формат даты. Пожалуйста, попробуйте еще раз.")

        # Передача дат в fetch_stock_data
        stock_data = dd.fetch_stock_data(ticker, start_date=start_date_obj, end_date=end_date_obj)

    else:
        print("Неверный выбор. Пожалуйста, попробуйте снова.")
        return

    # Запрос у пользователя порога для колебаний
    threshold = float(input("Введите порог колебания цены в процентах (например, 5 для 5%): "))

    # Запрос у пользователя тип стиля графика

    style = input("Введите стиль графика (_classic_test_patch,  bmh, classic, dark_background, fast, fivethirtyeight, ggplot, grayscale ): ")

    # Вычисляем и выводим среднюю цену закрытия акций
    dd.calculate_and_display_average_price(stock_data)

    # Уведомление о сильных колебаниях
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Добавляем скользящее среднее в данные
    stock_data = dd.add_moving_average(stock_data)

    # Расчёт MACD и RSI
    stock_data = dd.calculate_macd(stock_data)
    stock_data = dd.calculate_rsi(stock_data)

    # Добавляем стандартное отклонение в данные
    stock_data = dd.calculate_standard_deviation(stock_data)

    # Рисуем график
    dplt.create_and_save_plot(stock_data, ticker, period_choice, style)

    # Экспорт данных в CSV
    dd.export_data_to_csv(stock_data, ticker, 'custom')


if __name__ == "__main__":
    main()
