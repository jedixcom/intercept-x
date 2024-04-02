#! "C:\Users\polde\OneDrive - HvA\Cyber_Security_AD_1_2024\blok3\programming\new\env\Scripts\python"
#Notepad Banner Opener  - Offensive Programming - Blok3

import subprocess

def open_banner_in_notepad():
    notepad_path = "notepad.exe"
    file_path = "banner.txt"
    subprocess.Popen([notepad_path, file_path])

for _ in range(5):
    open_banner_in_notepad()