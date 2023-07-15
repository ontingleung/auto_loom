import csv
import pyautogui as pyg
import pygame
import tkinter as tk
from TkinterDnD2 import DND_FILES, TkinterDnD

def load_data(filename):
    """Loads CSV data into a list"""
    list_data = []
    with open(filename) as loom:
        loom_data = csv.reader(loom, delimiter=',')
        next(loom_data)
        for row in loom_data:
            list_data.append(row)
        return list_data

# need to test!!!
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer_music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(300)

    pygame.mixer.music.stop()


def dnd_cvs_path(event):
    pass




ld = load_data('Sheet1.csv')

for cols in ld:
    website = cols[1]
    owner_name = cols [2]

    print(f"Website: {website}, Owner: {owner_name}")

# window = TkinterDnD.Tk()
# window.geometry("800x500")
# window.title("Auto Loomer")







# window.mainloop()


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