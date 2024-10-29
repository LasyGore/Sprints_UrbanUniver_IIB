import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from bokeh.plotting import figure, output_file, show
from bokeh.io import save


def create_and_save_plot(data, ticker, period, style, filename=None):
    """
    Основная функция выдачи графиков по итогам работы программы.
    """
    # Существующий код для matplotlib
    print(style)
    plt.style.use(style)
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

    # Сохранение графиков Matplotlib
    directory = "plotfiles"
    if not os.path.exists(directory):
        os.makedirs(directory)
    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    filepath = os.path.join(directory, filename)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()  # Закрываем фигуру, если она больше не нужна
    print(f"График сохранен как {filepath}")


def create_interactive_plotly(data, ticker):
    """
    Создает интерактивный график цен закрытия с использованием Plotly.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Price'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Moving_Average'], mode='lines', name='Moving Average'))

    fig.update_layout(title=f'{ticker} Интерактивный график цен',
                      xaxis_title='Дата',
                      yaxis_title='Цена',
                      legend=dict(x=0, y=1))

    # Сохранение интерактивного графика в HTML файл
    plotly_path = f"plotfiles/{ticker}_interactive_plot.html"
    fig.write_html(plotly_path)
    print(f"Интерактивный график сохранен как {plotly_path}")


def create_interactive_bokeh(data, ticker):
    """
    Создает интерактивный график стандартного отклонения с использованием Bokeh.
    """
    data.index = data.index.tz_localize(None)
    output_file(f"plotfiles/{ticker}_standard_deviation.html")

    p = figure(title=f'{ticker} Стандартное отклонение цены закрытия', x_axis_label='Дата',
               y_axis_label='Standard Deviation', x_axis_type='datetime')
    p.line(data.index, data['Standard_Deviation'], legend_label='Standard Deviation', line_color='purple')

    save(p)  # Сохранить график в HTML файл
    print(f"Bokeh график сохранен как plotfiles/{ticker}_standard_deviation.html")