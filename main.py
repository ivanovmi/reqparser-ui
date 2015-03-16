from Tkinter import *
import lan
import body
import time
import threading


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.grid()
        self.create_widgets()

    def center(win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def processing_please_wait(self):
        window = Toplevel()
        self.center()
        window.overrideredirect(1)
        #window.geometry('100x30')
        # code before computation starts
        label = Label(window, text='Wait for login')
        label.grid(ipadx=4, ipady=8)

        def call():
            time.sleep(5)

        thread = threading.Thread(target=call)
        thread.start()  # start parallel computation
        while thread.is_alive():
            # code while computing
            window.update()
            time.sleep(0.001)
        window.destroy()

    def create_widgets(self):
        self.label_usr = Label(self, text='Login')
        self.label_pswd = Label(self, text='Password')
        self.entry_usr = Entry(self)
        self.entry_pswd = Entry(self, show='*')
        self.button = Button(self, text='Login', command=self.new_layout)
        self.label_usr.pack()
        self.entry_usr.pack()
        self.label_pswd.pack()
        self.entry_pswd.pack()
        self.button.pack()

    def new_layout(self):
        #self.button.destroy()
        self.label_err = Label(self)
        self.label = Label(self)
        self.processing_please_wait()
        try:
            gerrit = lan.login_to_launchpad(self.entry_usr.get(), self.entry_pswd.get())
        except KeyError:
            self.label_err.destroy()
            self.label_err = Label(self, text='Not autenticate')
            self.label_err.pack()
        else:
            self.label.destroy()
            self.label = Label(self, text='Done')
            self.label.grid(row=1, column=2, sticky=W)
            body.main(gerrit)

app = App()
app.title('Requirements parser')
app.geometry('640x480')
app.center()
app.mainloop()