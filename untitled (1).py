import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import requests
import json
import os

# Название файла для хранения избранных
FAVORITES_FILE = 'favorites.json'

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        
        # Поле поиска
        self.search_var = tk.StringVar()
        search_frame = ttk.Frame(root)
        search_frame.pack(padx=10, pady=10, fill='x')
        ttk.Label(search_frame, text="Введите имя пользователя GitHub:").pack(side='left')
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side='left', expand=True, fill='x', padx=5)
        ttk.Button(search_frame, text="Поиск", command=self.search_user).pack(side='left')
        
        # Результаты поиска
        self.results_frame = ttk.Frame(root)
        self.results_frame.pack(padx=10, pady=5, fill='both', expand=True)
        self.results_list = tk.Listbox(self.results_frame)
        self.results_list.pack(side='left', fill='both', expand=True)
        self.results_list.bind('<Double-1>', self.add_to_favorites)
        
        scrollbar = ttk.Scrollbar(self.results_frame, orient='vertical', command=self.results_list.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_list.config(yscrollcommand=scrollbar.set)
        
        # Панель с избранными
        favorites_btn_frame = ttk.Frame(root)
        favorites_btn_frame.pack(padx=10, pady=10)
        ttk.Button(favorites_btn_frame, text="Показать избранных", command=self.show_favorites).pack()
        
        # Загрузка избранных
        self.favorites = self.load_favorites()

    def load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_favorites(self):
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=2)

    def search_user(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым.")
            return
        url = f"https://api.github.com/users/{query}"
        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            self.results_list.delete(0, tk.END)
            user_info = f"{user_data['login']} - {user_data['name'] or 'Нет имени'}"
            self.results_list.insert(tk.END, user_info)
            # Сохраняем данные о пользователе для добавления
            self.current_user = user_data
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден.")

    def add_to_favorites(self, event):
        if hasattr(self, 'current_user'):
            user = self.current_user
            if not any(u['login'] == user['login'] for u in self.favorites):
                self.favorites.append(user)
                self.save_favorites()
                messagebox.showinfo("Добавлено", f"Пользователь {user['login']} добавлен в избранное.")
            else:
                messagebox.showinfo("Информация", "Этот пользователь уже в избранных.")
    
    def show_favorites(self):
        favs = self.favorites
        fav_names = [f"{u['login']} - {u.get('name', 'Нет имени')}" for u in favs]
        messagebox.showinfo("Избранные пользователи", "\n".join(fav_names) or "Нет избранных пользователей.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()