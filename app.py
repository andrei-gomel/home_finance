import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry, Calendar
import db as db
import helper as helper

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(self)
        # print(self.style.theme_names())
        self.style.theme_use('clam')
        self.title('Домашняя бухгалтерия')
        self['background'] = '#EBEBEB'
        self.conf = {'padx':(10, 30), 'pady':10}
        self.bold_font = 'Helvetica 15 bold'
        self.put_frames()        


    def refresh(self):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.put_frames()


    def put_frames(self):
        self.add_form_frame = AddForm(self).grid(row=0, column=0, sticky='nswe')
        self.stat_frame = StatFrame(self).grid(row=0, column=1, sticky='nswe')
        self.table_frame = TableFrame(self).grid(row=1, column=0, columnspan=2, sticky='ew')
        # self.buttom_frame = ButtomFrame(self).grid(row=2, column=0, columnspan=2, sticky='nswe')


class AddForm(tk.Frame):
    """docstring for AddForm"""
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.categories = db.get_categories()
        self.put_widgets()


    def put_widgets(self):
        self.l_choose = ttk.Label(self, text="Выберите категорию", font=self.master.bold_font)
        self.f_choose = ttk.Combobox(self, values=self.categories['names'])
        self.l_amount = ttk.Label(self, text="Введите сумму", font=self.master.bold_font)
        self.f_amount = ttk.Entry(self, justify=tk.RIGHT, validate="key", 
            validatecommand=(self.register(self.validate_amount), '%P'))
        self.l_date = ttk.Label(self, text="Введите дату", font=self.master.bold_font)
        self.f_date = DateEntry(self, date_pattern='yyyy-MM-dd', background = "green",
                          foreground = "white",
                          selectbackground = "red",
                          normalbackground = "lightgreen",
                          weekendbackground = "darkgreen",
                          weekendforeground = "white")
        self.button_submit = ttk.Button(self, text="Сохранить", command=self.form_submit)        
        self.l_choose.grid(row=0, column=0, sticky="w", cnf=self.master.conf)
        self.f_choose.grid(row=0, column=1, sticky="e", cnf=self.master.conf)
        self.l_amount.grid(row=1, column=0, sticky="w", cnf=self.master.conf)
        self.f_amount.grid(row=1, column=1, sticky="e", cnf=self.master.conf)
        self.l_date.grid(row=2, column=0, sticky="w", cnf=self.master.conf)
        self.f_date.grid(row=2, column=1, sticky="e", cnf=self.master.conf)
        self.button_submit.grid(row=3, column=0, columnspan=2, sticky="n", cnf=self.master.conf)
        # Для MacOS:
        # self.f_date._top_cal.overrideredirect(False)


    def validate_amount(self, input):
        try:
            x = float(input)
            return True
        except ValueError:
            return False


    def form_submit(self):
        flag = True        
        data = self.f_date.get()        
        try:
            category_id = self.categories['accordance'][self.f_choose.get()]
            price = float(self.f_amount.get())
        except KeyError:
            if self.f_choose.get() == '':
                flag = False
        except ValueError:
            flag = False
        if flag:
            insert_data = (category_id, data, price)
            # print(insert_data)
            if db.insert_new_payment(insert_data):
                self.master.refresh()


