import csv
import configparser
import pyautogui as pyg
import pygame
import time
import tkinter as tk
import subprocess
import webbrowser


from tkinter import filedialog, messagebox, ttk

class App:
    def __init__(self):
        
        # window setup
        self.window = tk.Tk()
        self.window.title("Auto Loom")
        self.window.geometry("450x250")
        self.window.iconbitmap("app.ico")
        self.window.pack_propagate(False)
        self.window.resizable(0, 0)

        # CVS File Frame
        self.csvfile_frame = tk.LabelFrame(self.window, text="CSV File")
        self.csvfile_frame.place(height=100, width=250, relx=0.02, rely=0.02)
      
        # Audio File Frame
        self.audiofile_frame = tk.LabelFrame(self.window, text="Audio File")
        self.audiofile_frame.place(height=100, width=250, relx=0.02, rely=0.42)

        # CSV Button
        self.load_csv_button = tk.Button(self.csvfile_frame, text="Load File", command=lambda file="CSV": self.file_dialog(file))
        self.load_csv_button.place(relx=0.7, rely=0.5)
        self.csv_label = ttk.Label(self.csvfile_frame, text="No File Selected")
        self.csv_label.place(relx=0, rely=0.15)

        # Audio Button 
        self.load_audio_button = tk.Button(self.audiofile_frame, text="Load File", command=lambda file="Audio": self.file_dialog(file))
        self.load_audio_button.place(relx=0.7, rely=0.5)
        self.audio_label = ttk.Label(self.audiofile_frame, text="No File Selected")
        self.audio_label.place(relx=0, rely=0.15)

        self.start_button = tk.Button(self.window, justify="center", text="Start (F6)", command=self.start_timer)
        self.start_button.place(height=58, width=175, relx=0.59, rely=0.05)

        self.stop_button = tk.Button(self.window, justify="center", state="disabled", text="Stop (F6)")
        self.stop_button.place(height=58, width=175, relx=0.59, rely=0.31)

        self.setting_button = tk.Button(self.window, justify="center", text="Settings", command=self.open_config)
        self.setting_button.place(height=58, width=175, relx=0.59, rely=0.58)

        self.status_frame = tk.LabelFrame(self.window, text="Status")
        self.status_frame.place(height=40, width=433, relx=0.02, rely=0.82)

        self.row_label = tk.Label(self.status_frame, text="Current Row: ")
        self.row_label.place(relx=0.75, rely=0)

        self.time_label = tk.Label(self.status_frame, text="Time elapsed: 0 mins 0 secs")
        self.time_label.place(relx=0, rely=0)

        self.is_running = False

        
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        chrome_path = parser.get('path', 'chrome_path')
        loom_path = parser.get('path', 'loom_path')

        print(chrome_path)

        self.window.mainloop()

    # Opens File Explorer and Loads file
    def file_dialog(self, file):
        match file:
            case 'CSV':
                self.filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetype=(("csv files", ".csv"), ("All Files", "*.*")))
                self.load_data(self.filename)
            case 'Audio':
                self.filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetype=(("audio files", ".csv"), ("All Files", "*.*")))
                self.audio_label["text"] = self.filename
            case _:
                return None

    def load_data(self, filename: str):
        list_data = []
        try:
            with open(filename) as loom:
                loom_data = csv.reader(loom, delimiter=',')
                next(loom_data)
                for row in loom_data:
                    list_data.append(row)
                self.csv_label["text"] = self.filename
                return list_data
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid CSV file.")
        except FileNotFoundError:
            tk.messagebox.showerror("Error", f"Could not find file '{filename}.'")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            self.update_time()

    def stop(self):
        self.is_running = False
 
    # Update the elapsed time
    def update_time(self):
        if self.is_running:
            elapsed_time = time.time() - self.start_time
            mins, secs = divmod(elapsed_time, 60)
            self.time_label.config(text="Time elapsed: {:.0f} mins {:.0f} secs".format(mins, secs))
            self.time_label.after(50, self.update_time)

    def open_config(self):
        webbrowser.open("config.ini")
        return None

# need to test!!!
def play_audio(file_path: str):
    try:
        pygame.mixer.init()
        pygame.mixer_music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(300)

        pygame.mixer.music.stop()
    except pygame.error:
        tk.messagebox.showerror("Error", f"Invalid audio file: '{file_path}'.")

def open_tab(url: str, path: str):
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(path))
    webbrowser.get('chrome').open_new(url)


def close_tab():
    pyg.hotkey('ctrl', 'w')



if __name__ == "__main__":
    app=App()


parser = configparser.ConfigParser()
parser.read('config.ini')
chrome_path = parser.get('path', 'chrome_path')
loom_path = parser.get('path', 'loom_path')

print(parser.get('path', 'chrome_path'))

# subprocess.Popen(loom_path)


    # open_tab(url, chrome_path)

    # close_tab()





# res = pyg.locateCenterOnScreen("recording.png")

