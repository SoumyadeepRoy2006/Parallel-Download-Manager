from customtkinter import CTk as Tk, set_appearance_mode, set_default_color_theme, CTkFrame as Frame, CTkScrollableFrame as ScrollableFrame, CTkLabel as Label, CTkButton as Button, CTkEntry as Entry, CTkProgressBar as ProgressBar
from Classes.Download_Job import DownloadJob, GUIBridge as Bridge
from Modules.Check_File import get_download_info
from Modules.Partitioner import partition_by_parts, partition_by_size
from threading import Thread

#set_appearance_mode("light")
set_default_color_theme("./Config/theme.json")
APP = Tk()
APP.geometry("1000x500")
APP.rowconfigure(0, weight=1)
for i, w in [(0, 1), (1,  5)]:
   APP.columnconfigure(i, weight=w)

def create_download_job(MASTER):
   FRAME_DOWNLOAD_JOB = Frame(MASTER, fg_color="transparent", corner_radius=15, border_width=1.25, border_color=("#eee", "#262626"))
   FRAME_DOWNLOAD_JOB.pack(side="top", fill="x", pady=5, padx=(0, 10))

   LABEL_FILE_NAME = Label(FRAME_DOWNLOAD_JOB, text="-", anchor="w")
   LABEL_FILE_NAME.pack(fill="x", padx=20, pady=(10, 0))

   DOWNLOAD_PROGRESS = ProgressBar(FRAME_DOWNLOAD_JOB, fg_color=("#E6E6E6", "#303030"), height=10)
   DOWNLOAD_PROGRESS.set(0)
   DOWNLOAD_PROGRESS.pack(fill="x", padx=20, pady=(10, 0))

   FRAME_DOWNLOAD_STATS = Frame(FRAME_DOWNLOAD_JOB, fg_color="transparent")
   FRAME_DOWNLOAD_STATS.pack(fill="x", padx=20)

   LABEL_DOWNLOADED_SIZE = Label(FRAME_DOWNLOAD_STATS, text=" ", anchor="w")
   LABEL_DOWNLOADED_SIZE.pack(side="left")

   LABEL_DOWNLOAD_PERCENTAGE = Label(FRAME_DOWNLOAD_STATS, text=" ", anchor="e")
   LABEL_DOWNLOAD_PERCENTAGE.pack(side="right")

   MERGE_PROGRESS = ProgressBar(FRAME_DOWNLOAD_JOB, progress_color="#50b000", fg_color=("#E6E6E6", "#303030"), height=10)
   MERGE_PROGRESS.set(0)
   MERGE_PROGRESS.pack(fill="x", padx=20, pady=(10, 0))

   LABEL_MERGE = Label(FRAME_DOWNLOAD_JOB, text="Merge...", anchor="w")
   LABEL_MERGE.pack(fill="x", padx=20, pady=(0, 10))

FRAME_CONTROL_PANEL = Frame(APP, fg_color="transparent", border_color=("#eee", "#262626"), border_width=2)
FRAME_CONTROL_PANEL.grid(row=0, column=0, sticky="news")

FRAME_QUERY = Frame(FRAME_CONTROL_PANEL, fg_color="transparent")
FRAME_QUERY.pack(side="top", fill="x", pady=(50,0), padx=50)
FRAME_QUERY.columnconfigure(0, weight=1)
FRAME_QUERY.rowconfigure(1, weight=1)
for i in [0, 2]:
   FRAME_QUERY.rowconfigure(i, weight=1)

INPUT_URL = Entry(FRAME_QUERY, placeholder_text="Paste direct URL to file")
INPUT_URL.grid(column=0, row=0, sticky="ew", pady=10)

BUTTON_QUERY = Button(FRAME_QUERY, text="Check")
BUTTON_QUERY.grid(column=0, row=2, sticky="ew", pady=10)

BUTTON_CONFIG = Button(FRAME_CONTROL_PANEL, text="Settings", fg_color=("#eee", "gray12"), hover_color=("#ddd", "gray10"), text_color=("gray14", "gray84"))
BUTTON_CONFIG.pack(fill="x", side="bottom", padx=50, pady=(0,50))

FRAME_DOWNLOAD_BODY = Frame(APP, fg_color="transparent")
FRAME_DOWNLOAD_BODY.grid(row=0, column=1, sticky="news")
FRAME_DOWNLOAD_BODY_SCROLLABLE = ScrollableFrame(FRAME_DOWNLOAD_BODY, fg_color="transparent")
FRAME_DOWNLOAD_BODY_SCROLLABLE._scrollbar.configure(width=0)
FRAME_DOWNLOAD_BODY_SCROLLABLE.pack(fill="both", expand=True)

BUTTON_QUERY.configure(command=lambda:Thread(target=lambda:create_download_job(FRAME_DOWNLOAD_BODY_SCROLLABLE), daemon=True).start())

#url = "https://fastly.mirror.pkgbuild.com/iso/2026.05.01/archlinux-x86_64.iso"

APP.mainloop()
