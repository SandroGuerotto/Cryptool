from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from bin.dataholder import Dataholder
from bin.messagebox import Messagebox
import os
from bin.encryption import *

# only run the code when executed directly
if __name__ == "__main__":
    root = Tk()
    root.title("Cryptool")


    # logic to create new AES Key
    def create_new_key():
        key = generate_new_key()
        bytes(key, "ascii")
        dataholder.set_key(key)


    # load key using var: keypath
    def import_key():
        keypath = filedialog.askopenfilename(parent=root)
        key = import_aeskey(keypath)
        dataholder.set_key(key)


    # Get currently used key and export to chosen location
    def export_key():
        exportpath = filedialog.askdirectory(parent=root)
        save_key(dataholder.get_key(), exportpath)


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
        if len(filename) > 0:
            btn_process["state"] = "normal"

        if os.path.splitext(os.path.basename(filename))[1] == ".aes":
            btn_process.config(text="entschlüsseln")
        else:
            btn_process.config(text="verschlüsseln")


    def select_destination(label):
        filename = filedialog.askdirectory(parent=root)
        dataholder.set_destination(str(filename))
        label.config(text=str(filename))


    # Import source File and encrypt & decyript. save at given destination or same directory as source file
    def process(progressbar):
        if btn_process["text"] == "entschlüsseln":
            on_process(progressbar, "entschlüsselt")
            bool = decrypt_file(bytes(dataholder.get_key(), "ascii"), dataholder.get_source(), dataholder.get_destination())
            if bool:
                on_success(progressbar, "entschlüsselt")
            else:
                on_error(progressbar, "entschlüsselt")

        elif btn_process["text"] == "verschlüsseln":
            on_process(progressbar, "verschlüsselt")
            bool = encrypt_file(bytes(dataholder.get_key(), "ascii"), dataholder.get_source(), dataholder.get_destination())
            if bool:
                on_success(progressbar, "verschlüsselt")
            else:
                on_error(progressbar, "verschlüsselt")

    #callback functions for en- /decryption
    def on_error(progressbar, mode):
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("red.Horizontal.TProgressbar", background='#e06666', foreground="#e06666")
        progressbar.config(style="red.Horizontal.TProgressbar")
        messagebox.failed(dataholder.get_source(), mode)


    def on_success(progressbar, mode):
        progressbar["value"] = 120
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("green.Horizontal.TProgressbar", background='#93c47d', foreground="#93c47d")
        progressbar.config(style="green.Horizontal.TProgressbar")
        messagebox.successful(dataholder.get_source(), mode)


    def on_process(progressbar, mode):
        progressbar["value"] = 50
        progressbar["maximum"]= 120
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("blue.Horizontal.TProgressbar", background='#76a5af', foreground="#76a5af")
        progressbar.config(style="blue.Horizontal.TProgressbar")
        messagebox.processing(dataholder.get_source(), mode)


    def on_reset(progressbar):
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("reset.Horizontal.TProgressbar")
        progressbar.config(style="reset.Horizontal.TProgressbar")
        progressbar["value"] = 0
        if messagebox is not None:
            messagebox.clear()


    dataholder = Dataholder()
    messagebox = Messagebox(root)

    # display the menu
    root.config(menu=create_menu())

    frame = Frame(root)
    frame.pack(pady=10, fill=X)

    # button to start en-/decrypt

    progressbar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    btn_process = Button(frame, text="verschlüsseln", command=lambda: process(progressbar), state=DISABLED)

    lbl_source = Label(frame, width=50, anchor=W)
    Button(frame, text="Datei auswählen", command=lambda: select_file(lbl_source, btn_process)).pack(padx=10, ipadx=2,
                                                                                                     side=LEFT)
    lbl_source.pack(padx=10, side=LEFT)

    btn_process.pack(padx=60, ipadx=2, side=LEFT)

    lbl_destination = Label(frame, width=50, anchor=E)
    Button(frame, text="Zielort auswählen", command=lambda: select_destination(lbl_destination)).pack(padx=10, ipadx=2,
                                                                                                      side=RIGHT)
    lbl_destination.pack(padx=10, side=RIGHT)

    progressbar.pack(padx=10, fill=X)

    on_reset(progressbar)
    messagebox.show()

    root.mainloop()
