from multiprocessing import connection
from sqlite3 import Cursor
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import psycopg2
from config import host, user, password, database

def connect_db():
    return psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
#Код для обновления табличек
def update_(table_name): 
    try:
        connection = connect_db()
        connection.autocommit = True
        cursor = connection.cursor()

        root = tk.Tk()
        root.title(f"Изменение данных в {table_name}")

        primary_key = get_primary_key(table_name)

        def pup():
            value2 = record_number_entry.get()
            column = column_entry.get()
            value1 = new_value_entry.get()
            cursor.execute(f'UPDATE {table_name} SET "{column}" = %s WHERE "{primary_key}" = %s', (value1, value2))
            connection.commit()
            messagebox.showinfo("Успех", "Запись успешно обновлена!")

        record_number_label = tk.Label(root, text=f"Введите {primary_key}, которое хотите изменить:")
        record_number_label.grid(row=0, column=0, padx=10, pady=5)
        record_number_entry = tk.Entry(root)
        record_number_entry.grid(row=0, column=1, padx=10, pady=5)

        column_label = tk.Label(root, text="Введите название столбца, которое хотите изменить:")
        column_label.grid(row=1, column=0, padx=10, pady=5)
        column_entry = tk.Entry(root)
        column_entry.grid(row=1, column=1, padx=10, pady=5)

        new_value_label = tk.Label(root, text="Введите новое значение:")
        new_value_label.grid(row=2, column=0, padx=10, pady=5)
        new_value_entry = tk.Entry(root)
        new_value_entry.grid(row=2, column=1, padx=10, pady=5)

        submit_button = tk.Button(root, text="Отправить", command=pup)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при работе с PostgreSQL: {e}")

#Код для удаления данных для выбраных таблиц
def delete_(table_name):
    try:
        connection = connect_db()
        connection.autocommit = True
        cursor = connection.cursor()

        primary_key = get_primary_key(table_name)

        root = tk.Tk()
        root.title(f"Удаление данных из {table_name}")

        def pup_del():
            try:
                value = new_value_entry.get()

                # Удаление зависимых записей перед удалением основной записи
                if table_name == 'Посетитель':
                    cursor.execute('DELETE FROM "Билет" WHERE "ID Посетителя" = %s', (value,))
                elif table_name == "Зоопарк":
                    cursor.execute('DELETE FROM "Поставщик_Зоопарк" WHERE "id_Зоопарка" = %s', (value,))
                    cursor.execute('DELETE FROM "Работники" WHERE "id_Зоопарка" = %s', (value,))
                    cursor.execute('DELETE FROM "Животные" WHERE "id_Зоопарка" = %s', (value,))
                elif table_name == 'Работники':
                    cursor.execute('DELETE FROM "Уход" WHERE "id_Работника" = %s', (value,))
                    cursor.execute('DELETE FROM "Уборщики" WHERE "id_Работника" = %s', (value,))
                    cursor.execute('DELETE FROM "Кипперы" WHERE "id_Работника" = %s', (value,))
                    cursor.execute('DELETE FROM "Мед. персонал" WHERE "id_Работника" = %s', (value,))
                elif table_name == 'Животные':
                    cursor.execute('DELETE FROM "Уход" WHERE "ID Животные" = %s', (value,))
                    cursor.execute('DELETE FROM "Клетка" WHERE "ID Животные" = %s', (value,))
                elif table_name == 'Клетка':
                    cursor.execute('DELETE FROM "Животные" WHERE "ID Клетка" = %s', (value,))
                elif table_name == 'Билет':
                    cursor.execute('DELETE FROM "Посетитель" WHERE "ID Билета" = %s', (value,))
                elif table_name == 'Поставщик':
                    cursor.execute('DELETE FROM "Поставщик_Зоопарк" WHERE "id_Поставщика" = %s', (value,))
                elif table_name == 'Класс':
                    cursor.execute('DELETE FROM "Животные" WHERE "ID Класса" = %s', (value,))
                elif table_name == 'Ракообразные':
                    cursor.execute('DELETE FROM "Животные" WHERE "ID Класса" = %s', (value,))
                elif table_name == 'Паукообразные':
                    cursor.execute('DELETE FROM "Животные" WHERE "ID Класса" = %s', (value,))
                elif table_name == 'Птицы':
                    cursor.execute('DELETE FROM "Животные" WHERE "ID Класса" = %s', (value,))
                elif table_name == 'Млекопитающие':
                    cursor.execute('DELETE FROM "Животные" WHERE "ID Класса" = %s', (value,))
                elif table_name == 'Земноводные':
                    cursor.execute('DELETE FROM "Животные" WHERE "ID Класса" = %s', (value,))

                # Удаление основной записи
                cursor.execute(f'DELETE FROM "{table_name}" WHERE "{primary_key}" = %s', (value,))
                connection.commit()
                messagebox.showinfo("Успех", "Запись успешно удалена!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при работе с PostgreSQL: {e}")

        new_value_label = tk.Label(root, text=f"Введите {primary_key}, которое хотите удалить:")
        new_value_label.grid(row=0, column=0, padx=10, pady=5)
        new_value_entry = tk.Entry(root)
        new_value_entry.grid(row=0, column=1, padx=10, pady=5)

        submit_button = tk.Button(root, text="Отправить", command=pup_del)
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при работе с PostgreSQL: {e}")

