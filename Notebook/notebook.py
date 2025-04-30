import sqlite3
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import time
import os


os.environ['TCL_LIBRARY'] = r'C:\Users\z1vertz\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'

# Создаем базу данных для хранения заметок
def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  title TEXT, 
                  content TEXT, 
                  timestamp TEXT)''')
    conn.commit()
    conn.close()


# Добавляем новую заметку
def add_note():
    title = entry_title.get()
    content = text_content.get("1.0", tk.END).strip()
    if title and content:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute('INSERT INTO notes (title, content, timestamp) VALUES (?, ?, ?)',
                  (title, content, timestamp))
        conn.commit()
        conn.close()
        messagebox.showinfo('Успех', 'Заметка добавлена!')
        entry_title.delete(0, tk.END)
        text_content.delete("1.0", tk.END)
        time.sleep(0.5)  # Пауза после добавления
        load_notes()
    else:
        messagebox.showwarning('Ошибка', 'Заголовок и содержание не могут быть пустыми!')


# Загружаем все заметки из базы данных
def load_notes():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM notes')
    rows = c.fetchall()
    listbox_notes.delete(0, tk.END)
    for row in rows:
        listbox_notes.insert(tk.END, f"{row[1]} ({row[3]})")
    conn.close()


# Экспорт заметок в файл JSON
def export_notes():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM notes')
    rows = c.fetchall()
    notes = [{'title': row[1], 'content': row[2], 'timestamp': row[3]} for row in rows]
    conn.close()

    file_path = filedialog.asksaveasfilename(defaultextension='.json',
                                             filetypes=[('JSON Files', '*.json')])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(notes, f, ensure_ascii=False, indent=4)
        messagebox.showinfo('Успех', 'Заметки экспортированы в JSON файл!')


# Импорт заметок из файла JSON
def import_notes():
    file_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            notes = json.load(f)

        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        for note in notes:
            c.execute('INSERT INTO notes (title, content, timestamp) VALUES (?, ?, ?)',
                      (note['title'], note['content'], note['timestamp']))
        conn.commit()
        conn.close()
        messagebox.showinfo('Успех', 'Заметки импортированы из JSON файла!')
        load_notes()


# Создаем графический интерфейс с помощью tkinter
root = tk.Tk()
root.title("Записная книжка")

# Поле для заголовка заметки
label_title = tk.Label(root, text="Заголовок:")
label_title.grid(row=0, column=0, padx=5, pady=5)
entry_title = tk.Entry(root, width=50)
entry_title.grid(row=0, column=1, padx=5, pady=5)

# Поле для содержания заметки
label_content = tk.Label(root, text="Содержание:")
label_content.grid(row=1, column=0, padx=5, pady=5)
text_content = tk.Text(root, width=50, height=10)
text_content.grid(row=1, column=1, padx=5, pady=5)

# Кнопка для добавления заметки
button_add = tk.Button(root, text="Добавить заметку", command=add_note)
button_add.grid(row=2, column=1, padx=5, pady=5)

# Список всех заметок
label_notes = tk.Label(root, text="Все заметки:")
label_notes.grid(row=3, column=0, padx=5, pady=5)
listbox_notes = tk.Listbox(root, width=50, height=10)
listbox_notes.grid(row=3, column=1, padx=5, pady=5)

# Кнопки для экспорта и импорта
button_export = tk.Button(root, text="Экспорт в JSON", command=export_notes)
button_export.grid(row=4, column=0, padx=5, pady=5)

button_import = tk.Button(root, text="Импорт из JSON", command=import_notes)
button_import.grid(row=4, column=1, padx=5, pady=5)

# Инициализация базы данных и загрузка заметок
init_db()
load_notes()

root.mainloop()
