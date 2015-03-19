from Tkinter import *
from tkFileDialog import askopenfilename

def callback():
    name=askopenfilename()
    print name

errmsg='err'
Button(text='Browse', command=callback).pack(fill=X)
mainloop()