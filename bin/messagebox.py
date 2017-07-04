from tkinter import *


class Messagebox:
    def __init__(self, root):
        self.root = root

        self.frame = Frame(root)

        self.lbl_status = Label(self.frame, anchor=W, width=10)
        self.lbl_message = Label(self.frame)
        self.freetext = Text(root, height=2, state=DISABLED)

    def show(self):
        self.frame.pack(pady=10, padx=10, fill=X)
        self.lbl_status.pack(side=LEFT)
        self.lbl_message.pack(side=LEFT, fill=X)
        self.freetext.pack(fill=X, padx=10, pady=3)

    def set_status(self, status):
        self.lbl_status.config(text=status)

    def set_message(self, message):
        text = ":\t" + str(message)
        self.lbl_message.config(text=text)

    def processing(self, file):
        self.set_message("Die Datei " + file + " wird entschlüsselt")
        self.set_status("Läuft")

    def successful(self, file):
        self.set_message("Die Datei " + file + " wurde erfolgreich entschlüsselt")
        self.set_status("Erfolgreich")

    def failed(self, file):
        self.set_message("Die Datei " + file + " wurde nicht erfolgreich entschlüsselt")
        self.set_status("Fehler")

    def clear(self):
        self.lbl_status.config(text="")
        self.lbl_message.config(text="")
