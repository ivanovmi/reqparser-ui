import Tkinter as tk

root = tk.Tk()

global num
num = 0

def create():
    global entry
    global num
    if num == 0:
        num = 1
        entry = tk.Entry()
        entry.pack()

def destroy():
    global entry
    global num
    if num == 1:
        num = 0
        entry.destroy()

button1 = tk.Button(text = 'create_email_entry entry', command = create)
button1.pack()

button2 = tk.Button(text = 'destroy entry', command = destroy)
button2.pack()

root.mainloop()