import yfinance as yf


#def fetch_stock_data(ticker, period='1mo'):
def fetch_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_and_display_average_price(data):
    if 'Close' in data.columns:
        average_price = data['Close'].mean()
        print(f"Средняя цена закрытия за выбранный период: {average_price:.2f}")
    else:
        print("Ошибочная дата: отсутствует колонка 'Close'")

def notify_if_strong_fluctuations(data, threshold):
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