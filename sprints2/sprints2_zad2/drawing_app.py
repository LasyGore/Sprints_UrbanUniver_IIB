import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw

class DrawingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (1280, 720), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=1280, height=720, bg='white')
        self.canvas.pack()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.brush_size = 1  # Начальный размер кисти
        self.previous_color = self.pen_color  # Сохранение предыдущего цвета кисти

        self.setup_ui()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.show_brush_size_menu)  # Обработка правого клика

        self.eraser_mode = False  # Параметр для отслеживания режима ластика

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.set(self.brush_size)  # Устанавливаем начальный размер
        self.brush_size_scale.pack(side=tk.LEFT)

        # Кнопка Ластик с изменяемым текстом и цветом
        self.eraser_button = tk.Button(control_frame, text="Ластик_OFF", command=self.toggle_eraser)
        self.eraser_button.pack(side=tk.LEFT)

    def toggle_eraser(self):
        if self.eraser_mode:
            self.pen_color = self.previous_color  # Возвращаем предыдущий цвет кисти
            self.eraser_button.config(text="Ластик_OFF", fg="black")  # Изменяем текст и цвет
            self.eraser_mode = False
        else:
            self.previous_color = self.pen_color  # Сохраняем текущий цвет перед переключением
            self.pen_color = 'white'  # Устанавливаем цвет фона для ластика
            self.eraser_button.config(text="Ластик_ON", fg="red")  # Изменяем текст и цвет
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

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
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
