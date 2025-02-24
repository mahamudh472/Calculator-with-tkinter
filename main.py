import tkinter as tk
from tkinter import ttk
import re

def add_to_entry(item):
    if item == '.':
        add_decimal()
        return
    current = entry.get()
    current += item
    entry.delete(0, tk.END)
    entry.insert(0, current)

def add_decimal():
    current = entry.get()
    last_number = re.split(r"[+\-*/]", current)[-1]
    if '.' not in last_number:
        current += '.'
        entry.delete(0, tk.END)
        entry.insert(0, current)

def clear_entry():
    entry.delete(0, tk.END)
    entry.insert(0, '0')

def delete_last():
    current = entry.get()[:-1]
    entry.delete(0, tk.END)
    entry.insert(0, current)
    

def calculate():
    current = entry.get().replace('x', '*')
    try:
        res = eval(current)
        entry.delete(0, tk.END)
        entry.insert(0, res)
    except:
        entry.delete(0, tk.END)
        entry.insert(0, 'Syntax error')
root = tk.Tk()
root.geometry()
frame = ttk.Frame(root, width=300, height=500)
frame.pack()

style = ttk.Style()
style.configure('custom.TButton', font=('Arial', 20,), width=5, height=20)

buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2),
    ('+/-', 5, 0), ('0', 5, 1), ('.', 5, 2)
]

operators = [
    ('/', 1, 3), ('x', 2, 3), ('-', 3, 3), ('+', 4, 3)
]

special_btns = [
    ('C', 1, 0, clear_entry), ('CE', 1, 1, clear_entry), ('DEL', 1, 2, delete_last)
]

entry = ttk.Entry(frame, justify='right', font=('Arial', 20, 'bold'))
entry.grid(row=0, column=0, columnspan=4, sticky='ew', ipadx=5, ipady=15)
entry.insert(0, '0')
for text, row, col in buttons+operators:
    btn = ttk.Button(frame, text=text, style='custom.TButton', command=lambda t=text: add_to_entry(t))
    btn.grid(row=row, column=col, ipadx=5, ipady=5)

for text, row, col, cmd in special_btns:
    btn = ttk.Button(frame, text=text, style='custom.TButton', command=cmd)
    btn.grid(row=row, column=col, ipadx=5, ipady=5)

equal_btn = ttk.Button(frame, text="=", style='custom.TButton', command=calculate)
equal_btn.grid(row=5, column=3, ipadx=5, ipady=5)
root.mainloop()