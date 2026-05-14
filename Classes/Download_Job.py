from os import path, rename
import requests
from threading import Thread, Lock
from time import sleep
from .File_Merger import MergeJob
from customtkinter import CTkProgressBar as ProgressBar, CTkLabel as Label

class DownloadJob:
   file_name = None
   directory = None
   url = None
   file_size_bytes = None

   partition_data = None
   total_parts = 0

   buffer_rw_size = 256 * 1024 # KB
   downloaded_parts = 0
   downloaded_bytes = 0
   thread_lock = Lock()

   merge_required = True
   merge_job = None

   bridge = None

   def __init__(this, url:str, file_name:str, directory:str, partition_data:list):
      if str(".part") in file_name:
         raise ValueError("'.part' cannot be used in names")
      
      elif path.exists(f"{directory}/{file_name}"):
         raise FileExistsError(f"A file named ' {file_name} ' already exists in your directory")
      
      elif not path.exists(f"{directory}/"):
         raise FileNotFoundError(f"{directory} not found.")
      
      else:
         this.file_name = file_name
         this.directory = directory
         this.url = url
         this.partition_data = partition_data
         this.file_size_bytes = partition_data[-1][1]
         this.total_parts = len(partition_data)
         this.merge_job = MergeJob(directory, file_name, len(partition_data), this.file_size_bytes)


   def set_dir(this, directory:str):
      if directory != "":
         this.directory = directory


   def set_file_name(this, file_name:str):
      if file_name != "":
         this.file_name = file_name


   def set_bridge(this, bridge):
      this.bridge = bridge
      this.merge_job.set_bridge(this.bridge)


   def _download_part(this, byte_range:tuple, part_no:int=None):
      part_name = f"{this.file_name}{(".part" + str(part_no)) if part_no else ""}"
      if not path.exists(f"{this.directory}/{part_name}"):
         try:
            with requests.get(this.url, headers={"Range": f"bytes={byte_range[0]}-{byte_range[1]}"}, stream=True) as res:
               res.raise_for_status()
               with open(f"{this.directory}/{part_name}.part", "wb") as file:
                  for buffer in res.iter_content(chunk_size=this.buffer_rw_size):
                     if buffer:
                        file.write(buffer)
                        with this.thread_lock:
                           this.downloaded_bytes += len(buffer)
                           this.bridge.set_download_size(this.downloaded_bytes)
                           this.bridge.set_download_progress(this.downloaded_bytes/this.file_size_bytes)

               rename(f"{this.directory}/{part_name}.part", f"{this.directory}/{part_name}")

               if part_no:
                  this.merge_job.add_part(part_no, f"{this.directory}/{part_name}")
               with this.thread_lock:
                  this.downloaded_parts += 1

         except Exception as error:
            print(error)

      else:
         with this.thread_lock:
            this.downloaded_bytes += path.getsize(f"{this.directory}/{part_name}")
            this.bridge.set_download_size(this.downloaded_bytes)
            this.bridge.set_download_progress(this.downloaded_bytes/this.file_size_bytes)
            this.downloaded_parts += 1
         if part_no:
            this.merge_job.add_part(part_no, f"{this.directory}/{part_name}")


   def start(this):
      this.bridge.set_file_name(this.file_name)
      if this.total_parts == 1:
         this._download_part(this.partition_data[0])

      elif this.total_parts > 1:
         for index, byte_range in enumerate(list(this.partition_data), start=1):
            Thread(target=lambda:this._download_part(byte_range, index), daemon=True).start()
      
      while this.downloaded_parts != this.total_parts:
         sleep(0.1)
      
      if this.total_parts > 1:
         Thread(target=lambda:this.merge_job.start(), daemon=True).start()
      else:
         this.bridge.set_merge_progress(1)
         this.bridge.set_merge_status("single_file")



class GUIBridge:
   download_job:DownloadJob

   file_size_bytes:int

   LABEL_FILE_NAME:Label
   
   LABEL_DOWNLOAD_SIZE:Label
   LABEL_DOWNLOAD_PERCENTAGE:Label
   PROGRESS_BAR_DOWNLOAD:ProgressBar

   LABEL_MERGE_STATUS:Label
   PROGRESS_BAR_MERGE:ProgressBar


   def __init__(this,
      download_job,
      file_name:Label,
      download_progress_bar:ProgressBar,
      download_percentage_label:Label,
      download_size_label:Label,
      merge_status:Label,
      merge_progress:ProgressBar
   ):
      this.download_job = download_job
      this.download_job.set_bridge(this)

      this.LABEL_FILE_NAME = file_name

      this.PROGRESS_BAR_DOWNLOAD = download_progress_bar
      this.LABEL_DOWNLOAD_SIZE = download_size_label
      this.LABEL_DOWNLOAD_PERCENTAGE = download_percentage_label
      
      this.LABEL_MERGE_STATUS = merge_status
      this.PROGRESS_BAR_MERGE = merge_progress


   def set_file_name(this, file_name:str):
      this.LABEL_FILE_NAME.configure(text=str(file_name))


   def set_download_size(this, byte_length:int):
      unit:str
      if byte_length >= 1024**3:
         byte_length /=  1024**3
         unit = "GB"

      elif byte_length >= 1024**2:
         byte_length /=  1024**2
         unit = "MB"

      elif byte_length >= 1024:
         byte_length /=  1024
         unit = "KB"

      else:
         unit = "B"

      this.LABEL_DOWNLOAD_SIZE.configure(text=f"{byte_length:.2f} {unit}")


   def set_merge_status(this, status:str):
      match status:
         case "start": this.LABEL_MERGE_STATUS.configure(text="Merging...")
         case "deleting_parts": this.LABEL_MERGE_STATUS.configure(text="Deleting parts...")
         case "end": this.LABEL_MERGE_STATUS.configure(text="Merge complete")
         case "single_file": this.LABEL_MERGE_STATUS.configure(text="Single file")

   def set_merge_progress(this, progress_decimal:float):
      this.PROGRESS_BAR_MERGE.set(progress_decimal)


   def set_download_progress(this, progress_decimal:float):
      this.PROGRESS_BAR_DOWNLOAD.set(progress_decimal)
      this.LABEL_DOWNLOAD_PERCENTAGE.configure(text=f"{int(progress_decimal * 100)}%")


