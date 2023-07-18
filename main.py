import csv
import configparser
import os
import pyautogui as pyg
import pygame
import time
import tkinter as tk
import subprocess
import webbrowser

from tkinter import filedialog, messagebox, ttk

# 16 hours

class App:
    def __init__(self):
        
        # window setup
        self.window = tk.Tk()
        self.window.title("Auto Loom")
        self.window.geometry("450x250")
        # self.window.iconbitmap("app.ico")
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

        self.start_button = tk.Button(self.window, justify="center", text="Start (F6)", command=self.start)
        self.start_button.place(height=58, width=175, relx=0.59, rely=0.05)

        self.stop_button = tk.Button(self.window, justify="center", state="disabled", text="Stop (F6)")
        self.stop_button.place(height=58, width=175, relx=0.59, rely=0.31)

        self.setting_button = tk.Button(self.window, justify="center", text="Settings", command=self.open_config)
        self.setting_button.place(height=58, width=175, relx=0.59, rely=0.58)

        self.status_frame = tk.LabelFrame(self.window, text="Status")
        self.status_frame.place(height=40, width=433, relx=0.02, rely=0.82)

        self.time_label = tk.Label(self.status_frame, text="Time elapsed: 0 mins 0 secs")
        self.time_label.place(relx=0, rely=0)

        self.failed_label = tk.Label(self.status_frame, text="Invaild Links: 0")
        self.failed_label.place(relx=0.5, rely=0)

        self.row_label = tk.Label(self.status_frame, text="Current Row: ")
        self.row_label.place(relx=0.75, rely=0)


        self.is_running = False

        self.window.mainloop()

    def start(self):
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        chrome_path = parser.get('path', 'chrome_path')
        loom_path = parser.get('path', 'loom_path')
        failed_counter = int(0)
        failed_list = []

        
        
        try: 
            if self.loaded_data:
                self.start_timer()
                self.start_button['state']="disabled"
                self.stop_button['state']="normal"
                # beginning
                for data in self.loaded_data:
                    self.row_label['text']=f"Current Row: {data}"
                    url = data[1]
                    owner_name = data[2]
                    # Window Setup
                    self.open_tab(url, chrome_path)
                    time.sleep(5)
                    pyg.hotkey("win", "up")
                    if (pyg.locateCenterOnScreen("reload.png") is None):
                        failed_list.append([data[1]])
                        failed_counter = failed_counter + 1
                        self.failed_label['text']=f"Invaild Links: {failed_counter}";
                        continue
                    # Check Loom
                    self.launch_loom(loom_path)




 
                    pyg.hotkey("ctrl", "w")
                # end 

        except:
             tk.messagebox.showerror("Error", "Please load files.")
    
    def open_tab(self, url: str, path: str):
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(path))
        webbrowser.get('chrome').open_new(url)

    def launch_loom(self, loom_path):
        os.startfile(loom_path)
        time.sleep(5)

        # Loom setup
        set_up_screen = pyg.locateCenterOnScreen('screen_only.png', confidence=0.95)
        if set_up_screen:
            pyg.click(set_up_screen)
            time.sleep(1)
            pyg.hotkey('down', 'enter')
            time.sleep(1)
        set_up_microphone = pyg.locateCenterOnScreen('microphone.png', confidence=0.95)
        if set_up_microphone:
            pyg.click(set_up_microphone)
            time.sleep(1)
        
        full_screen = pyg.locateCenterOnScreen('full_screen.png', confidence=0.95)
        if full_screen:
            pyg.click(full_screen)
            pyg.hotkey('down', 'down', 'enter')
        else:
            start_recording = pyg.locateCenterOnScreen('recording.png', confidence=0.95)
            pyg.click(start_recording)
        time.sleep(1)
        under_back_x, under_back_y = pyg.locateCenterOnScreen('back.png', confidence=0.95)
        pyg.click(under_back_x, under_back_y + 50)
        time.sleep(2)
        
        
    def add_failed(self, url):
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        with open(desktop + '\\failed.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerows(url)

    # Opens File Explorer and Loads file
    def file_dialog(self, file):
        match file:
            case 'CSV':
                self.filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetype=(("csv files", ".csv"), ("All Files", "*.*")))
                self.load_data(self.filename)
            case 'Audio':
                self.filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetype=(("MP3 files", ".mp3"), ("wav files", ".wav"), ("All Files", "*.*")))
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
                self.loaded_data = list_data
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid CSV file.")
        except FileNotFoundError:
            tk.messagebox.showerror("Error", f"Could not find file '{filename}.'")

    

    def play_audio(self, file_path: str):
        pygame.mixer.init()
        pygame.mixer_music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(300)

        pygame.mixer.music.stop()


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


def close_tab():
    pyg.hotkey('ctrl', 'w')


# if __name__ == "__main__":
#     app=App()

# subprocess.Popen(loom_path)


    # 

    # close_tab()


parser = configparser.ConfigParser()
parser.read('config.ini')
chrome_path = parser.get('path', 'chrome_path')
loom_path = parser.get('path', 'loom_path')

os.startfile(loom_path)
time.sleep(1)
# Microphone


# screen
# x, y = pyg.locateCenterOnScreen('screen_only.png', confidence=0.95)
# pyg.click(x, y)
# time.sleep(1)
# pyg.hotkey('down', 'enter')
# time.sleep(1)
# x, y = pyg.locateCenterOnScreen('microphone.png', confidence=0.95)
# pyg.click(x, y)

# x, y = pyg.locateCenterOnScreen('full_screen.png', confidence=0.95)
# pyg.click(x, y)




under_back_x, under_back_y = pyg.locateCenterOnScreen('back.png', confidence=0.95)
pyg.click(under_back_x, under_back_y + 50)




