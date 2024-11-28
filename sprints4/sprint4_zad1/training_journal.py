import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, PhotoImage
from tkcalendar import DateEntry
import json
from datetime import datetime
import csv
import matplotlib.pyplot as plt

# Файл для сохранения данных
data_file = 'training_log.json'


def load_data():
    """Загрузка данных о тренировках из файла."""
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data):
    """Сохранение данных о тренировках в файл."""
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)


class TrainingLogApp:
    def __init__(self, root):
        self.root = root
        root.title("Дневник тренировок")
        root.geometry("420x700")  # Увеличено для новых элементов
        icon = PhotoImage(file="G.png")  # Убедитесь, что файл существует
        root.iconphoto(False, icon)
        self.create_widgets()
        self.selected_item = None

    def create_widgets(self):
        """Создаем виджеты в главном окне"""
        # Виджеты для ввода данных
        self.exercise_label = ttk.Label(self.root, text="Упражнение:")
        self.exercise_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.exercise_entry = ttk.Entry(self.root)
        self.exercise_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        self.weight_label = ttk.Label(self.root, text="Вес:")
        self.weight_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        self.repetitions_label = ttk.Label(self.root, text="Повторения:")
        self.repetitions_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.repetitions_entry = ttk.Entry(self.root)
        self.repetitions_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        self.add_button = ttk.Button(self.root, text="Добавить запись", command=self.add_entry)
        self.add_button.grid(column=0, row=3, columnspan=2, pady=10)

        self.view_button = ttk.Button(self.root, text="Просмотреть записи", command=self.view_records)
        self.view_button.grid(column=0, row=4, columnspan=2, pady=10)

        self.edit_button = ttk.Button(self.root, text="Редактировать запись", command=self.edit_record)
        self.edit_button.grid(column=0, row=5, columnspan=2, pady=10)

        self.delete_button = ttk.Button(self.root, text="Удалить запись", command=self.delete_record)
        self.delete_button.grid(column=0, row=6, columnspan=2, pady=10)

        # Поля для фильтрации
        self.start_date_label = ttk.Label(self.root, text="Дата начала:")
        self.start_date_label.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
        self.start_date_entry = DateEntry(self.root)
        self.start_date_entry.grid(column=1, row=7, sticky=tk.EW, padx=5, pady=5)

        self.end_date_label = ttk.Label(self.root, text="Дата окончания:")
        self.end_date_label.grid(column=0, row=8, sticky=tk.W, padx=5, pady=5)
        self.end_date_entry = DateEntry(self.root)
        self.end_date_entry.grid(column=1, row=8, sticky=tk.EW, padx=5, pady=5)

        self.filter_button = ttk.Button(self.root, text="Фильтровать по датам", command=self.filter_by_date)
        self.filter_button.grid(column=0, row=9, columnspan=2, pady=10)

        self.exercise_filter_label = ttk.Label(self.root, text="Фильтр по упражнению:")
        self.exercise_filter_label.grid(column=0, row=10, sticky=tk.W, padx=5, pady=5)
        self.exercise_filter_entry = ttk.Entry(self.root)
        self.exercise_filter_entry.grid(column=1, row=10, sticky=tk.EW, padx=5, pady=5)

        self.exercise_filter_button = ttk.Button(self.root, text="Фильтровать по упражнению",
                                                 command=self.filter_by_exercise)
        self.exercise_filter_button.grid(column=0, row=11, columnspan=2, pady=10)

        # Кнопки для импорта и экспорта
        self.export_button = ttk.Button(self.root, text="Экспорт в CSV", command=self.export_to_csv)
        self.export_button.grid(column=0, row=12, columnspan=2, pady=10)

        self.import_button = ttk.Button(self.root, text="Импорт из CSV", command=self.import_from_csv)
        self.import_button.grid(column=0, row=13, columnspan=2, pady=10)

        # Кнопка статистики
        self.stats_button = ttk.Button(self.root, text="Показать статистику", command=self.show_statistics)
        self.stats_button.grid(column=0, row=14, columnspan=2, pady=10)

        # Кнопка для визуализации прогресса
        self.visualize_button = ttk.Button(self.root, text="Визуализация прогресса", command=self.visualize_progress)
        self.visualize_button.grid(column=0, row=15, columnspan=2, pady=10)

    def add_entry(self):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        entry = {
            'date': date,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        data = load_data()
        data.append(entry)
        save_data(data)

        # Очистка полей ввода после добавления
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")

    def view_records(self, records=None):
        """Просмотр записей"""
        # Использовать переданные записи, если они есть
        if records is None:
            data = load_data()
        else:
            data = records

        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")

        self.tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес(кг)", "Повторения"),
                                 show="headings")
        self.tree.heading('Дата', text="Дата")
        self.tree.heading('Упражнение', text="Упражнение")
        self.tree.heading('Вес(кг)', text="Вес(кг)")
        self.tree.heading('Повторения', text="Повторения")
        self.tree.pack(expand=True, fill=tk.BOTH)

        for entry in data:
            self.tree.insert('', tk.END,
                             values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))

        self.tree.bind("<ButtonRelease-1>", self.on_item_selected)  # Связываем выбор записи с обработчиком

    def on_item_selected(self, event):
        """Выбор действий"""
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_item = selected_item[0]
            item_data = self.tree.item(self.selected_item, 'values')
            self.exercise_entry.delete(0, tk.END)
            self.exercise_entry.insert(0, item_data[1])
            self.weight_entry.delete(0, tk.END)
            self.weight_entry.insert(0, item_data[2])
            self.repetitions_entry.delete(0, tk.END)
            self.repetitions_entry.insert(0, item_data[3])

    def edit_record(self):
        """Редактируем подсвеченную дату"""
        if not self.selected_item:
            messagebox.showerror("Ошибка", "Сначала выберите запись для редактирования!")
            return

        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        data = load_data()
        entry = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        # Обновляем запись в данных
        data[self.tree.index(self.selected_item)] = entry
        save_data(data)

        # Обновляем TreeView
        self.tree.item(self.selected_item,
                       values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
        messagebox.showinfo("Успешно", "Запись успешно отредактирована!")

    def delete_record(self):
        """Удаление подсвеченной даты"""
        if not self.selected_item:
            messagebox.showerror("Ошибка", "Сначала выберите запись для удаления!")
            return

        data = load_data()
        data.pop(self.tree.index(self.selected_item))  # Удаляем запись из данных
        save_data(data)

        # Удаляем запись из TreeView
        self.tree.delete(self.selected_item)
        messagebox.showinfo("Успешно", "Запись успешно удалена!")

    def filter_by_date(self):
        """Просмотр данных по дате."""
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        data = load_data()

        filtered_data = [entry for entry in data if
                         start_date <= datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S').date() <= end_date]
        if filtered_data:
            self.view_records(filtered_data)
        else:
            messagebox.showinfo("Результаты", "Не найдено записей за указанный период.")

    def filter_by_exercise(self):
        """Просмотр данных по упражнению."""
        exercise_name = self.exercise_filter_entry.get().strip()
        data = load_data()

        filtered_exercise_data = [entry for entry in data if entry['exercise'].lower() == exercise_name.lower()]
        if filtered_exercise_data:
            self.view_records(filtered_exercise_data)
        else:
            messagebox.showinfo("Результаты", "Не найдено записей для указанного упражнения.")

    def export_to_csv(self):
        """Выгрузка данных о тренировках из файла csv."""
        data = load_data()
        with open('training_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['date', 'exercise', 'weight', 'repetitions']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in data:
                writer.writerow(entry)
        messagebox.showinfo("Успешно", "Данные успешно экспортированы в CSV!")

    def import_from_csv(self):
        """Загрузка данных о тренировках из файла csv."""
        with open('training_log.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = load_data()
            for row in reader:
                data.append(row)
            save_data(data)
            messagebox.showinfo("Успешно", "Данные успешно импортированы из CSV!")

    def show_statistics(self):
        """Просмотр статистики по упражнениям."""
        data = load_data()
        statistics = {}
        for entry in data:
            month = entry['date'][:7]  # YYYY-MM
            weight = int(entry['weight'])

            if month in statistics:
                statistics[month] += weight
            else:
                statistics[month] = weight

        stats_window = Toplevel(self.root)
        stats_window.title("Статистика по упражнениям")
        stats_text = tk.Text(stats_window, wrap=tk.WORD)
        stats_text.pack(expand=True, fill=tk.BOTH)

        if statistics:
            for month, total_weight in statistics.items():
                stats_text.insert(tk.END, f"{month}: {total_weight} кг\n")
        else:
            stats_text.insert(tk.END, "Нет данных для отображения.")

    def visualize_progress(self):
        """Вывод графиков динамики по выполненным упражнениям."""
        data = load_data()
        exercises = {}
        for entry in data:
            exercise = entry['exercise']
            weight = int(entry['weight'])
            repetitions = int(entry['repetitions'])

            if exercise not in exercises:
                exercises[exercise] = {'weights': [], 'repetitions': [], 'dates': []}

            exercises[exercise]['weights'].append(weight)
            exercises[exercise]['repetitions'].append(repetitions)
            exercises[exercise]['dates'].append(datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S'))

        for exercise, values in exercises.items():
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.plot(values['dates'], values['weights'], marker='o')
            plt.title(f'Прогресс по {exercise} (вес)')
            plt.xlabel('Дата')
            plt.ylabel('Вес (кг)')
            plt.xticks(rotation=45)

            plt.subplot(1, 2, 2)
            plt.plot(values['dates'], values['repetitions'], marker='o', color='orange')
            plt.title(f'Прогресс по {exercise} (повторения)')
            plt.xlabel('Дата')
            plt.ylabel('Повторения')
            plt.xticks(rotation=45)

            plt.tight_layout()
            plt.show()


def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
