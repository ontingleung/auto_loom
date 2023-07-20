import csv
import configparser
import os
import pyautogui as pyg
import pygame
import time
import tkinter as tk
import webbrowser

from tkinter import filedialog, ttk



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

        self.start_button = tk.Button(self.window, justify="center", text="Start", command=self.start)
        self.start_button.place(height=92, width=175, relx=0.59, rely=0.05)

        self.setting_button = tk.Button(self.window, justify="center", text="Settings", command=self.open_config)
        self.setting_button.place(height=92, width=175, relx=0.59, rely=0.45)

        self.status_frame = tk.LabelFrame(self.window, text="Status")
        self.status_frame.place(height=40, width=433, relx=0.02, rely=0.82)

        self.time_label = tk.Label(self.status_frame, text="Time elapsed: 0 mins 0 secs")
        self.time_label.place(relx=0, rely=0)

        self.failed_label = tk.Label(self.status_frame, text="Invaild Links: 0")
        self.failed_label.place(relx=0.77, rely=0)

        self.is_running = False

        self.window.mainloop()

    def start(self):
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        chrome_path = parser.get('path', 'chrome_path')
        loom_path = parser.get('path', 'loom_path')
        button_link_url =  parser.get('add_link', 'button_link_url')
        button_text =  parser.get('add_link', 'button_text')
        failed_counter = int(0)
        failed_list = []

        self.stop()

        try: 
            if self.loaded_data:
                self.start_timer()
                self.start_button['state']="disabled"
                # beginning
                for data in self.loaded_data:
                    url = data[1]
                    owner_name = data[2]
                    # Window Setup
                    self.open_tab(url, chrome_path)
                    time.sleep(7)
                    pyg.hotkey("win", "up")
                    if pyg.locateCenterOnScreen("resources/assets/reload.png"):
                        failed_list.append([data[1]])
                        failed_counter = failed_counter + 1
                        self.failed_label['text']=f"Invaild Links: {failed_counter}";
                        continue
                    # Check Loom
                    self.launch_loom(loom_path)
                    time.sleep(5)

                    # play audio
                    self.play_audio(self.loaded_audio)
                    time.sleep(1)
                    pyg.hotkey('ctrl', 'shift', 'l')
                    time.sleep(3)
                    while not pyg.locateCenterOnScreen('resources/assets/loom_site.png', confidence=0.95):
                        pass
                    title_x, title_y = pyg.locateCenterOnScreen('resources/assets/loom_site.png', confidence=0.95)
                    pyg.click(title_x + 150, title_y - 15)
                    time.sleep(1)
                    pyg.typewrite(owner_name)
                    add_link = pyg.locateCenterOnScreen('resources/assets/add_link.png', confidence=.92)
                    pyg.click(add_link)
                    time.sleep(1)
                    pyg.typewrite(button_link_url)
                    pyg.press('tab')
                    time.sleep(1)
                    pyg.typewrite(button_text)
                    pyg.scroll(-200)
                    save_link = pyg.locateCenterOnScreen('resources/assets/save_link.png', confidence=0.9)
                    pyg.click(save_link)
                    time.sleep(2)
                    self.close_tab()
                    self.close_tab()
                # end 
        except:
             tk.messagebox.showerror("Error", "Please load files.")

            
        
        tk.messagebox.showinfo(title='Complete', message='Task complete.')
        self.start_button['state']="normal"
        
    
    def open_tab(self, url: str, path: str):
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(path))
        webbrowser.get('chrome').open_new(url)

    def launch_loom(self, loom_path):
        parser = configparser.ConfigParser()
        parser.read('config.ini')

        height = int(parser.get('screen_res', 'height'))
        width = int(parser.get('screen_res', 'width'))

        os.startfile(loom_path)
        while not pyg.locateCenterOnScreen('resources/assets/loom_on.png', confidence=0.95):
            pass

        # Loom setup
        time.sleep(3)
        set_up_screen = pyg.locateCenterOnScreen('resources/assets/screen_only.png', confidence=0.95)
        if set_up_screen:
            pyg.click(set_up_screen)
            time.sleep(1)
            pyg.hotkey('down', 'enter')
            time.sleep(2)
        anti_virus = pyg.locateCenterOnScreen('resources/v_assets/anti_v.png', grayscale=True, confidence=0.7)
        if anti_virus:
            anti_x, anti_y = pyg.locateCenterOnScreen('resources/v_assets/anti_v.png', grayscale=True, confidence=0.7)
            pyg.click(anti_x + 330, anti_y - 30)
            time.sleep(2)

        
        set_up_microphone = pyg.locateCenterOnScreen('resources/assets/microphone.png', confidence=0.95)
        if set_up_microphone:
            pyg.click(set_up_microphone)
            time.sleep(2)
        time.sleep(1)
        full_screen = pyg.locateCenterOnScreen('resources/assets/full_screen.png', confidence=0.95)
        if full_screen:
            pyg.click(full_screen)
            pyg.hotkey('down', 'down', 'enter')
        else:
            start_recording = pyg.locateCenterOnScreen('resources/assets/recording.png', confidence=0.95)
            pyg.click(start_recording)
        while not pyg.locateCenterOnScreen('resources/assets/back.png', confidence=0.95):
            pass
        time.sleep(1)
        under_back_x, under_back_y = pyg.locateCenterOnScreen('resources/assets/back.png', confidence=0.95)
        pyg.click(under_back_x, under_back_y + 50)

        time.sleep(2)
        anti_virus_two = pyg.locateCenterOnScreen('resources/v_assets/anti_v.png', grayscale=True, confidence=0.7)
        if anti_virus_two:
            anti_x, anti_y = pyg.locateCenterOnScreen('resources/v_assets/anti_v.png', grayscale=True, confidence=0.7)
            pyg.click(anti_x + 330, anti_y - 30)
            time.sleep(2)
        
        time.sleep(2)
        profile = pyg.locateCenterOnScreen('resources/v_assets/profile_pic.png', confidence=0.7)

        if not profile:
            sweep = 0.8
            pyg.moveTo(width/16, height/1.1)
            while not pyg.locateCenterOnScreen('resources/assets/loom_cam.png', confidence=0.9):
                sweep = sweep + 0.04
                pyg.moveTo(width/16, height/sweep)
            loom_cam = pyg.locateCenterOnScreen('resources/assets/loom_cam.png', confidence=0.9)
            pyg.moveTo(loom_cam)
            cam_fix = pyg.locateCenterOnScreen('resources/assets/cam_fix.png', confidence=0.9)
            pyg.click(cam_fix)
            time.sleep(1)

        while not pyg.locateCenterOnScreen('resources/assets/start_record.png', confidence=0.90):
            pass
        pyg.hotkey('ctrl', 'shift', 'l')
        while not pyg.locateCenterOnScreen('resources/assets/proceed.png', confidence=0.95):
            pass
        proceed = pyg.locateCenterOnScreen('resources/assets/proceed.png', confidence=0.95)
        pyg.click(proceed)

        
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
                self.loaded_audio = self.filename
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

        focus_chrome = pyg.locateCenterOnScreen('resources/assets/chrome.png',grayscale=True, confidence=.9)
        time.sleep(2)
        pyg.click(focus_chrome)
        pyg.moveTo(600, 600)

        for i in range(30):
            pyg.scroll(-80)

        time.sleep(1)

        for i in range(15):
            pyg.scroll(300)
            

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

    def close_tab(self):
        pyg.hotkey('ctrl', 'w')

if __name__ == "__main__":
    app=App()
