import pyautogui as pyg
import tkinter as tk
import csv
from TkinterDnD2 import DND_FILES, TkinterDnD

def load_data(filename):
    list_data = []
    with open(filename) as loom:
        loom_data = csv.reader(loom, delimiter=',')
        next(loom_data)

def dnd_cvs_path(event):
    pass

window = TkinterDnD.Tk()
window.geometry("800x500")
window.title("Auto Loomer")







window.mainloop()


# res = pyg.locateCenterOnScreen("recording.png")

# if res != None:
#     pyg.click(res)
# else:
#     print("Loom was not found")



# app = Application().start("C:/Users/Onting/AppData/Local/Programs/Loom/Loom.exe")

# try:
#     window = app.window(title_re="Loom")
# except ElementNotFoundError:
#     print("Loom window not found")
#     exit(1)

# try:
#     start_button = window.child_window(title="Start recording", control_type="Button")
#     start_button.click()
# except ElementNotFoundError:
#     print("Start Recording button not found")