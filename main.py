from Tkinter import *
import lan
import body
import time
import threading
from tkFileDialog import askopenfilename
import tkMessageBox
import requests
import ttk


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.label_usr = Label(self, text='Login')
        self.label_pswd = Label(self, text='Password')
        self.entry_usr = Entry(self)
        self.entry_pswd = Entry(self, show='*')
        self.button = Button(self, text='Login', command=self.new_layout)
        self.label_err = Label(self)
        self.grid()
        self.geometry('200x260')
        self.create_widgets()

    def create_email_entry(self):
        if self.email_exist == 1:
            pass
        else:
            self.email_label = Label(self, text='Input email address:')
            self.email_entry = Entry(self)
            self.email_label.grid(row=6, column=0)
            self.email_entry.grid(row=6, column=1, columnspan=2)
            self.email_exist = 1

    def delete_email_entry(self):
        if self.email_exist == 0:
            pass
        else:
            self.email_label.grid_forget()
            self.email_entry.grid_forget()
            self.email_exist = 0

    def generate_report(self):
        self.branch_name = self.branch_strvar.get()
        self.mode = self.mode_strvar.get()
        self.spec = self.strvar.get()
        self.global_branch = self.global_branch_strvar.get()
        self.send = self.boolvar.get()
        if self.send:
            self.mail = self.email_entry.get()
            body.main(self.gerrit, self.mode, self.spec, self.branch_name, self.global_branch, self.send, self.mail)
        else:
            body.main(self.gerrit, self.mode, self.spec, self.branch_name, self.global_branch)

    @staticmethod
    def center(win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def processing_please_wait(self):
        self.window = Toplevel()
        self.window.overrideredirect(1)
        self.window.geometry('100x30')
        self.center(self.window)
        # code before computation starts
        self.label = Label(self.window, text='Wait for login')
        self.label.grid(ipadx=4, ipady=8)

        def call():
            time.sleep(5)

        thread = threading.Thread(target=call)
        thread.start()  # start parallel computation
        while thread.is_alive():
            # code while computing
            self.window.update()
            time.sleep(0.001)
        self.window.destroy()

    def create_widgets(self):
        self.label_usr.pack()
        self.entry_usr.pack()
        self.label_pswd.pack()
        self.entry_pswd.pack()
        self.button.pack()

    def new_layout(self):
        self.label_err.destroy()
        self.button.destroy()
        self.processing_please_wait()
        try:
            self.gerrit = lan.login_to_launchpad(self.entry_usr.get(), self.entry_pswd.get())
        except KeyError:
            self.button = Button(self, text='Login', command=self.new_layout)
            self.label_err = Label(self, text='Not autenticate')
            self.button.pack()
            self.label_err.pack()
        except requests.ConnectionError:
            self.button = Button(self, text='Login', command=self.new_layout)
            self.label_err = Label(self, text='Connection refused')
            self.button.pack()
            self.label_err.pack()
        else:
            self.main_window()

    def callback(self):
        self.name = askopenfilename()
        self.file_entry.insert(0, self.name)
        self.file_entry.grid(row=7, column=0)

    def main_window(self):
        # Clear window to new use
        for widget in app.winfo_children():
            widget.destroy()

        self.geometry('520x260')
        self.center(self)

        self.mode_label = Label(self, text='Select a mode:')
        self.mode_strvar = StringVar()
        self.mode_strvar.set('requirements')
        self.mode_switcher = OptionMenu(self, self.mode_strvar, 'requirements', 'epoch')

        self.spec_label = Label(self, text='Select what we scan:')
        self.strvar = StringVar()
        self.strvar.set('')
        self.check_spec_switcher = OptionMenu(self, self.strvar, '', 'control', 'spec')

        self.branch_label = Label(self, text='At the what branch we should check requirements?')
        self.branch_strvar = StringVar()
        self.branch_strvar.set('master')
        self.branch_switcher = OptionMenu(self, self.branch_strvar, 'master', '6.1', '6.0.1')

        self.global_branch_label = Label(self, text='At the what branch we should find global requirements?')
        self.global_branch_strvar = StringVar()
        self.global_branch_strvar.set('master')
        self.global_branch_switcher = OptionMenu(self, self.global_branch_strvar, 'master', 'stable/juno', 'stable/icehouse')
        self.global_branch_switcher.configure(width=15)

        self.var = IntVar()
        self.var.set(1)
        self.select_format_label = Label(self, text='Please, select format of output:')
        self.pdf_format_radiobutton = Radiobutton(self, text='pdf', variable=self.var, value=1)
        self.html_format_radiobutton = Radiobutton(self, text='html', variable=self.var, value=2)

        self.boolvar = BooleanVar()
        self.email_exist = 0
        self.email_quiestion = Label(self, text='Would you like to send e-mail?')
        self.email_yes_radiobutton = Radiobutton(self, text='Yes', variable=self.boolvar, value=True, command=self.create_email_entry)
        self.email_no_radiobutton = Radiobutton(self, text='No', variable=self.boolvar, value=False, command=self.delete_email_entry)

        self.file_entry = Entry(self)
        self.browse_file = Button(text='Browse', command=self.callback)

        self.generate_button = Button(self, text='Generate report', command=self.generate_report)

        self.mode_label.grid(row=0)
        self.mode_switcher.grid(row=0, column=1, columnspan=2, sticky=EW)
        self.spec_label.grid(row=1)
        self.check_spec_switcher.grid(row=1, column=1, columnspan=2, sticky=EW)
        self.branch_label.grid(row=2)
        self.branch_switcher.grid(row=2, column=1, columnspan=2, sticky=EW)
        self.global_branch_label.grid(row=3)
        self.global_branch_switcher.grid(row=3, column=1, columnspan=2)#, sticky=EW)
        self.select_format_label.grid(row=4)
        self.pdf_format_radiobutton.grid(row=4, column=1)
        self.html_format_radiobutton.grid(row=4, column=2)
        self.email_quiestion.grid(row=5)
        self.email_yes_radiobutton.grid(row=5, column=1)
        self.email_no_radiobutton.grid(row=5, column=2)
        self.file_entry.grid(row=7, column=0, sticky=W+E)
        self.browse_file.grid(row=7, column=1, columnspan=2, sticky=EW)
        self.generate_button.grid(columnspan=3, sticky=W+E)

app = App()
app.title('Requirements parser')
App.center(app)
app.mainloop()