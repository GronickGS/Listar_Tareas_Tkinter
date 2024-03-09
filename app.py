import tkinter as tk
from tkinter import messagebox
import sqlite3

class TaskApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Aplicación de Lista de Tareas")
        self.geometry("400x400")

        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.task_listbox = tk.Listbox(self, width=50)
        self.task_listbox.pack(pady=10)

        self.refresh_task_list()

        self.task_entry = tk.Entry(self, width=40)
        self.task_entry.pack(pady=5)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)

        self.add_button = tk.Button(self.button_frame, text="Agregar Tarea", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Eliminar Tarea", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.complete_button = tk.Button(self, text="Completar Tarea", command=self.complete_task)
        self.complete_button.pack(pady=5)

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                    id INTEGER PRIMARY KEY,
                                    description TEXT,
                                    completed INTEGER
                                )''')
        self.conn.commit()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.cursor.execute("SELECT * FROM tasks").fetchall()
        for task in tasks:
            task_description = task[1]
            if task[2]:
                task_description += " - COMPLETADA"
            self.task_listbox.insert(tk.END, task_description)

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            # Asegurar que la primera letra sea mayúscula
            task_text = task_text.capitalize()
            self.cursor.execute("INSERT INTO tasks (description, completed) VALUES (?, ?)", (task_text, 0))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.refresh_task_list()

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_id = self.cursor.execute("SELECT id FROM tasks").fetchall()[selected_index][0]
            self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            self.conn.commit()
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Eliminar Tarea", "Selecciona una tarea para eliminar")

    def complete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_id = self.cursor.execute("SELECT id FROM tasks").fetchall()[selected_index][0]
            self.cursor.execute("UPDATE tasks SET completed=? WHERE id=?", (1, task_id))
            self.conn.commit()
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Completar Tarea", "Selecciona una tarea para marcar como completada")

if __name__ == "__main__":
    app = TaskApp()
    app.mainloop()