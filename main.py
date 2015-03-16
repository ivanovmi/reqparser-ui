from Tkinter import *
import lan, body


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.label_usr = Label(self, text='Login')
        self.label_pswd = Label(self, text='Password')
        self.entry_usr = Entry(self)
        self.entry_pswd = Entry(self, show='*')
        self.button = Button(self, text='Login', command=self.new_layout)
        self.label_usr.grid()
        self.entry_usr.grid()
        self.label_pswd.grid()
        self.entry_pswd.grid()
        self.button.grid()

    def new_layout(self):
        self.button.destroy()
        try:
            gerrit = lan.login_to_launchpad(self.entry_usr.get(), self.entry_pswd.get())
        except KeyError:
            self.label_err = Label(self, text='Not autenticate')
            self.label_err.grid()
        else:
            self.label = Label(self, text='Done')
            self.label.grid()
            body.main(gerrit)

app = App()
app.title('Requirements parser')
app.geometry('640x480')
app.mainloop()