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

        # Кнопка для добавления текста
        text_button = tk.Button(control_frame, text="Текст", command=self.add_text)
        text_button.pack(side=tk.LEFT)

        # Кнопка для изменения цвета фона
        background_color_button = tk.Button(control_frame, text="Изменить фон", command=self.change_background_color)
        background_color_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.set(self.brush_size)
        self.brush_size_scale.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(control_frame, text="Ластик_OFF", command=self.toggle_eraser)
        self.eraser_button.pack(side=tk.LEFT)

        self.color_preview = tk.Label(control_frame, bg=self.pen_color, width=6, height=1)
        self.color_preview.pack(side=tk.LEFT)

    def change_canvas_size(self):
        size = simpledialog.askstring("Размер холста", "Введите ширину и высоту через пробел (например, '1280 720'):")

        if size:
            try:
                width, height = map(int, size.split())
                if 100 <= width <= 3000 and 100 <= height <= 3000:
                    self.canvas_width = width
                    self.canvas_height = height
                    self.canvas.config(width=self.canvas_width, height=self.canvas_height)
                    self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
                    self.draw = ImageDraw.Draw(self.image)
                    self.clear_canvas()  # Очистить холст
                else:
                    messagebox.showerror("Ошибка", "Размеры должны быть от 100 до 3000.")
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите два числа.")

    def add_text(self):
        text = simpledialog.askstring("Введите текст", "Введите текст, который хотите добавить:")
        if text:
            self.canvas.bind('<Button-1>', lambda event: self.draw_text(event, text))

    def draw_text(self, event, text):
        x, y = event.x, event.y
        self.draw.text((x, y), text, fill=self.pen_color)  # Рисуем текст на изображении
        self.canvas.create_text(x, y, text=text, fill=self.pen_color)  # Рисуем текст на холсте

        # Снимаем привязку после добавления текста
        self.canvas.unbind('<Button-1>')

    def change_background_color(self):
        new_color = colorchooser.askcolor()[1]
        if new_color:
            # Обновляем только фон: создаем новое изображение с цветом фона
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), new_color)
            # Очищаем холст
            self.clear_canvas()
            # Устанавливаем новый цвет фона на Canvas
            self.canvas.config(bg=new_color)

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

    def rgb_to_hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def pick_color(self, event):
        x, y = event.x, event.y
        rgb_color = self.image.getpixel((x, y))
        self.pen_color = self.rgb_to_hex(rgb_color)
        self.update_color_preview()

    def update_color_preview(self):
        self.color_preview.config(bg=self.pen_color)

    def paint(self, event):
        if self.last_x is not None and self.last_y is not None:
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
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.update_color_preview()

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                 filetypes=[('PNG files', '*.png'), ('All files', '*.*')])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()