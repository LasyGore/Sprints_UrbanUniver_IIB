"������ ����������"
������������ tkinter ��� ������������ ����������.

- ������������� ������ tkinter, ttk �� tkinter ��� ������ � ����������� ����������� ������������, Toplevel ��� �������� ����� ����, 
messagebox ��� ������ ��������� ������������, json ��� ������ � ������� � ������� JSON, datetime ��� ������ � ������ � ��������.

- ���������� data_file ������ ��� �����, � ������� ����� ����������� ������ � ����������� � ������� JSON.
![alt text](1.png)
������� �������� � ���������� ������:

- ������� load_data �������� ������� ���� � ������, ��������� � ���������� data_file, � ��������� �� ���� ������ � ������� JSON.
���� ���� �� ���������� ��� ���������� ������ ��� ������� ������, ������������ ������ ������.

- ������� save_data ��������� ������ � ����������� � ���� ������ �������� � ��������� �� � ���� � ������� JSON.
������ ������������� � �������� ��� ������ ����������.
![alt text](8.png)

����� TrainingLogApp:

- ����������� ������ __init__ ��������� ������ root, ������� �������� ������� ����� ����������, � �������� ����� create_widgets
��� �������� �������� ����������.

- ����� create_widgets ������� ������� ��� ����� ������ � ���������� (�������� ����������, ���, ���������� ����������), ������ 
��� ���������� ������ � ���������� � ��������� ����������� �������.

- ����� add_entry ��������� ������ �� ����� �����, ��������� �� �������, ������� ������� � ����������� � ����������, ���������
��� � ������ � ������� � ��������� ��������� � ����. ����� ���������� ������ ���� ����� ���������, � ������������ ������������ ��������� �� ������.

- ����� view_records ��������� ����������� ������ � ���������� �� � ����� ���� � ������� ������� Treeview. ��� ������ ������ ��������� ������ � �������.

������� main:

- ������� ��������� Tk, ������� �������� ������� ����� ����������.

- ������� ��������� ���������� TrainingLogApp, ��������� ��� ������� ����.

- ��������� ������� ���� ��������� ������� Tkinter, ����� ���� ���������� ������������ � ����������� �� �������� ������������.

������ ���������:

- ���������, ��� ������ ������� ��� �������� ���������, � � ���� ������ �������� ������� main ��� ������������� � ������� ����������.

������������� �����������:

1. ���������� ������� �� ���� - ����������� ������������� ������ �� ������������ ������. ������� - filter_by_date
![alt text](5.png)
2. ���������� ������� �� ���������� - ����������� ������������� ������ �� ����������� ����������. ������� - filter_by_exercise
![alt text](2.png)
3. ������� ������ � CSV - ������� ��� �������� ���� ������� � CSV ����. ������� - export_to_csv
4. ������ ������ �� CSV - ������� ��� ������� ������� �� CSV �����.  ������� - import_from_csv
![alt text](7.png)
5. �������������� ������ - ����������� ������������� ��������� ������. ������� - edit_record
![alt text](3.png)
6. �������� ������ - ����������� ������� ��������� ������. ������� - delete_record
![alt text](4.png)
7. ���������� �� ����������� - ����������� ���������� �� ����������� ����������� (��������, ��������� ��� �� �����). ������� - show_statistics
![alt text](9.png)
8. ������������ ��������� - ������� ��������� ���� � ���������� �� ����������� �� ������������ ������. ������� - visualize_progress
![alt text](10.png)