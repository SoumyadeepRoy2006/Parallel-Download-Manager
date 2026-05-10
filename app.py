from threading import Thread
from tkinter import Tk, Frame, Label, Button
from Classes.Download_Job import DownloadJob
from Modules.Check_File import get_download_info
from Modules.Partitioner import partition_by_parts, partition_by_size

APP = Tk()
APP.geometry("500x500")
FRAME_MAIN = Frame(APP); FRAME_MAIN.pack(fill="both", expand=True)
LABEL_MAIN = Label(FRAME_MAIN); LABEL_MAIN.pack(fill="both", expand=True)
BUTTON_DOWNLOAD = Button(FRAME_MAIN, text="Download"); BUTTON_DOWNLOAD.pack(fill="both", expand=True)

#url = "https://fastly.mirror.pkgbuild.com/iso/2026.05.01/archlinux-x86_64.iso"

APP.mainloop()
