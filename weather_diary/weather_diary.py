import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "movies.json"


class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("750x550")

        # Данные
        self.movies = self.load_data()

        # Поля ввода
        self.create_input_frame()

        # Таблица для отображения
        self.create_treeview()

        # Кнопки управления
        self.create_buttons()

        # Фильтры
        self.create_filter_frame()

        self.refresh_table()

    # ------------------ Ввод данных ------------------
    def create_input_frame(self):
        frame = tk.LabelFrame(self.root, text="Добавить фильм", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        # Название
        tk.Label(frame, text="Название:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.title_entry = tk.Entry(frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Жанр
        tk.Label(frame, text="Жанр:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.genre_entry = tk.Entry(frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)

        # Год
        tk.Label(frame, text="Год выпуска:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.year_entry = tk.Entry(frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Рейтинг
        tk.Label(frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.rating_entry = tk.Entry(frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    # ------------------ Таблица ------------------
    def create_treeview(self):
        # Создаём контейнер с прокруткой
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(container, columns=("title", "genre", "year", "rating"),
                                 show="headings", yscrollcommand=scrollbar.set)
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")

        self.tree.column("title", width=250)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=80)
        self.tree.column("rating", width=80)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

    # ------------------ Кнопки ------------------
    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Button(frame, text="➕ Добавить фильм", command=self.add_movie,
                  bg="#4CAF50", fg="white", padx=10).pack(side="left", padx=5)
        tk.Button(frame, text="💾 Сохранить в JSON", command=self.save_to_file,
                  bg="#2196F3", fg="white", padx=10).pack(side="left", padx=5)
        tk.Button(frame, text="📂 Загрузить из JSON", command=self.load_from_file,
                  bg="#FF9800", fg="white", padx=10).pack(side="left", padx=5)
        tk.Button(frame, text="🗑️ Удалить выбранный", command=self.delete_movie,
                  bg="#F44336", fg="white", padx=10).pack(side="left", padx=5)
        tk.Button(frame, text="❌ Очистить фильтры", command=self.clear_filters,
                  bg="#9E9E9E", fg="white", padx=10).pack(side="left", padx=5)

    # ------------------ Фильтры ------------------
    def create_filter_frame(self):
        frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по жанру
        tk.Label(frame, text="Жанр:").grid(row=0, column=0, sticky="e", padx=5)
        self.filter_genre_entry = tk.Entry(frame, width=20)
        self.filter_genre_entry.grid(row=0, column=1, padx=5)

        # Фильтр по году
        tk.Label(frame, text="Год:").grid(row=0, column=2, sticky="e", padx=5)
        self.filter_year_entry = tk.Entry(frame, width=10)
        self.filter_year_entry.grid(row=0, column=3, padx=5)

        tk.Button(frame, text="🔍 Применить фильтры", command=self.apply_filters,
                  bg="#4CAF50", fg="white").grid(row=0, column=4, padx=10)

    # ------------------ Основная логика ------------------
    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        # Валидация названия
        if not title:
            messagebox.showerror("Ошибка", "Название фильма не может быть пустым")
            return

        # Валидация жанра
        if not genre:
            messagebox.showerror("Ошибка", "Жанр не может быть пустым")
            return

        # Валидация года
        try:
            year = int(year_str)
            if year < 1888 or year > 2030:
                messagebox.showerror("Ошибка", "Год должен быть между 1888 и 2030")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return

        # Валидация рейтинга
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
            return

        self.movies.append({
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        })

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

        self.refresh_table()
        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления")
            return

        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранный фильм?"):
            # Получаем название фильма для удаления
            item = self.tree.item(selected[0])
            values = item['values']
            title_to_delete = values[0]

            # Удаляем из списка
            self.movies = [m for m in self.movies if m["title"] != title_to_delete]

            self.refresh_table()
            messagebox.showinfo("Успех", f"Фильм '{title_to_delete}' удалён!")

    def refresh_table(self, filtered_movies=None):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = filtered_movies if filtered_movies is not None else self.movies
        for movie in data:
            self.tree.insert("", "end", values=(movie["title"], movie["genre"],
                                                movie["year"], movie["rating"]))

    def apply_filters(self):
        filter_genre = self.filter_genre_entry.get().strip().lower()
        filter_year_str = self.filter_year_entry.get().strip()

        filtered = self.movies[:]

        if filter_genre:
            filtered = [m for m in filtered if filter_genre in m["genre"].lower()]

        if filter_year_str:
            try:
                filter_year = int(filter_year_str)
                filtered = [m for m in filtered if m["year"] == filter_year]
            except ValueError:
                messagebox.showerror("Ошибка", "Год для фильтра должен быть числом")
                return

        self.refresh_table(filtered)

        if len(filtered) == 0:
            messagebox.showinfo("Результат", "Фильмы не найдены")

    def clear_filters(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.refresh_table()

    # ------------------ Работа с JSON ------------------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_to_file(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", f"Сохранено {len(self.movies)} фильмов в {DATA_FILE}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def load_from_file(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    loaded_movies = json.load(f)
                if isinstance(loaded_movies, list):
                    self.movies = loaded_movies
                    self.clear_filters()
                    messagebox.showinfo("Успех", f"Загружено {len(self.movies)} фильмов")
                else:
                    messagebox.showerror("Ошибка", "Неверный формат файла")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
        else:
            messagebox.showwarning("Нет файла", f"Файл {DATA_FILE} не найден")


# ------------------ Запуск ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()