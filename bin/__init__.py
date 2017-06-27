from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from pip._vendor import progress

from bin.dataholder import Dataholder
import os

# only run the code when executed directly
if __name__ == "__main__":
    root = Tk()
    root.title("Cryptool")


    def create_new_key():
        # ToDo: logic to create new AES Key
        dataholder.set_key(None)


    def import_key():
        keypath = filedialog.askopenfilename(parent=root)
        # ToDo: load key using var: keypath
        dataholder.set_key(None)


    def export_key():
        pass


    def create_menu():
        menubar = Menu(root)

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Neuer Schlüssel erstellen", command=create_new_key)
        filemenu.add_separator()
        filemenu.add_command(label="Schlüssel importieren", command=import_key)
        filemenu.add_command(label="Schlüssel exportieren", command=export_key)

        filemenu.add_separator()
        filemenu.add_command(label="Beenden", command=lambda: root.quit)
        menubar.add_cascade(label="Datei", menu=filemenu)
        return menubar


    def select_file(label, btn_process):
        filename = filedialog.askopenfilename(parent=root)
        dataholder.set_source(str(filename))
        label.config(text=str(filename))
        if os.path.splitext(os.path.basename(filename))[1] == ".aes":
            btn_process.config(text="entschlüsseln")
        else:
            btn_process.config(text="verschlüsseln")


    def select_destination(label):
        filename = filedialog.askdirectory(parent=root)
        dataholder.set_destination(str(filename))
        label.config(text=str(filename))


    def process(progressbar):
        on_process(progressbar)
        # ToDo: import source File and en-/decrypt. save at given destination or same directory as source file
        # handling with on_ methods
        pass


    def on_error(progressbar):
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("red.Horizontal.TProgressbar", background='#e06666', foreground="#e06666")
        progressbar.config(style="red.Horizontal.TProgressbar")


    def on_success(progressbar):
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("green.Horizontal.TProgressbar", background='#93c47d', foreground="#93c47d")
        progressbar.config(style="green.Horizontal.TProgressbar")


    def on_process(progressbar):
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("blue.Horizontal.TProgressbar", background='#76a5af', foreground="#76a5af")
        progressbar.config(style="blue.Horizontal.TProgressbar")


    def on_reset(progressbar):
        progressbar["value"] = 0


    dataholder = Dataholder()

    # display the menu
    root.config(menu=create_menu())

    frame = Frame(root)
    frame.pack(pady=10, fill=X)

    # button to start en-/decrypt

    progressbar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    btn_process = Button(frame, text="verschlüsseln", command=lambda: process(progressbar))

    lbl_source = Label(frame, text="Pfad", width=50, anchor=W)
    Button(frame, text="Datei auswählen", command=lambda: select_file(lbl_source, btn_process)).pack(padx=10, ipadx=2,
                                                                                                     side=LEFT)
    lbl_source.pack(padx=10, side=LEFT)

    btn_process.pack(padx=60, ipadx=2, side=LEFT)

    lbl_destination = Label(frame, text="Pfad", width=50, anchor=E)
    Button(frame, text="Zielort auswählen", command=lambda: select_destination(lbl_destination)).pack(padx=10, ipadx=2,
                                                                                                      side=RIGHT)
    lbl_destination.pack(padx=10, side=RIGHT)

    progressbar.pack(padx=10, fill=X)
    progressbar["value"] = 100
    progressbar["maximum"] = 5000
    on_error(progressbar)

    root.mainloop()
