import json, requests
from os import path, mkdir, rename
from threading import Thread
from time import sleep
from merger import merge_files
TIMEOUT = 15
CHUNK_SIZE = 64 * 1024
def download_partition(url: str, filename:str, part_info: dict, download_dir: str):
   start = part_info["start_byte"]
   end = part_info["end_byte"]
   part_path = path.join(download_dir, f"{filename}.temp{part_info["part"]}")
   final_path = path.join(download_dir, f"{filename}.part{part_info["part"]}")

   expected_size = end - start + 1

   # Skip if already complete
   if path.exists(part_path):
      if path.getsize(part_path) == expected_size:
         print("Already downloaded!")
         return True

   headers = {
      "Range": f"bytes={start}-{end}"
   }

   response = requests.get(
      url,
      headers=headers,
      stream=True,
      timeout=TIMEOUT
   )
   response.raise_for_status()

   with open(part_path, "wb") as f:
      for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
         if chunk: f.write(chunk)

   rename(part_path, final_path)
   
   metadata:dict
   with open(path.join(download_dir, "metadata.json"), "r") as metadata_file:
      metadata = json.load(metadata_file)
      metadata["finished_parts"] += 1
   with open(path.join(download_dir, "metadata.json"), "w") as metadata_file:
      json.dump(metadata, metadata_file, indent=3)
   









def download(url:str, filename:str, download_data:dict):
   total_parts = len(download_data["partition_data"])
   finished_parts = 0
   if not path.isdir("./Downloads/"): mkdir("./Downloads/")
   filename_noext = filename.split(".")[0]
   target_path = str("./Downloads/" + filename_noext)
   metadata = dict()
   if not path.isdir(target_path):
      mkdir(target_path)
      metadata = {
         "filename": filename,
         "finished_parts": 0
         #"finished": False
         #"filesize": download_data["filesize"],
      }
      with open(target_path+"/metadata.json", "w") as metadata_file:
         json.dump(metadata, metadata_file, indent=3)
      print("Metadata file created")

      print("Downloading...")
      for info in download_data["partition_data"]:
         Thread(daemon=True, target=lambda:download_partition(url=url, filename=filename, part_info=info, download_dir=target_path)).start()
   while True:
      try:
         with open(target_path+"/metadata.json", "r") as metadata_file:
            data = json.load(metadata_file)
            if not data["finished_parts"] == total_parts: sleep(10)
            else: break
      except: pass
   print("Download complete!")

   merge_files([path.join(target_path, f"{filename}.part{partition_info["part"]}") for partition_info in download_data["partition_data"]], path.join(target_path, filename))