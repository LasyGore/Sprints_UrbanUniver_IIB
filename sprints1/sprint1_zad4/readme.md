������ ��� ������� � ������������ ������ �� ������.

������������� ����������:

main.py





data_plotting.py

1. �������: create_and_save_plot(data, ticker, period, filename=None)
����������� � ������ ������, ���������� �� ������ � ��������� � �����.

![img.png](img.png)

[AAPL_1mo_22_18_18_10_2024.csv](AAPL_1mo_22_18_18_10_2024.csv)
 
data_download.py

1. fetch_stock_data(ticker, period)
��������: ��� ������� �������� ������������ ������ � ����� ����� ���
���������� ������ (��������, "AAPL" ��� Apple Inc.) �� �������� ���������
������ (��������, "1mo" ��� ������ ������). ��� ���������� ����������
yfinance ��� �������� ������ � ���������� �� � ������� DataFrame.

���������:

ticker (str): ����� �����, ��� ������� ���������� �������� ������.
period (str): ��������� ������ ��� ������ (��������, '1d', '5d', '1mo' � �.�.).
����������: DataFrame � ������������� ������� �����, ������� ���������� � ����� ��������, ��������, ���������� � ��������� �� ��������� ������.

2. add_moving_average(data, window_size=5)
��������: ��� ������� ��������� � DataFrame ������� �� ���������� �������
��� ��� �������� �����. ��� ��������� ������� �������� ��� �������� �� 
�������� ���� (�� ��������� 5), ��� �������� ������ ��������� � �������� ���.

���������:

data (DataFrame): DataFrame, ���������� ������ ����� � �������� 'Close'.
window_size (int): ���������� ��������, �� ������� ����������� ���������� ������� (�� ��������� 5).
����������: ���������������� DataFrame, ������� �������� �������������� ������� 'Moving_Average'.

3. calculate_and_display_average_price(data)
��������: ��� ������� ��������� ������� ���� �������� ����� �� ��������� ������ � ����������
� � �������. ���� ������� 'Close' ����������� � DataFrame, ������� ������� ��������� �� ������.

���������:

data (DataFrame): DataFrame, ���������� ������ ����� � �������� 'Close'.
����������: ������ �� ����������, �� ������� ������� ���� �������� � ������� ��� ��������� �� ������, ���� ������ �����������.

4. �������: notify_if_strong_fluctuations(data, threshold)
��������� � ������� ������� ���� �������� ����� �� �������� ������.
��������: ��� ������� ����������� ������ � ����� ����� � ���������� ������������� � ������� ������������ ��������� ��� 
�� ��������� ������. ��� ��������� ������������ � ����������� �������� ��� �������� � ����������, ���������� �� ����
����� ��� �� �������� ������� (�����). ���� ��������� ��������� �����, � ������� ��������� ��������������� �����������.

���������:

data (DataFrame): DataFrame, ���������� ������ �����, ������� ������� 'Close', � ������� ����� ����������� ����������.
threshold (float): ���������� ����� ���������, ������� ������������ ��� ���������.

����������: ������ �� ����������, �� ������� ����������� � ���������� ��� � ������� ��� ��������� �� ������, ���� ������ �����������.

5. ������� def export_data_to_csv(data, ticker, period)
��������� ��� �����, ��������� ������ � ���� ������ CSV � ������������ ����� - ;

���������:
data (DataFrame): DataFrame, ���������� ������ ����� � �������� 'Close'.
ticker (str): ����� �����, ��� ������� ���������� �������� ������.
period (str): ��������� ������ ��� ������ (��������, '1d', '5d', '1mo' � �.�.).
 
