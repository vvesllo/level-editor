from tkinter import filedialog

def askFilepathToOpen(filetypes, default_extension):
    return filedialog.askopenfilename(
        filetypes=filetypes,
        defaultextension=default_extension
    )

def askFilepathToSave(filetypes, default_extension):
    return filedialog.asksaveasfilename(
        filetypes=filetypes,
        defaultextension=default_extension
    )