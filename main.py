from Tkinter import *
import lan
import body
import time
import threading
import tkMessageBox


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.label_usr = Label(self, text='Login')
        self.label_pswd = Label(self, text='Password')
        self.entry_usr = Entry(self)
        self.entry_pswd = Entry(self, show='*')
        self.button = Button(self, text='Login', command=self.new_layout)
        self.label_info = Label(self, text='Waiting')
        self.grid()
        self.create_widgets()

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
        self.button.destroy()
        self.button = Button(self, text='Wait for login')
        self.label_err = Label(self)
        self.processing_please_wait()
        try:
            self.gerrit = lan.login_to_launchpad(self.entry_usr.get(), self.entry_pswd.get())
        except KeyError:
            self.label_info.destroy()
            self.button = Button(self, text='Login')
            self.label_err.destroy()
            self.label_err = Label(self, text='Not autenticate')
            self.button.pack()
            self.label_err.pack()
        else:
            self.main_window()

    def main_window(self):
        # In this function will create main window with all settings for parser
        body.main(self.gerrit)


app = App()
app.title('Requirements parser')
app.geometry('640x480')
App.center(app)
app.mainloop()