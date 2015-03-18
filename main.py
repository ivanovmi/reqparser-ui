from Tkinter import *
import lan
import body
import time
import threading
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
        self.create_widgets()

    def create_email_entry(self):
        if self.email_exist == 1:
            pass
        else:
            self.email_label = Label(self, text='Input email address:')
            self.email_entry = Entry(self)
            self.email_label.pack()
            self.email_entry.pack()
            self.email_exist = 1

    def delete_email_entry(self):
        self.email_label.pack_forget()
        self.email_entry.pack_forget()
        self.email_exist = 0

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
        self.window.geometry('100x30+500+300')
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
        self.button = Button(self, text='Wait for login')
        self.processing_please_wait()
        try:
            pass#self.gerrit = lan.login_to_launchpad(self.entry_usr.get(), self.entry_pswd.get())
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

    def main_window(self):
        # In this function will create_email_entry main window with all settings for parser
        # body.main(self.gerrit)
        for widget in app.winfo_children():
            widget.destroy()

        var = IntVar()
        boolvar = BooleanVar()

        self.generate_button = Button(self, text='Generate report', command='')
        self.select_format_label = Label(self, text='Please, select format of output:')
        self.pdf_format_radiobutton = Radiobutton(self, text='pdf', variable=var, value=1)
        self.html_format_radiobutton = Radiobutton(self, text='html', variable=var, value=2)

        self.email_quiestion = Label(self, text='Would you like to send e-mail?')
        self.email_exist = 0
        self.email_yes_radiobutton = Radiobutton(self, text='Yes', variable=boolvar, value=True, command=self.create_email_entry)
        self.email_no_radiobutton = Radiobutton(self, text='No', variable=boolvar, value=False, command=self.delete_email_entry)

        self.mode_label = Label(self, text='Select a mode:')
        self.mode_switcher = ttk.Combobox(self, values=['requirements', 'epoch'])
        self.mode_switcher.set('requirements')

        self.spec_label = Label(self, text='Select what we scan:')
        self.check_spec_switcher = ttk.Combobox(self, values=['', 'control', 'specs'])
        self.check_spec_switcher.set('')

        self.branch_label = Label(self, text='At the what branch we should check requirements?')
        self.branch_switcher = ttk.Combobox(self, values=['master', '6.1', '6.0.1'])
        self.branch_switcher.set('master')

        self.mode_label.pack()
        self.mode_switcher.pack()
        self.spec_label.pack()
        self.check_spec_switcher.pack()
        self.branch_label.pack()
        self.branch_switcher.pack()
        self.select_format_label.pack()
        self.pdf_format_radiobutton.pack()
        self.html_format_radiobutton.pack()
        self.email_quiestion.pack()
        self.email_yes_radiobutton.pack()
        self.email_no_radiobutton.pack()
        self.generate_button.pack()
        # After click to generate report button
        # self.branch_name = self.branch_switcher.get()
        # self.mode = self.mode_switcher.get()
        # self.spec = self.check_spec_switcher.get()


app = App()
app.title('Requirements parser')
app.geometry('640x480')
App.center(app)
app.mainloop()