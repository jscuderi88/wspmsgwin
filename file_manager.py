from tkinter import filedialog

def browse_file(file_path_var):
    filename = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx")]
    )
    if filename:
        file_path_var.set(filename)