def search_(query, params_label):
    try:
        connection = connect_db()
        connection.autocommit = True
        cursor = connection.cursor()

        root = tk.Tk()
        root.title("Ввод данных для поиска")

        def execute_query():
            params = [entry.get() for entry in entry_fields]
            cursor.execute(query % tuple(params))
            connection.commit()
            search_record = cursor.fetchall()

            data_window = tk.Toplevel(root)
            data_window.title("Данные")

            tree = ttk.Treeview(data_window)
            tree["columns"] = tuple(range(len(cursor.description)))
            tree.column("#0", width=0, stretch=NO)  # Убираем лишнее место слева, скрывая колонку с индексом

            for i, column in enumerate(cursor.description):
                tree.heading(i, text=column[0], anchor='w')
                tree.column(i, anchor="w", width=100)

            for row in search_record:
                tree.insert("", tk.END, values=row)

            tree.pack(fill="both", expand=True)

        entry_fields = []
        for i in range(len(params_label)):
            label = tk.Label(root, text=f"Введите {params_label[i]}:")
            label.grid(row=i, column=0)
            entry_field = tk.Entry(root)
            entry_field.grid(row=i, column=1, padx=10, pady=5)
            entry_fields.append(entry_field)

        submit_button = tk.Button(root, text="Отправить", command=execute_query)
        submit_button.grid(row=len(params_label), column=0, columnspan=2, pady=10)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при работе с PostgreSQL: {e}")

