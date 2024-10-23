import matplotlib.pyplot as plt


def create_and_save_plot(data, ticker, period, filename=None):
    """
        Основная функция выдачи графиков по итогам работы программы.

    """
    plt.figure(figsize=(12, 8))

    # График цен закрытия и скользящих средних
    plt.subplot(3, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.plot(data.index, data['Moving_Average'], label='Moving Average')
    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    # График RSI
    plt.subplot(3, 1, 2)
    plt.plot(data.index, data['RSI'], label='RSI', color='orange')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green')
    plt.title('Relative Strength Index (RSI)')
    plt.xlabel("Дата")
    plt.ylabel("RSI")
    plt.legend()

    # График MACD
    plt.subplot(3, 1, 3)
    plt.plot(data.index, data['MACD'], label='MACD', color='green')
    plt.plot(data.index, data['Signal_Line'], label='Signal Line', color='red')
    plt.title('MACD')
    plt.xlabel("Дата")
    plt.ylabel("MACD")
    plt.legend()

    # Сохранение графиков
    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"
    plt.tight_layout()
    plt.savefig(filename)
    print(f"График сохранен как {filename}")