class StatFrame(tk.Frame):
    """docstring for StatFrame"""
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.most_popular_item = db.get_most_popular_item()
        self.most_rich_item = db.get_most_rich_item()
        self.total_sum = db.get_total_sum()
        # print('Самая дорогая категория ', self.most_rich_item['name'])
        print('Итого за месяц: ', self.total_sum['Total'])
        self.put_widgets()


    def put_widgets(self):
        l_most_common_text = tk.Label(self, text='Самая популярная позиция', font=self.master.bold_font)
        l_most_common_value = tk.Label(self, text=self.most_popular_item['name'], font=self.master.bold_font)
        l_exp_item_text = tk.Label(self, text='Самая дорогая позиция', font=self.master.bold_font)
        l_exp_item_value = tk.Label(self, text=self.most_rich_item['name'], font=self.master.bold_font)
        l_exp_day_text = tk.Label(self, text='Дорогая категория, итого', font=self.master.bold_font)
        l_exp_day_value = tk.Label(self, text=self.most_rich_item['total'], font=self.master.bold_font)
        l_exp_month_text = tk.Label(self, text='Итого за месяц', font=self.master.bold_font)
        l_exp_month_value = tk.Label(self, text=self.total_sum['Total'], font=self.master.bold_font)
        l_most_common_text.grid(row=0, column=0, sticky='w', cnf=self.master.conf)
        l_most_common_value.grid(row=0, column=1, sticky='e', cnf=self.master.conf)
        l_exp_item_text.grid(row=1, column=0, sticky='w', cnf=self.master.conf)
        l_exp_item_value.grid(row=1, column=1, sticky='e', cnf=self.master.conf)
        l_exp_day_text.grid(row=2, column=0, sticky='w', cnf=self.master.conf)
        l_exp_day_value.grid(row=2, column=1, sticky='e', cnf=self.master.conf)
        l_exp_month_text.grid(row=3, column=0, sticky='w', cnf=self.master.conf)
        l_exp_month_value.grid(row=3, column=1, sticky='e', cnf=self.master.conf)


class TableFrame(tk.Frame):
    """docstring for TableFrame"""
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']        
        self.payments = db.get_list_payments()
        self.all_payments = helper.convert_payments(self.payments)
        helper.output_payments(self.payments)
        self.put_widgets()


    def get_number_list(self, table):
        return table.selection()

    
    def put_widgets(self):
        heads = ['id', 'Дата', 'Наименование', 'Сумма']
        table = ttk.Treeview(self, show="headings")
        # selected_items = self.table.selection()
        # print(selected_items)
        table['columns'] = heads
        # Меняем очередность вывода данных
        # table['displaycolumns'] = ['price', 'model', 'owner', 'id']
        for header in heads:
            table.heading(header, text=header, anchor='center')
            table.column(header, anchor='center')
        for row in self.all_payments:
            table.insert('', tk.END, values=row)
        scroll_pane = ttk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        button_edit = ttk.Button(self, text="Редактировать", command=lambda:self.edit_item(table))
        button_edit.pack(side=tk.LEFT, padx=240, pady=10, anchor='center')
        button_del = ttk.Button(self, text="Удалить", command=lambda:self.edit_item(table))
        button_del.pack(side=tk.LEFT, pady=10)
        
        
    def edit_item(self, table):
        self.selected_item = table.selection()[0]
        # if selected_item.startswith('I'):
        self.item_id = int(self.selected_item[1:], 16)  # Интерпретируем как hex и преобразуем в int
        print(self.item_id)
        self.item_payment = db.select_one(self.item_id)
        # Создаем дочернее окно
        edit_window = tk.Tk()
        edit_window.title("Редактировать запись")
        edit_window.geometry("400x300")
        edit_window.grab_set()  # Сделать модальным
        
        # Поля ввода
        tk.Label(edit_window, text="Дата:").grid(row=0, column=0, padx=10, pady=5)
        data_entry = tk.Entry(edit_window)
        data_entry.grid(row=0, column=1, padx=10, pady=5)
        data_entry.insert(0, self.item_payment['data'])  # Предзаполнение
        
        tk.Label(edit_window, text="Категория:").grid(row=1, column=0, padx=10, pady=5)
        name_entry = tk.Entry(edit_window)
        name_entry.grid(row=1, column=1, padx=10, pady=5)
        name_entry.insert(0, self.item_payment['name'])

        tk.Label(edit_window, text="Сумма:").grid(row=2, column=0, padx=10, pady=5)
        price_entry = tk.Entry(edit_window)
        price_entry.grid(row=2, column=1, padx=10, pady=5)
        price_entry.insert(0, self.item_payment['price'])
        button_save = ttk.Button(edit_window, text="Сохранить", command=lambda:self.save_item(table))
        button_save.grid(row=3, columnspan=2)


    def save_item():
        pass


class ButtomFrame(tk.Frame):
    """docstring for ButtomFrame"""
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        # self.put_widgets()


    def put_widgets(self):
        self.button_submit = ttk.Button(self, text="Сохранить", command=self.edit_item)
        self.button_submit.grid(row=3, column=0, sticky="n", cnf=self.master.conf)
        

    def edit_item(self):
        self.selected_item = TableFrame.get_number_list(self)
        print(self.selected_item)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