def add_(table_name):
    try:
        connection = connect_db()
        connection.autocommit = True
        cursor = connection.cursor()

        root = tk.Tk()
        root.title(f"Добавление данных в {table_name}")

        entry_fields = []

        # Получаем все столбцы таблицы
        cursor.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
              AND table_name = '{table_name}'
        """)
        columns = [column[0] for column in cursor.fetchall()]

        def add_():
            values = [entry.get() for entry in entry_fields]
            columns_str = ', '.join(columns)
            query = f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({", ".join(["%s"] * len(values))})'
            cursor.execute(query, values)
            connection.commit()
            messagebox.showinfo("Успех", "Запись успешно добавлена!")
            root.destroy()

        row_index = 0
        for column in columns:
            label = tk.Label(root, text=f"Введите значение для {column}:")
            label.grid(row=row_index, column=0, padx=10, pady=5)
            entry_field = tk.Entry(root)
            entry_field.grid(row=row_index, column=1, padx=10, pady=5)
            entry_fields.append(entry_field)
            row_index += 1

        add_button = tk.Button(root, text="Добавить запись", command=add_)
        add_button.grid(row=row_index, columnspan=2, padx=10, pady=10)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при работе с PostgreSQL: {e}")

def show_table(table_name):
    try:
        connection = connect_db()
        connection.autocommit = True
        cursor = connection.cursor()
        primary_key = get_primary_key(table_name)
        cursor.execute(f'SELECT * FROM "{table_name}" ORDER BY "{primary_key}" ASC')
        rows = cursor.fetchall()

        display_window = tk.Toplevel(root)
        display_window.title(f"Таблица {table_name}")

        tree = ttk.Treeview(display_window)
        tree["columns"] = tuple(range(len(cursor.description)))
        tree.column("#0", width=0, stretch=NO)  # Убираем лишнее место слева, скрывая колонку с индексом

        for i, column in enumerate(cursor.description):
            tree.heading(i, text=column[0], anchor='w')
            tree.column(i, anchor="w", width=100)

        for row in rows:
            tree.insert("", tk.END, values=row)

        tree.pack(fill="both", expand=True)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при работе с PostgreSQL: {e}")

#выявления таюлицы если возникла ошибки
def on_table_selected(event=None):
    selected_index = table_list.curselection()
    if not selected_index:
        messagebox.showerror("Ошибка", "Не выбрана таблица")
        return None
    selected_table = table_list.get(selected_index)
    return selected_table

#конеретное название таблиц, чтоб можно было с ними работать с данными из pgAdmin 4
def get_primary_key(table_name):
    primary_keys = {
        "Билет": "ID Билета",
        "Животные": "ID Животные",
        "Земноводные": "ID Земноводного",
        "Зоопарк": "id_Зоопарка",
        "Кипперы": "id_Киппера",
        "Класс": "ID Класса",
        "Клетка": "ID Клетка",
        "Мед. персонал": "ID Мед.персонал",
        "Млекопитающие": "ID Млекопитающих",
        "Паукообразыне": "ID Паукообразных",
        "Посетитель": "ID Посетителя",
        "Поставщик_Зоопарк": "id_Поставщика",
        "Поставщики": "id_Поставщика",
        "Птицы": "ID Птиц",
        "Работники": "id_Работника",
        "Ракообразыне": "ID Ракообразного",
        "Уборщики": "ID Уборщика",
        "Уход": "id_Работника",
    }
    return primary_keys.get(table_name, "ID")

root = tk.Tk()
root.title("Управление базой данных")

table_names = [
        "Билет",
        "Животные",
        "Земноводные",
        "Зоопарк",
        "Кипперы",
        "Класс",
        "Клетка",
        "Мед. персонал",
        "Млекопитающие",
        "Паукообразыне",
        "Посетитель",
        "Поставщик_Зоопарк",
        "Поставщики",
        "Птицы",
        "Работники",
        "Ракообразыне",
        "Уборщики",
        "Уход",
]

table_list = tk.Listbox(root)
for table in table_names:
    table_list.insert(tk.END, table)
table_list.pack()

query_frame = ttk.LabelFrame(root, text="Запросы")
query_frame.pack(padx=10, pady=10, fill="both", expand="yes")

request_queries = [
    ("Запрос 1", 'SELECT * FROM "Животные" WHERE "ID Класса" = %s', 
     ["ID класса"]),
    ("Запрос 2", 'SELECT * FROM Работники WHERE Работники."Должность" = %s', 
     ["Должность работника"]),
    ("Запрос 3", 'SELECT "Должность" COUNT(*) AS "Количество работников" FROM "Работники" WHERE "Зарплата" = %s GROUP BY "Должность"', 
     ["Зарплата"]),
    ("Запрос 4", 'SELECT * FROM "Животные" WHERE "Название животного" = %s ORDER BY "Название животного" DESC', 
     ["Название животного"]),
    ("Запрос 5", 'SELECT * FROM "Работники" WHERE "Должность" = %s ORDER BY "id_Работника" DESC', 
     ["Должность"])
]

for label, query, params in request_queries:
    button = ttk.Button(query_frame, text=label, command=lambda q=query, p=params: search_(q, p))
    button.pack(fill="x")

operation_frame = ttk.LabelFrame(root, text="Операции")
operation_frame.pack(padx=10, pady=10, fill="both", expand="yes")

delete_button = ttk.Button(operation_frame, text="Удалить", command=lambda: delete_(on_table_selected()))
delete_button.pack(fill="x")

update_button = ttk.Button(operation_frame, text="Изменить", command=lambda: update_(on_table_selected()))
update_button.pack(fill="x")

add_button = ttk.Button(operation_frame, text="Добавить", command=lambda: add_(on_table_selected()))
add_button.pack(fill="x")

show_table_button = ttk.Button(root, text="Показать таблицу", command=lambda: show_table(on_table_selected()))
show_table_button.pack(fill="x")

root.mainloop() 