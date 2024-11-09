import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw


class DrawingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.canvas_width = 1280
        self.canvas_height = 720
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.brush_size = 1
        self.previous_color = self.pen_color

        self.setup_ui()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)

        # Привязка горячих клавиш
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

        self.eraser_mode = False

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Кнопка для изменения размера холста
        resize_button = tk.Button(control_frame, text="Изменить размер холста", command=self.change_canvas_size)
        resize_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.set(self.brush_size)
        self.brush_size_scale.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(control_frame, text="Ластик_OFF", command=self.toggle_eraser)
        self.eraser_button.pack(side=tk.LEFT)

        self.color_preview = tk.Label(control_frame, bg=self.pen_color, width=6, height=1)
        self.color_preview.pack(side=tk.LEFT)

    def change_canvas_size(self):
        # Запрашиваем новые размеры холста
        size = simpledialog.askstring("Размер холста", "Введите ширину и высоту через пробел (например, '1280 720'): ")

        if size:
            try:
                width, height = map(int, size.split())
                if 100 <= width <= 3000 and 100 <= height <= 3000:
                    self.canvas_width = width
                    self.canvas_height = height
                    # Обновляем холст
                    self.canvas.config(width=self.canvas_width, height=self.canvas_height)
                    # Создаем новое изображение
                    self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
                    self.draw = ImageDraw.Draw(self.image)
                    self.clear_canvas()  # Очистить холст
                else:
                    messagebox.showerror("Ошибка", "Размеры должны быть от 100 до 3000.")
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите два числа.")
    # Остальные методы остаются без изменений...

    def toggle_eraser(self):
        if self.eraser_mode:
            self.pen_color = self.previous_color
            self.eraser_button.config(text="Ластик_OFF", fg="black")
            self.eraser_mode = False
        else:
            self.previous_color = self.pen_color
            self.pen_color = 'white'
            self.eraser_button.config(text="Ластик_ON", fg="red")
            self.eraser_mode = True

    def show_brush_size_menu(self, event):
        sizes = [1, 3, 5, 7, 10]
        menu = tk.Menu(self.root, tearoff=0)

        for size in sizes:
            menu.add_command(label=f"{size}", command=lambda s=size: self.update_brush_size(s))

        menu.post(event.x_root, event.y_root)  # Отображаем меню в позиции курсора

    def update_brush_size(self, selected_size):
        self.brush_size = selected_size  # Обновляем размер кисти
        self.brush_size_scale.set(selected_size)  # Обновляем слайдер (для синхронизации)

    def rgb_to_hex(self, rgb):
        """Преобразует RGB-кортеж в HEX-строку, понятную Tkinter."""
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def pick_color(self, event):
        x, y = event.x, event.y
        rgb_color = self.image.getpixel((x, y))
        self.pen_color = self.rgb_to_hex(rgb_color)
        self.update_color_preview()

    # Остальные функции...
    # (методы: paint, reset, clear_canvas, choose_color, save_image, update_color_preview, rgb_to_hex)
    def update_color_preview(self):
        self.color_preview.config(bg=self.pen_color)  # Изменяем фон label на текущий цвет кисти

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)

            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (1280, 720), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.update_color_preview()  # Обновляем предварительный просмотр цвета

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()