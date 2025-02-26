from tkinter import ttk
import tkinter as tk
import re

class Calculator:
    entry_state = ""
    temp_result = ""
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.style.theme_use("xpnative")
        self.root.bind('<Key>', self.handle_keypress)
        # self.style.configure('custom.TButton', font=('Arial', '15'), width=5)
        self.style.configure('TButton', font=('Arial, 15'), width=6)
        self.entry = ttk.Entry(self.root, font=('Arial', 20, 'bold'), justify='right')
        self.entry.grid(row=0, column=0, sticky='ew', columnspan=4, ipady=15, ipadx=5)
        self.entry.insert(0, '0')

        self.setup_btns()

    def setup_btns(self):
        digits = [
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2)
        ]
        operators = [
            ('/', 1, 3),
            ('x', 2, 3),
            ('-', 3, 3),
            ('+', 4, 3),

            ('^', 2, 0), ('²√', 2, 1), ('%', 2, 2)
        ]
        special_btns = [
            ('C', 1, 0, self.clear_entry), ('CE', 1, 1, self.clear_entry), ('DEL', 1, 2, self.delete_digit),
            ('0', 6, 0, lambda t='0' :self.add_digits(t)), ('00', 6, 1, lambda t='00' :self.add_digits(t)), ('.', 6, 2, self.add_decimal)
        ]
        for text, row, col in digits+operators:
            btn = ttk.Button(self.root, text=text, style='custom.TButton', command=lambda t=text: self.add_digits(t))
            btn.grid(row=row, column=col, ipadx=5, ipady=15)

        for text, row, col, cmd in special_btns:
            btn = ttk.Button(self.root, text=text, style='custom.TButton', command=cmd)
            btn.grid(row=row, column=col, ipadx=5, ipady=15)
            ('=', 6, 3, self.calculate)
        btn = ttk.Button(self.root, text="=", style='custom.TButton', command=self.calculate)
        btn.grid(row=5, column=3, ipadx=5, ipady=15, rowspan=2, sticky='ns')
        
        # theme_btn = ttk.Button(self.root, text="Theme", command=self.change_theme)
        # theme_btn.grid(row=6, column=0, sticky='ew', columnspan=4) 
    
    def add_digits(self, digit):
        if digit in "+-x/":
            if self.temp_result != "":
                self.entry_state = str(self.temp_result)
            return self.add_operator(digit)
        if self.temp_result != "" : self.temp_result = ""

        if digit == "0" or digit == "00":
            if self.entry_state == "":
                return
        data = self.entry_state + digit
        self.entry.delete(0, tk.END)
        self.entry.insert(0, data)
        self.entry_state = data

    def add_operator(self, operator):
        if self.entry_state == "":
            data = "0" + operator
            self.entry_state = data
            self.entry.delete(0, tk.END)
            self.entry.insert(0, data)
        elif self.entry_state[-1] in "+-x/":
            data = self.entry_state[:-1] + operator
            self.entry_state = data
            self.entry.delete(0, tk.END)
            self.entry.insert(0, data)
        else:
            data = self.entry_state + operator 
            self.entry_state = data
            self.entry.delete(0, tk.END)
            self.entry.insert(0, data)      

    def add_decimal(self):
        data = self.entry_state
        last_number = re.split(r"[+\-*x/]", self.entry_state)[-1]
        if data == "" or data[-1] in "+-x/":
            self.entry_state = data + "0" + "."
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.entry_state)
        elif '.' in last_number:
            return
        else:
            self.entry_state = data + "."
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.entry_state)

    def calculate(self):
        data = self.entry_state.replace('x', '*').replace('^', '**')
        data = re.sub(r'(\d+)%', r'\1/100', data)
        data = re.sub(r'(\d+)([+-/])(\d+/100)', r'\1\2(\1*\3)', data)
        if data == "":
            return
        try:
            result = eval(data)
            self.temp_result = result
            self.entry_state = ""
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        except (SyntaxError, NameError):
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Syntax error")
        except ZeroDivisionError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Zero Division Error")

    def clear_entry(self):
        self.entry_state = ""
        self.temp_result = ""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, '0') 

    def delete_digit(self):
        if self.temp_result != "":
            self.entry_state = str(self.temp_result)
            self.temp_result = ""
        data = self.entry_state[:-1]
        self.entry_state = data
        if len(data) == 0:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, '0')
        else:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, data)
    
    def handle_keypress(self, event):
        if event.char == "\r":
            self.calculate()
        self.entry_state = self.entry.get()

    def change_theme(self):
        themes = self.style.theme_names()
        import random
        theme = random.choices(themes)
        self.style.theme_use(theme)
        print(theme)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Calculator")
    root.resizable(False, False)
    calculator = Calculator(root)
    root.mainloop()
