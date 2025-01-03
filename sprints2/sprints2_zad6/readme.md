��������� ��� �������� ����������� �� ������ TKinter.

������������� ����������:

drawing_app.py

������ ��������� ������������ ����� ������ ������������� ���������� TKinter ��� �������� ������������ ����������.



����� DrawingApp
������������� __init__(self, root)

����������� ������ ��������� ���� ��������:

- root: ��� �������� ������ Tkinter, ������� ������ ����������� ��� ����� ���������� ����������.

������ ������������ ����������� ��������� �������� ��������:

- ��������������� ��������� ���� ����������.

- ��������� ������ ����������� (self.image) � �������������� ���������� Pillow. ��� ����������� ������ ����������� �������, �� ������� ���������� ���������. ���������� ��� ��������� ����� ������.

- ���������������� ������ ImageDraw.Draw(self.image), ������� ��������� �������� �� ������� �����������.

- ��������� ������ Canvas Tkinter, ������� ���������� ����������� ��������� ��� ���������. ������� ������ ����������� � 600x400 ��������.

- ���������� ����� self.setup_ui(), ������� ����������� �������� ���������� ����������.

- ������������� ����������� ������� � ������ ��� ������������ �������� ���� ��� ��������� () � ������ ��������� ����� ��� ���������� ������ ���� ().



����� setup_ui(self)

���� ����� �������� �� �������� � ������������ �������� ����������:

- ������ "��������", "������� ����" � "���������" ��������� ������������ ������� �����, �������� ���� ����� � ��������� ������� ����������� ��������������.

- ������� ��� ��������� ������� ����� ���� ����������� �������� ������� ����� �� 1 �� 10 ��������.



����� paint(self, event)

������� ���������� ��� �������� ���� � ������� ����� ������� �� ������. ��� ������ ����� �� ������ Tkinter � ����������� �� ������� Image �� Pillow:

- event: ������� �������� ���������� ����, ������� ������������ ��� ���������.

- ����� �������� ����� ������� � ��������� ��������������� ��������� �������, ��� ������� ����������� �����������.



����� reset(self, event)

���������� ��������� ���������� �����. ��� ���������� ��� ����������� ������ ����� ����� ����� ����, ��� ������������ �������� ������ ���� � ����� ����� ��������.



����� clear_canvas(self)

������� �����, ������ ��� ������������, � ����������� ������� Image � ImageDraw��� ������ �����������.



����� choose_color(self)

��������� ����������� ���������� ���� ������ ����� � ������������� ��������� ���� ��� ������� ��� �����.



����� save_image(self)

��������� ������������ ��������� �����������, ��������� ����������� ���������� ���� ��� ���������� �����. ������������ ������ ������ PNG.
� ������ ��������� ���������� ��������� ��������� �� �������� ����������.



��������� �������

- : ������� ��������� � ������ paint, �������� �������� �� ������ ��� ����������� ���� � ������� ����� �������.

- : ������� ��������� � ������ reset, ������� ���������� ��������� ��������� ��� ������ ����� �����.



������������� ����������

������������ ����� �������� �� ������, �������� ���� � ������ �����, ������� ����� � ��������� � ������� PNG.

��������� ���������:
1. ����� ������� ����� �� ������:
�����������: tk.OptionMenu ��� �������� ����������� ������. �������� ����������������� ����������, sizes = [1, 2, 5, 7, 10].
��� ������ ������� �� ������ ����������� ������� ������ �����
(� ��� ����� �������� ��������� ��������).
���������� ��������� ����� �����: self.brush_size = 1  # ��������� ������ �����
��������� ��������� ������� �����: self.canvas.bind('<Button-3>', self.show_brush_size_menu)  # ��������� ������� �����
self.brush_size_scale.set(self.brush_size)  # ������������� ��������� ������
��������� ��� �������:

    def show_brush_size_menu(self, event):
        sizes = [1, 3, 5, 7, 10]
        menu = tk.Menu(self.root, tearoff=0)

        for size in sizes:
            menu.add_command(label=f"{size}", command=lambda s=size: self.update_brush_size(s))

        menu.post(event.x_root, event.y_root)  # ���������� ���� � ������� �������

    def update_brush_size(self, selected_size):
        self.brush_size = selected_size  # ��������� ������ ����� �� ������ ������
        self.brush_size_scale.set(selected_size)  # ��������� ������� (��� �������������)

2.���������� ����������� � ���� ������ "������".
��������� ������ "������" (tk.Button), � ��� � ������� �������������� self.pen_color � ���� ���� ("white").
��� ������������ ������� �� ���������� ����� ����������������� ���������� ����.
3. �������� ���������� "�������". �� ����� ������ ������� ���� ����� ���� �� �������� ������� � ������ ���� ������.
��������� ����������������:
    def show_brush_size_menu(self, event):
        sizes = [1, 3, 5, 7, 10]
        menu = tk.Menu(self.root, tearoff=0)

        for size in sizes:
            menu.add_command(label=f"{size}", command=lambda s=size: self.update_brush_size(s))

        menu.post(event.x_root, event.y_root)  # ���������� ���� � ������� �������

    def update_brush_size(self, selected_size):
        self.brush_size = selected_size  # ��������� ������ �����
        self.brush_size_scale.set(selected_size)  # ��������� ������� (��� �������������)

    def rgb_to_hex(self, rgb):
        """����������� RGB-������ � HEX-������, �������� Tkinter."""
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def pick_color(self, event):
        # �������� ���������� �������
        x, y = event.x, event.y
        # �������� ���� ������� �� �����������
        rgb_color = self.image.getpixel((x, y))
        self.pen_color = self.rgb_to_hex(rgb_color)  # ����������� � HEX ������
#       print(f"���� ������: {self.pen_color}")  # ������ ��� � �������, ������� Tkinter ��������
4.���������� �������������� ������� ������ �������� ��������.
��� ���������� ������� ������ ���������� ����� self.root.bind('<Control-s>', self.save_image)
��� ���������� � self.root.bind('<Control-c>', self.choose_color) ��� ������ �����.
������� ��������� ������ ��������� �������� �������, ���� ���� ��� ��� �� ����������.

5.���������� ��������� ��� ���������������� ��������� ����� �����.
���������: Label ��� ��������� ���������������� ��������� � ������ � ���������� ���� label,
������� ���������� ������� ���� �����. ���������� ����� � ����� update_color_preview()
��������� ���� ���� ����� label ��� ��� ������ ����� ����� ������, ��� � ��� ������������� "�������".

6.���������� ����������� ��������� ������� ������.����������� ���������: ��� ��������� ������� ������ �������� ������,
������� ��������� ���������� ���� (tk.simpledialog.askinteger) ��� ����� ����� ��������. ����� ��������� ����� ��������
��������� �������� width � height ������ � ������� ����� ������ Image � ������ ���������... 