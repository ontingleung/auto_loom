import csv
import configparser
import pyautogui as pyg
import pygame
import tkinter as tk
import subprocess
import webbrowser

from tkinter import filedialog, messagebox, ttk

class App:
    def __init__(self):
        # window setup
        self.window = tk.Tk()
        self.window.title("Auto Loom")
        self.window.geometry("800x500")
        self.window.pack_propagate(False)
        self.window.resizable(0, 0)

        self.audiofile_frame = tk.LabelFrame(self.window, text="Audio File")
        self.audiofile_frame.place(height=100, width=400, relx=0.5, rely=0)

        self.csvfile_frame = tk.LabelFrame(self.window, text="CSV File")
        self.csvfile_frame.place(height=100, width=400, relx=0.001, rely=0)

        self.load_cvs_button = tk.Button()

        self.window.mainloop()


def load_data(filename: str):
    """Loads CSV data into a list"""
    list_data = []
    with open(filename) as loom:
        loom_data = csv.reader(loom, delimiter=',')
        next(loom_data)
        for row in loom_data:
            list_data.append(row)
        return list_data

# need to test!!!
def play_audio(file_path: str):
    pygame.mixer.init()
    pygame.mixer_music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(300)

    pygame.mixer.music.stop()

def open_tab(url: str, path: str):
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(path))
    webbrowser.get('chrome').open_new(url)
    

def close_tab():
    pyg.hotkey('ctrl', 'w')





ld = load_data('Sheet1.csv')

parser = configparser.ConfigParser()
parser.read('config.ini')
chrome_path = parser.get('path', 'chrome_path')
loom_path = parser.get('path', 'chrome_path')

print(parser.get('path', 'chrome_path'))

subprocess.Popen()

for cols in ld:
    url = cols[1]
    owner_name = cols [2]

    # open_tab(url, chrome_path)

    # close_tab()


if __name__ == "__main__":
    app=App()


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