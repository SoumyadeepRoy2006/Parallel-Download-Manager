from os import path, rename, remove
import requests
from threading import Thread
from time import sleep
from Classes.File_Merger import MergeJob

class DownloadJob:
   file_name = None
   directory = None
   url = None
   file_size_bytes = None

   partition_data = None
   total_parts = 0

   buffer_rw_size = 32768 # 32 KB
   downloaded_parts = 0
   downloaded_bytes = 0

   merge_required = True
   merge_job = None

   def __init__(this, url:str, file_name:str, directory:str, partition_data:list):
      if str(".part") in file_name:
         raise ValueError("'.part' cannot be used in names")
      
      elif path.exists(f"{directory}/{file_name}"):
         raise FileExistsError(f"A file named ' {file_name} ' already exists in your directory")
      
      else:
         this.file_name = file_name
         this.directory = directory
         this.url = url
         this.partition_data = partition_data
         this.file_size_bytes = partition_data[-1][1]
         this.total_parts = len(partition_data)
         this.merge_job = MergeJob(directory, file_name, len(partition_data))


   def set_dir(this, directory:str):
      if directory != "":
         this.directory = directory


   def set_file_name(this, file_name:str):
      if file_name != "":
         this.file_name = file_name


   def _download_part(this, byte_range:tuple, part_no:int=None):
      part_name = f"{this.file_name}{(".part" + str(part_no)) if part_no else ""}"
      if not path.exists(f"{this.directory}/{part_name}"):
         try:
            if path.exists(f"{this.directory}/{part_name}.part"):
               this.downloaded_bytes -= path.getsize(f"{this.directory}/{part_name}.part")
            with requests.get(this.url, headers={"Range": f"bytes={byte_range[0]}-{byte_range[1]}"}, stream=True) as res:
               res.raise_for_status()
               with open(f"{this.directory}/{part_name}.part", "wb") as file:
                  for buffer in res.iter_content(chunk_size=this.buffer_rw_size):
                     if buffer:
                        file.write(buffer)
                        this.downloaded_bytes += len(buffer)

               rename(f"{this.directory}/{part_name}.part", f"{this.directory}/{part_name}")

               if part_no:
                  this.merge_job.add_part(part_no, f"{this.directory}/{part_name}")

               this.downloaded_parts += 1

         except Exception as error:
            print(error)



   def start(this):
      if this.total_parts == 1:
         this._download_part(this.partition_data[0])

      elif this.total_parts > 1:
         for index, byte_range in enumerate(list(this.partition_data), start=1):
            Thread(target=lambda:this._download_part(byte_range, index), daemon=True).start()
      
      while this.downloaded_parts != this.total_parts:
         sleep(0.1)
      
      if this.total_parts > 1:
         Thread(target=lambda:this.merge_job.start(), daemon=True).start()


