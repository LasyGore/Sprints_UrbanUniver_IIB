import os
import matplotlib.pyplot as plt

def create_and_save_plot(data, ticker, period, style, filename=None):
    """
    Основная функция выдачи графиков по итогам работы программы.
    """
    print(style)
    plt.style.use(style)  # Применяем выбранный стиль
    plt.figure(figsize=(12, 8))

    # График цен закрытия и скользящих средних
    plt.subplot(4, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.plot(data.index, data['Moving_Average'], label='Moving Average')
    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    # График стандартного отклонения
    plt.subplot(4, 1, 2)
    plt.plot(data.index, data['Standard_Deviation'], label='Standard Deviation', color='purple')
    plt.title('Стандартное отклонение цены закрытия')
    plt.xlabel("Дата")
    plt.ylabel("Стандартное отклонение")
    plt.legend()

    # График RSI
    plt.subplot(4, 1, 3)
    plt.plot(data.index, data['RSI'], label='RSI', color='orange')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green')
    plt.title('Relative Strength Index (RSI)')
    plt.xlabel("Дата")
    plt.ylabel("RSI")
    plt.legend()

    # График MACD
    plt.subplot(4, 1, 4)
    plt.plot(data.index, data['MACD'], label='MACD', color='green')
    plt.plot(data.index, data['Signal_Line'], label='Signal Line', color='red')
    plt.title('MACD')
    plt.xlabel("Дата")
    plt.ylabel("MACD")
    plt.legend()

    # Указываем путь к каталогу plotfiles
    directory = "plotfiles"

    # Проверяем, существует ли каталог; если нет, создаем его
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Сохранение графиков
    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    # Полный путь к файлу
    filepath = os.path.join(directory, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()  # Закрываем фигуру, если она больше не нужна
    print(f"График сохранен как {filepath}")

# Пример использования функции
# data_example = ...  # Здесь должен быть ваш DataFrame с данными
# create_and_save_plot(data_example, "AAPL", "daily", "seaborn")